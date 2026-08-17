terraform {
  backend "s3" {}

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

module "security" {
  source = "../../modules/security"

  db_username = var.db_username
  databases   = var.databases
}

module "rds" {
  source = "../../modules/rds"

  databases = var.databases
}

module "elasticache" {
  source = "../../modules/elasticache"
}

module "eks" {
  source = "../../modules/eks"
}