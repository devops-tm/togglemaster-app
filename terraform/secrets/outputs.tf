output "database_credentials" {
  description = "Senhas geradas para os bancos de dados"
  value       = {
    for k, v in random_password.password : k => v.result
  }
  sensitive   = true
}