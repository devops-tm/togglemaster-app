output "ecr_repository_urls" {
  description = "URLs dos repositorios ECR"

  value = {
    for k, v in aws_ecr_repository.togglemaster_repos :
    k => v.repository_url
  }
}