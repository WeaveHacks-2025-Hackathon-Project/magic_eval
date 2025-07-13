#!/usr/bin/env python
import sys
from scenario import Scenario_Eval_Crew

"""Scenario evaluation crew for ScenarioEval project."""
def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'Store Location': 'OneDrive',
    }
    result = Scenario_Eval_Crew().crew().kickoff(inputs=inputs)
    print(result)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'Store Location': 'OneDrive',
    }
    try:
        Scenario_Eval_Crew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")