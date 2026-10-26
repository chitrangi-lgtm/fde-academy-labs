# FDE Academy labs kit

Real tools, real code, on a real machine: free.

## Open it

| Where | How | Cost |
|---|---|---|
| **GitHub Codespaces** (recommended) | Use the course's "Open in GitHub Codespaces" link. To keep your work and get checks on every push, choose **Use this template → Create a new repository** first, then Code → Codespaces → Create codespace on your copy. Everything installs itself in a few minutes. | Free on your own account: 120 core hours and 15 GB of storage a month (about 60 hours on the default 2-core machine) |
| **Google Cloud Shell** | Open shell.cloud.google.com, upload or clone this folder, run `pip install --user -r requirements.txt` | Free, 50 hours a week |
| **Your computer** | Python 3.12 and Docker Desktop: `pip install -r requirements.txt`, then `docker compose up -d --build` | Free |

Stay inside the free allowance: keep the 2-core machine and one codespace at a time, stop it when you finish (Codespaces →
Stop), set a 15-minute idle timeout and a 3-day retention period at github.com/settings/codespaces, and look at
github.com/settings/billing/usage each week. With no payment method on your GitHub account, it can never bill you.
`guides/00_free_environments.md` has the full checklist.

## What is inside

| Folder | What you do | Check your work |
|---|---|---|
| `labs/` + `guides/` | 15 real-tools labs: LangGraph, Qdrant, pgvector, OpenTelemetry, DeepEval, MCP, smolagents, LlamaIndex, Google ADK, AutoGen, CrewAI, Docker, kind, Terraform | Each guide lists the expected output |
| `missions/` | 36 challenge missions, one per course module: a client's email, data and no steps | `python tools/fde_check.py m05` |
| `pylabs/` | 16 Python labs with pandas, scikit-learn, pydantic, DuckDB, NetworkX, SciPy and matplotlib | `python tools/fde_check.py m01-py1` |
| `notebooks/` | Fine-tune a small model with LoRA on a free Kaggle or Colab GPU | The notebook's own checks |

`python tools/fde_check.py --list` lists everything you can check, with your current score. Push your repository and GitHub
Actions runs the same checks for you (the Actions tab shows the summary).

## Real cloud accounts, free

`guides/00_free_environments.md` lists the free plans (AWS Free plan, Azure for Students, Google Cloud Shell, Databricks
Free Edition, free model APIs) and the emulators in this kit (Moto, kind, Azurite). Set a budget alert on day one.

## Using a real model

Live labs work with a scripted model by default. To use a real one, add three Codespaces secrets (Settings → Codespaces →
Secrets): `FDE_LLM_BASE_URL`, `FDE_LLM_MODEL` and `FDE_LLM_API_KEY`. Free options: Gemini (Flash-Lite), Groq, OpenRouter.
