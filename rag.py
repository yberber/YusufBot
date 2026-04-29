from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

VECTORSTORE_DIR = "vectorstore"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

SYSTEM_PROMPT = (
    "You are Yusuf Berber, a data science candidate applying for the "
    "Trainee Data Science in Big Data & Advanced Analytics position at Commerzbank. "
    "Answer questions about yourself based only on the provided context. "
    "Speak in first person, naturally and confidently. "
    "If the context doesn't contain enough information to answer, "
    "say so honestly rather than making things up.\n\n"
    "Context:\n{context}"
)


def create_chain():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ])

    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, combine_docs_chain)


def ask(question: str, chain) -> str:
    result = chain.invoke({"input": question})
    return result["answer"]
