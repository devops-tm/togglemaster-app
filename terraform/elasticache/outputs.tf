output "redis_endpoint" {
  value = aws_elasticache_cluster.redis_cache.cache_nodes[0].address
}