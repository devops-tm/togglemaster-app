variable "aws_region" {
  description = "Regiao da AWS onde os recursos serao provisionados"
  type        = string
}

variable "cluster_id" {
  description = "Identificador do cluster Redis"
  type        = string
}

variable "node_type" {
  description = "Tipo de instancia do nó de cache"
  type        = string
}

variable "redis_port" {
  description = "Porta de conexao do Redis"
  type        = number
}