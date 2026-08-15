resource "aws_sqs_queue" "evaluation_queue" {
  name                      = var.sqs_queue_name
  message_retention_seconds = 86400
}

resource "aws_dynamodb_table" "analytics_table" {
  name           = var.dynamodb_table_name
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "event_id"

  attribute {
    name = "event_id"
    type = "S"
  }
}

output "sqs_queue_url" {
  value = aws_sqs_queue.evaluation_queue.url
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.analytics_table.name
}