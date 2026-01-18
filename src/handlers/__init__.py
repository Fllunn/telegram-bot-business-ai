import telebot

from ..bot.client import bot
from ..config.settings import is_user_allowed
from ..core import state


@bot.message_handler(commands=["enable_auto"])
def enable_auto_handler(message: telebot.types.Message) -> None:
    if not is_user_allowed(message.from_user.id):
        return
    state.auto_reply_enabled = True
    bot.reply_to(message, "Автоответ теперь ВКЛЮЧЕН для всех чатов.")


@bot.message_handler(commands=["disable_auto"])
def disable_auto_handler(message: telebot.types.Message) -> None:
    if not is_user_allowed(message.from_user.id):
        return
    state.auto_reply_enabled = False
    bot.reply_to(message, "Автоответ теперь ВЫКЛЮЧЕН для всех чатов.")


@bot.message_handler(commands=["start", "help"])
def handle_start_help(message: telebot.types.Message) -> None:
    if not is_user_allowed(message.from_user.id):
        return
    bot.send_message(
        message.chat.id,
        "Это бизнес-бот с возможностью логировать удалённые сообщения и отвечать через ИИ.\n\n"
        "Доступные команды:\n"
        "/enable_auto – включить автоответ во всех чатах\n"
        "/disable_auto – выключить автоответ во всех чатах",
    )
