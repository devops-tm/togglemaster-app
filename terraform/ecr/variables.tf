variable "aws_region" {
  description = "Regiao da AWS onde os recursos serao provisionados"
  type        = string
}

variable "ecr_repositories" {
  description = "Lista com os nomes dos repositorios ECR"
  type        = list(string)
}