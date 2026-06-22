import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from prod_rag.config import settings
from functools import lru_cache


@lru_cache(maxsize=1)
def get_chroma_client():
    _client = chromadb.PersistentClient(path=settings.chroma_db_path)
    return _client


@lru_cache(maxsize=1)
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
    )


def get_vector_store(collection_name: str):
    client = get_chroma_client()
    return Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=get_embeddings(),
    )


def get_retriever(collection_name: str):
    vs = get_vector_store(collection_name)
    return vs.as_retriever()


if __name__ == "__main__":
    vs = get_vector_store("genius-lyrics-the-strokes")
    results = vs.similarity_search("At the door")
    print(results)
