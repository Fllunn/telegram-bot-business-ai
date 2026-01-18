import telebot
from openai import OpenAI

from ..config.settings import OPENAI_API_KEY, TELEGRAM_TOKEN

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode="HTML")
openai_client = OpenAI(api_key=OPENAI_API_KEY)
