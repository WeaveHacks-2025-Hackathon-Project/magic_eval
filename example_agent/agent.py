"""Example agent implementation using Google ADK with MCP toolset."""

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

COIN_FLIP_MCP_SERVER = [
    MCPToolset(
        connection_params=StdioServerParameters(
            command="npx", args=["-y", "@modelcontextprotocol/server-coin-flip"]
        )
    )
]

root_agent = LlmAgent(
    model="gemini-2.0-flash",  # TODO: Change this to LiteLLM
    name="filesystem_assistant_agent",
    instruction="Help the user manage their files. You can list files, read files, etc.",
    tools=[COIN_FLIP_MCP_SERVER],
)
