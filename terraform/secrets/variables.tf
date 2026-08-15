variable "environment" {
  description = "Identificador do ambiente"
  type        = string
  default     = "prod"
}

variable "database_identifiers" {
  description = "Lista de identificadores para geracao de senhas"
  type        = set(string)
  default     = ["auth", "flag", "targeting", "redis"]
}