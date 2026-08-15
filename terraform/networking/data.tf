data "aws_db_instance" "databases" {
  for_each               = toset(var.rds_instances)
  db_instance_identifier = each.key
}

data "aws_elasticache_cluster" "redis" {
  cluster_id = var.redis_cluster_id
}