resource "random_password" "db_password" {
  for_each = var.databases

  length  = 16
  special = false
}

resource "aws_ssm_parameter" "db_secrets" {
  for_each = var.databases

  name = "/togglemaster/prod/${each.key}/credentials"

  type = "SecureString"

  value = jsonencode({
    username = var.db_username
    password = random_password.db_password[each.key].result
  })

  tags = {
    Project     = "ToggleMaster"
    Environment = "AWSAcademy"
    Service     = each.key
  }
}

resource "random_password" "redis_password" {
  length  = 16
  special = false
}

resource "aws_ssm_parameter" "redis_secret" {
  name = "/togglemaster/prod/redis/credentials"

  type = "SecureString"

  value = jsonencode({
    password = random_password.redis_password.result
  })

  tags = {
    Project     = "ToggleMaster"
    Environment = "AWSAcademy"
    Service     = "redis"
  }
}