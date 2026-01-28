import telebot

from ..bot.client import bot
from ..config.settings import OWNER_IDS
from ..core import state
from ..utils.chat_utils import get_chat_title


@bot.deleted_business_messages_handler()
def handle_deleted_business_messages(deleted: telebot.types.BusinessMessagesDeleted) -> None:
    """
    Когда сообщение удаляют, сюда прилетает список message_ids. Мы ищем их в логах и отправляем владельцу.
    """
    # Проверяем доступ (проверяем через первое сообщение, если есть контекст)
    # В deleted нет прямого from_user, поэтому проверяем через chat
    # Для бизнес-сообщений это всегда будет работать через business_connection
    chat_id = deleted.chat.id
    chat_name = get_chat_title(deleted.chat)

    for msg_id in deleted.message_ids:
        data = state.messages_log.pop((chat_id, msg_id), None)
        if not data:
            text_for_owner = (
                "Сообщение удалено, но бот не успел залогировать.\n"
                f"Чат: {chat_name}, msg_id={msg_id}"
            )
            for owner_id in OWNER_IDS:
                bot.send_message(owner_id, text_for_owner, parse_mode=None)
            continue

        ctype = data.get("type", "unknown")
        content = data.get("content", "")
        caption = data.get("caption", "")

        text_for_owner = (
            "Сообщение удалено.\n"
            f"Тип: {ctype}\n"
            f"Чат: {chat_name}\n"
        )

        if ctype == "text":
            text_for_owner += f"Текст: {content}"
            for owner_id in OWNER_IDS:
                bot.send_message(owner_id, text_for_owner, parse_mode=None)
        elif ctype == "photo":
            for owner_id in OWNER_IDS:
                bot.send_message(owner_id, text_for_owner, parse_mode=None)
                bot.send_photo(owner_id, content, caption=f"[deleted photo] {caption}")
        elif ctype == "video":
            for owner_id in OWNER_IDS:
                bot.send_message(owner_id, text_for_owner, parse_mode=None)
                bot.send_video(owner_id, content, caption=f"[deleted video] {caption}")
        elif ctype == "document":
            for owner_id in OWNER_IDS:
                bot.send_message(owner_id, text_for_owner, parse_mode=None)
                bot.send_document(owner_id, content, caption=f"[deleted doc] {caption}")
        elif ctype == "voice":
            for owner_id in OWNER_IDS:
                bot.send_message(owner_id, text_for_owner, parse_mode=None)
                bot.send_voice(owner_id, content)
        elif ctype == "audio":
            for owner_id in OWNER_IDS:
                bot.send_message(owner_id, text_for_owner, parse_mode=None)
                bot.send_audio(owner_id, content)
        elif ctype == "animation":
            for owner_id in OWNER_IDS:
                bot.send_message(owner_id, text_for_owner, parse_mode=None)
                bot.send_animation(owner_id, content, caption=f"[deleted animation] {caption}")
        elif ctype == "sticker":
            for owner_id in OWNER_IDS:
                bot.send_message(owner_id, text_for_owner, parse_mode=None)
                bot.send_sticker(owner_id, content)
        elif ctype == "location":
            text_for_owner += f"Данные: {content}"
            for owner_id in OWNER_IDS:
                bot.send_message(owner_id, text_for_owner, parse_mode=None)
        elif ctype == "contact":
            text_for_owner += f"Данные: {content}"
            for owner_id in OWNER_IDS:
                bot.send_message(owner_id, text_for_owner, parse_mode=None)
        else:
            text_for_owner += f"Данные: {content}"
            for owner_id in OWNER_IDS:
                bot.send_message(owner_id, text_for_owner, parse_mode=None)
