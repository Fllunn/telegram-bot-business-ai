import json

from ..core.state import chat_histories


def save_chat_histories_to_json(file_path: str = "chat_histories.json") -> None:
    """
    Пример сохранения историй в JSON, если вдруг нужно.
    """
    data_to_save = {}
    for c_id, history_deque in chat_histories.items():
        data_to_save[str(c_id)] = list(history_deque)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
