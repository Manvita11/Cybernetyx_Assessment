from fastapi import FastAPI, UploadFile, File
from sentence_transformers import SentenceTransformer
import chromadb
from utils.file_utils import extract_text

app = FastAPI()

# Initialize the SentenceTransformer model (running on CPU)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Initialize ChromaDB client with persistence
client = chromadb.PersistentClient(path="./chroma_db")  # Persistence in the chroma_db directory
collection = client.get_or_create_collection("documents")

@app.get("/")
async def root():
    return {"message": "Welcome to the RAG API!"}

@app.post("/ingest/")
async def ingest_file(file: UploadFile = File(...)):
    text = extract_text(file)
    if text:
        embedding = model.encode(text)
        # Add embedding to ChromaDB
        collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[{"filename": file.filename}]
        )
        return {"status": "Document ingested successfully"}
    return {"status": "Failed to extract text"}

@app.get("/query/")
async def query_documents(query: str):
    query_embedding = model.encode(query)
    # Search in ChromaDB for similar documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
    return {"results": results}
