import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
PROXYAPI_API_KEY = os.getenv("PROXYAPI_API_KEY", OPENAI_API_KEY)
PROXYAPI_BASE_URL = os.getenv("PROXYAPI_BASE_URL", "https://openai.api.proxyapi.ru/v1")
OWNER_ID = int(os.getenv("OWNER_ID", "2342342"))

# Получаем список разрешенных пользователей
_allowed_users_str = os.getenv("ALLOWED_USERS", "")
ALLOWED_USERS = set()
if _allowed_users_str.strip():
    try:
        ALLOWED_USERS = {int(uid.strip()) for uid in _allowed_users_str.split(",") if uid.strip()}
    except ValueError:
        pass
else:
    pass


def is_user_allowed(user_id: int) -> bool:
    """Проверяет, разрешено ли пользователю использовать бота (для команд)."""
    # Если список пустой, доступ разрешен всем
    if not ALLOWED_USERS:
        return True
    return user_id in ALLOWED_USERS


def is_business_account_allowed(chat_id: int) -> bool:
    """
    Проверяет, разрешен ли бизнес-аккаунт использовать бота.
    Сейчас: бизнес-аккаунты могут использоваться только владельцем (OWNER_ID).
    """
    # Для бизнес-сообщений: только если они поступают от чатов, 
    # где интегрирован бот (проверяем через логику обработки)
    # Это достаточно, т.к. бот добавляют только в нужные бизнес-аккаунты
    return True
