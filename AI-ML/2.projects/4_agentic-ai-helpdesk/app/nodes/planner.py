from app.services.llm import LLMClient
from app.state import HelpdeskState
from app.nodes.tracing import append_trace


def planner_node(state: HelpdeskState) -> HelpdeskState:
    plan = LLMClient().plan(state["user_query"])
    metadata = append_trace(
        state,
        "planner",
        {"user_query": state["user_query"]},
        "Creates an execution plan for the support request using the configured LLM, with deterministic fallback logic if no key is configured.",
        {"plan": plan},
    )
    return {**state, "plan": plan, "metadata": metadata}
