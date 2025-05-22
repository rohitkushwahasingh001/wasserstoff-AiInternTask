from fastapi import FastAPI
from app.api import document, query
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
app = FastAPI()
app.include_router(document.router)
app.include_router(query.router)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Document Chatbot"}