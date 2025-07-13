"""Pydantic models for scenario creation and testing."""

from typing import List, Optional
from pydantic import BaseModel, Field


class Scenario(BaseModel):
    """A scenario is a set of inputs and expected outputs for an agent."""

    # TODO: Add Field, description using Pydantic
    query: str
    expected_tool_calls: list[str]


class ToolInfo(BaseModel):
    """Information about a tool available to an agent."""

    name: str = Field(..., description="The name of the tool")
    description: str = Field(..., description="A description of what the tool does")
    parameters: Optional[dict] = Field(
        None, description="Tool parameters schema if available"
    )


class AgentTools(BaseModel):
    """Collection of tools available to an agent."""

    tools: List[ToolInfo] = Field(
        ..., description="List of tools and their descriptions"
    )
    agent_name: str = Field(..., description="Name of the agent these tools belong to")
