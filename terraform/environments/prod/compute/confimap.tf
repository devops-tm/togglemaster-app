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

data "aws_caller_identity" "current" {}