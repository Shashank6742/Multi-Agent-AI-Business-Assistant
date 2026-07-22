from agents.base_agent import BaseAgent


class EmailAgent(BaseAgent):
    name = "email_agent"
    system_prompt = (
        "You are the Email Agent for a business assistant. "
        "You draft clear, professional business emails based on the user's request. "
        "Always include a subject line and a proper greeting/closing. "
        "Keep tone professional unless the user specifies otherwise."
    )
