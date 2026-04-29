from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os
import shutil

load_dotenv()

DATA_DIR = "data"
VECTORSTORE_DIR = "vectorstore"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def ingest() -> None:
    txt_loader = DirectoryLoader(DATA_DIR, glob="**/*.txt", loader_cls=TextLoader)
    pdf_loader = DirectoryLoader(DATA_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)

    docs = txt_loader.load() + pdf_loader.load()

    if not docs:
        raise ValueError(f"No documents found in {DATA_DIR}/")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    if os.path.exists(VECTORSTORE_DIR):
        shutil.rmtree(VECTORSTORE_DIR)

    Chroma.from_documents(chunks, embeddings, persist_directory=VECTORSTORE_DIR)
    print(f"Ingested {len(docs)} document(s) → {len(chunks)} chunks → {VECTORSTORE_DIR}/")


if __name__ == "__main__":
    ingest()
