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


# Create a custom completion function that uses your specific model
def llama_completion(messages, **kwargs):
    return completion(
        model="meta-llama/Llama-4-Scout-17B-16E-Instruct-FP8",  # Your specific model
        messages=messages,
        **kwargs,
    )


root_agent = LlmAgent(
    model="meta-llama/Llama-4-Scout-17B-16E-Instruct-FP8",  # Correct model identifier
    name="filesystem_assistant_agent",
    instruction="Help the user manage their files. You can list files, read files, etc.",
    tools=[COIN_FLIP_MCP_SERVER],
    llm_completion_function=llama_completion,  # Use custom completion function
)
