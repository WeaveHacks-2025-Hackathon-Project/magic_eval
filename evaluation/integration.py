"""Integration tests for the time agent using Google ADK evaluation framework."""

import os
import sys
from pathlib import Path
from google.adk.evaluation.agent_evaluator import AgentEvaluator
import pytest

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.mark.asyncio
async def test_time_agent_with_single_test_file():
    """Test the time agent's basic ability via a session file."""
    await AgentEvaluator.evaluate(
        agent_module="example_agent",
        eval_dataset_file_path_or_dir="evaluation/evaluation.test.json",
    )

@pytest.mark.asyncio
async def test_time_agent_with_config():
    """Test the time agent with custom evaluation criteria."""
    await AgentEvaluator.evaluate(
        agent_module="example_agent",
        eval_dataset_file_path_or_dir="evaluation/evaluation.test.json",
        config_file_path="evaluation/test_config.json",
    )

@pytest.mark.asyncio
async def test_time_agent_specific_cases():
    """Test specific evaluation cases from the test file."""
    # This will run only specific test cases if needed
    await AgentEvaluator.evaluate(
        agent_module="example_agent",
        eval_dataset_file_path_or_dir="evaluation/evaluation.test.json:get_current_time_test,no_tool_needed_test",
    )

if __name__ == "__main__":
    # Run the tests directly
    import asyncio
    
    async def main():
        print("Running time agent evaluation tests...")
        
        try:
            await test_time_agent_with_single_test_file()
            print("✓ Basic evaluation test passed")
        except Exception as e:
            print(f"✗ Basic evaluation test failed: {e}")
        
        try:
            await test_time_agent_with_config()
            print("✓ Config-based evaluation test passed")
        except Exception as e:
            print(f"✗ Config-based evaluation test failed: {e}")
        
        try:
            await test_time_agent_specific_cases()
            print("✓ Specific cases evaluation test passed")
        except Exception as e:
            print(f"✗ Specific cases evaluation test failed: {e}")
    
    asyncio.run(main())