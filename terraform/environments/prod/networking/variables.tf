variable "aws_region" {
  description = "Região AWS"
  type        = string
}

variable "terraform_state_bucket" {
  description = "Bucket S3 utilizado para armazenar os estados do Terraform"
  type        = string
  sensitive   = true
}