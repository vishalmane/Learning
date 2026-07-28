from app.nodes.governance import governance_node, route_after_governance


def test_governance_requires_approval_for_sensitive_operation():
    state = governance_node({"user_id": "u1", "user_query": "Please delete my account", "metadata": {}})

    assert state["approval_required"] is True
    assert route_after_governance(state) == "human_review"


def test_governance_allows_standard_support_request():
    state = governance_node({"user_id": "u1", "user_query": "My VPN stopped working", "metadata": {}})

    assert state["approval_required"] is False
    assert route_after_governance(state) == "retriever"

