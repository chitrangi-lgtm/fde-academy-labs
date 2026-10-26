"""Lab 04 — OpenTelemetry traces from the decision service, through the Collector, into Jaeger.

Run:   docker compose exec labs python 04_otel_tracing.py   then open http://localhost:16686 and search service "decision-service".
Check: the span "llm.chat" has gen_ai.* attributes but NO prompt.text — the collector's attributes processor deleted it
       (see otel-collector.yaml). Change the processor and watch the attribute appear: that is a data leak in one line.
"""

from __future__ import annotations

import os
import time

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

provider = TracerProvider(resource=Resource.create({"service.name": "decision-service", "deployment.environment": "lab"}))
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"),
                                                                insecure=True)))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("decision-service")


def decide(app_id: str) -> str:
    with tracer.start_as_current_span("POST /decide") as root:
        root.set_attribute("tenant", "crestfin")
        root.set_attribute("app.id", app_id)
        with tracer.start_as_current_span("retrieve") as s:
            s.set_attribute("retrieval.doc_ids", ["POL-7.1", "POL-4.2"])
            time.sleep(0.05)
        with tracer.start_as_current_span("llm.chat") as s:
            s.set_attribute("gen_ai.request.model", "general-large")
            s.set_attribute("gen_ai.usage.input_tokens", 1820)
            s.set_attribute("gen_ai.usage.output_tokens", 240)
            s.set_attribute("prompt.text", "Borrower taxpayer ID TP39038808 ...")      # deliberately unsafe: the collector must drop it
            time.sleep(0.2)
        return "REFER"


if __name__ == "__main__":
    for i in range(3):
        print(decide(f"BHF-00{i + 1}"))
    provider.force_flush()
    print("sent 3 traces; open Jaeger at http://localhost:16686")
