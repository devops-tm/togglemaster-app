variable "aws_region" {
  description = "Região AWS"
  type        = string
}

variable "eks_node_security_group" {
  description = "Security Group do EKS"
  type        = string
}

variable "rds_instances" {
  description = "Identificadores das instâncias RDS"
  type        = list(string)
}

variable "redis_cluster_id" {
  description = "ID do cluster Redis"
  type        = string
}