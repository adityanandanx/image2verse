from prod_rag.vectorstore import get_vector_store


def query_lyrics_service(query: str):
    """Semantically search lyrics of the strokes"""
    vector_store = get_vector_store("genius-lyrics-the-strokes")
    retrieved_docs = vector_store.similarity_search(query, k=10)
    return retrieved_docs
