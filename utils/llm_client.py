"""
Shared LLM client. Uses Groq's free cloud API — no local model download,
no GPU/RAM requirements on your machine. Requires a free API key from
https://console.groq.com (no credit card needed).
"""
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL


def get_llm(temperature: float = 0.3):
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is not set. Get a free key at https://console.groq.com/keys "
            "and add it to your .env file."
        )
    return ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=temperature,
    )
