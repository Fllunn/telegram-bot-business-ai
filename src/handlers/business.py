import threading
import time

import telebot

from ..bot.client import bot
from ..config.settings import OWNER_ID
from ..core.state import AUTO_REPLY_DELAY, auto_reply_enabled, auto_reply_timers, last_client_message, messages_log
from ..services.auto_reply import auto_reply


@bot.business_message_handler(content_types=[
    "text",
    "photo",
    "video",
    "voice",
    "document",
    "animation",
    "audio",
    "sticker",
    "location",
    "contact",
])
def handle_business_message(message: telebot.types.Message) -> None:
    """
    Обрабатывает новые бизнес-сообщения логирует их и при необходимости запускает таймер для автоответа.
    """
    chat_id = message.chat.id
    bc_id = message.business_connection_id
    from_user_id = message.from_user.id

    log_data = {}
    ctype = message.content_type
    log_data["type"] = ctype

    if ctype == "text":
        log_data["content"] = message.text
    elif ctype == "photo":
        photo_obj = message.photo[-1]
        log_data["content"] = photo_obj.file_id
        if message.caption:
            log_data["caption"] = message.caption
    elif ctype == "video":
        log_data["content"] = message.video.file_id
        if message.caption:
            log_data["caption"] = message.caption
    elif ctype == "document":
        log_data["content"] = message.document.file_id
        if message.caption:
            log_data["caption"] = message.caption
    elif ctype == "voice":
        log_data["content"] = message.voice.file_id
    elif ctype == "audio":
        log_data["content"] = message.audio.file_id
    elif ctype == "animation":
        log_data["content"] = message.animation.file_id
        if message.caption:
            log_data["caption"] = message.caption
    elif ctype == "sticker":
        log_data["content"] = message.sticker.file_id
    elif ctype == "location":
        lat = message.location.latitude
        lon = message.location.longitude
        log_data["content"] = f"[location] lat={lat}, lon={lon}"
    elif ctype == "contact":
        phone = message.contact.phone_number
        first_name = message.contact.first_name
        last_name = message.contact.last_name or ""
        log_data["content"] = f"[contact] {first_name} {last_name}, tel={phone}"
    else:
        log_data["content"] = f"[{ctype}]"

    messages_log[(chat_id, message.message_id)] = log_data

    if from_user_id == OWNER_ID:
        if chat_id in auto_reply_timers:
            t = auto_reply_timers.pop(chat_id)
            t.cancel()
            print(f"[Cancel Timer] Владелец ответил сам, отменяем таймер в чате {chat_id}.")
        return

    if not auto_reply_enabled:
        print("[BusinessMessage] Автоответ выключен, выходим.")
        return

    if ctype == "text":
        last_client_message[chat_id] = (message, time.time())
        if chat_id in auto_reply_timers:
            old_t = auto_reply_timers.pop(chat_id)
            old_t.cancel()

        new_t = threading.Timer(AUTO_REPLY_DELAY, auto_reply, args=(chat_id, bc_id))
        auto_reply_timers[chat_id] = new_t
        new_t.start()
    else:
        pass
