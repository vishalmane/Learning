from langchain_core.messages import HumanMessage, SystemMessage

from lc_lab.models import get_chat_model


def main() -> None:
    model = get_chat_model()
    response = model.invoke(
        [
            SystemMessage(content="You explain technical ideas with compact examples."),
            HumanMessage(content="Explain LangChain in three bullet points."),
        ]
    )
    print(response.content)


if __name__ == "__main__":
    main()

