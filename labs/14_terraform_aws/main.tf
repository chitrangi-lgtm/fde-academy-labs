# Lab 14 — Terraform on AWS: the cloud footprint of a document assistant, against a local AWS emulator or a real account.
#
# Emulator (no AWS account, nothing billed):
#   pip install "moto[server]" && moto_server -p 5000          # in a second terminal
#   terraform init
#   terraform plan -out plan.out && terraform show -json plan.out > plan.json
#   python policy_check.py plan.json                           # the CI gate: fails on public data, missing encryption or tags
#   terraform apply plan.out
#   python inspect_stack.py                                    # list what was created, through the AWS API
#   terraform destroy
#
# Real AWS (free tier; read the guide's cost section first):
#   cp real-aws.tfvars.example real-aws.tfvars                 # set your budget e-mail
#   terraform plan -var-file=real-aws.tfvars -out plan.out     # then the same check, apply and destroy
#
# Guide: ../../guides/14_terraform_aws.md

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.70"
    }
  }
}

provider "aws" {
  region = var.region

  # Emulator mode: fake credentials, every service pointed at moto, and no calls to AWS's account APIs.
  access_key                  = var.use_emulator ? "testing" : null
  secret_key                  = var.use_emulator ? "testing" : null
  skip_credentials_validation = var.use_emulator
  skip_requesting_account_id  = var.use_emulator
  skip_metadata_api_check     = var.use_emulator
  s3_use_path_style           = var.use_emulator

  dynamic "endpoints" {
    for_each = var.use_emulator ? [var.emulator_url] : []
    content {
      s3       = endpoints.value
      dynamodb = endpoints.value
      sqs      = endpoints.value
      iam      = endpoints.value
      sts      = endpoints.value
      kms      = endpoints.value
      budgets  = endpoints.value
    }
  }

  # Every resource gets these tags, so cost reports and access reviews can find it.
  default_tags {
    tags = {
      project     = var.project
      environment = var.environment
      owner       = var.owner
      data_class  = "confidential"
      managed_by  = "terraform"
    }
  }
}

locals {
  name = "${var.project}-${var.environment}"
}

# ---------------------------------------------------------------- documents: private, encrypted, versioned
resource "aws_kms_key" "documents" {
  description             = "Encrypts ${local.name} documents and conversation state"
  deletion_window_in_days = 7
  enable_key_rotation     = true
}

resource "aws_s3_bucket" "documents" {
  bucket        = "${local.name}-documents-${var.bucket_suffix}"
  force_destroy = var.use_emulator # a real bucket with data should never be deleted by a plan
}

resource "aws_s3_bucket_public_access_block" "documents" {
  bucket                  = aws_s3_bucket.documents.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "documents" {
  bucket = aws_s3_bucket.documents.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "documents" {
  bucket = aws_s3_bucket.documents.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.documents.arn
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "documents" {
  bucket = aws_s3_bucket.documents.id
  rule {
    id     = "expire-old-versions"
    status = "Enabled"
    filter {}
    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}

# ---------------------------------------------------------------- conversation state: on-demand, recoverable
resource "aws_dynamodb_table" "conversations" {
  name         = "${local.name}-conversations"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "tenant_conversation"
  range_key    = "turn"

  attribute {
    name = "tenant_conversation"
    type = "S"
  }
  attribute {
    name = "turn"
    type = "N"
  }
  ttl {
    attribute_name = "expires_at"
    enabled        = true
  }
  point_in_time_recovery {
    enabled = true
  }
  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.documents.arn
  }
}

# ---------------------------------------------------------------- ingestion queue with a dead-letter queue
resource "aws_sqs_queue" "ingest_dlq" {
  name                      = "${local.name}-ingest-dlq"
  message_retention_seconds = 1209600 # 14 days to investigate failures
  sqs_managed_sse_enabled   = true
}

resource "aws_sqs_queue" "ingest" {
  name                       = "${local.name}-ingest"
  visibility_timeout_seconds = 300
  sqs_managed_sse_enabled    = true
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.ingest_dlq.arn
    maxReceiveCount     = 3
  })
}

# ---------------------------------------------------------------- the ingestion worker's role: least privilege
data "aws_iam_policy_document" "assume_lambda" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ingest_worker" {
  name               = "${local.name}-ingest-worker"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda.json
}

data "aws_iam_policy_document" "ingest_worker" {
  statement {
    sid       = "ReadDocuments"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.documents.arn}/incoming/*"]
  }
  statement {
    sid       = "ConsumeQueue"
    actions   = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"]
    resources = [aws_sqs_queue.ingest.arn]
  }
  statement {
    sid       = "WriteState"
    actions   = ["dynamodb:PutItem", "dynamodb:UpdateItem"]
    resources = [aws_dynamodb_table.conversations.arn]
  }
  statement {
    sid       = "UseKey"
    actions   = ["kms:Decrypt", "kms:GenerateDataKey"]
    resources = [aws_kms_key.documents.arn]
  }
}

resource "aws_iam_role_policy" "ingest_worker" {
  name   = "least-privilege"
  role   = aws_iam_role.ingest_worker.id
  policy = data.aws_iam_policy_document.ingest_worker.json
}

# ---------------------------------------------------------------- a budget alarm, real accounts only
resource "aws_budgets_budget" "monthly" {
  count        = var.use_emulator ? 0 : 1
  name         = "${local.name}-monthly"
  budget_type  = "COST"
  limit_amount = var.monthly_budget_usd
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.budget_email]
  }
}
