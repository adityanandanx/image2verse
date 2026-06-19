# from langchain.agents import AgentExecutor
from prod_rag.agents.default import default_agent
import uuid
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from typing import Any
import uuid
from typing import Any
from langchain_core.messages import (
    HumanMessage,
    AIMessageChunk,
    AnyMessage,
    AIMessage,
    ToolMessage,
)
from langchain_core.runnables import RunnableConfig

# 1. Type-hint your config using the strict LangChain class
config: RunnableConfig = {"configurable": {"thread_id": str(uuid.uuid4())}}


def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)


def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")


def run_cli():
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            # Format the input structure for the agent
            inputs: Any = {"messages": [HumanMessage(content=user_input)]}

            # 3. Consume the message streams dynamically
            for chunk in default_agent.stream(
                inputs, config=config, stream_mode=["messages", "updates"], version="v2"
            ):

                if chunk["type"] == "messages":
                    token, metadata = chunk["data"]
                    if isinstance(token, AIMessageChunk):
                        _render_message_chunk(token)
                elif chunk["type"] == "updates":
                    for source, update in chunk["data"].items():
                        if source in ("model", "tools"):  # `source` captures node name
                            _render_completed_message(update["messages"][-1])

            print("\n")  # Clear break after the response terminates

        except KeyboardInterrupt:
            print("\nSession interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}\n")


if __name__ == "__main__":
    run_cli()
