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
  validation {
    condition     = var.vpc_id == null || can(regex("^vpc-[0-9a-f]{8,17}$", var.vpc_id))
    error_message = "VPC ID must be a valid AWS VPC ID format (vpc-xxxxxxxx)."
  }
}

variable "subnet_ids" {
  description = "List of subnet IDs for the cluster"
  type        = list(string)
  default     = null
  validation {
    condition = var.subnet_ids == null || (
      length(var.subnet_ids) >= 1 && 
      alltrue([for s in var.subnet_ids : can(regex("^subnet-[0-9a-f]{8,17}$", s))])
    )
    error_message = "Subnet IDs must be valid AWS subnet ID format (subnet-xxxxxxxx)."
  }
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access the cluster"
  type        = list(string)
  default     = ["10.0.0.0/16"]
  
  validation {
    condition = alltrue([
      for cidr in var.allowed_cidr_blocks :
      can(cidrhost(cidr, 0))
    ])
    error_message = "All CIDR blocks must be valid IPv4 CIDR notation."
  }
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
}# Updated 20251109_123825
# Updated Sun Nov  9 12:52:32 CET 2025
# Updated Sun Nov  9 12:56:17 CET 2025
