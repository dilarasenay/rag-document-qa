import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL, TOP_K_RESULTS

model = SentenceTransformer(EMBEDDING_MODEL)

index = None
chunks_store = []
metadata_store = []

def chunk_text(text: str):
    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks

def add_document(text: str, filename: str):
    global index

    chunks = chunk_text(text)

    if not chunks:
        return

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
            "chunk_id": i
        })

def search(query: str):
    if index is None or index.ntotal == 0:
        return []

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, TOP_K_RESULTS)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1:
            results.append({
                "content": chunks_store[idx],
                "metadata": metadata_store[idx],
                "score": float(distances[0][i])
            })

    return results