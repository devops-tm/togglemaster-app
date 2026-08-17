output "cluster_name" {
  description = "Nome do cluster EKS"
  value       = aws_eks_cluster.eks.name
}

output "cluster_endpoint" {
  description = "Endpoint do cluster EKS"
  value       = aws_eks_cluster.eks.endpoint
}

output "cluster_certificate_authority_data" {
  description = "Certificado da autoridade do cluster EKS"
  value       = aws_eks_cluster.eks.certificate_authority[0].data
  sensitive   = true
}

output "cluster_security_group_id" {
  description = "Security Group principal do cluster EKS"
  value       = aws_eks_cluster.eks.vpc_config[0].cluster_security_group_id
}

output "node_group_id" {
  description = "ID do Node Group"
  value       = aws_eks_node_group.nodes.id
}