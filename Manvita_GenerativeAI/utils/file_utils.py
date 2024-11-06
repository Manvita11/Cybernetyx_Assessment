from PyPDF2 import PdfReader
import docx
from fastapi import UploadFile

def extract_text(file: UploadFile) -> str:
    content = ""
    if file.filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        for page in reader.pages:
            content += page.extract_text()
    elif file.filename.endswith(".docx"):
        doc = docx.Document(file.file)
        for paragraph in doc.paragraphs:
            content += paragraph.text
    elif file.filename.endswith(".txt"):
        content = file.file.read().decode("utf-8")
    return content
