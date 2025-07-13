"""Weave configuration for ADK integration with OTEL tracing."""

import os
import base64
import weave
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SimpleSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Load environment variables
load_dotenv()


def setup_weave_tracing():
    """Set up Weave with OTEL tracing for ADK integration."""

    # Initialize Weave with your project
    weave.init("Magic_evals")

    # Set up OpenTelemetry tracing
    trace.set_tracer_provider(TracerProvider())

    # Configure Weave tracing parameters
    WANDB_BASE_URL = "https://trace.wandb.ai"
    PROJECT_ID = "Magic_evals"  # You can update this to include entity if needed
    WANDB_API_KEY = os.getenv("WANDB_API_KEY")

    OTEL_EXPORTER_OTLP_ENDPOINT = f"{WANDB_BASE_URL}/otel/v1/traces"

    # Create authorization header
    AUTH = base64.b64encode(f"api:{WANDB_API_KEY}".encode()).decode()

    OTEL_EXPORTER_OTLP_HEADERS = {
        "Authorization": f"Basic {AUTH}",
        "project_id": PROJECT_ID,
    }

    # Configure the OTLP HTTP exporter
    otlp_exporter = OTLPSpanExporter(
        endpoint=OTEL_EXPORTER_OTLP_ENDPOINT,
        headers=OTEL_EXPORTER_OTLP_HEADERS,
    )

    # Add span processors
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    # Optionally, print the spans to the console for debugging
    trace.get_tracer_provider().add_span_processor(
        SimpleSpanProcessor(ConsoleSpanExporter())
    )

    return trace.get_tracer(__name__)


def create_weave_op(func):
    """Decorator to create a Weave operation with tracing."""
    return weave.op()(func)
