variable "aws_region" {
  description = "Regiao da AWS onde os recursos serao provisionados"
  type        = string
}

variable "sqs_queue_name" {
  description = "Nome da fila SQS para os eventos de avaliacao"
  type        = string
}

variable "dynamodb_table_name" {
  description = "Nome da tabela DynamoDB para analytics"
  type        = string
}