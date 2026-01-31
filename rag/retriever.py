import pickle
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Anchor paths safely
BASE_DIR = Path(__file__).resolve().parent
FAISS_PATH = BASE_DIR / "faiss.index"
DOCS_PATH = BASE_DIR / "docs.pkl"

_model = None
_index = None
_docs = None


def _load_resources():
    global _model, _index, _docs

    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    if _docs is None:
        if not DOCS_PATH.exists():
            raise FileNotFoundError(f"Docs file not found: {DOCS_PATH}")
        with open(DOCS_PATH, "rb") as f:
            _docs = pickle.load(f)

    if _index is None:
        if not FAISS_PATH.exists():
            raise FileNotFoundError(f"FAISS index not found: {FAISS_PATH}")
        _index = faiss.read_index(str(FAISS_PATH))


def retrieve_context(question, top_k=5):
    _load_resources()

    q_emb = _model.encode([question])
    scores, indices = _index.search(q_emb, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        results.append({
            "text": _docs[int(idx)],
            "score": float(score)
        })

    return results

