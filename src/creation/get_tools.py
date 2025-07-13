from google.adk.agents import Agent
from src.models import AgentTools, ToolInfo


def get_tools_from_agent(adk_agent: Agent) -> AgentTools:
    """
    Extract tools and their descriptions from an ADK agent.

    Args:
        adk_agent: The ADK agent to extract tools from

    Returns:
        AgentTools: A Pydantic model containing the list of tools and their descriptions
    """
    tools_info = []

    # Extract tools from the agent
    if hasattr(adk_agent, "tools") and adk_agent.tools:
        for tool in adk_agent.tools:
            tool_info = ToolInfo(
                name=tool.name if hasattr(tool, "name") else str(tool),
                description=tool.description
                if hasattr(tool, "description")
                else "No description available",
                parameters=getattr(tool, "parameters", None),
            )
            tools_info.append(tool_info)

    # Get agent name
    agent_name = getattr(adk_agent, "name", "Unknown Agent")

    return AgentTools(tools=tools_info, agent_name=agent_name)
