from scenario_creator import Scenario_Eval_Crew


def run():
    """Run the scenario evaluation crew with default inputs."""
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        "Store Location": "OneDrive",
    }
    result = Scenario_Eval_Crew().crew().kickoff(inputs=inputs)
    print(result)


if __name__ == "__main__":
    run()
