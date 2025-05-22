import os
from PIL import Image
import pytesseract
import pdfplumber
import docx2txt


# Suppress CropBox warnings from pdfplumber
import warnings
warnings.filterwarnings("ignore", message="CropBox.*")

def extract_text_from_pdf(pdf_path):
    texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                texts.append({"page": i + 1, "text": text})
    return texts

def extract_text_from_image(image_path):
    return pytesseract.image_to_string(Image.open(image_path))

def extract_text_from_docx(docx_path):
    text = docx2txt.process(docx_path)
    return [{"page": 1, "text": text}]

def process_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        return [{"page": 1, "text": extract_text_from_image(file_path)}]
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")