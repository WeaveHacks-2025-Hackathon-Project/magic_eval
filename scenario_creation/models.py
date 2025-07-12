"""Pydantic models for scenario creation and testing."""

from pydantic import BaseModel


class Scenario(BaseModel):
    """A scenario is a set of inputs and expected outputs for an agent."""

    # TODO: Add Field, description using Pydantic
    query: str
    expected_tool_calls: list[str]
