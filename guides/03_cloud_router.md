# Lab 03: Residency-aware routing across cloud model providers

**Time:** 60 minutes · **Level:** Intermediate · **Builds on:** Professional Practice P1, FDE Module 21 (enterprise deployment), FDE Module 16 (security and data protection)

## The problem

CrestFin uses language models on three clouds: Amazon Bedrock, Microsoft Foundry and Google Vertex AI. Its data policy
says Restricted data (credit memos, anything with personal or financial details) must be processed in the EU. Public
data, such as summaries of public central-bank circulars, can go to any endpoint. When the preferred endpoint is down, requests should
fall back to the next compliant one, and if there is none, the request must be refused rather than sent abroad.

This lab builds a small router that reads its endpoints from configuration, applies the residency rule, tries endpoints
in priority order and refuses when nothing compliant is left. It runs offline with mock endpoints, and you can enable
real providers when you have accounts.

## What you'll learn

- How to hide provider differences behind one function signature (adapters).
- How to keep region and model choice in configuration, not code.
- How to apply a data-classification rule before choosing an endpoint.
- How to fall back on failure without breaking the residency rule, and how to fail safely.

## Before you start

1. From `realtools/`: `docker compose up -d --build`.
2. Run `docker compose exec labs python 03_cloud_router.py`.
3. Read `labs/router_config.json`: five endpoints, each with a platform, region, jurisdiction, priority, and `enabled` and
   `available` flags. Only the two mock endpoints are enabled by default.

To use a real provider, set its `enabled` to `true`, install its SDK and set the environment variables its adapter reads
(for example `BEDROCK_MODEL_ID` and AWS credentials for Bedrock). Never put keys in the config file.

## Key ideas

**Adapters make providers interchangeable.** Each `call_*` function takes an endpoint and a prompt and returns text.
Bedrock uses `converse`, Azure uses the OpenAI-style chat API and Vertex uses `generate_content`, but the router doesn't
care. Adding a provider means adding one adapter and one config entry.

**Configuration decides where data goes.** Regions, priorities and which endpoints are switched on live in
`router_config.json`. An operator can disable a region during an incident without a code release, and an auditor can
read one file to see where data may go.

**Classification comes first.** For `Restricted` data the router keeps only endpoints whose `jurisdiction` matches the
required residency before it tries anything. Public data can use any available endpoint.

**Fallback stays inside the rules.** If an endpoint raises an error, the router logs it and tries the next candidate,
but only from the already filtered list. When the list is exhausted it returns `REFUSED`, so the caller can queue the
work for a person or retry later.

## Steps

1. **Run the lab.** Expected output:
   `[mock endpoint local-eu] summary of: Draft a credit memo for BHF-001 from the...` and
   `[mock endpoint local-us] summary of: Summarise this public central-bank circu...`.
   The Restricted request went to the EU mock; the Public one went to the US mock because its priority (8) is
   higher than the EU mock's (9). Lower numbers are tried first.

2. **Make the EU unavailable.** Set `"available": false` on the `local-eu` mock and run again. The Restricted request now
   returns `REFUSED: no compliant endpoint available ...`, while the Public request still works. That refusal is the
   correct, safe behaviour.

3. **Simulate a failing provider.** Set `local-eu` back to available. Make `call_mock` raise an exception when
   `endpoint["region"] == "local-us"`, then run. The Public request prints `mock/local-us failed: ...; trying next` and
   falls back to `local-eu`.

4. **Prefer the EU for everything.** Some clients want all data in the EU where possible. Change the priorities so
   `local-eu` comes first and check both requests use it. Note that this is a configuration change, not a code change.

5. **Add a classification.** Add `"Confidential"` handling: allowed in the EU or in a named list of approved countries
   from the config. Write the rule so an unknown classification is treated as Restricted, never as Public.

6. **Enable a real provider (optional).** If you have an AWS account with Bedrock access in `eu-central-1`, set the
   Bedrock entry to enabled, export `BEDROCK_MODEL_ID` and your AWS credentials, and run. The Restricted request now goes
   to Bedrock in Frankfurt first.

## Check yourself

<details><summary>Why filter by jurisdiction before trying endpoints, rather than checking after a failure?</summary>
If the filter came later, a fallback could send Restricted data abroad before the check ran. Filtering first guarantees
that every endpoint the router could possibly try is compliant.
</details>

<details><summary>Why is an unknown classification treated as Restricted?</summary>
Failing safe: if someone sends a label the router doesn't recognise, the strictest rule applies. Treating unknown data as
Public could send sensitive data anywhere.
</details>

<details><summary>What should the caller do with a REFUSED result?</summary>
Not retry blindly against other endpoints. It should queue the work, tell the user it will be processed later or by a
person, and raise an alert so operations can restore a compliant endpoint.
</details>

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| Every request goes to the mock even after enabling a provider | The provider's adapter fails (missing SDK or credentials) and falls through | Read the `failed:` line; install the SDK and set the environment variables |
| `KeyError` for a model variable | The adapter reads the model name from an environment variable that isn't set | Export the variable named in `model_env` |
| Restricted data reaches a foreign endpoint | The endpoint's `jurisdiction` is wrong in the config | Review the config like code; add a test that asserts every Restricted route stays in the EU |
| The router hides real errors | A broad `except` swallows everything | Log each failure with the endpoint and error type, as the lab does, and alert on repeated failures |

## Take it further

- Add a circuit breaker: after three failures in a minute, skip that endpoint for five minutes.
- Record which endpoint served each request in an audit log, with the data classification.
- Write unit tests for the routing rules with a fake config, so a config change can't silently break residency.

## In a real client project

- Agree the classification scheme and residency rules with the client's data protection officer, in writing.
- Check each provider's data-processing terms and regional availability for the exact model you use.
- Keep credentials in the cloud's secret manager or workload identity, never in files or code.
