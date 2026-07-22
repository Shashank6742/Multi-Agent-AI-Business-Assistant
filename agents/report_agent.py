from agents.base_agent import BaseAgent


class ReportAgent(BaseAgent):
    name = "report_agent"
    system_prompt = (
        "You are the Report Agent for a business assistant. "
        "You generate well-structured business reports with clear sections: "
        "Title, Executive Summary, Key Findings, and Recommendations. "
        "Use the context and data given to you; do not fabricate numbers."
    )

    def run(self, task: str) -> str:
        context_chunks = []
        if self.rag:
            context_chunks = self.rag.retrieve(task, k=4)
        context_text = "\n\n".join(context_chunks) if context_chunks else "(No related documents found.)"

        prompt = (
            f"Relevant background information:\n{context_text}\n\n"
            f"Report request: {task}\n\n"
            "Produce a structured business report."
        )
        messages = [("system", self.system_prompt), ("human", prompt)]
        response = self.llm.invoke(messages)
        return response.content
