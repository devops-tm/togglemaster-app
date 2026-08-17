output "rds_instance_identifiers" {
  description = "Identificadores das instâncias RDS"

  value = {
    for k, v in module.rds.rds_instance_identifiers :
    k => v
  }
}

output "redis_cluster_id" {
  description = "Identificador do cluster Redis"
  value       = module.elasticache.redis_cluster_id
}