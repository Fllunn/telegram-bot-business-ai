import threading
import time

from ..bot.client import bot
from ..core import state
from ..utils.logger import logger
from .gpt_service import generate_bot_answer


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
        gpt_answer = generate_bot_answer(chat_id, user_text)
        bot.send_message(chat_id=user_id, text=gpt_answer, business_connection_id=bc_id)
