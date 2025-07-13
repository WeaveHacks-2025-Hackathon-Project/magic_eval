#!/usr/bin/env python3
"""
Setup script for the magic_eval project - Time Agent.
This script will help you install dependencies and run evaluations for the time agent.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"  Error: {e}")
        print(f"  Output: {e.stdout}")
        print(f"  Error output: {e.stderr}")
        return None

def install_dependencies():
    """Install required dependencies."""
    print("Installing required dependencies...")
    
    # Install ADK and other dependencies
    dependencies = [
        "google-adk",
        "pytest",
        "pytest-asyncio",
        "litellm",
        "python-dotenv",
        "weave",
        "crewai",
        "pydantic"
    ]
    
    for dep in dependencies:
        run_command(f"pip install {dep}", f"Installing {dep}")

def setup_environment():
    """Set up the environment for evaluation."""
    print("\nSetting up environment...")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# Add your API keys here
LLAMA_API_KEY=your_llama_api_key_here
WANDB_API_KEY=your_wandb_api_key_here
WEAVE_PROJECT_NAME=magic_eval
"""
        env_file.write_text(env_content)
        print("✓ Created .env file - please add your API keys")
    else:
        print("✓ .env file already exists")

def run_evaluation():
    """Run the evaluation tests."""
    print("\nRunning time agent evaluation tests...")
    
    # Generate scenarios first
    run_command("python evaluation/generate_scenarios.py", "Generating evaluation scenarios")
    
    # Run pytest
    run_command("pytest evaluation/integration.py -v", "Running integration tests")

def main():
    """Main setup and evaluation runner."""
    print("Magic Eval Setup and Evaluation Runner - Time Agent")
    print("=" * 58)
    
    # Change to project directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Running in virtual environment")
    else:
        print("⚠ Warning: Not running in a virtual environment. Consider using venv or conda.")
    
    # Menu
    while True:
        print("\nOptions:")
        print("1. Install dependencies")
        print("2. Setup environment")
        print("3. Generate evaluation scenarios")
        print("4. Run evaluation tests")
        print("5. Run ADK web UI")
        print("6. Do all of the above")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            install_dependencies()
        elif choice == "2":
            setup_environment()
        elif choice == "3":
            run_command("python evaluation/generate_scenarios.py", "Generating evaluation scenarios")
        elif choice == "4":
            run_evaluation()
        elif choice == "5":
            print("\nStarting ADK web UI...")
            print("This will start the web interface for interactive evaluation.")
            run_command("adk web example_agent", "Starting ADK web UI")
        elif choice == "6":
            install_dependencies()
            setup_environment()
            run_command("python evaluation/generate_scenarios.py", "Generating evaluation scenarios")
            run_evaluation()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
