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

module "ecr" {
  source = "../../../modules/ecr"

  aws_region       = var.aws_region
  ecr_repositories = var.ecr_repositories
}

module "sqs" {
  source = "../../../modules/sqs"

  aws_region     = var.aws_region
  sqs_queue_name = var.sqs_queue_name
}

module "dynamodb" {
  source = "../../../modules/dynamodb"

  aws_region          = var.aws_region
  dynamodb_table_name = var.dynamodb_table_name
}