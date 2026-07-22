# 🤖 Multi-Agent AI Business Assistant

A working implementation of a Multi-Agent AI Business Assistant with RAG
(Retrieval-Augmented Generation). **100% free to run** — no paid API keys,
no billing. The LLM runs on Groq's free cloud API (so your laptop doesn't
need to be powerful), and everything else (embeddings, vector store) runs
locally.

## How it works

```
User request
     │
     ▼
Manager Agent  ──(routes via LLM classification)──►  one of:
     │                                                  ├── Research Agent  (RAG-backed Q&A)
     │                                                  ├── Email Agent
     │                                                  ├── Report Agent    (RAG-backed)
     │                                                  ├── Data Analysis Agent
     │                                                  └── Calendar Agent
     ▼
Final response returned to user
```

The **Manager Agent** asks the LLM to classify each request, dispatches it to
the right specialist, and returns the result. The **Research** and **Report**
agents pull context from your own documents via a local **ChromaDB** vector
store before answering, so responses are grounded in your data instead of
guesses.

## Tech stack (all free)

| Component     | Tool                                   |
|----------------|-----------------------------------------|
| LLM            | [Groq API](https://console.groq.com) — free tier, cloud-hosted (no local compute needed) |
| Embeddings     | `sentence-transformers` (local, no API) |
| Vector store   | ChromaDB (local, persisted to disk)     |
| Orchestration  | LangChain                               |
| UI             | Streamlit                               |

## Setup (VS Code)

### 1. Get a free Groq API key
Groq hosts the LLM in the cloud for free, so your laptop only needs internet —
no local model download, no GPU/RAM requirements.
- Go to https://console.groq.com/keys
- Sign up (free, no credit card required)
- Click "Create API Key" and copy it — you'll paste it into `.env` in Step 5.

### 2. Open the project in VS Code
- Open this folder (`multi-agent-assistant`) in VS Code.
- Install the **Python extension** if you don't have it already.

### 3. Create a virtual environment
Open a terminal in VS Code (`` Ctrl+` ``) and run:
```bash
python -m venv venv
```
Activate it:
- **Windows**: `venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

Then select this environment as your interpreter in VS Code:
`Ctrl+Shift+P` → "Python: Select Interpreter" → choose the `venv` one.

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set up environment variables
```bash
cp .env.example .env
```
Open `.env` and paste your Groq API key:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

### 6. Add your documents (optional but recommended)
Drop PDF, DOCX, or TXT files into `data/documents/`. A sample document is
already there so you can test immediately.

Then ingest them into the vector store:
```bash
python ingest_documents.py
```
Re-run this any time you add or change documents.

### 7. Run the assistant

**Option A — Web chat UI (recommended):**
```bash
streamlit run app.py
```
This opens a browser tab with a chat interface.

**Option B — Terminal CLI:**
```bash
python main.py
```

## Example things to try
- *"What's our remote work policy on equipment?"* → Research Agent (uses the sample doc)
- *"Draft an email to the team about a schedule change"* → Email Agent
- *"Write a quarterly performance report"* → Report Agent
- *"What trends should I watch in a sales dataset with declining Q3 numbers?"* → Data Analysis Agent
- *"Help me plan a 1-hour meeting with the marketing team next week"* → Calendar Agent

## Project structure
```
multi-agent-assistant/
├── app.py                     # Streamlit chat UI (main entry point)
├── main.py                    # Terminal CLI alternative
├── config.py                  # Central settings (loaded from .env)
├── ingest_documents.py        # One-off script to load documents into RAG
├── requirements.txt
├── .env.example
├── agents/
│   ├── base_agent.py          # Shared base class
│   ├── manager_agent.py       # Router/coordinator
│   ├── research_agent.py      # RAG-backed Q&A
│   ├── email_agent.py
│   ├── report_agent.py        # RAG-backed reports
│   ├── data_analysis_agent.py
│   └── calendar_agent.py
├── rag/
│   └── rag_pipeline.py        # Document loading, chunking, embedding, retrieval
├── utils/
│   └── llm_client.py          # Shared Ollama LLM connector
├── data/
│   ├── documents/              # Put your source documents here
│   └── chroma_db/              # Vector store (auto-generated, gitignored)
└── tests/
    └── test_agents_import.py  # Basic smoke tests
```

## Extending the system
This is designed to be easy to grow — matching the project's objective of
a "scalable architecture that can accommodate additional AI agents":

1. Create a new file in `agents/`, subclass `BaseAgent`, set a `name` and
   `system_prompt`.
2. Register it in `agents/manager_agent.py` — add it to the `self.agents`
   dict and describe it in `ROUTING_PROMPT`.
3. That's it — the Manager Agent will start routing relevant requests to it.

## Troubleshooting
- **`ValueError: GROQ_API_KEY is not set`**: you forgot to paste your key into
  `.env`, or the file is still named `.env.example`. Confirm it's exactly
  named `.env` and sits in the project root.
- **401/authentication errors from Groq**: double-check you copied the full
  key from https://console.groq.com/keys with no extra spaces.
- **Rate limit errors**: Groq's free tier has generous but finite request
  limits per minute. Wait a few seconds and retry, or reduce how fast you're
  sending requests.
- **Import errors on `unstructured` or `chromadb`**: these have native
  dependencies; ensure you're on Python 3.10–3.12 and re-run
  `pip install -r requirements.txt` inside the activated venv.

## Notes on the original proposal
This implementation covers the proposal's Manager Agent + specialized agents
+ RAG architecture with a runnable code base. Things like live email sending,
real calendar integration (Google Calendar/Outlook), and multi-agent
collaboration on a *single* request (rather than one-agent-per-request
routing) are natural next steps once this foundation is working end to end.
