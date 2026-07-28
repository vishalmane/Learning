from typing import Any

from app.state import HelpdeskState


def append_trace(
    state: HelpdeskState,
    node_name: str,
    received: dict[str, Any],
    action: str,
    returned: dict[str, Any],
) -> dict[str, Any]:
    metadata = dict(state.get("metadata", {}))
    trace = list(metadata.get("execution_trace", []))
    trace.append(
        {
            "node_name": node_name,
            "received": received,
            "action": action,
            "returned": returned,
        }
    )
    metadata["execution_trace"] = trace
    return metadata
