from app.nodes.planner import planner_node


def test_planner_creates_vpn_plan():
    state = planner_node({"user_id": "u1", "user_query": "My VPN stopped working"})

    assert "Search support knowledge" in state["plan"]
    assert "Run VPN diagnostics" in state["plan"]

