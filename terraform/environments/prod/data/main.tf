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
  eks_security_group_id = data.terraform_remote_state.compute.outputs.cluster_primary_security_group_id
}

module "elasticache" {
  source = "../../../modules/elasticache"
}

data "terraform_remote_state" "compute" {
  backend = "s3"
  config = {
    bucket = var.terraform_state_bucket
    key    = "prod/compute/terraform.tfstate"
    region = var.aws_region
  }
}