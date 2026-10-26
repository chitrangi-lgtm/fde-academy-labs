"""Lab 03 — a provider-agnostic model client with residency-aware routing and fallback.

Offline:   docker compose exec labs python 03_cloud_router.py   (uses the mock adapter; no accounts needed)
Real:      set "enabled": true for a provider in router_config.json, install its SDK (see requirements.txt) and set the
           environment variables it names. Region and model come from configuration, never from code.
Try:       mark the EU endpoints unavailable in router_config.json and send Restricted data: the router must refuse.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

CONFIG = json.loads((Path(__file__).parent / "router_config.json").read_text())


def call_mock(endpoint: dict, prompt: str) -> str:
    return f"[mock endpoint {endpoint['region']}] summary of: {prompt[:40]}..."


def call_bedrock(endpoint: dict, prompt: str) -> str:
    import boto3
    client = boto3.client("bedrock-runtime", region_name=endpoint["region"])
    resp = client.converse(modelId=os.environ[endpoint["model_env"]], messages=[{"role": "user", "content": [{"text": prompt}]}],
                           inferenceConfig={"maxTokens": 300, "temperature": 0})
    return resp["output"]["message"]["content"][0]["text"]


def call_azure(endpoint: dict, prompt: str) -> str:
    from openai import AzureOpenAI
    client = AzureOpenAI(azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["AZURE_OPENAI_API_KEY"],
                         api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21"))
    out = client.chat.completions.create(model=os.environ[endpoint["model_env"]], messages=[{"role": "user", "content": prompt}])
    return out.choices[0].message.content


def call_vertex(endpoint: dict, prompt: str) -> str:
    from google import genai
    client = genai.Client(vertexai=True, project=os.environ["GCP_PROJECT"], location=endpoint["region"])
    return client.models.generate_content(model=os.environ[endpoint["model_env"]], contents=prompt).text


ADAPTERS = {"mock": call_mock, "bedrock": call_bedrock, "azure-foundry": call_azure, "vertex": call_vertex}


def route(prompt: str, data_class: str, residency: str) -> str:
    candidates = [e for e in CONFIG["endpoints"] if e["available"] and (e["enabled"] or e["platform"] == "mock")]
    if data_class == "Restricted":
        candidates = [e for e in candidates if e["jurisdiction"] == residency]
    for endpoint in sorted(candidates, key=lambda e: e["priority"]):
        try:
            return ADAPTERS[endpoint["platform"]](endpoint, prompt)
        except Exception as exc:  # noqa: BLE001 — fall through to the next compliant endpoint
            print(f"  {endpoint['platform']}/{endpoint['region']} failed: {type(exc).__name__}; trying next")
    return "REFUSED: no compliant endpoint available — queue for a human or retry later"


if __name__ == "__main__":
    print(route("Draft a credit memo for BHF-001 from the redacted application.", "Restricted", "EU"))
    print(route("Summarise this public central-bank circular.", "Public", "EU"))
