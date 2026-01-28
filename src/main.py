from .bot.client import bot
from . import handlers  # registers command handlers
# from .handlers import business, edited, deleted  # registers message handlers
from .handlers import business  # registers message handlers
from .utils.logger import logger


def main() -> None:
    logger.info("Bot started and waiting for messages...")
    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
