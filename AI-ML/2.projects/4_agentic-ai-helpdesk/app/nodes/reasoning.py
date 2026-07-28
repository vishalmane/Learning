from app.services.llm import LLMClient
from app.state import HelpdeskState
from app.nodes.tracing import append_trace


def reasoning_node(state: HelpdeskState) -> HelpdeskState:
    payload = {
        "user_query": state["user_query"],
        "plan": state.get("plan", []),
        "retrieved_docs": state.get("retrieved_docs", []),
        "tool_output": state.get("tool_output", []),
        "conversation_history": state.get("conversation_history", []),
    }
    result = LLMClient().reason(payload)
    reasoning_output = result.model_dump()
    metadata = append_trace(
        state,
        "reasoning",
        payload,
        "Combines the plan, retrieved documents, tool results, and memory to produce structured root-cause analysis and recommended action.",
        {"reasoning_output": reasoning_output},
    )
    return {**state, "reasoning_output": reasoning_output, "metadata": metadata}
