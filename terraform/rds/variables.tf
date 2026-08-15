variable "aws_region" {
  description = "Regiao da AWS onde os recursos serao provisionados"
  type        = string
}

variable "db_username" {
  description = "Usuário administrador do PostgreSQL"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Senha do PostgreSQL"
  type        = string
  sensitive   = true
}

variable "databases" {
  description = "Mapeamento dos bancos de dados a serem criados"
  type = map(object({
    identifier = string
    db_name    = string
  }))
}