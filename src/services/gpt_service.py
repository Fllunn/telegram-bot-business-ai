from ..bot.client import openai_client
from ..core import state
from ..storage.persistence import save_chat_histories_to_json
from ..config.prompts import SYSTEM_PROMPT, AI_MODEL


def build_gpt_messages(chat_id: int) -> list:
    """
    Подготавливаем историю переписки (25 последних сообщений) + системный промт
    для передачи в OpenAI ChatCompletion.
    """
    messages_for_gpt = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]
    for role, content in state.chat_histories[chat_id]:
        messages_for_gpt.append({"role": role, "content": content})
    return messages_for_gpt


def generate_bot_answer(chat_id: int, user_text: str) -> str:
    """
    Генерация ответа через OpenAI ChatCompletion.
    """
    state.chat_histories[chat_id].append(("user", user_text))
    gpt_messages = build_gpt_messages(chat_id)

    try:
        response = openai_client.chat.completions.create(
            model=AI_MODEL,
            messages=gpt_messages,
            max_tokens=300,
            temperature=0.7,
        )
        gpt_answer = response.choices[0].message.content.strip()
    except Exception as e:  # noqa: BLE001
        print(f"[OpenAI Error] {e}")
        gpt_answer = "Извините, но ИИ сейчас молчит..."

    state.chat_histories[chat_id].append(("assistant", gpt_answer))
    save_chat_histories_to_json("chat_histories.json")
    return gpt_answer
