import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OWNER_ID = int(os.getenv("OWNER_ID", "2342342"))

# Получаем список разрешенных пользователей
_allowed_users_str = os.getenv("ALLOWED_USERS", "")
ALLOWED_USERS = set()
if _allowed_users_str.strip():
    try:
        ALLOWED_USERS = {int(uid.strip()) for uid in _allowed_users_str.split(",") if uid.strip()}
    except ValueError:
        print("Ошибка при парсинге ALLOWED_USERS. Проверьте формат в .env")


def is_user_allowed(user_id: int) -> bool:
    """Проверяет, разрешено ли пользователю использовать бота."""
    # Если список пустой, доступ разрешен всем
    if not ALLOWED_USERS:
        return True
    return user_id in ALLOWED_USERS
