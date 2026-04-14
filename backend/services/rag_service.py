import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_docs():
    text = open("rag_data/knowledge.txt").read()
    chunks = text.split("\n\n")
    return [c.strip() for c in chunks if c.strip()]


docs = load_docs()

embeddings = model.encode(docs)
embeddings = np.array(embeddings).astype("float32")

faiss.normalize_L2(embeddings) 

index = faiss.IndexFlatIP(embeddings.shape[1]) 
index.add(embeddings)


def get_rag_context(query, k=5):
    q_emb = model.encode([query])
    q_emb = np.array(q_emb).astype("float32")

    faiss.normalize_L2(q_emb) 

    D, I = index.search(q_emb, k)

    results = []
    seen = set()

    for idx, score in zip(I[0], D[0]):
        doc = docs[idx]

        if doc not in seen:
            seen.add(doc)

            if score > 0.4:
                results.append(doc)

    return "\n\n".join(results[:3])