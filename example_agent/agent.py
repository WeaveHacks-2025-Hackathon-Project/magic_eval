"""Example agent implementation using Google ADK with MCP toolset."""

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from litellm import completion

# Load environment variables
load_dotenv()

COIN_FLIP_MCP_SERVER = [
    MCPToolset(
        connection_params=StdioServerParameters(
            command="npx", args=["-y", "@modelcontextprotocol/server-coin-flip"]
        )
    )
]

# Configure LiteLLM with Llama
os.environ["LLAMA_API_KEY"] = os.getenv("LLAMA_API_KEY")

root_agent = LlmAgent(
    model="llama",  # Using Llama through LiteLLM
    name="filesystem_assistant_agent",
    instruction="Help the user manage their files. You can list files, read files, etc.",
    tools=[COIN_FLIP_MCP_SERVER],
    llm_completion_function=completion,  # Use LiteLLM's completion function
)
