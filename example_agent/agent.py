"""Example agent implementation using Google ADK with MCP toolset and Weave tracing."""

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from litellm import completion
from src.weave_config import setup_weave_tracing, create_weave_op

# Load environment variables
load_dotenv()

# Set up Weave tracing
tracer = setup_weave_tracing()

COIN_FLIP_MCP_SERVER = [
    MCPToolset(
        connection_params=StdioServerParameters(
            command="npx", args=["-y", "@modelcontextprotocol/server-coin-flip"]
        )
    )
]

# Configure LiteLLM with Llama
os.environ["LLAMA_API_KEY"] = os.getenv("LLAMA_API_KEY")
os.environ["WANDB_API_KEY"] = os.getenv("WANDB_API_KEY")


# Create a custom completion function that uses your specific model with Weave tracing
@create_weave_op
def llama_completion(messages, **kwargs):
    with tracer.start_as_current_span("llama_completion") as span:
        span.set_attribute("model", "meta-llama/Llama-4-Scout-17B-16E-Instruct-FP8")
        span.set_attribute("messages_count", len(messages))

        result = completion(
            model="meta-llama/Llama-4-Scout-17B-16E-Instruct-FP8",  # Your specific model
            messages=messages,
            **kwargs,
        )

        span.set_attribute("response_length", len(str(result)))
        return result


root_agent = LlmAgent(
    model="meta-llama/Llama-4-Scout-17B-16E-Instruct-FP8",  # Correct model identifier
    name="coinflip_agent",
    instruction="You are a coinflip agent. You will be given a message and you will need to flip a coin. You will need to return the result of the coin flip.",
    tools=[COIN_FLIP_MCP_SERVER],
    llm_completion_function=llama_completion,  # Use custom completion function with Weave tracing
)
