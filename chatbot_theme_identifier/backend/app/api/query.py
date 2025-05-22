from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
import numpy as np

# Import services
from app.services import embedding_service, llm_service, theme_service

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query/")
async def answer_query(req: QueryRequest):
    try:
        db = embedding_service.load_vector_db()
    except Exception as e:
        return {"error": "Vector DB not initialized", "details": str(e)}

    try:
        results = db.similarity_search_with_score(req.question, k=5)
    except Exception as e:
        return {"error": "Similarity search failed", "details": str(e)}

    responses = []
    citations = []

    for res, score in results:
        # Debug: Print raw content and score
        print(f"\n[DEBUG] FAISS Result - Score: {score}")
        print(f"Content Preview: {res.page_content[:200]}...")

        prompt = f"""
You are an AI assistant. Answer the user's question strictly based on the provided context.

Context:
{res.page_content}

Question:
{req.question}

Instructions:
- If the answer is not found in the context, say so explicitly.
- Include citation: Document ID and Page Number
"""

        ans = llm_service.query_llm(prompt)
        responses.append(ans)

        # Convert np.float32 to Python float before adding to JSON response
        citations.append({
            "id": res.metadata.get("id", "unknown"),
            "page": res.metadata.get("page", "unknown"),
            "score": float(score)  # ← Important Fix: Cast to Python float
        })

    if not responses:
        return {
            "answer": "I couldn't find any relevant information to answer this query.",
            "citations": []
        }

    try:
        final_answer = theme_service.identify_themes(responses)
    except Exception as e:
        final_answer = f"Theme identification failed: {str(e)}"

    return {
        "answer": final_answer,
        "citations": citations
    }