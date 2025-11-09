output "cluster_name" {
  description = "Name of the EVS cluster"
  value       = var.cluster_name
}

output "security_group_id" {
  description = "ID of the security group created for the cluster"
  value       = aws_security_group.evs_cluster.id
}

output "log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.evs_cluster.name
}

output "log_group_arn" {
  description = "ARN of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.evs_cluster.arn
}

output "vpc_id" {
  description = "VPC ID where the cluster is deployed"
  value       = local.vpc_id
}

output "tags" {
  description = "Tags applied to the cluster resources"
  value       = local.common_tags
}

output "cluster_placeholder_id" {
  description = "Placeholder for EVS cluster ID"
  value       = null_resource.evs_cluster_placeholder.id
}# Updated 20251109_123825
# Updated Sun Nov  9 12:52:32 CET 2025
# Updated Sun Nov  9 12:56:17 CET 2025
