"""
Base class for all specialized agents.
Each agent has a name, a system role/persona, and access to the shared RAG pipeline.
"""
from utils.llm_client import get_llm


class BaseAgent:
    name = "base_agent"
    system_prompt = "You are a helpful business assistant."

    def __init__(self, rag_pipeline=None):
        self.llm = get_llm()
        self.rag = rag_pipeline

    def run(self, task: str) -> str:
        """Override in subclasses. Default: just ask the LLM directly."""
        messages = [
            ("system", self.system_prompt),
            ("human", task),
        ]
        response = self.llm.invoke(messages)
        return response.content
