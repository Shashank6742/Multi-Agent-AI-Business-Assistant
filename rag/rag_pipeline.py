"""
Retrieval-Augmented Generation (RAG) pipeline.

Responsible for:
1. Loading documents from data/documents (pdf, docx, txt)
2. Splitting them into chunks
3. Embedding chunks with a free local model (sentence-transformers)
4. Storing/retrieving them from a local ChromaDB vector store

No external API calls or API keys are required — everything runs locally.
"""
import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import pandas as pd

from config import CHROMA_DB_PATH, DOCUMENTS_PATH, EMBEDDING_MODEL

# Kaggle-style CSVs can have 10,000+ rows. Embedding every single row is slow
# and rarely necessary for RAG Q&A, so we cap how many rows get ingested.
# Increase this in .env-driven config if you need more coverage.
MAX_CSV_ROWS = 2000

LOADER_MAP = {
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".txt": TextLoader,
    ".md": TextLoader,
}


class RAGPipeline:
    def __init__(self):
        self.embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
        os.makedirs(CHROMA_DB_PATH, exist_ok=True)
        os.makedirs(DOCUMENTS_PATH, exist_ok=True)
        self.vectorstore = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=self.embeddings,
            collection_name="business_documents",
        )

    def load_csv_files(self):
        """
        Load CSV files with pandas instead of the default LangChain CSVLoader,
        for two reasons:
        1. Kaggle datasets can have thousands of rows — we cap rows for speed.
        2. Turning each row into a readable "column: value" sentence embeds
           and retrieves better than raw comma-separated text.
        """
        docs = []
        for filename in os.listdir(DOCUMENTS_PATH):
            if not filename.lower().endswith(".csv"):
                continue
            filepath = os.path.join(DOCUMENTS_PATH, filename)
            try:
                df = pd.read_csv(filepath, encoding="utf-8", on_bad_lines="skip")
            except UnicodeDecodeError:
                df = pd.read_csv(filepath, encoding="latin-1", on_bad_lines="skip")

            total_rows = len(df)
            if total_rows > MAX_CSV_ROWS:
                print(
                    f"⚠️  {filename} has {total_rows} rows — only ingesting the "
                    f"first {MAX_CSV_ROWS} for speed. Adjust MAX_CSV_ROWS in "
                    f"rag/rag_pipeline.py if you need more."
                )
                df = df.head(MAX_CSV_ROWS)

            for i, row in df.iterrows():
                row_text = ", ".join(f"{col}: {row[col]}" for col in df.columns)
                docs.append(
                    Document(page_content=row_text, metadata={"source": filename, "row": i})
                )
            print(f"✅ Loaded {len(df)} rows from {filename}")
        return docs

    def load_documents(self):
        """Load every supported file from the documents folder."""
        docs = []
        for filename in os.listdir(DOCUMENTS_PATH):
            ext = os.path.splitext(filename)[1].lower()
            loader_cls = LOADER_MAP.get(ext)
            if not loader_cls:
                continue
            filepath = os.path.join(DOCUMENTS_PATH, filename)
            try:
                loader = loader_cls(filepath)
                docs.extend(loader.load())
            except Exception as e:
                print(f"⚠️  Could not load {filename}: {e}")

        docs.extend(self.load_csv_files())
        return docs

    def ingest(self):
        """Load, chunk, embed, and persist all documents into ChromaDB."""
        docs = self.load_documents()
        if not docs:
            print("No documents found in data/documents/. Add PDFs, DOCX, or TXT files and re-run.")
            return 0

        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        self.vectorstore.add_documents(chunks)
        self.vectorstore.persist()
        print(f"✅ Ingested {len(docs)} document(s) -> {len(chunks)} chunks.")
        return len(chunks)

    def retrieve(self, query: str, k: int = 4):
        """Return the top-k most relevant chunks for a query."""
        results = self.vectorstore.similarity_search(query, k=k)
        return [r.page_content for r in results]

    def retrieve_with_sources(self, query: str, k: int = 4):
        """Return chunks along with their source filename."""
        results = self.vectorstore.similarity_search(query, k=k)
        return [
            {"content": r.page_content, "source": r.metadata.get("source", "unknown")}
            for r in results
        ]
