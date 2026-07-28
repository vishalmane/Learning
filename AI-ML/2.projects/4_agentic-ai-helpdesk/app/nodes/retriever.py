from app.services.vector_store import VectorStore
from app.state import HelpdeskState
from app.nodes.tracing import append_trace


def retriever_node(state: HelpdeskState) -> HelpdeskState:
    docs = VectorStore().retrieve_docs(state["user_query"])
    metadata = append_trace(
        state,
        "retriever",
        {"user_query": state["user_query"]},
        "Searches the enterprise knowledge source and returns the top matching support documents.",
        {"retrieved_docs": docs},
    )
    return {**state, "retrieved_docs": docs, "metadata": metadata}
