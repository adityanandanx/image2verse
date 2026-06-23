from fastapi import APIRouter, UploadFile, Form, File
from prod_rag.agents.local_gemma4 import local_agent
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel
from typing import Any, Annotated
from uuid import uuid4
import base64

checkpointer = InMemorySaver()

agent = local_agent
agent.checkpointer = checkpointer

chat_router = APIRouter(prefix="/chat")


class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    trace: str
    thread_id: str


@chat_router.post("/", response_model=ChatResponse)
async def chat(
    message: str = Form(),
    thread_id: str | None = Form(default=None),
    image: UploadFile = File(default=None),
):
    thread_id = thread_id or str(uuid4())

    content: list[dict[str, Any]] = [
        {"type": "text", "text": message},
    ]
    if image:
        image_bytes = await image.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{image.content_type};base64,{base64_image}"
                },
            }
        )

    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": content}]},
        config={"configurable": {"thread_id": thread_id}},
    )

    response_text = result["messages"][-1].content
    print(result)
    return ChatResponse(response=response_text, trace="", thread_id=thread_id)
