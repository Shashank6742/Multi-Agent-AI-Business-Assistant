"""
Central configuration for the Multi-Agent AI Business Assistant.
Loads settings from .env (falls back to sane defaults if not set).
"""
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "data/chroma_db")
DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH", "data/documents")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # free, local, runs via sentence-transformers
