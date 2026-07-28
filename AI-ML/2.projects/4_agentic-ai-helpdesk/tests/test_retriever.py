from app.nodes.retriever import retriever_node
from app.services.vector_store import VectorStore


def test_retriever_returns_ranked_documents():
    docs = VectorStore().retrieve_docs("vpn mfa timeout")

    assert docs
    assert docs[0]["source"].startswith("kb://")


def test_retriever_node_updates_state():
    state = retriever_node({"user_id": "u1", "user_query": "VPN MFA timeout"})

    assert state["retrieved_docs"]

