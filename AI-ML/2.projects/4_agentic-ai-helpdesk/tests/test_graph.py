from app.graph import invoke


def test_graph_executes_standard_path():
    state = invoke("u1", "My VPN stopped working")

    assert state["final_answer"]
    assert state["approval_required"] is False
    assert state["tool_output"]


def test_graph_routes_sensitive_request_to_human_review():
    state = invoke("u1", "Please remove access for this account")

    assert state["approval_required"] is True
    assert "human approval" in state["final_answer"].lower()

