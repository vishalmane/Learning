from app.state import HelpdeskState, ReasoningResult
from app.nodes.tracing import append_trace


def human_review_node(state: HelpdeskState) -> HelpdeskState:
    answer = "This request requires human approval before any sensitive account operation can be performed."
    metadata = append_trace(
        state,
        "human_review",
        {"approval_required": state.get("approval_required"), "governance": state.get("metadata", {}).get("governance", {})},
        "Stops automated execution and prepares a human approval response for sensitive operations.",
        {"final_answer": answer},
    )
    return {**state, "final_answer": answer, "metadata": metadata}


def response_node(state: HelpdeskState) -> HelpdeskState:
    if state.get("approval_required"):
        answer = state.get("final_answer") or "Human approval is required."
        metadata = append_trace(
            state,
            "response",
            {"approval_required": True, "human_review_answer": answer},
            "Returns the human approval message without running retrieval, tools, reasoning, or memory update.",
            {"final_answer": answer},
        )
        return {**state, "final_answer": answer, "metadata": metadata}
    reasoning = ReasoningResult.model_validate(state.get("reasoning_output", {}))
    answer = f"{reasoning.summary}\n\nRecommended action: {reasoning.recommended_action}"
    if reasoning.escalation_required:
        answer += "\n\nEscalation is recommended."
    metadata = append_trace(
        state,
        "response",
        {"approval_required": False, "reasoning_output": state.get("reasoning_output", {})},
        "Formats the structured reasoning result into the final user-facing answer.",
        {"final_answer": answer},
    )
    return {**state, "final_answer": answer, "metadata": metadata}
