data "aws_vpc" "default" {
  default = true
}

data "aws_secretsmanager_secret" "redis_secret" {
  name = "togglemaster/prod/redis-credentials"
}

data "aws_secretsmanager_secret_version" "redis_secret_val" {
  secret_id = data.aws_secretsmanager_secret.redis_secret.id
}

locals {
  redis_creds = jsondecode(data.aws_secretsmanager_secret_version.redis_secret_val.secret_string)
}

resource "aws_security_group" "redis" {
  name        = "${var.cluster_id}-sg"
  description = "Redis SG para o cluster ${var.cluster_id}"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = var.redis_port
    to_port     = var.redis_port
    protocol    = "tcp"
    cidr_blocks = []
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_elasticache_cluster" "redis_cache" {
  cluster_id           = var.cluster_id
  engine               = "redis"
  node_type            = var.node_type
  num_cache_nodes      = 1
  port                 = var.redis_port
  apply_immediately    = true
  
  transit_encryption_enabled = true
  auth_token                 = local.redis_creds["password"]

  security_group_ids = [
    aws_security_group.redis.id
  ]
}