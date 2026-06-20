from langchain_core.chat_history import InMemoryChatMessageHistory
from lc_lab.models import get_chat_model


def main() -> None:
    history = InMemoryChatMessageHistory()
    model = get_chat_model()

    for user_text in ["My favorite database is Postgres.", "What database did I mention?"]:
        history.add_user_message(user_text)
        response = model.invoke(history.messages)
        history.add_ai_message(response.content)
        print(f"User: {user_text}")
        print(f"AI: {response.content}\n")

    assert len(history.messages) == 4


if __name__ == "__main__":
    main()
