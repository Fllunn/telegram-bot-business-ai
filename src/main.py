import time

from .bot.client import bot
from . import handlers  # registers command handlers
# from .handlers import business, edited, deleted  # registers message handlers
from .handlers import business  # registers message handlers
from .utils.logger import logger


def main() -> None:
    logger.info("Bot started and waiting for messages...")
    backoff_seconds = 1
    max_backoff_seconds = 60

    while True:
        try:
            bot.polling(
                none_stop=True,
                interval=0,
                timeout=20,
                long_polling_timeout=20,
            )
        except Exception as exc:
            logger.error("Polling error (%s: %s). Restarting in %s seconds.", 
                        type(exc).__name__, str(exc), backoff_seconds)
            time.sleep(backoff_seconds)
            backoff_seconds = min(backoff_seconds * 2, max_backoff_seconds)
        else:
            backoff_seconds = 1


if __name__ == "__main__":
    main()
