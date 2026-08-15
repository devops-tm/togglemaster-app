data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "postgres" {
  for_each = var.databases

  name        = "${each.key}-postgres-sg"
  description = "Security Group do banco ${each.key}"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 5432
    to_port     = 5432
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

resource "aws_db_instance" "postgres" {
  for_each = var.databases

  identifier = each.value.identifier

  engine         = "postgres"
  engine_version = "15"

  instance_class    = "db.t3.micro"
  allocated_storage = 20
  storage_type      = "gp2"

  db_name  = each.value.db_name
  username = var.db_username
  password = var.db_password

  publicly_accessible = false
  multi_az            = false

  skip_final_snapshot = true
  deletion_protection = false

  apply_immediately          = true
  auto_minor_version_upgrade = true

  backup_retention_period = 0

  storage_encrypted = true

  monitoring_interval          = 0
  performance_insights_enabled = false

  copy_tags_to_snapshot = false

  vpc_security_group_ids = [
    aws_security_group.postgres[each.key].id
  ]

  tags = {
    Project     = "ToggleMaster"
    Environment = "AWSAcademy"
    Service     = each.key
  }
}