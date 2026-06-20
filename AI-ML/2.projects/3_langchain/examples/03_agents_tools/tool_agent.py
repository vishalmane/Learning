from langchain.agents import create_agent

from lc_lab.models import get_chat_model


def word_count(text: str) -> int:
    """Count words in a piece of text."""
    return len(text.split())


def main() -> None:
    agent = create_agent(
        model=get_chat_model(),
        tools=[word_count],
        system_prompt="Use tools when they help answer exactly.",
    )
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "How many words are in 'LangChain makes apps composable'?"}]}
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
