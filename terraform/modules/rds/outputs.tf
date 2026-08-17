output "rds_endpoints" {
  value = {
    for k, v in aws_db_instance.postgres :
    k => v.endpoint
  }
}

output "rds_databases" {
  value = {
    for k, v in aws_db_instance.postgres :
    k => v.db_name
  }
}

output "rds_instance_identifiers" {
  description = "Identificadores das instancias RDS"

  value = {
    for k, v in aws_db_instance.postgres :
    k => v.identifier
  }
}

