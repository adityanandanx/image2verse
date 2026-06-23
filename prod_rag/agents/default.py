from langchain_groq import ChatGroq
from langchain.agents import create_agent
from prod_rag.config import settings
from langgraph.checkpoint.memory import InMemorySaver
from prod_rag.tools import query_lyrics
from prod_rag.prompts import SYSTEM_PROMPT

checkpointer = InMemorySaver()

llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=settings.groq_api_key,
)

tools = [query_lyrics]

default_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    # checkpointer=checkpointer,
)
