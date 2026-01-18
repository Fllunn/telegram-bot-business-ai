from .bot.client import bot
from . import handlers  # registers command handlers
from .handlers import business, edited, deleted  # registers message handlers


def main() -> None:
    print("Бот запущен и ждёт сообщений...")
    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
