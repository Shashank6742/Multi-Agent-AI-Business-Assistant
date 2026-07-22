"""
Lightweight smoke tests that don't require Ollama to be running —
they just verify the project structure and imports are correct.
Run with: pytest tests/
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_imports():
    from agents.base_agent import BaseAgent
    from agents.research_agent import ResearchAgent
    from agents.email_agent import EmailAgent
    from agents.report_agent import ReportAgent
    from agents.data_analysis_agent import DataAnalysisAgent
    from agents.calendar_agent import CalendarAgent
    from agents.manager_agent import ManagerAgent
    from rag.rag_pipeline import RAGPipeline

    assert BaseAgent.name == "base_agent"
    assert ResearchAgent.name == "research_agent"
    assert EmailAgent.name == "email_agent"
    assert ReportAgent.name == "report_agent"
    assert DataAnalysisAgent.name == "data_analysis_agent"
    assert CalendarAgent.name == "calendar_agent"


def test_manager_has_all_agents():
    from agents.manager_agent import ManagerAgent

    expected = {
        "research_agent",
        "email_agent",
        "report_agent",
        "data_analysis_agent",
        "calendar_agent",
    }
    manager = ManagerAgent.__new__(ManagerAgent)  # skip __init__ (needs live LLM)
    manager.agents = {}
    # just verifying the class defines the expected agent registry keys via source
    import inspect

    source = inspect.getsource(ManagerAgent.__init__)
    for name in expected:
        assert name in source
