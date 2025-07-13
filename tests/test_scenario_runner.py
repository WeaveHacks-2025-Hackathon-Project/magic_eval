import pytest
from src.runner.scenario_runner import call_agent_async
from example_agent.agent import root_agent


@pytest.mark.asyncio
async def test_scenario_runner():
    events = await call_agent_async(
        agent=root_agent,
        query="Flip a coin",
        user_id="test_user",
        session_id="test_session",
        app_name="test_app",
    )

    assert len(events) > 0
    assert events is not None
