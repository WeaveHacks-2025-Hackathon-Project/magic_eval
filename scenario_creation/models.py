"""Pydantic models for scenario creation and testing."""

from pydantic import BaseModel


class Scenario(BaseModel):
    """A scenario is a set of inputs and expected outputs for an agent."""

    query: str
    expected_tool_calls: list[str]
