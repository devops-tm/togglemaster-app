variable "aws_region" {
  description = "Região da AWS onde o cluster será provisionado"
  type        = string
}

variable "cluster_name" {
  description = "Nome do cluster EKS"
  type        = string
  default     = "togglemaster-cluster"
}

variable "cluster_version" {
  description = "Versão do Kubernetes"
  type        = string
  default     = "1.29"
}

variable "node_group_name" {
  description = "Nome do Node Group"
  type        = string
  default     = "togglemaster-nodegroup"
}

variable "instance_types" {
  description = "Tipos de instância para os worker nodes"
  type        = list(string)
  default     = ["t3.medium"]
}

variable "desired_size" {
  description = "Quantidade desejada de instâncias nos nós"
  type        = number
  default     = 2
}

variable "min_size" {
  description = "Quantidade mínima de instâncias"
  type        = number
  default     = 1
}

variable "max_size" {
  description = "Quantidade máxima de instâncias"
  type        = number
  default     = 3
}