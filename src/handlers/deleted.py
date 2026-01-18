import telebot

from ..bot.client import bot
from ..config.settings import OWNER_ID
from ..core.state import messages_log
from ..utils.chat_utils import get_chat_title


@bot.deleted_business_messages_handler()
def handle_deleted_business_messages(deleted: telebot.types.BusinessMessagesDeleted) -> None:
    """
    Когда сообщение удаляют, сюда прилетает список message_ids. Мы ищем их в логах и отправляем владельцу.
    """
    chat_id = deleted.chat.id
    chat_name = get_chat_title(deleted.chat)

    for msg_id in deleted.message_ids:
        data = messages_log.pop((chat_id, msg_id), None)
        if not data:
            text_for_owner = (
                "Сообщение удалено, но бот не успел залогировать.\n"
                f"Чат: {chat_name}, msg_id={msg_id}"
            )
            bot.send_message(OWNER_ID, text_for_owner)
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
            bot.send_message(OWNER_ID, text_for_owner)
        elif ctype == "photo":
            bot.send_message(OWNER_ID, text_for_owner)
            bot.send_photo(OWNER_ID, content, caption=f"[deleted photo] {caption}")
        elif ctype == "video":
            bot.send_message(OWNER_ID, text_for_owner)
            bot.send_video(OWNER_ID, content, caption=f"[deleted video] {caption}")
        elif ctype == "document":
            bot.send_message(OWNER_ID, text_for_owner)
            bot.send_document(OWNER_ID, content, caption=f"[deleted doc] {caption}")
        elif ctype == "voice":
            bot.send_message(OWNER_ID, text_for_owner)
            bot.send_voice(OWNER_ID, content)
        elif ctype == "audio":
            bot.send_message(OWNER_ID, text_for_owner)
            bot.send_audio(OWNER_ID, content)
        elif ctype == "animation":
            bot.send_message(OWNER_ID, text_for_owner)
            bot.send_animation(OWNER_ID, content, caption=f"[deleted animation] {caption}")
        elif ctype == "sticker":
            bot.send_message(OWNER_ID, text_for_owner)
            bot.send_sticker(OWNER_ID, content)
        elif ctype == "location":
            text_for_owner += f"Данные: {content}"
            bot.send_message(OWNER_ID, text_for_owner)
        elif ctype == "contact":
            text_for_owner += f"Данные: {content}"
            bot.send_message(OWNER_ID, text_for_owner)
        else:
            text_for_owner += f"Данные: {content}"
            bot.send_message(OWNER_ID, text_for_owner)
