from app.nodes.tool_executor import ToolExecutor, default_registry, tool_executor_node


def test_tool_executor_runs_registered_tool():
    result = ToolExecutor(default_registry()).run("check_vpn_status", user_id="u1")

    assert result.success is True
    assert result.data["connected"] is False


def test_tool_executor_node_runs_vpn_tool():
    state = tool_executor_node({"user_id": "u1", "user_query": "My VPN stopped working"})

    assert state["tool_output"][0]["tool_name"] == "check_vpn_status"

