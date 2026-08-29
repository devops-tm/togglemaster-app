provider "kubernetes" {
  host                   = aws_eks_cluster.eks.endpoint
  cluster_ca_certificate = base64decode(aws_eks_cluster.eks.certificate_authority[0].data)
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["eks", "get-token", "--cluster-name", aws_eks_cluster.eks.name, "--region", var.aws_region]
  }
}

resource "kubernetes_config_map" "aws_config" {
  metadata {
    name      = "aws-config"
    namespace = "togglemaster"
  }

  data = {
    AWS_ACCOUNT_ID = data.aws_caller_identity.current.account_id
    AWS_REGION     = var.aws_region
  }
}