# Lab 04: Trace a decision service and strip prompt text in the collector

**Time:** 60 minutes · **Level:** Intermediate · **Builds on:** Professional Practice P1, FDE Module 18 (evaluation and observability), Agentic Module 11 (cost, latency and observability)

## The problem

CrestFin's loan decision service sometimes takes four seconds instead of one, and the operations team can't tell
whether the delay is in document retrieval, the model call or something else. They want traces: a timeline of every
request, step by step. The CISO adds a condition: prompts contain borrowers' taxpayer IDs and other personal data, and
prompt text must never be stored in the tracing system.

This lab instruments the service with **OpenTelemetry**, the open standard for traces, sends spans through the
**OpenTelemetry Collector**, which deletes prompt text, and views them in **Jaeger**.

## What you'll learn

- How spans nest to form a trace: a root span for the request and child spans for each step.
- How to record useful attributes, including the `gen_ai.*` attributes for model calls (model name, token counts).
- How the Collector's `attributes` processor deletes sensitive attributes before they reach storage.
- How to read a trace in Jaeger to find where the time goes.

## Before you start

1. From `realtools/`: `docker compose up -d --build`. This starts the Collector (ports 4317 and 4318) and Jaeger (UI on 16686).
2. Run `docker compose exec labs python 04_otel_tracing.py`.
3. Open <http://localhost:16686>, choose the service `decision-service` and click **Find Traces**.

## Key ideas

**A trace is a tree of spans.** `POST /decide` is the root span. Inside it, `retrieve` and `llm.chat` are child spans.
Each span has a start, an end and attributes, so Jaeger can draw the timeline and show what each step was doing.

**Attributes make traces searchable.** The root span records the tenant and application id; `retrieve` records which
documents were used; `llm.chat` records the model and token counts using the OpenTelemetry generative AI conventions
(`gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`). Those are what you'd use to find
slow or expensive requests.

**Sensitive data is removed centrally.** The code deliberately sets a `prompt.text` attribute containing a taxpayer ID, the kind
of mistake developers make. The Collector's `attributes/strip_prompt` processor (in `otel-collector.yaml`) deletes it,
so it never reaches Jaeger. Doing this in the Collector protects you from every service's mistakes, not just this one.

**Batching and flushing.** The `BatchSpanProcessor` sends spans in groups in the background. `force_flush()` at the end
makes sure they're sent before the script exits; without it, short scripts can lose spans.

## Steps

1. **Run the lab.** Expected output: `REFER` three times, then `sent 3 traces; open Jaeger at http://localhost:16686`.

2. **Find the traces.** In Jaeger, open one trace. You should see `POST /decide` lasting about 250 ms, with `retrieve`
   (about 50 ms) followed by `llm.chat` (about 200 ms). The model call is the slow step here.

3. **Check the attributes.** Click `llm.chat`. You should see `gen_ai.request.model = general-large`, 1,820 input tokens
   and 240 output tokens, and **no** `prompt.text`. The Collector deleted it.

4. **See the leak happen.** In `otel-collector.yaml`, comment out the `prompt.text` delete action, run
   `docker compose restart otel-collector`, then run the lab again. The new traces show the taxpayer ID in `prompt.text`. That is
   a personal-data leak caused by one line of configuration. Restore the action and restart the Collector.

5. **Find a slow step.** Change `time.sleep(0.05)` in `retrieve` to `time.sleep(1.5)` and run. In Jaeger, search for
   traces longer than 1 second (**Min Duration**) and confirm the timeline shows retrieval as the cause.

6. **Add an error.** Make the third request raise an exception inside `llm.chat`, record it with
   `s.record_exception(exc)` and `s.set_status(trace.Status(trace.StatusCode.ERROR))`, and find the red span in Jaeger.

## Check yourself

<details><summary>Why delete the prompt in the Collector rather than only fixing the code?</summary>
Fix the code too, but the Collector is a single control point for every service. New services and new developers will
make the same mistake; the Collector catches it before anything is stored.
</details>

<details><summary>Which attributes would you use to find the most expensive requests?</summary>
The token counts on `llm.chat` (`gen_ai.usage.input_tokens` and `gen_ai.usage.output_tokens`) together with the model
name, multiplied by the model's prices. Group by tenant to see which client drives the cost.
</details>

<details><summary>What happens if you remove force_flush()?</summary>
The script may exit before the background batch processor sends the spans, so some or all traces never reach Jaeger.
Long-running servers flush regularly, but short scripts and serverless functions need an explicit flush.
</details>

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| No service in Jaeger's list | Spans never arrived | Check `OTEL_EXPORTER_OTLP_ENDPOINT`, that the Collector is running and that `force_flush()` is called |
| `StatusCode.UNAVAILABLE` errors | The Collector isn't reachable on 4317 | `docker compose ps`; inside Docker use `http://otel-collector:4317` |
| The prompt still appears after editing the config | The Collector wasn't restarted | `docker compose restart otel-collector` |
| Spans appear as separate traces | Child spans were started outside the parent's `with` block | Start child spans inside the parent's context |

## Take it further

- Add a span for a call to a second service and propagate the context over HTTP so both appear in one trace.
- Add a metric (a histogram of request duration) and export it alongside the traces.
- Write a Collector rule that hashes the tenant id instead of deleting it, so you can group by tenant without the raw value.

## In a real client project

- Agree with the client which attributes may be recorded, and enforce it in the Collector.
- Sample traces in high-volume services (for example keep all errors and 10% of successes) to control cost.
- Set retention on trace storage to match the client's data policy.
