from fastapi import APIRouter, UploadFile, File
import uuid
import os
from app.services import ocr_service, embedding_service

# Define the router
router = APIRouter()

@router.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    file_location = f"data/{uuid.uuid4()}_{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    try:
        extracted_content = ocr_service.process_document(file_location)
    except Exception as e:
        return {"error": f"Document processing failed: {str(e)}"}

    if not extracted_content:
        return {"error": "No content could be extracted from the document."}

    doc_id = os.path.basename(file_location)

    texts = [chunk["text"] for chunk in extracted_content]
    metadatas = [{"page": chunk.get("page", 1)} for chunk in extracted_content]

    try:
        db = embedding_service.load_vector_db()
    except Exception:
        db = None

    if not db:
        try:
            db = embedding_service.create_vector_db(texts=texts, ids=[doc_id]*len(texts), metadatas=metadatas)
        except Exception as e:
            return {"error": f"Vector DB creation failed: {str(e)}"}
    else:
        try:
            for text, meta in zip(texts, metadatas):
                embedding_service.add_to_vector_db(db, text, doc_id, metadata=meta)
        except Exception as e:
            return {"error": f"Failed to add content to vector DB: {str(e)}"}

    return {"doc_id": doc_id}