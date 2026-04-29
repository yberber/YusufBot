from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

VECTORSTORE_DIR = "vectorstore"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

GROQ_MODELS = {
    "llama-3.3-70b-versatile": {"label": "LLaMA 3.3 70B", "daily_limit": 100_000},
    "llama-3.1-8b-instant": {"label": "LLaMA 3.1 8B (Fast)", "daily_limit": 500_000},
    "gemma2-9b-it": {"label": "Gemma 2 9B", "daily_limit": 500_000},
}

SYSTEM_PROMPT = (
    "You are Yusuf Berber, a data science candidate applying for the "
    "Trainee Data Science in Big Data & Advanced Analytics position at Commerzbank. "
    "Answer questions about yourself based only on the provided context. "
    "Speak in first person, naturally and confidently. "
    "If the context doesn't contain enough information to answer, "
    "say so honestly rather than making things up.\n\n"
    "Context:\n{context}"
)


def create_retriever():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 4})


def ask(question: str, model_name: str, retriever) -> tuple[str, dict]:
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)

    llm = ChatGroq(model=model_name, api_key=os.getenv("GROQ_API_KEY"))
    messages = [
        SystemMessage(content=SYSTEM_PROMPT.format(context=context)),
        HumanMessage(content=question),
    ]
    response = llm.invoke(messages)

    usage = {
        "input_tokens": (response.usage_metadata or {}).get("input_tokens", 0),
        "output_tokens": (response.usage_metadata or {}).get("output_tokens", 0),
        "total_tokens": (response.usage_metadata or {}).get("total_tokens", 0),
    }
    return response.content, usage
