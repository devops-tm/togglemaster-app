terraform {
  backend "s3" {
    key     = "prod/compute/terraform.tfstate"
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

module "eks" {
  source = "../../../modules/eks"

  cluster_name     = var.cluster_name
  cluster_version  = var.cluster_version
  node_group_name  = var.node_group_name
  instance_types   = var.instance_types
  desired_size     = var.desired_size
  min_size         = var.min_size
  max_size         = var.max_size
}