"""Test script to verify Weave integration with ADK."""

import asyncio
import os
import pytest
from example_agent.agent import root_agent
from src.runner.scenario_runner import call_agent_async
from weave_config import setup_weave_tracing


@pytest.mark.asyncio
async def test_weave_integration():
    """Test the Weave integration with ADK agent."""

    print("Starting Weave integration test...")
    print(f"Using model: {root_agent.model}")
    print(f"Agent name: {root_agent.name}")

    # Verify environment variables
    llama_key = os.getenv("LLAMA_API_KEY")
    wandb_key = os.getenv("WANDB_API_KEY")

    if not llama_key:
        print("❌ LLAMA_API_KEY not found in environment")
        return False
    else:
        print("✅ LLAMA_API_KEY found")

    if not wandb_key:
        print("❌ WANDB_API_KEY not found in environment")
        return False
    else:
        print("✅ WANDB_API_KEY found")

    # Verify Weave tracing setup
    try:
        tracer = setup_weave_tracing()
        print("✅ Weave tracing initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Weave tracing: {e}")
        return False

    print("Running agent with message: 'Flip a coin'")
    print("This should trigger the coin flip MCP tool...")

    # Run the agent with tracing using scenario_runner helper
    try:
        all_events = await call_agent_async(
            agent=root_agent,
            query="Flip a coin",
            user_id="test_user",
            session_id="test_session",
            app_name="test_app",
        )

        # Log events for debugging
        for event in all_events:
            if hasattr(event, "content") and event.content:
                print(
                    f"Event: {type(event).__name__} - Content: {event.content.parts[0].text if event.content.parts else 'No text'}"
                )
            else:
                print(f"Event: {type(event).__name__}")

        print("\nTest completed! Check Weave dashboard for traces.")
        print(f"Number of events generated: {len(all_events)}")

        # Check if we got a final response
        final_events = [
            e
            for e in all_events
            if hasattr(e, "is_final_response") and e.is_final_response()
        ]
        if final_events:
            print("✅ Final response received")
            return True
        else:
            print("⚠️  No final response detected")
            return False

    except Exception as e:
        print(f"❌ Error during agent execution: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_weave_integration())
    if success:
        print("\n🎉 Weave integration test PASSED!")
    else:
        print("\n💥 Weave integration test FAILED!")
        exit(1)
