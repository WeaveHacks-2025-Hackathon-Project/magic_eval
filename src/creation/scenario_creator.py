from typing import Optional
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from surprise_travel.tools.custom_tool import MyCustomTool

# Check our tools documentation for more information on how to use them
from src.models import Scenario, ScenarioList


LLAMA_MODEL = "Llama-4-Maverick-17B-128E-Instruct-FP8"


@CrewBase
class Scenario_Eval_Crew:
    """Scenario evaluation crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    llm = LLM(
        model=f"meta_llama/{LLAMA_MODEL}",
    )

    @agent
    def scenario_evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config["scenario_evaluator"],
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )

    @task
    def scenario_evaluator_task(self) -> Task:
        return Task(
            config=self.tasks_config["scenario_evaluator_task"],
            agent=self.scenario_evaluator(),
            expected_output="A list of scenarios that should be tested to verify that the AI agent works successfully. Each scenario should be a structured object with name, description, why_its_suitable, and expected_tool_call fields. The expected_tool_call field should contain only the tool name (not the full function call with parameters) or None.",
            output_json=ScenarioList,
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
