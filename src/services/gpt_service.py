from ..bot.client import openai_client
from ..core import state
from ..storage.persistence import save_chat_histories_to_json
from ..config.prompts import build_system_prompt_with_context, SYSTEM_PROMPT, AI_MODEL
from ..utils.logger import logger
import re


def build_gpt_messages(chat_id: int) -> list:
    """
    Подготавливаем историю переписки (25 последних сообщений) + системный промт
    для передачи в OpenAI ChatCompletion.
    """
    # Получаем текущие собранные данные
    booking = state.booking_data.get(chat_id, {})
    system_prompt = build_system_prompt_with_context(
        service=booking.get("service"),
        master=booking.get("master"),
        time_val=booking.get("time")
    )
    
    messages_for_gpt = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]
    for role, content in state.chat_histories[chat_id]:
        messages_for_gpt.append({"role": role, "content": content})
    return messages_for_gpt


def extract_booking_data(text: str) -> dict:
    """
    Парсит ответ ИИ и извлекает данные Услуга, Мастер, Время.
    Ищет строки вида:
    Услуга: значение или Услуга: [значение]
    Мастер: значение или Мастер: [значение]
    Время: значение или Время: [значение]
    
    Возвращает словарь с найденными полями (могут быть None).
    """
    extracted = {
        "service": None,
        "master": None,
        "time": None
    }
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('Услуга:'):
            service = line.replace('Услуга:', '').strip()
            # Убираем квадратные скобки если есть
            if service.startswith('[') and service.endswith(']'):
                service = service[1:-1].strip()
            # Пропускаем заполнители "?"
            if service and service != "?":
                extracted["service"] = service
        elif line.startswith('Мастер:'):
            master = line.replace('Мастер:', '').strip()
            # Убираем квадратные скобки если есть
            if master.startswith('[') and master.endswith(']'):
                master = master[1:-1].strip()
            if master and master != "?":
                extracted["master"] = master
        elif line.startswith('Время:'):
            time_val = line.replace('Время:', '').strip()
            # Убираем квадратные скобки если есть
            if time_val.startswith('[') and time_val.endswith(']'):
                time_val = time_val[1:-1].strip()
            if time_val and time_val != "?":
                extracted["time"] = time_val
    
    return extracted


def update_booking_data(chat_id: int, new_data: dict) -> None:
    """
    Обновляет данные бронирования для чата.
    Если новое значение не None, оно заменяет старое.
    """
    if chat_id not in state.booking_data:
        state.booking_data[chat_id] = {
            "service": None,
            "master": None,
            "time": None
        }
    
    for key, value in new_data.items():
        if value is not None:
            state.booking_data[chat_id][key] = value


def generate_bot_answer(chat_id: int, user_text: str) -> str:
    """
    Генерация ответа через OpenAI ChatCompletion.
    """
    state.chat_histories[chat_id].append(("user", user_text))
    gpt_messages = build_gpt_messages(chat_id)

    try:
        response = openai_client.chat.completions.create(
            model=AI_MODEL,
            messages=gpt_messages,
            max_tokens=300,
            # max_completion_tokens=300,
            temperature=0.7,
        )
        # print(response)
        gpt_answer = response.choices[0].message.content.strip()
    except Exception as e:  # noqa: BLE001
        logger.error(f"OpenAI API error: {e}")
        gpt_answer = "Извините, сейчас с ИИ какие-то проблемы. Скоро подключится администратор и запишет вас, если есть свободные слоты."

    # Парсим ответ и обновляем данные бронирования
    extracted_data = extract_booking_data(gpt_answer)
    update_booking_data(chat_id, extracted_data)
    
    state.chat_histories[chat_id].append(("assistant", gpt_answer))
    # save_chat_histories_to_json("chat_histories.json")
    return gpt_answer
