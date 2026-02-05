# rag/build_index_openai.py
from __future__ import annotations

import os
import pickle
from pathlib import Path
from typing import Iterator, List

import faiss
import numpy as np
from openai import OpenAI

EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
BATCH_SIZE = int(os.getenv("EMBED_BATCH_SIZE", "64"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
MAX_CHUNKS = int(os.getenv("MAX_CHUNKS", "0"))  # 0 = no limit

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
DATA_DIR = ROOT / "data"
DOCS_PATH = BASE / "docs.pkl"
FAISS_PATH = BASE / "faiss.index"

client = OpenAI()

def chunk_text(text: str, chunk_size: int, overlap: int) -> Iterator[str]:
    text = text.replace("\r\n", "\n").strip()
    n = len(text)
    if n == 0:
        return
    start = 0
    while start < n:
        end = min(n, start + chunk_size)
        c = text[start:end].strip()
        if c:
            yield c
        start = max(0, end - overlap)
        if start >= n:
            break

def embed_batch(texts: List[str]) -> np.ndarray:
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    vecs = np.array([d.embedding for d in resp.data], dtype="float32")
    faiss.normalize_L2(vecs)
    return vecs

def iter_sources() -> Iterator[tuple[str, str]]:
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Missing data folder: {DATA_DIR}")
    files = sorted(DATA_DIR.rglob("*.txt"))
    if not files:
        raise FileNotFoundError(f"No .txt files found in: {DATA_DIR}")
    for fp in files:
        yield fp.name, fp.read_text(encoding="utf-8", errors="ignore")

def main():
    docs: List[str] = []
    vec_batches: List[np.ndarray] = []

    chunk_count = 0
    pending: List[str] = []

    for fname, text in iter_sources():
        for i, c in enumerate(chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP), start=1):
            docs.append(f"[{fname} | chunk {i}]\n{c}")
            pending.append(docs[-1])
            chunk_count += 1

            if MAX_CHUNKS and chunk_count >= MAX_CHUNKS:
                break

            if len(pending) >= BATCH_SIZE:
                vec_batches.append(embed_batch(pending))
                pending.clear()

        if MAX_CHUNKS and chunk_count >= MAX_CHUNKS:
            break

    if pending:
        vec_batches.append(embed_batch(pending))
        pending.clear()

    if not docs:
        raise RuntimeError("No chunks produced. Check your data/*.txt files.")

    vecs = np.vstack(vec_batches)
    dim = vecs.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vecs)

    with open(DOCS_PATH, "wb") as f:
        pickle.dump(docs, f)

    faiss.write_index(index, str(FAISS_PATH))

    print(f"Chunks: {len(docs)}")
    print("Wrote:", DOCS_PATH, FAISS_PATH)

if __name__ == "__main__":
    main()
