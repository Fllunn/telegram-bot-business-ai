import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# Создаем директорию для логов если её нет
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOG_FILE = LOGS_DIR / "bot.log"


def setup_logger() -> logging.Logger:
    """
    Настраивает логгер с сохранением в файл и ротацией каждые 24 часа.
    """
    logger = logging.getLogger("telegram_bot")
    logger.setLevel(logging.DEBUG)

    # Удаляем старые обработчики если они есть
    logger.handlers.clear()

    # Формат логов
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Ротация каждые 24 часа (в полночь), хранит максимум 7 файлов
    file_handler = TimedRotatingFileHandler(
        LOG_FILE,
        when="midnight",  # Ротация в полночь
        interval=1,       # Интервал в днях
        backupCount=7,    # Хранит 7 файлов (последние 7 дней)
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Глобальный логгер
logger = setup_logger()
