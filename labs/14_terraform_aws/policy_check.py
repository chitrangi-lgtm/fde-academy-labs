"""The policy gate for lab 14: read a Terraform plan (terraform show -json plan.out > plan.json) and fail it if it would
create public or unencrypted data, untagged resources, wildcard IAM permissions, a queue without a dead-letter queue, or
delete a stateful resource. This is the check a CI pipeline runs on every pull request before anyone may apply.

    python policy_check.py plan.json            exit code 0 = every rule passes, 1 = at least one violation
    ALLOW_DESTROY=1 python policy_check.py ...  accept planned deletions (for a deliberate teardown)
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, Iterator, List, Tuple

REQUIRED_TAGS = ("project", "environment", "owner", "data_class")
STATEFUL = ("aws_s3_bucket", "aws_dynamodb_table", "aws_kms_key")


def resources(plan: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
    """Every planned resource, including those in child modules."""
    stack = [plan.get("planned_values", {}).get("root_module", {})]
    while stack:
        module = stack.pop()
        yield from module.get("resources", [])
        stack.extend(module.get("child_modules", []))


def config_policy_statements(plan: Dict[str, Any]) -> Iterator[Tuple[str, Dict[str, Any]]]:
    """IAM policy-document statements from the configuration (their ARNs are often unknown until apply)."""
    for r in plan.get("configuration", {}).get("root_module", {}).get("resources", []):
        if r.get("type") == "aws_iam_policy_document":
            for st in r.get("expressions", {}).get("statement", []):
                yield r["address"], st


def set_or_pending(plan: Dict[str, Any], resource: Dict[str, Any], key: str) -> bool:
    """True when the attribute has a value, or will have one after apply (it refers to something not created yet)."""
    if resource["values"].get(key):
        return True
    change = next((rc for rc in plan.get("resource_changes", []) if rc.get("address") == resource["address"]), {})
    return bool(change.get("change", {}).get("after_unknown", {}).get(key))


def check(plan: Dict[str, Any]) -> List[Tuple[bool, str]]:
    res = list(resources(plan))
    by_type: Dict[str, List[Dict[str, Any]]] = {}
    for r in res:
        by_type.setdefault(r["type"], []).append(r)
    results: List[Tuple[bool, str]] = []

    buckets = by_type.get("aws_s3_bucket", [])
    blocks = [b for b in by_type.get("aws_s3_bucket_public_access_block", [])
              if all(b["values"].get(k) for k in ("block_public_acls", "block_public_policy", "ignore_public_acls", "restrict_public_buckets"))]
    results.append((len(blocks) >= len(buckets), f"S3: {len(buckets)} bucket(s), {len(blocks)} with every public-access block switched on"))
    sse = by_type.get("aws_s3_bucket_server_side_encryption_configuration", [])
    results.append((len(sse) >= len(buckets), f"S3: {len(sse)} of {len(buckets)} bucket(s) encrypted by default"))
    for acl in by_type.get("aws_s3_bucket_acl", []):
        results.append((acl["values"].get("acl") not in ("public-read", "public-read-write"), f"S3: {acl['address']} ACL is not public"))

    for t in by_type.get("aws_dynamodb_table", []):
        v = t["values"]
        pitr = any(p.get("enabled") for p in v.get("point_in_time_recovery") or [])
        enc = any(s.get("enabled") for s in v.get("server_side_encryption") or [])
        results.append((pitr, f"DynamoDB: {t['address']} has point-in-time recovery"))
        results.append((enc, f"DynamoDB: {t['address']} is encrypted with a customer-managed key"))

    for q in by_type.get("aws_sqs_queue", []):
        v = q["values"]
        results.append((bool(v.get("sqs_managed_sse_enabled") or v.get("kms_master_key_id")), f"SQS: {q['address']} is encrypted"))
        if not q["name"].endswith("dlq"):
            results.append((set_or_pending(plan, q, "redrive_policy"), f"SQS: {q['address']} sends failures to a dead-letter queue"))

    for address, st in config_policy_statements(plan):
        actions = st.get("actions", {}).get("constant_value") or []
        res_list = st.get("resources", {}).get("constant_value") or []
        wildcard_action = any(a == "*" or a.endswith(":*") for a in actions)
        results.append((not wildcard_action, f"IAM: {address} grants named actions, not wildcards ({', '.join(actions) or 'computed'})"))
        results.append(("*" not in res_list, f"IAM: {address} names its resources instead of '*'"))

    for r in res:
        tags = r["values"].get("tags_all")
        if isinstance(tags, dict):
            missing = [k for k in REQUIRED_TAGS if not tags.get(k)]
            results.append((not missing, f"Tags: {r['address']} has {', '.join(REQUIRED_TAGS)}" + (f" (missing {', '.join(missing)})" if missing else "")))

    allow_destroy = os.getenv("ALLOW_DESTROY") == "1"
    for rc in plan.get("resource_changes", []):
        if rc.get("type") in STATEFUL and "delete" in rc.get("change", {}).get("actions", []):
            results.append((allow_destroy, f"Destroy: {rc['address']} would be deleted" + (" (allowed)" if allow_destroy else "; set ALLOW_DESTROY=1 only for a deliberate teardown")))
    return results


def main(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        plan = json.load(f)
    results = check(plan)
    for ok, message in results:
        print(("PASS  " if ok else "FAIL  ") + message)
    failed = sum(1 for ok, _ in results if not ok)
    print(f"\n{len(results) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "plan.json"))
