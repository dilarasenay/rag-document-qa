from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import sys
import shutil
import uuid

# Backend dizinini path'e ekle (Import hatalarını önlemek için)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_UPLOAD_SIZE
from file_processor import extract_text
from embeddings import (
    add_document,
    list_documents,
    toggle_document,
    remove_document,
    metadata_store,
)
from rag_engine import ask_question


app = FastAPI(
    title="RAG Doküman Soru-Cevap Sistemi",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(UPLOAD_DIR, exist_ok=True)


class QuestionRequest(BaseModel):
    question: str
    selected_files: list[str] = []
    top_k: int = 5


@app.get("/")
def root():
    return {
        "message": "RAG API çalışıyor 🚀",
        "version": "1.1.0"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "total_chunks": len(metadata_store),
        "documents": list_documents()
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Sadece {ALLOWED_EXTENSIONS} desteklenir."
        )

    content = await file.read()

    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Dosya çok büyük. Maksimum dosya boyutu aşıldı."
        )

    safe_filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as f:
        f.write(content)

    try:
        text = extract_text(file_path)

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Dosya içeriği okunamadı veya boş."
            )

        chunk_count = add_document(text, file.filename)

        return {
            "message": f"{file.filename} yüklendi",
            "stored_as": safe_filename,
            "chunks": chunk_count
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Dosya işlenirken hata oluştu: {str(e)}"
        )


@app.post("/ask")
def ask(req: QuestionRequest):
    selected_files = req.selected_files if req.selected_files else None

    return ask_question(
        question=req.question,
        selected_files=selected_files,
        top_k=req.top_k
    )


@app.get("/documents")
def documents():
    return {
        "documents": list_documents()
    }


@app.post("/toggle_file/{filename}")
def toggle_file(filename: str):
    result = toggle_document(filename)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Dosya bulunamadı."
        )

    return {
        "filename": filename,
        "status": result
    }


@app.delete("/remove_file/{filename}")
def delete_file(filename: str):
    result = remove_document(filename)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Dosya bulunamadı."
        )

    for uploaded_file in os.listdir(UPLOAD_DIR):
        if uploaded_file.endswith(filename):
            try:
                os.remove(os.path.join(UPLOAD_DIR, uploaded_file))
            except Exception:
                pass

    return {
        "message": f"{filename} silindi",
        "status": result
    }


@app.get("/preview/{filename}")
def preview_file(filename: str):
    target_file = None

    for uploaded_file in os.listdir(UPLOAD_DIR):
        if uploaded_file.endswith(filename):
            target_file = os.path.join(UPLOAD_DIR, uploaded_file)
            break

    if not target_file:
        raise HTTPException(
            status_code=404,
            detail="Dosya bulunamadı."
        )

    try:
        content = extract_text(target_file)

        return {
            "filename": filename,
            "preview": content[:5000]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Önizleme hatası: {str(e)}"
        )


@app.get("/get_pdf/{filename}")
def get_pdf(filename: str):
    target_file = None

    for uploaded_file in os.listdir(UPLOAD_DIR):
        if uploaded_file.endswith(filename):
            target_file = os.path.join(UPLOAD_DIR, uploaded_file)
            break

    if not target_file:
        raise HTTPException(
            status_code=404,
            detail="PDF bulunamadı."
        )

    return FileResponse(
        target_file,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline"}
    )