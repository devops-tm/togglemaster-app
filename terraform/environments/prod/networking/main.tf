terraform {
  backend "s3" {
    key     = "prod/networking/terraform.tfstate"
    encrypt = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "networking" {
  source = "../../../modules/networking"

  eks_node_security_group = var.eks_node_security_group
  rds_instances            = var.rds_instances
  redis_cluster_id         = var.redis_cluster_id
}