from agents.base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    name = "research_agent"
    system_prompt = (
        "You are the Research Agent for a business assistant. "
        "You answer questions using ONLY the context provided from company documents. "
        "If the context doesn't contain the answer, say so honestly instead of guessing. "
        "Be concise and cite which source each fact came from when possible."
    )

    def run(self, task: str) -> str:
        context_chunks = []
        if self.rag:
            context_chunks = self.rag.retrieve_with_sources(task, k=4)

        if context_chunks:
            context_text = "\n\n".join(
                f"[Source: {c['source']}]\n{c['content']}" for c in context_chunks
            )
        else:
            context_text = "(No matching documents found in the knowledge base.)"

        prompt = (
            f"Context from company documents:\n{context_text}\n\n"
            f"Question: {task}\n\n"
            "Answer using the context above. If it's insufficient, say so."
        )
        messages = [("system", self.system_prompt), ("human", prompt)]
        response = self.llm.invoke(messages)
        return response.content
