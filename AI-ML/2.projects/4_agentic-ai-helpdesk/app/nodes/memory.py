from datetime import UTC, datetime

from app.services.redis_memory import RedisMemoryStore
from app.state import HelpdeskState
from app.nodes.tracing import append_trace


def load_conversation_history(user_id: str) -> list[dict]:
    return RedisMemoryStore().load_memory(user_id)


def memory_node(state: HelpdeskState) -> HelpdeskState:
    store = RedisMemoryStore()
    memory_item = {
        "query": state["user_query"],
        "plan": state.get("plan", []),
        "reasoning": state.get("reasoning_output", {}),
        "timestamp": datetime.now(UTC).isoformat(),
    }
    store.save_memory(
        state["user_id"],
        memory_item,
    )
    metadata = append_trace(
        state,
        "memory",
        {"user_id": state["user_id"], "reasoning_output": state.get("reasoning_output", {})},
        "Stores the completed interaction in short-term memory with TTL support.",
        {"saved": True, "memory_item": memory_item},
    )
    return {**state, "metadata": metadata}
