import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastmcp import FastMCP, tools
from prod_rag.tools import query_lyrics
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import asyncio

mcp = FastMCP("image2verse")

# Configure CORS for browser-based clients
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins; use specific origins for security
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=[
            "mcp-protocol-version",
            "mcp-session-id",
            "Authorization",
            "Content-Type",
        ],
        expose_headers=["mcp-session-id"],
    )
]

# Automatically create mcp tools from tools array
# doesnt work
# for lc_tool in ALL_TOOLS:
#     print(lc_tool.name)
#     tool = tools.Tool(
#         name=lc_tool.name, parameters=lc_tool.args, description=lc_tool.description
#     )
#     mcp.add_tool(tool)


# @mcp.tool
# def query_lyrics(query: str):
#     """Semantically search lyrics of the strokes"""


@mcp.tool(name="query_lyrics", description="Semantically search lyrics of the strokes")
def query_lyrics_mcp(query: str):
    return query_lyrics.invoke({"query": query})


app = mcp.http_app(middleware=middleware)
