import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL, TOP_K_RESULTS, MAX_TOP_K

# =========================
# Embedding Model
# =========================
model = SentenceTransformer(EMBEDDING_MODEL)

# =========================
# Global Bellek Yapıları
# =========================
index = None
chunks_store = []
metadata_store = []
files_store = {}


# =========================
# Chunk Oluşturma
# =========================
def chunk_text(text: str):
    """
    Uzun metni overlap kullanarak küçük parçalara böler.
    """
    chunks = []
    start = 0

    if not text or not text.strip():
        return chunks

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


# =========================
# Doküman Ekleme
# =========================
def add_document(text: str, filename: str):
    """
    Dokümanı chunk'lara böler, embedding üretir ve FAISS index'e ekler.
    """
    global index

    chunks = chunk_text(text)

    if not chunks:
        return 0

    embeddings = model.encode(chunks, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    if index is None:
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    for i, chunk in enumerate(chunks):
        chunks_store.append(chunk)
        metadata_store.append({
            "filename": filename,
            "chunk_id": i,
            "active": True,
            "deleted": False
        })

    files_store[filename] = {
        "active": True,
        "deleted": False,
        "chunks": len(chunks)
    }

    return len(chunks)


# =========================
# Arama
# =========================
def search(query: str, selected_files=None, top_k: int = TOP_K_RESULTS):
    """
    Kullanıcı sorusuna en yakın chunk'ları FAISS ile bulur.
    selected_files verilirse sadece seçilen dosyalarda arama yapar.
    """
    if index is None or index.ntotal == 0:
        return []

    if not query or not query.strip():
        return []

    top_k = max(1, min(int(top_k), MAX_TOP_K))

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k * 5)

    results = []

    for i, idx in enumerate(indices[0]):
        if idx == -1 or idx >= len(metadata_store):
            continue

        metadata = metadata_store[idx]
        filename = metadata["filename"]

        if metadata.get("deleted", False):
            continue

        if selected_files:
            if filename not in selected_files:
                continue
        else:
            if not metadata.get("active", True):
                continue

        results.append({
            "content": chunks_store[idx],
            "metadata": metadata,
            "score": float(distances[0][i])
        })

        if len(results) >= top_k:
            break

    return results


# =========================
# Doküman Listeleme
# =========================
def list_documents():
    """
    Sisteme yüklenen dokümanların durumunu döndürür.
    """
    return files_store


# =========================
# Doküman Aktif/Pasif
# =========================
def toggle_document(filename: str):
    """
    Bir dokümanı aktif/pasif yapar.
    Pasif doküman genel aramalara dahil edilmez.
    """
    if filename not in files_store:
        return None

    files_store[filename]["active"] = not files_store[filename]["active"]

    for metadata in metadata_store:
        if metadata["filename"] == filename:
            metadata["active"] = files_store[filename]["active"]

    return files_store[filename]


# =========================
# Doküman Silme
# =========================
def remove_document(filename: str):
    """
    Dokümanı soft-delete yapar.
    FAISS index fiziksel olarak silinmez ama aramalarda dikkate alınmaz.
    """
    if filename not in files_store:
        return None

    files_store[filename]["deleted"] = True
    files_store[filename]["active"] = False

    for metadata in metadata_store:
        if metadata["filename"] == filename:
            metadata["deleted"] = True
            metadata["active"] = False

    return files_store[filename]