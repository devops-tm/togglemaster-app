resource "random_password" "db_passwords" {
  for_each = var.databases

  length           = 32
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
  min_lower        = 2
  min_upper        = 2
  min_numeric      = 2
  min_special      = 2
}

resource "aws_ssm_parameter" "db_secrets" {
  for_each = var.databases

  name        = "/togglemaster/prod/${each.key}/credentials"
  description = "Database credentials for ${each.key} service"
  type        = "SecureString"

  value = jsonencode({
    username = var.db_username
    password = random_password.db_passwords[each.key].result
  })

  tags = {
    Project     = "ToggleMaster"
    Environment = "AWSAcademy"
    Service     = each.key
  }
}
