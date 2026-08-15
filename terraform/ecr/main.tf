resource "aws_ecr_repository" "togglemaster_repos" {
  for_each             = toset(var.ecr_repositories)
  name                 = each.key
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = false
  }
}

output "ecr_repository_urls" {
  value = { for k, v in aws_ecr_repository.togglemaster_repos : k => v.repository_url }
}