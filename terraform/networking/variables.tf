variable "aws_region" {
  description = "Regiao da AWS onde os recursos serao provisionados"
  type        = string
}

variable "eks_node_security_group" {
  description = "Security Group dos Worker Nodes do EKS"
  type        = string
}

variable "rds_instances" {
  description = "Identificadores das instancias RDS para busca via data source"
  type        = list(string)
}

variable "redis_cluster_id" {
  description = "Identificador do cluster Redis para busca via data source"
  type        = string
}