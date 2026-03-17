from rag_engine.vector_store import search

def retrieve_context(code, language="general"):

    docs = search(code, language=language, k=2)

    context = "\n".join(docs)

    return context