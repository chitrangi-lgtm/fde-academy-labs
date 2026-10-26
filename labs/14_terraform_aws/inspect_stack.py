"""List what lab 14 created, through the AWS API, the way an operator checks a deployment.

    python inspect_stack.py                      against the emulator at http://localhost:5000
    AWS_PROFILE=... python inspect_stack.py --real   against your real account (uses your normal AWS credentials)
"""

from __future__ import annotations

import sys

import boto3

REAL = "--real" in sys.argv
REGION = "ap-south-1"
kwargs = {"region_name": REGION} if REAL else {"region_name": REGION, "endpoint_url": "http://localhost:5000",
                                                "aws_access_key_id": "testing", "aws_secret_access_key": "testing"}

s3, ddb, sqs = boto3.client("s3", **kwargs), boto3.client("dynamodb", **kwargs), boto3.client("sqs", **kwargs)

for b in s3.list_buckets().get("Buckets", []):
    if "-documents-" not in b["Name"]:
        continue
    enc = s3.get_bucket_encryption(Bucket=b["Name"])["ServerSideEncryptionConfiguration"]["Rules"][0]["ApplyServerSideEncryptionByDefault"]
    block = s3.get_public_access_block(Bucket=b["Name"])["PublicAccessBlockConfiguration"]
    versioning = s3.get_bucket_versioning(Bucket=b["Name"]).get("Status")
    print(f"bucket {b['Name']}: encryption {enc['SSEAlgorithm']}, public access blocked {all(block.values())}, versioning {versioning}")

for name in ddb.list_tables()["TableNames"]:
    t = ddb.describe_table(TableName=name)["Table"]
    pitr = ddb.describe_continuous_backups(TableName=name)["ContinuousBackupsDescription"]["PointInTimeRecoveryDescription"]["PointInTimeRecoveryStatus"]
    print(f"table {name}: billing {t.get('BillingModeSummary', {}).get('BillingMode')}, keys {[k['AttributeName'] for k in t['KeySchema']]}, PITR {pitr}")

for url in sqs.list_queues().get("QueueUrls", []):
    attrs = sqs.get_queue_attributes(QueueUrl=url, AttributeNames=["All"])["Attributes"]
    print(f"queue {url.rsplit('/', 1)[-1]}: dead-letter policy {'yes' if 'RedrivePolicy' in attrs else 'no'}, "
          f"encrypted {attrs.get('SqsManagedSseEnabled', 'false')}")
