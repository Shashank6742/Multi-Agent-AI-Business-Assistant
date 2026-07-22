"""
Terminal CLI for the Multi-Agent AI Business Assistant.
Useful for quick testing without launching Streamlit.

Usage:
    python main.py
"""
from agents.manager_agent import ManagerAgent
from rag.rag_pipeline import RAGPipeline


def main():
    print("=" * 60)
    print("🤖 Multi-Agent AI Business Assistant (CLI mode)")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 60)

    rag = RAGPipeline()
    manager = ManagerAgent(rag_pipeline=rag)

    while True:
        task = input("\nYou: ").strip()
        if task.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if not task:
            continue

        result = manager.handle(task)
        print(f"\n[Handled by: {result['agent_used']}]")
        print(f"Assistant: {result['response']}")


if __name__ == "__main__":
    main()
