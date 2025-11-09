variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-west-2"
}

variable "evs_cluster_name" {
  description = "Name of the EVS cluster"
  type        = string
  default     = "example-evs-cluster"
}

variable "evs_instance_type" {
  description = "Instance type for EVS nodes"
  type        = string
  default     = "i3.metal"
}

variable "evs_node_count" {
  description = "Number of nodes in the cluster"
  type        = number
  default     = 3
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access the cluster"
  type        = list(string)
  default     = ["10.0.0.0/8"]
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "development"
}# Updated 20251109_123825
