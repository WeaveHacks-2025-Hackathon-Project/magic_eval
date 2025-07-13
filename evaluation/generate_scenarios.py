#!/usr/bin/env python3
"""
Script to generate evaluation test cases using the scenario creator.
Run this to create test scenarios for your time agent.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timezone

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def create_time_agent_scenarios() -> List[Dict[str, Any]]:
    """Create evaluation scenarios for the time agent."""
    scenarios = [
        {
            "eval_id": "get_current_time_basic",
            "conversation": [
                {
                    "invocation_id": "time-001",
                    "user_content": {
                        "parts": [{"text": "What time is it?"}],
                        "role": "user"
                    },
                    "final_response": {
                        "parts": [{"text": "The current time is 2025-07-13 14:30:00 UTC"}],
                        "role": "model"
                    },
                    "intermediate_data": {
                        "tool_uses": [{"args": {}, "name": "get_current_time"}],
                        "intermediate_responses": []
                    }
                }
            ],
            "session_input": {
                "app_name": "time_agent",
                "user_id": "test_user",
                "state": {}
            }
        },
        {
            "eval_id": "get_current_date_basic",
            "conversation": [
                {
                    "invocation_id": "time-002", 
                    "user_content": {
                        "parts": [{"text": "What is today's date?"}],
                        "role": "user"
                    },
                    "final_response": {
                        "parts": [{"text": "Today's date is July 13, 2025"}],
                        "role": "model"
                    },
                    "intermediate_data": {
                        "tool_uses": [{"args": {}, "name": "get_current_date"}],
                        "intermediate_responses": []
                    }
                }
            ],
            "session_input": {
                "app_name": "time_agent",
                "user_id": "test_user", 
                "state": {}
            }
        },
        {
            "eval_id": "time_with_timezone",
            "conversation": [
                {
                    "invocation_id": "time-003",
                    "user_content": {
                        "parts": [{"text": "What time is it in PST?"}],
                        "role": "user"
                    },
                    "final_response": {
                        "parts": [{"text": "The current time in PST is 6:30 AM"}],
                        "role": "model"
                    },
                    "intermediate_data": {
                        "tool_uses": [{"args": {"timezone": "PST"}, "name": "get_time_in_timezone"}],
                        "intermediate_responses": []
                    }
                }
            ],
            "session_input": {
                "app_name": "time_agent",
                "user_id": "test_user",
                "state": {}
            }
        },
        {
            "eval_id": "no_tool_greeting",
            "conversation": [
                {
                    "invocation_id": "time-004",
                    "user_content": {
                        "parts": [{"text": "Hello, how are you?"}],
                        "role": "user"
                    },
                    "final_response": {
                        "parts": [{"text": "Hello! I'm doing well, thank you for asking. How can I help you today?"}],
                        "role": "model"
                    },
                    "intermediate_data": {
                        "tool_uses": [],
                        "intermediate_responses": []
                    }
                }
            ],
            "session_input": {
                "app_name": "time_agent",
                "user_id": "test_user",
                "state": {}
            }
        },
        {
            "eval_id": "no_tool_unrelated_query",
            "conversation": [
                {
                    "invocation_id": "time-005",
                    "user_content": {
                        "parts": [{"text": "Tell me about the weather"}],
                        "role": "user"
                    },
                    "final_response": {
                        "parts": [{"text": "I'm sorry, but I can't provide weather information. I'm specialized in time-related queries. Is there anything time-related I can help you with?"}],
                        "role": "model"
                    },
                    "intermediate_data": {
                        "tool_uses": [],
                        "intermediate_responses": []
                    }
                }
            ],
            "session_input": {
                "app_name": "time_agent",
                "user_id": "test_user",
                "state": {}
            }
        }
    ]
    
    return scenarios

def create_evaluation_file(scenarios: List[Dict[str, Any]], output_path: str):
    """Create a complete evaluation file with the given scenarios."""
    eval_set = {
        "eval_set_id": "time_agent_comprehensive_evaluation",
        "name": "Time Agent Comprehensive Evaluation",
        "description": "Comprehensive evaluation set for testing time agent behavior including tool usage and edge cases",
        "eval_cases": scenarios
    }
    
    with open(output_path, 'w') as f:
        json.dump(eval_set, f, indent=2)
    
    print(f"Created evaluation file: {output_path}")

def main():
    """Generate evaluation scenarios and create test file."""
    scenarios = create_time_agent_scenarios()
    
    # Create the evaluation file
    eval_dir = project_root / "evaluation"
    eval_dir.mkdir(exist_ok=True)
    
    output_path = eval_dir / "time_agent_comprehensive.test.json"
    create_evaluation_file(scenarios, str(output_path))
    
    print(f"Generated {len(scenarios)} evaluation scenarios")
    print("\nScenarios created:")
    for scenario in scenarios:
        print(f"  - {scenario['eval_id']}")
    
    print(f"\nTo run the evaluation, use:")
    print(f"  pytest evaluation/integration.py")
    print(f"  # or")
    print(f"  adk eval example_agent {output_path}")

if __name__ == "__main__":
    main()
