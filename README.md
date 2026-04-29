# YusufBot

A RAG-powered personal chatbot that answers recruiter questions about Yusuf Berber in first person, grounded in his CV and interview notes. Built with LangChain, Groq, ChromaDB, and Streamlit.

**Live demo:** https://yusufbot.streamlit.app

---

## Features

- **Conversational Q&A** — answers recruiter questions as Yusuf, in first person, based only on provided documents
- **Model selector** — switch between Groq-hosted LLMs (LLaMA 3.3 70B, LLaMA 3.1 8B, Gemma 2 9B) in the sidebar
- **Session token tracker** — displays tokens used in the current session with a progress bar against the daily limit
- **Honest guardrails** — the bot says so when it doesn't have enough information, rather than hallucinating
- **Graceful error handling** — API failures show a friendly message instead of crashing

---

## Architecture

```
data/                        ← source documents (CV, Q&A notes)
    cv.txt
    interview_qa.txt
          │
          ▼
    ingest.py                ← one-time script: chunk → embed → persist
          │
          ▼
vectorstore/                 ← ChromaDB (committed to repo)
          │
          ▼
    rag.py                   ← retriever + Groq LLM → (answer, token usage)
          │
          ▼
    app.py                   ← Streamlit chat UI
```

**Data flow per question:**
1. User types a question in the chat
2. ChromaDB retrieves the 4 most relevant document chunks (via `all-MiniLM-L6-v2` embeddings)
3. Retrieved chunks are injected into a system prompt as context
4. Groq LLM generates a first-person answer grounded in that context
5. Answer and token usage are returned and displayed

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM inference | [Groq Cloud](https://console.groq.com) (`llama-3.3-70b-versatile` default) |
| LLM orchestration | [LangChain](https://python.langchain.com) |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (runs locally, no API key needed) |
| Vector store | [ChromaDB](https://www.trychroma.com) (persisted to disk) |
| UI | [Streamlit](https://streamlit.io) |
| Deployment | [Streamlit Community Cloud](https://share.streamlit.io) |

---

## Local Setup

### Prerequisites

- Python 3.11
- A [Groq API key](https://console.groq.com/keys) (free tier is sufficient)

### 1. Clone the repository

```bash
git clone https://github.com/yberber/YusufBot.git
cd YusufBot
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up the environment file

```bash
cp .env.example .env
```

Open `.env` and fill in your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the app

The vectorstore is already committed to the repo, so you can run the app immediately:

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Updating Personal Data

To update the CV or Q&A notes:

### 1. Edit the source files

| File | Purpose |
|---|---|
| `data/cv.txt` | CV — education, experience, skills, projects |
| `data/interview_qa.txt` | Pre-written answers to common interview questions |

Format Q&A entries as:

```
Q: Why do you want to work in this position?
A: I am drawn to this role because...

Q: What is your biggest strength?
A: My strongest quality is...
```

### 2. Rebuild the vectorstore

```bash
source .venv/bin/activate
python ingest.py
```

Expected output:
```
Ingested 2 document(s) → 51 chunks → vectorstore/
```

### 3. Commit and push

```bash
git add data/ vectorstore/
git commit -m "feat: update personal data"
git push
```

Streamlit Cloud picks up the new vectorstore automatically on the next reboot.

---

## Deployment (Streamlit Community Cloud)

### 1. Fork or push to GitHub

The repo must be on GitHub (public or private).

### 2. Connect to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **New app**
3. Select repository `yberber/YusufBot`, branch `main`, main file `app.py`
4. Click **Advanced settings → Secrets** and add:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

5. Click **Deploy**

Build takes ~2–3 minutes. The app is then live at a public URL.

---

## Project Structure

```
YusufBot/
├── app.py                   # Streamlit chat UI
├── rag.py                   # RAG logic: retriever + LLM + token usage
├── ingest.py                # One-time ingestion script
├── requirements.txt         # Python dependencies
├── pytest.ini               # pytest config
├── .python-version          # Pins Python 3.11 for Streamlit Cloud
├── .env.example             # Environment variable template
├── data/
│   ├── cv.txt               # Yusuf's CV
│   └── interview_qa.txt     # Interview Q&A notes
├── vectorstore/             # ChromaDB persisted embeddings (auto-generated)
├── tests/
│   ├── test_ingest.py       # Tests for the ingestion pipeline
│   └── test_rag.py          # Tests for the RAG chain
└── docs/
    └── superpowers/
        ├── specs/           # Design specification
        └── plans/           # Implementation plan
```

---

## Running Tests

```bash
source .venv/bin/activate
pytest tests/ -v
```

Expected output:

```
tests/test_ingest.py::test_ingest_creates_vectorstore PASSED
tests/test_ingest.py::test_ingest_fails_on_empty_data_dir PASSED
tests/test_rag.py::test_ask_returns_answer_and_usage PASSED
tests/test_rag.py::test_ask_passes_question_to_retriever PASSED
tests/test_rag.py::test_ask_injects_retrieved_context_into_prompt PASSED

5 passed
```

---

## Available Models

| Model | Speed | Quality | Daily token limit (free tier) |
|---|---|---|---|
| LLaMA 3.3 70B *(default)* | Medium | Highest | 100,000 |
| LLaMA 3.1 8B (Fast) | Fast | Good | 500,000 |
| Gemma 2 9B | Fast | Good | 500,000 |

Switch models using the sidebar dropdown. Token usage is tracked per session.
