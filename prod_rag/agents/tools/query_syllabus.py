from langchain.tools import tool

from prod_rag.vectorstore import get_vector_store


@tool(response_format="content_and_artifact")
def query_syllabus(query: str):
    """Retrieve information from the Graphic Era University(GEU) syllabus."""
    vector_store = get_vector_store("geu-syllabus")
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs
