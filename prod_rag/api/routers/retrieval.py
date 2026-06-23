from fastapi import APIRouter
from prod_rag.api.services.query_lyrics import query_lyrics_service

retrieval_router = APIRouter(prefix="/retrieve")


@retrieval_router.get("/query-lyrics")
def query_lyrics(query: str):
    result = query_lyrics_service(query)
    return result
