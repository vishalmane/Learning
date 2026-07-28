from app.nodes.reasoning import reasoning_node


def test_reasoning_outputs_structured_result():
    state = reasoning_node(
        {
            "user_id": "u1",
            "user_query": "My VPN stopped working",
            "plan": ["Run VPN diagnostics"],
            "retrieved_docs": [],
            "tool_output": [{"data": {"error": "MFA timeout"}}],
            "conversation_history": [],
        }
    )

    assert state["reasoning_output"]["confidence"] > 0
    assert "MFA timeout" in state["reasoning_output"]["summary"]

