from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from lc_lab.models import get_chat_model
from lc_lab.rag import build_retriever


ROOT = Path(__file__).resolve().parents[2]


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def main() -> None:
    retriever = build_retriever(ROOT / "data" / "sample_docs")
    prompt = ChatPromptTemplate.from_template(
        "Answer using only this context:\n\n{context}\n\nQuestion: {question}"
    )
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | get_chat_model()
        | StrOutputParser()
    )
    print(chain.invoke("tell me about basic chains?"))


if __name__ == "__main__":
    main()

