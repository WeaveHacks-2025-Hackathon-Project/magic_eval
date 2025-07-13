"""Example agent implementation using Google ADK with MCP toolset and Weave tracing."""

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from src.weave_config import setup_weave_tracing, create_weave_op

# Load environment variables
load_dotenv()

# Set up Weave tracing
tracer = setup_weave_tracing()

MCP_TIME_SERVER = MCPToolset(
    connection_params=StdioServerParameters(
        command="python", args=["-m", "mcp_server_time"]
    )
)

LLAMA_MODEL = "Llama-4-Scout-17B-16E-Instruct-FP8"

# Configure environment variables for the model
os.environ["LLAMA_API_KEY"] = os.getenv("LLAMA_API_KEY")
os.environ["WANDB_API_KEY"] = os.getenv("WANDB_API_KEY")


# Create a custom completion function that uses your specific model with Weave tracing
@create_weave_op
def llama_completion(messages, **kwargs):
    with tracer.start_as_current_span("llama_completion") as span:
        span.set_attribute("model", LLAMA_MODEL)
        span.set_attribute("messages_count", len(messages))

        # Create LiteLLM model instance
        model = LiteLlm(model=f"meta-llama/{LLAMA_MODEL}")

        # Use the model's completion method
        result = model.complete(messages=messages, **kwargs)

        span.set_attribute("response_length", len(str(result)))
        return result


root_agent = LlmAgent(
    model=LiteLlm(model=f"meta_llama/{LLAMA_MODEL}"),
    name="time_agent",
    instruction="You are a helpful assistant.",
    tools=[MCP_TIME_SERVER],
)
