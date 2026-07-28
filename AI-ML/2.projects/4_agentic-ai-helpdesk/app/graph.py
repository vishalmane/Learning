from uuid import uuid4

from langgraph.graph import END, StateGraph

from app.nodes.governance import governance_node, route_after_governance
from app.nodes.memory import load_conversation_history, memory_node
from app.nodes.planner import planner_node
from app.nodes.reasoning import reasoning_node
from app.nodes.response import human_review_node, response_node
from app.nodes.retriever import retriever_node
from app.nodes.tool_executor import tool_executor_node
from app.state import HelpdeskState


def build_graph():
    graph = StateGraph(HelpdeskState)
    graph.add_node("planner", planner_node)
    graph.add_node("governance", governance_node)
    graph.add_node("human_review", human_review_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("tool_executor", tool_executor_node)
    graph.add_node("reasoning", reasoning_node)
    graph.add_node("memory", memory_node)
    graph.add_node("response", response_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "governance")
    graph.add_conditional_edges(
        "governance",
        route_after_governance,
        {"human_review": "human_review", "retriever": "retriever"},
    )
    graph.add_edge("human_review", "response")
    graph.add_edge("retriever", "tool_executor")
    graph.add_edge("tool_executor", "reasoning")
    graph.add_edge("reasoning", "memory")
    graph.add_edge("memory", "response")
    graph.add_edge("response", END)
    return graph.compile()


compiled_graph = build_graph()


def invoke(user_id: str, query: str) -> HelpdeskState:
    trace_id = str(uuid4())
    initial_state: HelpdeskState = {
        "user_id": user_id,
        "user_query": query,
        "conversation_history": load_conversation_history(user_id),
        "metadata": {"trace_id": trace_id},
    }
    return compiled_graph.invoke(initial_state)

