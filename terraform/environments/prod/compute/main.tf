# ------------------------------------------------------------------
# PROVIDERS
# ------------------------------------------------------------------

terraform {
  backend "s3" {
    key            = "prod/compute/terraform.tfstate"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_eks_cluster" "eks" {
  name = module.eks.cluster_name
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_name
  depends_on = [module.eks]
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.eks.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.eks.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.cluster.token
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

resource "aws_ssm_parameter" "cluster_name" {
  name  = "/togglemaster/prod/cluster-name"
  type  = "String"
  value = module.eks.cluster_name

  tags = {
    Project     = "ToggleMaster"
    Environment = "prod"
  }
}