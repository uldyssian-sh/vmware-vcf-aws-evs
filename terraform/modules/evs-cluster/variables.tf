variable "cluster_name" {
  description = "Name of the EVS cluster"
  type        = string
  validation {
    condition     = length(var.cluster_name) > 0 && length(var.cluster_name) <= 63
    error_message = "Cluster name must be between 1 and 63 characters."
  }
}

variable "instance_type" {
  description = "EC2 instance type for EVS nodes"
  type        = string
  default     = "i3.metal"
  validation {
    condition = contains([
      "i3.metal", "i3en.metal", "r5.metal", "r5d.metal", "m5.metal", "m5d.metal"
    ], var.instance_type)
    error_message = "Instance type must be a supported metal instance type."
  }
}

variable "node_count" {
  description = "Number of nodes in the EVS cluster"
  type        = number
  default     = 3
  validation {
    condition     = var.node_count >= 3 && var.node_count <= 16
    error_message = "Node count must be between 3 and 16."
  }
}

variable "vpc_id" {
  description = "VPC ID where the cluster will be deployed"
  type        = string
  default     = null
}

variable "subnet_ids" {
  description = "List of subnet IDs for the cluster"
  type        = list(string)
  default     = null
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access the cluster"
  type        = list(string)
  default     = ["10.0.0.0/8"]
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 30
}

variable "tags" {
  description = "Additional tags for resources"
  type        = map(string)
  default     = {}
}