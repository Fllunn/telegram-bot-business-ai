import telebot
from openai import OpenAI

from ..config.settings import PROXYAPI_API_KEY, PROXYAPI_BASE_URL, TELEGRAM_TOKEN

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode="HTML")
openai_client = OpenAI(api_key=PROXYAPI_API_KEY, base_url=PROXYAPI_BASE_URL)
