"""Pydantic models for scenario creation and testing."""

from typing import List, Optional, Union
from pydantic import BaseModel, Field


class Scenario(BaseModel):
    name: str = Field(..., description="Name of the scenario")
    query: str = Field(..., description="User query for the scenario")
    why_its_suitable: str = Field(..., description="Why it's a suitable scenario")
    expected_tool_call: Union[str, None] = Field(
        ...,
        description="Expected tool call that should be made. This can be set to None if no tool should be called",
    )


class ToolInfo(BaseModel):
    """Information about a tool available to an agent."""

    name: str = Field(..., description="The name of the tool")
    description: str = Field(..., description="A description of what the tool does")
    parameters: Optional[dict] = Field(
        None, description="Tool parameters schema if available"
    )


class ScenarioList(BaseModel):
    scenarios: list[Scenario] = Field(..., description="List of scenarios")


class AgentTools(BaseModel):
    """Collection of tools available to an agent."""

    tools: List[ToolInfo] = Field(
        ..., description="List of tools and their descriptions"
    )
    agent_name: str = Field(..., description="Name of the agent these tools belong to")
