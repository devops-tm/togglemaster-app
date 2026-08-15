output "rds_security_groups" {
  value = { for k, v in data.aws_db_instance.databases : k => v.vpc_security_groups[0] }
}

output "redis_security_group" {
  value = tolist(data.aws_elasticache_cluster.redis.security_group_ids)[0]
}