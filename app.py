"""
Multi-Agent AI Business Assistant — Streamlit chat interface.

Run with:
    streamlit run app.py
"""
import streamlit as st
from agents.manager_agent import ManagerAgent
from rag.rag_pipeline import RAGPipeline

st.set_page_config(page_title="Multi-Agent AI Business Assistant", page_icon="🤖", layout="centered")

st.title("🤖 Multi-Agent AI Business Assistant")
st.caption("Manager Agent routes your request to a specialized agent (Research, Email, Report, Data Analysis, Calendar).")


@st.cache_resource
def load_manager():
    rag = RAGPipeline()
    return ManagerAgent(rag_pipeline=rag)


manager = load_manager()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("agent_used"):
            st.caption(f"🔧 Handled by: `{msg['agent_used']}`")

user_input = st.chat_input("Ask me to research something, draft an email, write a report, analyze data, or schedule a meeting...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Manager Agent is routing your request..."):
            result = manager.handle(user_input)
        st.markdown(result["response"])
        st.caption(f"🔧 Handled by: `{result['agent_used']}`")

    st.session_state.messages.append(
        {"role": "assistant", "content": result["response"], "agent_used": result["agent_used"]}
    )

with st.sidebar:
    st.header("⚙️ Setup Status")
    st.markdown(
        "- **LLM**: Groq API (cloud, free tier)\n"
        "- **Embeddings**: sentence-transformers (local, free)\n"
        "- **Vector DB**: ChromaDB (local, free)"
    )
    st.divider()
    st.markdown(
        "**To add knowledge:** drop PDF/DOCX/TXT files into `data/documents/`, "
        "then run `python ingest_documents.py` and restart this app."
    )
