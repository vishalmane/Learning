from collections.abc import Callable
from typing import Any

from app.services.notification_tool import send_notification
from app.services.ticket_tool import create_ticket
from app.services.vpn_tool import check_vpn_status
from app.state import HelpdeskState, ToolResult
from app.nodes.tracing import append_trace


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., dict[str, Any]]] = {}

    def register(self, name: str, func: Callable[..., dict[str, Any]]) -> None:
        self._tools[name] = func

    def get(self, name: str) -> Callable[..., dict[str, Any]]:
        return self._tools[name]


class ToolExecutor:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def run(self, tool_name: str, **kwargs: Any) -> ToolResult:
        try:
            result = self.registry.get(tool_name)(**kwargs)
            return ToolResult(tool_name=tool_name, success=True, data=result)
        except Exception as exc:
            return ToolResult(tool_name=tool_name, success=False, error=str(exc))


def default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register("check_vpn_status", check_vpn_status)
    registry.register("create_ticket", create_ticket)
    registry.register("send_notification", send_notification)
    return registry


def tool_executor_node(state: HelpdeskState) -> HelpdeskState:
    executor = ToolExecutor(default_registry())
    query = state["user_query"].lower()
    results: list[ToolResult] = []
    if "vpn" in query:
        results.append(executor.run("check_vpn_status", user_id=state["user_id"]))
    if "ticket" in query or "escalate" in query or "urgent" in query:
        results.append(
            executor.run(
                "create_ticket",
                user_id=state["user_id"],
                summary=state["user_query"],
                priority="high" if "urgent" in query else "normal",
            )
        )
    tool_output = [result.model_dump() for result in results]
    metadata = append_trace(
        state,
        "tool_executor",
        {"user_id": state["user_id"], "user_query": state["user_query"], "plan": state.get("plan", [])},
        "Selects and executes registered helpdesk tools based on the request intent.",
        {"tool_output": tool_output, "tools_called": [result.tool_name for result in results]},
    )
    return {**state, "tool_output": tool_output, "metadata": metadata}
