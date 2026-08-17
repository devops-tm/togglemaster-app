output "ssm_db_parameter_names" {
  value = {
    for k, v in aws_ssm_parameter.db_secrets :
    k => v.name
  }
}

output "ssm_redis_parameter_name" {
  value = aws_ssm_parameter.redis_secret.name
}