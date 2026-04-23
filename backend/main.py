from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, shutil

from config import UPLOAD_DIR
from file_processor import extract_text
from embeddings import add_document, metadata_store
from rag_engine import ask_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(UPLOAD_DIR, exist_ok=True)

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "RAG API çalışıyor 🚀"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_text(file_path)
    add_document(text, file.filename)

    return {"message": f"{file.filename} yüklendi"}

@app.post("/ask")
def ask(req: QuestionRequest):
    return ask_question(req.question)

@app.get("/documents")
def list_docs():
    files = list(set([m["filename"] for m in metadata_store]))
    return {"documents": files}