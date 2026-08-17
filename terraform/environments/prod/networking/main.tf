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

data "terraform_remote_state" "data" {
  backend = "s3"

  config = {
    bucket = var.terraform_state_bucket
    key    = "prod/data/terraform.tfstate"
    region = var.aws_region
  }
}

data "terraform_remote_state" "compute" {
  backend = "s3"

  config = {
    bucket = var.terraform_state_bucket
    key    = "prod/compute/terraform.tfstate"
    region = var.aws_region
  }
}

module "networking" {
  source = "../../../modules/networking"

  eks_node_security_group = data.terraform_remote_state.compute.outputs.node_security_group_id

  rds_instance_identifiers = toset(
    values(data.terraform_remote_state.data.outputs.rds_instance_identifiers)
  )

  redis_cluster_id = data.terraform_remote_state.data.outputs.redis_cluster_id
}