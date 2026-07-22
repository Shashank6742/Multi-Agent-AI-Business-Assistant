"""
Run this once (or whenever you add/update files in data/documents/)
to load them into the local ChromaDB vector store.

Usage:
    python ingest_documents.py
"""
from rag.rag_pipeline import RAGPipeline

if __name__ == "__main__":
    print("Starting document ingestion...")
    pipeline = RAGPipeline()
    pipeline.ingest()
