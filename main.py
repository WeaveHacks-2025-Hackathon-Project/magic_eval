# 1. Get tools from agent

from src.models import ToolInfo
from src.runner.scenario_runner import run_scenario
from src.creation.main import create_scenarios
from rich.console import Console
import asyncio

console = Console()

tool_info = [
    ToolInfo(
        name="get_current_time",
        description="Get the current time",
        parameters={"timezone": "string"},
    ),
    ToolInfo(
        name="get_current_time",
        description="Get the current time",
        parameters={"timezone": "string"},
    ),
]


# 2. Create scenarios
scenarios = create_scenarios(tool_info)

# Pretty print scenario and allow user to select yes or not
final_scenarios = []

for scenario in scenarios:
    console.print(scenario)
    user_input = console.input("Do you want to keep this scenario? (y/n): ")
    if user_input == "y":
        final_scenarios.append(scenario)
    else:
        console.print(f"Skipping scenario: {scenario.name}")

from example_agent.agent import root_agent


async def run_scenarios():
    # 3. Run scenarios
    results = []
    for scenario in final_scenarios:
        console.print(f"Running scenario: {scenario.name}")
        result = await run_scenario(scenario, root_agent)
        results.append(result)

    console.print("--------------------------------")
    console.print("Results:")
    console.print("--------------------------------")
    # 4. Evaluate scenarios
    for result in results:
        console.print(result)


# Run the async function
if __name__ == "__main__":
    asyncio.run(run_scenarios())
