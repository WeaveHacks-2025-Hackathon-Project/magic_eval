from typing import Optional
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from surprise_travel.tools.custom_tool import MyCustomTool

# Check our tools documentation for more information on how to use them
from pydantic import BaseModel, Field

LLAMA_MODEL = "Llama-4-Scout-17B-16E-Instruct-FP8"


class Scenario(BaseModel):
    name: str = Field(..., description="Name of the scenario")
    description: str = Field(..., description="Description of the scenario")
    why_its_suitable: str = Field(..., description="Why it's a suitable scenario")
    expected_tool_call: Optional[str] = Field(
        ...,
        description="Expected tool call that should be made. This can be set to None if no tool should be called",
    )
    # TODO: Add another field for the expected tool calls that should be made


class ScenarioList(BaseModel):
    scenarios: list[Scenario] = Field(..., description="List of scenarios")


@CrewBase
class Scenario_Eval_Crew:
    """Scenario evaluation crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def scenario_evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config["scenario_evaluator"],
            verbose=True,
            allow_delegation=False,
            llm=f"meta_llama/{LLAMA_MODEL}",
        )

    @task
    def scenario_evaluator_task(self) -> Task:
        return Task(
            config=self.tasks_config["scenario_evaluator_task"],
            agent=self.scenario_evaluator(),
            output_pydantic=ScenarioList,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SurpriseTravel crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you want to use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
