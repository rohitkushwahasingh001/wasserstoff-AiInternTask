from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def create_vector_db(texts, ids, metadatas=None):
    if not texts or not ids:
        raise ValueError("Cannot create vector DB with empty texts or IDs")
    db = FAISS.from_texts(
        texts=texts,
        embedding=embed_model,
        metadatas=[{"id": i, "page": m.get("page", 1)} for i, m in zip(ids, metadatas)]
    )
    db.save_local("faiss_index")
    return db

def load_vector_db():
    if not os.path.exists("faiss_index"):
        raise FileNotFoundError("FAISS index does not exist. Create one first.")
    return FAISS.load_local(
        "faiss_index",
        embed_model,
        allow_dangerous_deserialization=True
    )

def add_to_vector_db(db, new_text, doc_id, metadata=None):
    if not new_text.strip():
        raise ValueError("Empty text cannot be added to vector DB")
    db.add_texts(
        texts=[new_text],
        metadatas=[{"id": doc_id, "page": metadata.get("page", 1)}]
    )
    db.save_local("faiss_index")