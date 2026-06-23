from fastapi import FastAPI
from prod_rag.api.routers import *

app = FastAPI()


@app.get("/")
async def hello():
    print("Hello world")
    return {"message": "Hello world"}


app.include_router(retrieval_router)
app.include_router(chat_router)

if __name__ == "__main__":
    pass
