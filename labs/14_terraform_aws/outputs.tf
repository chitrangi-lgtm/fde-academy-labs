output "documents_bucket" {
  value = aws_s3_bucket.documents.bucket
}

output "conversations_table" {
  value = aws_dynamodb_table.conversations.name
}

output "ingest_queue_url" {
  value = aws_sqs_queue.ingest.url
}

output "ingest_worker_role" {
  value = aws_iam_role.ingest_worker.arn
}
