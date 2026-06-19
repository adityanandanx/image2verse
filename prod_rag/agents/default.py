from langchain_groq import ChatGroq
from langchain.agents import create_agent
from prod_rag.config import settings
from langgraph.checkpoint.memory import InMemorySaver
from prod_rag.agents.tools import query_syllabus

checkpointer = InMemorySaver()

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    api_key=settings.groq_api_key,
)

tools = [query_syllabus]

default_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful assistant",
    # checkpointer=checkpointer,
)
