from langchain_core.prompts import ChatPromptTemplate

from lc_lab.models import get_chat_model


def main() -> None:
    prompt = ChatPromptTemplate.from_template("Write a five-line learning plan for {topic}.")
    chain = prompt | get_chat_model()
 
    for chunk in chain.stream({"topic": "LangChain agents"}):
        print(chunk.content, end="", flush=True)
    print()


if __name__ == "__main__":
    main()

