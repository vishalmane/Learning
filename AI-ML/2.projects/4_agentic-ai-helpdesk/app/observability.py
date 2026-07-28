from contextlib import contextmanager
from time import perf_counter
from typing import Iterator

try:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
except Exception:  # pragma: no cover - optional runtime dependency guard
    trace = None


def setup_observability(service_name: str) -> None:
    if trace is None:
        return
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(provider)


@contextmanager
def timed_span(name: str) -> Iterator[float]:
    start = perf_counter()
    tracer = trace.get_tracer(__name__) if trace else None
    if tracer:
        with tracer.start_as_current_span(name):
            yield start
    else:
        yield start

