"""
Manager Agent — the central coordinator.

Receives the user's request, decides which specialized agent(s) should
handle it, dispatches the task(s), and combines results into one response.

Routing uses the LLM itself (classification prompt) rather than brittle
keyword matching, so it generalizes to phrasing the user didn't anticipate.
"""
import json
from utils.llm_client import get_llm
from agents.research_agent import ResearchAgent
from agents.email_agent import EmailAgent
from agents.report_agent import ReportAgent
from agents.data_analysis_agent import DataAnalysisAgent
from agents.calendar_agent import CalendarAgent

ROUTING_PROMPT = """You are a routing controller for a multi-agent business assistant.
Given the user's request, decide which ONE agent should handle it.

Available agents:
- research_agent: answering questions, looking up information, summarizing documents/knowledge base
- email_agent: drafting or rewriting emails
- report_agent: generating structured business reports
- data_analysis_agent: interpreting data, trends, numbers, comparisons
- calendar_agent: scheduling, meetings, agendas, time planning

Respond with ONLY valid JSON in this exact format, nothing else:
{{"agent": "<agent_name>", "reason": "<short reason>"}}

User request: {task}
"""


class ManagerAgent:
    def __init__(self, rag_pipeline=None):
        self.llm = get_llm(temperature=0)
        self.rag = rag_pipeline
        self.agents = {
            "research_agent": ResearchAgent(rag_pipeline),
            "email_agent": EmailAgent(rag_pipeline),
            "report_agent": ReportAgent(rag_pipeline),
            "data_analysis_agent": DataAnalysisAgent(rag_pipeline),
            "calendar_agent": CalendarAgent(rag_pipeline),
        }

    def route(self, task: str) -> str:
        """Ask the LLM which agent should handle this task. Falls back to research_agent."""
        prompt = ROUTING_PROMPT.format(task=task)
        raw = self.llm.invoke(prompt).content.strip()

        try:
            start = raw.index("{")
            end = raw.rindex("}") + 1
            parsed = json.loads(raw[start:end])
            agent_name = parsed.get("agent", "research_agent")
        except (ValueError, json.JSONDecodeError):
            agent_name = "research_agent"

        if agent_name not in self.agents:
            agent_name = "research_agent"
        return agent_name

    def handle(self, task: str) -> dict:
        """Route the task, run the chosen agent, and return the result with metadata."""
        agent_name = self.route(task)
        agent = self.agents[agent_name]
        result = agent.run(task)
        return {
            "agent_used": agent_name,
            "response": result,
        }
