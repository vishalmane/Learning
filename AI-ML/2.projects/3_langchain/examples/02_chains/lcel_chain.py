from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

from lc_lab.models import get_chat_model


def main() -> None:
    greet = RunnableLambda(lambda name: f"Hello, {name}")
    exclaim = RunnableLambda(lambda text: f"{text}!")
    deterministic_chain = greet | exclaim

    print("Deterministic LCEL chain:")
    print(deterministic_chain.invoke("World"))
    print()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a concise Python tutor. Answer in plain text only, without Markdown fences.",
            ),
            ("human", "Explain this LCEL chain in three short lines: {chain}"),
        ]
    )
    llm_chain = prompt | get_chat_model() | StrOutputParser()

    print("Gemini-backed LCEL chain:")
    print(llm_chain.invoke({"chain": "greet | exclaim | StrOutputParser()"}))


if __name__ == "__main__":
    main()
