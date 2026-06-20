from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class LearningState(TypedDict):
    topic: str
    next_step: str


def choose_next_step(state: LearningState) -> LearningState:
    topic = state["topic"].lower()
    if "agent" in topic:
        return {"topic": state["topic"], "next_step": "Try tool calling and tracing."}
    if "rag" in topic or "retrieval" in topic:
        return {"topic": state["topic"], "next_step": "Load documents, split them, embed them, then query."}
    return {"topic": state["topic"], "next_step": "Start with prompts and LCEL chains."}


def build_graph():
    graph = StateGraph(LearningState)
    graph.add_node("choose_next_step", choose_next_step)
    graph.add_edge(START, "choose_next_step")
    graph.add_edge("choose_next_step", END)
    return graph.compile()


def main() -> None:
    app = build_graph()
    print(app.invoke({"topic": "agents", "next_step": ""}))


if __name__ == "__main__":
    main()

