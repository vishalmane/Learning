from __future__ import annotations

import re
from pathlib import Path

import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from lc_lab.models import get_chat_model
from lc_lab.rag import build_retriever
from lc_lab.schemas import InvoiceSummary


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DOCS = ROOT / "data" / "sample_docs"


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def show_provider_error(error: Exception) -> None:
    message = str(error)
    if "insufficient_quota" in message or "exceeded your current quota" in message:
        st.error(
            "The provider rejected the request because the API key has no available quota. "
            "Use Demo mode, or update billing/quota for the key in `.env`."
        )
        return
    st.error(f"Provider call failed: {error}")


def demo_chat_response(prompt: str) -> str:
    return (
        "Demo response:\n\n"
        "- LangChain standardizes model calls, prompts, tools, retrieval, and output parsing.\n"
        "- Agents use a model plus tools to decide which action to take next.\n"
        "- LangGraph is useful when the workflow needs explicit state, branching, retries, or checkpoints.\n\n"
        f"Your prompt was: `{prompt}`"
    )


def demo_rag_response(question: str) -> str:
    context = (SAMPLE_DOCS / "langchain_learning_path.md").read_text(encoding="utf-8")
    return (
        "Demo RAG response:\n\n"
        "After basic prompts, try LCEL chains, then structured output, then tools and agents. "
        "For knowledge-heavy apps, move to retrieval augmented generation. "
        "Use LangGraph when your workflow needs explicit state or branching.\n\n"
        f"Question: `{question}`\n\n"
        f"Source context preview:\n\n{context[:500]}..."
    )


def demo_invoice_summary(text: str) -> InvoiceSummary:
    total_match = re.search(r"Total\s+(\d+(?:\.\d+)?)\s+([A-Z]{3})", text, re.IGNORECASE)
    vendor_match = re.search(r"Invoice from ([^:]+)", text, re.IGNORECASE)
    return InvoiceSummary(
        vendor=vendor_match.group(1).strip() if vendor_match else "Unknown",
        total=float(total_match.group(1)) if total_match else 0.0,
        currency=total_match.group(2).upper() if total_match else "USD",
        line_items=["embeddings kit", "prompt book"] if "embeddings kit" in text.lower() else [],
    )


st.set_page_config(page_title="LangChain Lab", page_icon=":material/hub:", layout="wide")
st.title("LangChain Lab")

mode = st.sidebar.radio("Provider", ["Demo", "Live Gemini"], horizontal=True)
use_demo = mode == "Demo"
if use_demo:
    st.sidebar.info("Demo mode does not call Gemini, so it works without API quota.")
else:
    st.sidebar.warning("Live mode calls Gemini and requires `GOOGLE_API_KEY` in `.env`.")

tab_chat, tab_rag, tab_structured = st.tabs(["Chat", "RAG", "Structured Output"])

with tab_chat:
    prompt = st.text_area("Prompt", "Explain what LangChain agents are in five sentences.")
    if st.button("Run Chat", type="primary"):
        if use_demo:
            st.markdown(demo_chat_response(prompt))
        else:
            try:
                with st.spinner("Calling model..."):
                    response = get_chat_model().invoke(prompt)
                st.markdown(response.content)
            except Exception as error:
                show_provider_error(error)

with tab_rag:
    question = st.text_input("Question", "What should I try after prompts?")
    if st.button("Run RAG"):
        if use_demo:
            st.markdown(demo_rag_response(question))
        else:
            try:
                with st.spinner("Retrieving and answering..."):
                    retriever = build_retriever(SAMPLE_DOCS)
                    rag_prompt = ChatPromptTemplate.from_template(
                        "Answer using only this context:\n\n{context}\n\nQuestion: {question}"
                    )
                    chain = (
                        {"context": retriever | format_docs, "question": RunnablePassthrough()}
                        | rag_prompt
                        | get_chat_model()
                        | StrOutputParser()
                    )
                    st.markdown(chain.invoke(question))
            except Exception as error:
                show_provider_error(error)

with tab_structured:
    text = st.text_area(
        "Text",
        "Invoice from Acme AI Tools: embeddings kit 120 USD, prompt book 30 USD. Total 150 USD.",
    )
    if st.button("Extract"):
        if use_demo:
            st.json(demo_invoice_summary(text).model_dump())
        else:
            try:
                with st.spinner("Extracting schema..."):
                    result = get_chat_model().with_structured_output(InvoiceSummary).invoke(
                        f"Extract invoice fields from this text: {text}"
                    )
                st.json(result.model_dump())
            except Exception as error:
                show_provider_error(error)
