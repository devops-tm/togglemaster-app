resource "random_password" "password" {
  for_each         = var.database_identifiers
  length           = 16
  special          = true
  override_special = "!#%&*()-_=+[]{}<>:?"
}

resource "aws_secretsmanager_secret" "secret" {
  for_each    = var.database_identifiers
  name        = "togglemaster/${var.environment}/${each.key}-credentials"
  description = "Credenciais para o banco de dados do servico ${each.key}"
}

resource "aws_secretsmanager_secret_version" "secret_version" {
  for_each      = var.database_identifiers
  secret_id     = aws_secretsmanager_secret.secret[each.key].id
  secret_string = jsonencode({
    username = "${each.key}_admin"
    password = random_password.password[each.key].result
  })
}