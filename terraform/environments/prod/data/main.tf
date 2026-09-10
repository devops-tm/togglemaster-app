terraform {
  backend "s3" {
    key     = "prod/data/terraform.tfstate"
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

module "rds" {
  source = "../../../modules/rds"

  databases = var.databases
  # NÃO passe eks_security_group_id aqui
}

module "elasticache" {
  source = "../../../modules/elasticache"
}