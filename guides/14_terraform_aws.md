# Lab 14: The AWS footprint of a document assistant, in Terraform, with a policy gate

**Time:** 90 minutes · **Level:** Advanced · **Builds on:** FDE Module 17 (containers and Kubernetes), Module 21 (cloud architecture), P1.4 (infrastructure as code), P10 (deployment)

## The problem

CrestFin is moving its policy assistant from a pilot laptop to AWS in Frankfurt (`eu-central-1`), because its customers'
data must stay in the EU. The security team has set four conditions before anything goes live:

- Documents must never be public, and must be encrypted with a key CrestFin controls.
- Conversation history must be recoverable to any point in the last 35 days.
- Failed ingestion jobs must be kept for investigation, not silently dropped.
- Every resource must say who owns it and what data it holds, and no role may have wildcard permissions.

Their platform team will only accept infrastructure as code that passes an automated policy check in CI. You'll write
that infrastructure in Terraform, run it against a **local AWS emulator** (no account, no bill), prove the policy gate
catches a bad change, and optionally deploy it to a real free-tier account with a budget alarm.

## What you'll learn

- How a Terraform configuration is organised: providers, variables, resources, data sources and outputs.
- The AWS building blocks behind most AI assistants: S3 with KMS encryption, versioning and a public-access block; a
  DynamoDB table with point-in-time recovery and TTL; an SQS queue with a dead-letter queue; a least-privilege IAM role.
- The plan-review-apply discipline: `plan -out`, read the plan as JSON, gate it, and only then apply exactly that plan.
- How to write a policy gate over `terraform show -json`, and why some values are only "known after apply".
- How to keep cost under control in a real account: tags, budgets, and `destroy`.

## Before you start

You need Terraform 1.5 or newer and Python 3.10 or newer.

1. In one terminal: `pip install "moto[server]" boto3` then `moto_server -p 5000`. **moto** is an open-source AWS
   emulator, so every API call stays on your machine.
2. In another terminal: `cd realtools/labs/14_terraform_aws` and `terraform init`. This downloads the AWS provider
   (about 150 MB) once.

The provider block switches to the emulator when `use_emulator = true`, which is the default. It does that with fake
credentials and an `endpoints` block, so nothing reaches AWS.

## Key ideas

**Plan, then apply exactly that plan.** `terraform plan -out plan.out` saves the change set. `terraform show -json
plan.out` turns it into JSON your tools can check, and `terraform apply plan.out` applies that exact plan and nothing
else. Applying without a saved plan can apply changes nobody reviewed.

**Defence in depth on S3.** The bucket has four controls:
- a public access block, with all four switches on;
- default KMS encryption with a customer-managed key that rotates yearly;
- versioning, so an overwrite or delete can be undone;
- a lifecycle rule that removes old versions after 30 days, so versioning doesn't grow the bill for ever.

**State you can recover.** The conversation table is on-demand (`PAY_PER_REQUEST`, so there is no idle cost), and has
point-in-time recovery, encryption with the same key, and TTL. The `expires_at` attribute lets old turns delete
themselves, which supports the retention rules in the GDPR and India's DPDP Act.

**Failures you can investigate.** After three failed receives, a message moves to the dead-letter queue and stays there
for 14 days. Without a dead-letter queue, a poison message retries for ever or disappears.

**Least privilege.** The ingestion worker's role can read only `incoming/` objects in this bucket, consume only this
queue, and write only to this table. Wildcards like `s3:*` on `*` are how one compromised function becomes a data breach.

**Tags by default.** `default_tags` in the provider puts `project`, `environment`, `owner`, `data_class` and
`managed_by` on every resource. That is what makes cost reports and access reviews possible.

**Known after apply.** Some values don't exist until a resource is created, such as the dead-letter queue's ARN inside
the main queue's redrive policy. In the plan JSON they appear under `after_unknown`, not under values. The gate treats
"pending" as present. A naive gate would wrongly fail this plan, and the first version of this lab's gate did exactly
that.

## Steps

1. **Validate and plan.** Run `terraform validate`, then `terraform plan -out plan.out`. Expect "Plan: 11 to add". Read
   the plan output and find the bucket's public access block, the table's recovery setting and the queue's redrive
   policy.

2. **Gate the plan.** Run `terraform show -json plan.out > plan.json`, then `python policy_check.py plan.json`. Expect
   about 23 PASS lines and "0 failed". Open `policy_check.py` and match each rule to one of the security team's four
   conditions.

3. **Apply and inspect.** Run `terraform apply plan.out`, then `python inspect_stack.py`. You should see:
   - the bucket encrypted with `aws:kms`, public access blocked and versioning enabled;
   - the table billed per request with point-in-time recovery enabled;
   - the main queue with a dead-letter policy, and both queues encrypted.

   Run `terraform output` for the names.

4. **Make a bad change and watch the gate stop it.** Add a policy document with `actions = ["s3:*"]` and
   `resources = ["*"]`, plus an `aws_s3_bucket_acl` with `acl = "public-read"`. Plan again and run the gate. Expect three
   FAIL lines and exit code 1. Remove the bad change. In CI, that exit code blocks the merge.

5. **See what a destructive change looks like.** Change the table's `hash_key` and plan. Terraform must replace the
   table, which means deleting its data. Run the gate on that plan: the destroy rule fails unless you set
   `ALLOW_DESTROY=1`. Change the key back. Always read "must be replaced" lines in a plan before approving it.

6. **Clean up.** Run `terraform destroy`. With the emulator, stopping `moto_server` also discards everything.

7. **Optional: a real AWS account.** Copy `real-aws.tfvars.example` to `real-aws.tfvars`, set a unique bucket suffix
   and your e-mail, and run `terraform plan -var-file=real-aws.tfvars -out plan.out`. Then gate, apply, inspect with
   `python inspect_stack.py --real`, and **destroy the same day**. The budget resource e-mails you when the month's
   forecast passes 80% of $5.

## Cost in a real account

Everything here is on-demand. With no traffic, the monthly cost is the KMS key (about $1 a month while it exists)
plus pennies of S3 storage. DynamoDB on-demand, SQS and IAM cost nothing when idle within the free tier. Destroy the stack
when you finish. The key enters a 7-day deletion window, during which it isn't billed for use. Never leave a lab stack
running.

## Check yourself

<details><summary>Why save the plan to a file and apply that file?</summary>
So exactly the reviewed change is applied. Between a plan and an unsaved apply, the code, variables or the real
infrastructure can change, and the apply would do something nobody reviewed.
</details>

<details><summary>The gate failed "sends failures to a dead-letter queue" although the redrive policy is in the code. Why might that happen?</summary>
The redrive policy contains the DLQ's ARN, which is unknown until the DLQ exists, so the plan JSON lists it under
after_unknown instead of values. A gate must treat pending values as present.
</details>

<details><summary>Which two controls stop an accidental public bucket, and why have both?</summary>
The public access block (it overrides public ACLs and bucket policies) and the gate's ACL rule (which catches the
change before it is applied). One is a guardrail in AWS, the other a review in CI; either alone can be misconfigured.
</details>

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `connection refused` on plan or apply | `moto_server` isn't running, or is on another port | Start it with `moto_server -p 5000`, or set `emulator_url` |
| `BucketAlreadyExists` in a real account | S3 bucket names are global | Change `bucket_suffix` |
| Real apply tries to reach the emulator | `use_emulator` still true | Use `-var-file=real-aws.tfvars`, which sets it to false |
| The gate passes a plan you know is wrong | The rule reads `values` but the attribute is unknown, or a resource type is missing | Check `after_unknown`, and add a rule plus a failing test plan for each new resource type |
| Surprise bill | The stack was left running | Budget alarm, tags, and `terraform destroy` at the end of every session |

## Take it further

- Add an AWS Lambda for the ingestion worker, triggered by the queue, with its own log group and 30-day retention.
- Move the configuration into a module (`modules/assistant`) and create `dev` and `prod` stacks with different settings.
- Add a remote state backend (S3 with locking) and explain why a team can't share local state files.
- Write the same gate as an Open Policy Agent (Rego) policy and compare it with the Python version.

## In a real client project

- Every change goes through pull request, plan, gate and review, then an apply from CI with a short-lived role. Nobody
  applies from a laptop.
- Keep the region and data-classification decisions in variables with validation, and record them in an architecture
  decision record (FDE Module 10).
- Review the plan's "must be replaced" lines for anything stateful, every time.
