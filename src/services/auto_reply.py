import threading
import time

from ..bot.client import bot
from ..core import state
from .gpt_service import generate_bot_answer


def auto_reply(chat_id: int, bc_id: str) -> None:
    """
    Функция, срабатывающая через AUTO_REPLY_DELAY секунд, если владелец не ответил.
    Формирует ответ с помощью ИИ и отправляет в чат.
    """
    print(f"\n[AUTO_REPLY_TRIGGERED] chat_id={chat_id}, bc_id={bc_id}")
    print(f"[AUTO_REPLY] auto_reply_enabled={state.auto_reply_enabled}")
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
        print("[AutoReply] Глобально автоответ отключён, ничего не отправляем.")
        return

    if message.content_type == "text":
        user_text = message.text
        gpt_answer = generate_bot_answer(chat_id, user_text)
        bot.send_message(chat_id=chat_id, text=gpt_answer, business_connection_id=bc_id)
        print(f"[AutoReply] Бот сам ответил в чат {chat_id}")
