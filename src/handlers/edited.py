import telebot

from ..bot.client import bot
from ..config.settings import OWNER_IDS
from ..core import state
from ..utils.chat_utils import get_chat_title


@bot.edited_business_message_handler(content_types=[
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
def handle_edited_business_message(message: telebot.types.Message) -> None:
    """
    Обрабатываем отредактированные сообщения узнаём, что было до, что стало, сообщаем владельцу.
    """
    old_data = state.messages_log.get((message.chat.id, message.message_id), {})
    old_desc = f"{old_data.get('type', '?')}: {old_data.get('content', '?')}"

    new_data = {}
    ctype = message.content_type
    new_data["type"] = ctype
    if ctype == "text":
        new_data["content"] = message.text
    else:
        new_data["content"] = f"[edited {ctype}]"

    state.messages_log[(message.chat.id, message.message_id)] = new_data
    chat_name = get_chat_title(message.chat)

    notify_text = (
        "Сообщение отредактировано.\n"
        f"Старое: {old_desc}\n"
        f"Новое: {new_data['content']}\n"
        f"Чат: {chat_name}"
    )
    for owner_id in OWNER_IDS:
        bot.send_message(owner_id, notify_text, parse_mode="HTML")
