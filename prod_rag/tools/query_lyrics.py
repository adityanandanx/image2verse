from langchain.tools import tool

from prod_rag.vectorstore import get_vector_store


@tool(response_format="content_and_artifact")
def query_lyrics(query: str):
    """Semantically search lyrics of the strokes"""
    vector_store = get_vector_store("genius-lyrics-the-strokes")
    retrieved_docs = vector_store.similarity_search(query, k=10)
    print(retrieved_docs)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs
