# Real environments and real cloud accounts, free

Paid training platforms hand you a temporary cloud account inside the lab. You can get the same experience for free: a real
Linux machine with Docker in your browser, real cloud consoles on free plans, and free emulators when you do not want an
account at all. Everything on this page was checked in October 2026. Free plans change, so read the provider's page before
you sign up.

## The one rule: you are never billed

- **Never add a payment method you do not need.** GitHub Codespaces, Google Cloud Shell, Databricks Free Edition, Kaggle,
  Colab and the free model APIs need none. Without one, they stop at the free limit instead of charging you.
- **Where a card is required for sign-up (AWS, the standard Azure account), stay on the free plan** and set a budget alert at
  1 dollar on day one. Labs in this course list their teardown command: run it before you close the tab.
- **Use the emulators first.** Every cloud lab runs against a local emulator in Codespaces before it touches a real account.

## Your machine in the browser

| Environment | What you get | Free allowance | Card needed |
|---|---|---|---|
| [GitHub Codespaces](https://github.com/features/codespaces) | VS Code in the browser on a real Linux machine with Docker, Kubernetes (kind), Terraform, the AWS, Azure and GitHub CLIs and every lab library, from this kit's dev container | 120 core hours and 15 GB of storage a month on GitHub Free (about 60 hours on the 2-core machine); 180 core hours on GitHub Pro, which verified students get free | No |
| [Google Cloud Shell](https://shell.cloud.google.com) | A browser terminal and editor with Docker, gcloud, kubectl and Terraform, and 5 GB of storage that persists | Free with a Google account; 50 hours a week | No |
| [Kaggle Notebooks](https://www.kaggle.com/code) | Jupyter with a free GPU (T4 or P100) for fine-tuning and embeddings | About 30 GPU hours a week | No |
| [Google Colab](https://colab.research.google.com) | Jupyter with a free GPU when one is available | Varies with demand | No |
| Your browser | Python with pandas, scikit-learn, pydantic, DuckDB and more, in this course's Python labs | Unlimited: it runs on your computer | No |

**Open the labs in Codespaces.** Click **Open in GitHub Codespaces** on the course's Real tools page. To keep your work
and have GitHub check it on every push, first make your own copy: on the labs repository choose **Use this template →
Create a new repository** (private is fine), then **Code → Codespaces → Create codespace** on your copy. Without the
link, download the labs kit, create a repository and upload the kit's files instead. The dev container installs
everything in a few minutes.

### Stay inside the free allowance (check this every week)

| Do this | Why |
|---|---|
| Keep the **2-core** machine this kit asks for; never pick a bigger one | Hours are counted per core: 2 cores use your 120 core hours in 60 hours, 4 cores in 30 |
| In [github.com/settings/codespaces](https://github.com/settings/codespaces) set **Default idle timeout** to 15 minutes and **Default retention period** to 3 days | An idle codespace stops sooner, and a stopped one you forgot is deleted before it eats storage |
| Keep **one** codespace at a time, and stop it when you finish (**Codespaces → Stop**) | A codespace for this kit stores about 6 to 8 GB once the Docker images are pulled; the free 15 GB-month covers one kept all month, not two |
| Look at [github.com/settings/billing/usage](https://github.com/settings/billing/usage) each week | It shows core hours and storage used this month. Past 75% of either, delete old codespaces and work in Cloud Shell or your browser's Python labs until the month resets |
| Leave the Codespaces **spending limit at 0 dollars** (the default) and add no payment method | At the limit GitHub stops your codespace instead of billing you |
| Never turn on **prebuilds** for your copy | Prebuilds run and store on the repository owner's allowance |

GitHub Actions checks on your copy are free on a public repository and use about 2 minutes of the 2,000 free minutes a
month on a private one; a newer push cancels a check still running.

## Real cloud accounts on free plans

| Cloud | Free plan | Card needed | Good for these labs |
|---|---|---|---|
| [AWS Free plan](https://aws.amazon.com/free/) | New accounts: 100 dollars of credit on sign-up and up to 100 more for trying core services, for up to 6 months; no charges unless you choose the Paid plan; the account closes when the 6 months or the credit run out | Yes, at sign-up | Lab 14 (Terraform on AWS), Bedrock in lab 03 |
| [Azure for Students](https://azure.microsoft.com/free/students/) | 100 dollars of credit for 12 months, renewable each year you are a full-time student | No (verify with your school email) | Lab 03 (Microsoft Foundry), Azure versions of the cloud labs |
| [Azure free account](https://azure.microsoft.com/free/) | 200 dollars of credit for 30 days, then free amounts of popular services | Yes, for identity checks | As above, if you are not a student |
| [Google Cloud](https://cloud.google.com/free) | Cloud Shell is free; the free trial gives credit for new accounts | Cloud Shell: no; the trial: yes | Vertex AI in lab 03; Cloud Shell for any lab |
| [Databricks Free Edition](https://www.databricks.com/learn/free-edition) | A serverless workspace with notebooks, SQL, Delta Lake, Unity Catalog and pipelines; a daily fair-use limit; not for commercial use | No | Data engineering and lakehouse practice (P11) |

**Set a budget alert on day one.** AWS: Billing → Budgets → a zero-spend budget. Azure: Cost Management → Budgets. Google
Cloud: Billing → Budgets and alerts. A budget alert costs nothing and emails you before anything is charged.

## No account at all: emulators in your codespace

| Emulator | Stands in for | How |
|---|---|---|
| [Moto](https://github.com/getmoto/moto) (Apache 2.0) | AWS: S3, DynamoDB, SQS, KMS, IAM and more | `moto_server -p 5000`, then point Terraform or boto3 at `http://localhost:5000` (lab 14 does this) |
| [kind](https://kind.sigs.k8s.io) | A Kubernetes cluster | `kind create cluster` (lab 06) |
| [Azurite](https://github.com/Azure/Azurite) | Azure Storage (blobs, queues, tables) | `docker run -p 10000:10000 mcr.microsoft.com/azure-storage/azurite` |
| Google Cloud emulators | Pub/Sub, Firestore, Bigtable, Spanner | `gcloud beta emulators pubsub start` in Cloud Shell |
| PostgreSQL + pgvector, Qdrant, OpenTelemetry, Jaeger | Managed databases and observability | `docker compose up -d` in this kit |

LocalStack, a popular AWS emulator, has needed an account and token since March 2026 (its free Hobby plan is for
non-commercial use), so this kit uses Moto.

## Real models, free

| Provider | Free tier | Card needed |
|---|---|---|
| [Google Gemini API](https://aistudio.google.com/apikey) | Flash and Flash-Lite models; limits per project in AI Studio | No (keep billing off) |
| [Groq](https://console.groq.com/keys) | Open models (Llama and others) with per-minute and per-day limits | No |
| [OpenRouter](https://openrouter.ai/keys) | Models ending in `:free`, and the `openrouter/free` router | No |
| [GitHub Models](https://github.com/marketplace/models) | Rate-limited access with a GitHub token | No |
| Ollama in your codespace | Small open models on the CPU (try `qwen2.5:1.5b`) | No |

In the course, live labs can use **your own key in your browser**: choose "Your model key" on a live lab. The key stays in
your browser and goes only to the provider. In this kit, set `FDE_LLM_BASE_URL`, `FDE_LLM_MODEL` and `FDE_LLM_API_KEY` in
your codespace (Codespaces → Settings → Secrets keeps them out of your files).

<details><summary>Why not just give every learner a cloud account?</summary>

Platforms such as Pluralsight, Whizlabs and Google Cloud Skills Boost buy lab time from providers and charge a subscription
for it. The free route above gives you the same tools and teaches one more professional habit: keeping your own cloud spend
at zero with budgets, teardown and emulators.
</details>
