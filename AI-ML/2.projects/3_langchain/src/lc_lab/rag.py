from __future__ import annotations

from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from lc_lab.settings import load_settings


def load_text_documents(folder: str | Path) -> list[Document]:
    docs: list[Document] = []
    for path in sorted(Path(folder).glob("*.md")):
        docs.append(Document(page_content=path.read_text(encoding="utf-8"), metadata={"source": str(path)}))
    return docs


def build_retriever(folder: str | Path, persist_directory: str | Path | None = None):
    settings = load_settings()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(load_text_documents(folder))
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=GoogleGenerativeAIEmbeddings(model=settings.embedding_model),
        persist_directory=str(persist_directory) if persist_directory else None,
    )
    return vectorstore.as_retriever(search_kwargs={"k": 4})
