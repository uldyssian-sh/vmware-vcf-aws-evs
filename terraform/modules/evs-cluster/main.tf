terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}



data "aws_vpc" "default" {
  count   = var.vpc_id == null ? 1 : 0
  default = true
}

locals {
  vpc_id = var.vpc_id != null ? var.vpc_id : data.aws_vpc.default[0].id
  
  common_tags = merge(var.tags, {
    Name        = var.cluster_name
    Environment = var.environment
    ManagedBy   = "terraform"
  })
}

resource "aws_security_group" "evs_cluster" {
  name_prefix = "${var.cluster_name}-evs-"
  vpc_id      = local.vpc_id
  description = "Security group for EVS cluster ${var.cluster_name}"

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
    description = "HTTPS for vCenter"
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
    description = "SSH access"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound traffic"
  }

  tags = merge(local.common_tags, {
    Name = "${var.cluster_name}-evs-sg"
  })
}

resource "aws_kms_key" "evs_logs" {
  description             = "KMS key for EVS cluster logs encryption"
  deletion_window_in_days = 30
  
  tags = merge(local.common_tags, {
    Name = "${var.cluster_name}-logs-key"
  })
}

resource "aws_kms_alias" "evs_logs" {
  name          = "alias/${var.cluster_name}-evs-logs"
  target_key_id = aws_kms_key.evs_logs.key_id
}

resource "aws_cloudwatch_log_group" "evs_cluster" {
  name              = "/aws/evs/${var.cluster_name}"
  retention_in_days = var.log_retention_days
  kms_key_id        = aws_kms_key.evs_logs.arn
  
  tags = merge(local.common_tags, {
    Name = "${var.cluster_name}-logs"
  })
}

# Placeholder for EVS cluster (would be actual EVS resource when available)
resource "null_resource" "evs_cluster_placeholder" {
  triggers = {
    cluster_name = var.cluster_name
    instance_type = var.instance_type
    node_count = var.node_count
  }
  
  provisioner "local-exec" {
    command = "echo 'EVS cluster ${var.cluster_name} would be created here'"
  }
