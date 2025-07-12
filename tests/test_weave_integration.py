"""Test script to verify Weave integration with ADK."""

import asyncio
from example_agent.agent import root_agent
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService


async def test_weave_integration():
    """Test the Weave integration with ADK agent."""

    # Set up session and runner
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="test_app", user_id="test_user", session_id="test_session"
    )

    runner = Runner(
        agent=root_agent, app_name="test_app", session_service=session_service
    )

    # Create a test message
    content = types.Content(
        role="user",
        parts=[types.Part(text="Hello! Can you help me with file management?")],
    )

    # Run the agent with tracing
    events = runner.run_async(
        user_id="test_user", session_id="test_session", new_message=content
    )

    # Collect all events
    all_events = [event async for event in events]

    print("Test completed! Check Weave dashboard for traces.")
    print(f"Number of events generated: {len(all_events)}")

    return all_events


if __name__ == "__main__":
    asyncio.run(test_weave_integration())
