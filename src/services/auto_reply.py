import threading
import time
import re

from ..bot.client import bot
from ..config.settings import OWNER_IDS
from ..core import state
from ..utils.logger import logger
from .gpt_service import generate_bot_answer


def remove_booking_info_from_message(text: str) -> str:
    """
    Удаляет служебные строки из сообщения.
    НО сохраняет их если это ФИНАЛЬНЫЙ БЛОК (все три поля подряд без '?')
    """
    lines = text.split('\n')
    
    # Ищем финальный блок: три строки Услуга/Мастер/Время (возможно с пустыми между ними) без '?'
    # Находим все непустые строки с полями
    service_lines = []
    master_lines = []
    time_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('Услуга:') and '?' not in line:
            service_lines.append(i)
        elif stripped.startswith('Мастер:') and '?' not in line:
            master_lines.append(i)
        elif stripped.startswith('Время:') and '?' not in line:
            time_lines.append(i)
    
    # Проверяем: есть ли три поля близко друг к другу (разница не больше 3 строк)
    if service_lines and master_lines and time_lines:
        for s_idx in service_lines:
            for m_idx in master_lines:
                for t_idx in time_lines:
                    # Проверяем что они идут примерно подряд (в пределах 3 строк друг от друга)
                    indices = sorted([s_idx, m_idx, t_idx])
                    if indices[2] - indices[0] <= 4:  # Максимум 4 строки между первым и последним
                        # Это финальный блок!
                        return text
    
    # Нет финального блока - удаляем все служебные строки
    filtered_lines = []
    skip_next_empty = False
    
    for line in lines:
        stripped = line.strip()
        
        # Служебные строки
        if (stripped.startswith('Услуга:') or 
            stripped.startswith('Мастер:') or 
            stripped.startswith('Время:')):
            skip_next_empty = True
            continue
        
        # Пропускаем пустую строку после служебной
        if skip_next_empty and stripped == '':
            skip_next_empty = False
            continue
        
        skip_next_empty = False
        filtered_lines.append(line)
    
    # Убираем пустые строки в конце
    while filtered_lines and filtered_lines[-1].strip() == '':
        filtered_lines.pop()
    
    return '\n'.join(filtered_lines).strip()


def auto_reply(chat_id: int, user_id: int, bc_id: str) -> None:
    """
    Функция, срабатывающая через AUTO_REPLY_DELAY секунд, если владелец не ответил.
    Формирует ответ с помощью ИИ и отправляет в чат.
    """
    state.auto_reply_timers.pop(chat_id, None)

    info = state.last_client_message.get(chat_id)
    if not info:
        return  # Нет данных, нечего отвечать

    message, msg_time = info
    now = time.time()
    if now - msg_time < (state.AUTO_REPLY_DELAY - 0.5):
        # Вдруг таймер сработал раньше?
        return

    if not state.auto_reply_enabled:
        return

    if message.content_type == "text":
        user_text = message.text
        
        # Проверка длины сообщения - не более 200 символов
        if len(user_text) > 200:
            bot.send_message(
                chat_id=user_id,
                text="Здравствуйте! Для записи напишите, какую услугу хотите, к какому мастеру и когда. Пожалуйста, отправляйте сообщения длиной не более 200 символов.",
                business_connection_id=bc_id,
                parse_mode=None
            )
            return
        
        gpt_answer = generate_bot_answer(chat_id, user_text)
        
        # Удаляем служебные строки перед отправкой пользователю
        clean_answer = remove_booking_info_from_message(gpt_answer)
        
        bot.send_message(
            chat_id=user_id, 
            text=clean_answer, 
            business_connection_id=bc_id,
            parse_mode=None
        )
        
        # Проверяем, является ли это финальным сообщением (все три поля заполнены)
        if "Скоро подключится администратор и запишет вас, если есть свободные слоты" in gpt_answer:
            try:
                # Получаем информацию о пользователе
                try:
                    user_info = bot.get_chat(user_id)
                    user_name = user_info.first_name or ""
                    if user_info.last_name:
                        user_name += f" {user_info.last_name}"
                    username = user_info.username
                except:
                    user_name = "Пользователь"
                    username = None
                
                # Формируем ссылку на пользователя
                if username:
                    user_link = f'<a href="https://t.me/{username}">{user_name}</a>'
                else:
                    user_link = f'<a href="tg://user?id={user_id}">{user_name}</a>'
                
                # Очищаем ответ ИИ для владельца (удаляем служебные строки)
                clean_gpt_answer = remove_booking_info_from_message(gpt_answer)
                
                # Формируем сообщение с информацией о чате
                owner_message = f"🔔 Новая заявка от клиента:\n\n"
                owner_message += f"👤 Клиент: {user_link}\n"
                owner_message += f"\nДанные заявки:\n{clean_gpt_answer}"
                
                # Отправляем сообщение всем владельцам
                for owner_id in OWNER_IDS:
                    bot.send_message(
                        chat_id=owner_id,
                        text=owner_message,
                        parse_mode='HTML'
                    )
            except Exception as e:
                pass
