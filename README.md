# Docker tier: the real tools (Professional Practice P1)

The browser sandbox teaches every idea with standard-library code. This folder runs the **real** tools the industry uses,
on your own machine, with no cloud account and no model API key required.

| Lab | Tools | Lesson | What you do |
|---|---|---|---|
| `labs/01_langgraph_agent.py` | LangGraph + SQLite checkpointer | P1.1 | Pause an underwriting workflow before human approval, restart, resume the same thread |
| `labs/02_vector_databases.py` | Qdrant, PostgreSQL + pgvector | P1.2 | Run the same tenant-filtered search in both and write an ADR |
| `labs/03_cloud_router.py` | Bedrock, Microsoft Foundry, Vertex AI adapters + mock | P1.3 | Residency-aware routing with fallback; works offline via the mock |
| `labs/04_otel_tracing.py` | OpenTelemetry SDK, Collector, Jaeger | P1.5 | Trace the decision service; confirm the collector deletes prompt text |
| `labs/05_deepeval_tests.py` | DeepEval + pytest | P1.5 | Evaluation as unit tests; a hallucinated rate fails the build |
| `labs/06_containers_iac/` | Docker, Kubernetes (kind), Terraform | P1.4 | Build a reviewer-proof image, deploy to kind, read a Terraform plan |
| `labs/07_mcp_server.py` | Official MCP Python SDK (FastMCP server + stdio client) | Module 15, Agentic 8 | Build an ERP tool server, connect as a client, list and call tools, read a resource |
| `labs/08_live_agent.py` | LangGraph + any OpenAI-compatible model | Agentic 1 | Run the agent loop as a graph against a real model (scripted stand-in without one) |
| `labs/09_smolagents_agent.py` | Hugging Face smolagents | Agentic 2, P7 | An invoice-checking ToolCallingAgent: tax-ID and HS-rate tools, `final_answer`, a step budget |
| `labs/10_llamaindex_rag.py` | LlamaIndex | FDE 14, Agentic 5, P7 | Tenant-filtered retrieval with numbered citations, and a refusal when the sources don't cover it |
| `labs/11_google_adk_agent.py` | Google Agent Development Kit (ADK) | Agentic 4, P7 | A loan pre-check agent: function tools, a session, the event stream and session state |
| `labs/12_autogen_team.py` | Microsoft AutoGen (AgentChat) | Agentic 7, P7 | A writer and a compliance reviewer in a round-robin team with a tool check and a message budget |
| `labs/13_crewai_crew.py` | CrewAI | Agentic 6, P7 | A researcher and a writer crew: tasks with expected outputs and a context hand-off |
| `labs/14_terraform_aws/` | Terraform + AWS (moto emulator or a real account) | FDE 17 and 21, P10 | S3 + KMS, DynamoDB, SQS with a dead-letter queue and least-privilege IAM, gated by a plan policy check |

## Prerequisites

- Docker Desktop (or Docker Engine) with Compose
- For lab 06: [kind](https://kind.sigs.k8s.io/) and kubectl, and [Terraform](https://developer.hashicorp.com/terraform) 1.5+

## Start

```bash
cd realtools
docker compose up -d --build
docker compose exec labs python 02_vector_databases.py
```

The first `up --build` builds the labs image (`labs.Dockerfile`) with the requirements installed, which takes a couple of
minutes; after that, restarting the container keeps them. Every lab runs from the `labs` container's working directory,
for example `docker compose exec labs python -m pytest -q 05_deepeval_tests.py`. Jaeger UI: <http://localhost:16686>.
Stop everything with `docker compose down` (add `-v` to delete the data volumes). The five services use about 250 MB of
RAM when idle, on top of Docker Desktop's own virtual machine.

Last verified end to end on 19 October 2026 with Qdrant 1.19.2, pgvector on PostgreSQL 16, OpenTelemetry Collector
0.111.0, Jaeger 1.62.0, LangGraph 1.2, qdrant-client 1.19, DeepEval 3.9 and Python 3.12.7. Lab 06 was verified with
kind 0.33.0 (default node image) and Terraform 1.16.6 with the kreuzwerker/docker 3.9 and hashicorp/local 2.9 providers:
two replicas run non-root on a read-only filesystem, a rolling update keeps both available, pods stop within a second
on SIGTERM, and the Terraform plan, apply, replacement plan and destroy all behave as the lab describes. The autoscaler
needs metrics-server, which kind does not install.

Labs 09 to 13 were verified on 24 October 2026 with smolagents 1.26, LlamaIndex core 0.14, Google ADK 1.14 and 2.13, AutoGen AgentChat 0.7.5 and CrewAI 1.15 on Python 3.12, each with its scripted model, all installed together with the requirements above (`pip check` clean). Lab 14 was verified the same day with Terraform 1.16.6, the hashicorp/aws 5.x provider and moto 5 as the emulator: plan, the policy gate (23 rules pass), apply of 11 resources, inspection through the AWS API, a deliberately bad change rejected by the gate, and destroy.

Every lab has a self-study guide in `guides/` (the problem, key ideas, step-by-step tasks with expected output, self-checks with answers, common mistakes and extensions). The portal shows the labs and guides at `/realtools`, with a download of this folder.

Labs 07 and 08 were verified on 24 October 2026 with mcp 1.30.0 and LangGraph 1.2.17 on Python 3.12 (lab 08 with its scripted model; point FDE_LLM_BASE_URL and FDE_LLM_MODEL at any OpenAI-compatible endpoint, such as a local Ollama or vLLM server, to use a real one).

## Live labs in the browser

When the site has a model configured (FDE_LLM_BASE_URL and FDE_LLM_MODEL), eight lectures are live labs: sandboxed code calls `call_model(messages)` and the portal makes the call, so the API key never reaches learner code. Each run may make up to 8 model calls, and each learner 30 an hour by default (FDE_LIVE_CALLS_PER_HOUR); FDE_LLM_DAILY_CALLS caps the whole site per day. Without a configured model those lectures point here.

## Notes for real client work

- The passwords in `docker-compose.yml` are local lab values only; real credentials come from a secret store.
- `requirements.txt` uses version ranges so the labs keep installing; real projects install from a generated lock file.
- The toy embedding in `labs/common.py` avoids model downloads; swap in a real embedding model and keep one dimension per collection.
- Lab 03 reads regions and model IDs from `router_config.json` and environment variables — never hard-code them.
