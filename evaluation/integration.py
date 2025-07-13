from google.adk.evaluation.agent_evaluator import AgentEvaluator
import pytest

@pytest.mark.asyncio
async def test_with_single_test_file():
    """Test the agent's basic ability via a session file."""
    await AgentEvaluator.evaluate(
        agent_module="automation_agent_store_file_set",
        eval_dataset_file_path_or_dir="evaluation/evaluation.test.json",
    )