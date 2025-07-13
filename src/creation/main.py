from scenario_creator import Scenario_Eval_Crew
from src.models import Scenario, ScenarioList, Tool
import json


def run():
    """Run the scenario evaluation crew with default inputs."""
    # Define the tools that the AI agent can use
    tools = [
        Tool(
            tool_name="get_weather",
            tool_description="Get weather information for a specific location and date. Accepts location (string) and date (string in YYYY-MM-DD format).",
        ),
        Tool(
            tool_name="send_email",
            tool_description="Send an email to a recipient. Accepts recipient_email (string), subject (string), and body (string).",
        ),
        Tool(
            tool_name="search_web",
            tool_description="Search the web for information. Accepts query (string) and returns relevant search results.",
        ),
        Tool(
            tool_name="calculate",
            tool_description="Perform mathematical calculations. Accepts expression (string) and returns the result.",
        ),
    ]

    inputs = {
        "tools": [tool.model_dump() for tool in tools],
    }
    result = Scenario_Eval_Crew().crew().kickoff(inputs=inputs)
    print(result.json_dict)

    scenarios = [Scenario(**scenario) for scenario in result.json_dict["scenarios"]]
    print(scenarios)


def create_scenarios(tools) -> list[Scenario]:
    """Create scenarios for the given tools."""
    inputs = {
        "tools": [tool.model_dump() for tool in tools],
    }
    result = Scenario_Eval_Crew().crew().kickoff(inputs=inputs)
    return [Scenario(**scenario) for scenario in result.json_dict["scenarios"]]


if __name__ == "__main__":
    run()
