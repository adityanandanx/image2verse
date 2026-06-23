# from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from prod_rag.config import settings
from langgraph.checkpoint.memory import InMemorySaver
from prod_rag.tools import query_lyrics
from prod_rag.prompts import SYSTEM_PROMPT
from pydantic import SecretStr

llm = ChatOpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key=SecretStr("something"),
    reasoning_effort="minimal",
    temperature=0,
    timeout=None,
    max_retries=2,
)

tools = [query_lyrics]

local_agent = create_agent(model=llm, tools=tools, system_prompt=SYSTEM_PROMPT)
