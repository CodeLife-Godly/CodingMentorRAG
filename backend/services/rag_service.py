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


def filter_by_language(results, language):
    return [r for r in results if language.lower() in r.lower()]


def prioritize(results, query):
    query_lower = query.lower()

    if "error" in query_lower or "exception" in query_lower:
        return sorted(results, key=lambda x: "Runtime" not in x)

    return results


def get_rag_context(query, language, k=8):
    # Encode query
    q_emb = model.encode([query])
    q_emb = np.array(q_emb).astype("float32")
    faiss.normalize_L2(q_emb)

    # Search FAISS
    D, I = index.search(q_emb, k)

    results = []
    seen = set()

    for idx, score in zip(I[0], D[0]):
        doc = docs[idx]

        if doc not in seen:
            seen.add(doc)
            results.append((doc, score))

    lang_filtered = filter_by_language(
        [doc for doc, _ in results],
        language
    )

    # fallback if too few
    if len(lang_filtered) < 3:
        lang_filtered = [doc for doc, _ in results]

    prioritized = prioritize(lang_filtered, query)

    final = prioritized[:5]

    return "\n\n".join(final)