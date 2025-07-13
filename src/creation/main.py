from scenario_creator import Scenario_Eval_Crew
from src.models import Scenario, ScenarioList, ToolInfo
import json


def run():
    """Run the scenario evaluation crew with default inputs."""
    # Define the tools that the AI agent can use
    tools = [
        ToolInfo(
            name="get_weather",
            description="Get weather information for a specific location and date. Accepts location (string) and date (string in YYYY-MM-DD format).",
            parameters={"location": "string", "date": "string (YYYY-MM-DD)"},
        ),
        ToolInfo(
            name="send_email",
            description="Send an email to a recipient. Accepts recipient_email (string), subject (string), and body (string).",
            parameters={
                "recipient_email": "string",
                "subject": "string",
                "body": "string",
            },
        ),
        ToolInfo(
            name="search_web",
            description="Search the web for information. Accepts query (string) and returns relevant search results.",
            parameters={"query": "string"},
        ),
        ToolInfo(
            name="calculate",
            description="Perform mathematical calculations. Accepts expression (string) and returns the result.",
            parameters={"expression": "string"},
        ),
    ]

    inputs = {
        "tools": [tool.model_dump() for tool in tools],
    }
    result = Scenario_Eval_Crew().crew().kickoff(inputs=inputs)
    print(result.json_dict)

    scenarios = [Scenario(**scenario) for scenario in result.json_dict["scenarios"]]
    print(scenarios)


def create_scenarios(tools: list[ToolInfo]) -> list[Scenario]:
    """Create scenarios for the given tools."""
    inputs = {
        "tools": [tool.model_dump() for tool in tools],
    }
    result = Scenario_Eval_Crew().crew().kickoff(inputs=inputs)
    return [Scenario(**scenario) for scenario in result.json_dict["scenarios"]]


if __name__ == "__main__":
    run()
