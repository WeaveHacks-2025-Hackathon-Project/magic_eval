"""Scenario runner utilities for Google ADK agent interactions."""

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from src.creation.scenario_creator import Scenario


async def setup_session_and_runner(
    agent: Agent, app_name: str, user_id: str, session_id: str
):
    """Set up session and runner for agent interaction."""
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )
    runner = Runner(agent=agent, app_name=app_name, session_service=session_service)
    return session, runner


async def call_agent_async(
    agent: Agent, query, user_id: str, session_id: str, app_name: str
):
    """Call agent asynchronously with a query and return all events."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    _, runner = await setup_session_and_runner(agent, app_name, user_id, session_id)
    events = runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    )

    all_events = [event async for event in events]
    return all_events


# TODO: Create a function to run a scenario
async def run_scenario(scenario: Scenario, agent: Agent) -> bool:
    """Run a scenario and return True if successful, False otherwise."""
    expected_tool_call = scenario.expected_tool_call

    # Filler names
    user_id = ("1",)
    session_id = ("2",)
    app_name = ("3",)

    events = await call_agent_async(
        agent, scenario.query, user_id, session_id, app_name
    )

    all_function_calls = []
    for event in events:
        all_function_calls.extend(event.get_function_calls())

    if expected_tool_call is None and len(all_function_calls) == 0:
        return True

    if expected_tool_call is not None and expected_tool_call in all_function_calls:
        return True

    return False
