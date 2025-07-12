"""Weave configuration for ADK integration with OTEL tracing."""

import os
import weave
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Load environment variables
load_dotenv()


def setup_weave_tracing():
    """Set up Weave with OTEL tracing for ADK integration."""

    # Initialize Weave with your project
    weave.init("Magic_evals")

    # Set up OpenTelemetry tracing
    trace.set_tracer_provider(TracerProvider())

    # Configure OTLP exporter for Weave
    otlp_exporter = OTLPSpanExporter(
        endpoint="https://api.wandb.ai/otel/v1/traces",
        headers={
            "Authorization": f"Bearer {os.getenv('WANDB_API_KEY')}",
            "X-Wandb-Project": "Magic_evals",
        },
    )

    # Add span processor
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    return trace.get_tracer(__name__)


def create_weave_op(func):
    """Decorator to create a Weave operation with tracing."""
    return weave.op()(func)
