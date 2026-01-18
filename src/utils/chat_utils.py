import telebot


def get_chat_title(chat: telebot.types.Chat) -> str:
    """
    Возвращает удобочитаемое название чата (имя, фамилия или username, если это приват).
    """
    if chat.type == "private":
        full_name = ""
        if chat.first_name:
            full_name += chat.first_name
        if chat.last_name:
            full_name += f" {chat.last_name}"
        if not full_name and chat.username:
            full_name = f"@{chat.username}"
        return full_name.strip() if full_name else str(chat.id)
    else:
        return chat.title if chat.title else str(chat.id)
