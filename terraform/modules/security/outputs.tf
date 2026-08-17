output "ssm_db_parameter_names" {
  description = "Nomes dos parâmetros SSM das credenciais dos bancos"

  value = {
    for k, v in aws_ssm_parameter.db_secrets :
    k => v.name
  }
}