# YusufBot — Design Spec

**Date:** 2026-04-30  
**Purpose:** A RAG-powered chatbot that answers recruiter questions about Yusuf Berber, presented during and after a Commerzbank interview for the "Trainee Data Science in Big Data & Advanced Analytics" position.

---

## Context

Yusuf will briefly demo YusufBot during the interview, then share the public URL so recruiters can ask follow-up questions afterward. The bot answers in first person as Yusuf, grounded in his CV and prepared interview Q&A notes.

---

## Architecture

```
YusufBot/
├── data/               ← CV + Q&A files (txt or pdf)
├── vectorstore/        ← ChromaDB persisted files (committed to repo)
├── ingest.py           ← one-time script: chunk → embed → save to ChromaDB
├── rag.py              ← RAG chain: retrieve from ChromaDB + generate via Groq
├── app.py              ← Streamlit chat UI
├── .env                ← GROQ_API_KEY (gitignored)
└── requirements.txt
```

---

## Components

### 1. Ingest Pipeline (`ingest.py`)

- Loads all files from `data/` (supports `.txt` and `.pdf`)
- Splits into chunks using `RecursiveCharacterTextSplitter` (chunk size ~500, overlap ~50)
- Embeds using `sentence-transformers/all-MiniLM-L6-v2` via `langchain-huggingface` (free, runs locally, no API key needed)
- Persists to `vectorstore/` using ChromaDB
- Run once locally; the resulting `vectorstore/` is committed to the repo

### 2. RAG Chain (`rag.py`)

- **Retriever**: ChromaDB similarity search, top 4 chunks
- **LLM**: `llama-3.3-70b-versatile` on Groq Cloud
- **Chain type**: `stuff` (all retrieved chunks in one prompt)
- **System prompt**:
  > "You are Yusuf Berber, a data science candidate applying for the Trainee Data Science in Big Data & Advanced Analytics position at Commerzbank. Answer questions about yourself based only on the provided context. Speak in first person, naturally and confidently. If the context doesn't contain enough information to answer, say so honestly rather than making things up."

### 3. Streamlit UI (`app.py`)

- **Title**: "YusufBot — Ask me anything about Yusuf"
- **Subtitle**: "Yusuf is applying for Trainee Data Science in Big Data & Advanced Analytics at Commerzbank"
- **Chat interface**: `st.chat_message` bubbles with full conversation history in session state
- **Input**: `st.chat_input` fixed at the bottom
- **Loading state**: spinner while Groq generates the answer
- No login, no sidebar — just the chat

---

## Data Flow

```
User question
     ↓
Streamlit (app.py)
     ↓
RAG chain (rag.py)
     ↓
ChromaDB similarity search → top 4 chunks
     ↓
Groq LLM (llama-3.3-70b-versatile) + system prompt + chunks + question
     ↓
First-person answer displayed in chat
```

---

## Deployment

- **Platform**: Streamlit Cloud (free, GitHub-integrated)
- **URL**: `https://yusufbot.streamlit.app` (or similar)
- **Secret**: `GROQ_API_KEY` set in Streamlit Cloud dashboard (never in code or git)
- **`vectorstore/`** committed to repo — no ingestion step needed in the cloud
- **`.env`** gitignored — used locally only

### Go-live steps
1. Add CV + Q&A files to `data/`
2. Run `ingest.py` locally
3. Commit everything including `vectorstore/` and push to GitHub
4. Connect repo to Streamlit Cloud, add `GROQ_API_KEY` secret, deploy

---

## Key Decisions

| Decision | Choice | Reason |
|---|---|---|
| LLM | Groq `llama-3.3-70b-versatile` | Fast inference, free tier, strong quality |
| Embeddings | `all-MiniLM-L6-v2` (local) | Free, no API key, small model (~90MB) |
| Vector store | ChromaDB (persisted to disk) | Simple, file-based, committable to git |
| UI | Streamlit | Python-native, DS-relevant, zero frontend work |
| Deployment | Streamlit Cloud | Free, GitHub-integrated, no cold-start issues |
