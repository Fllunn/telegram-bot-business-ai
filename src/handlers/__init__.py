import telebot

from ..bot.client import bot
from ..config.settings import is_user_allowed
from ..core import state
from ..utils.logger import logger


@bot.message_handler(commands=["enable_auto"])
def enable_auto_handler(message: telebot.types.Message) -> None:
    user_id = message.from_user.id
    if not is_user_allowed(user_id):
        logger.warning(f"User {user_id} NOT ALLOWED for /enable_auto command")
        return
    state.auto_reply_enabled = True
    logger.info(f"User {user_id} enabled auto reply")
    bot.reply_to(message, "Автоответ теперь ВКЛЮЧЕН для всех чатов.")


@bot.message_handler(commands=["disable_auto"])
def disable_auto_handler(message: telebot.types.Message) -> None:
    user_id = message.from_user.id
    if not is_user_allowed(user_id):
        logger.warning(f"User {user_id} NOT ALLOWED for /disable_auto command")
        return
    state.auto_reply_enabled = False
    logger.info(f"User {user_id} disabled auto reply")
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
