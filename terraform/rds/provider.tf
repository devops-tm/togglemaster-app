terraform {
  backend "s3" {
    bucket = "nome-do-seu-bucket"
    key    = "eks/terraform.tfstate"
    region = "sua-regiao-aqui"
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