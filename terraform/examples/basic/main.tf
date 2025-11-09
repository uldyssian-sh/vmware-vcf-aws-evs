terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "evs_cluster" {
  source = "../../modules/evs-cluster"

  cluster_name         = var.evs_cluster_name
  instance_type        = var.evs_instance_type
  node_count          = var.evs_node_count
  allowed_cidr_blocks = var.allowed_cidr_blocks
  environment         = var.environment

  tags = {
    Project     = "vcf-evs-integration"
    Owner       = "infrastructure-team"
    CostCenter  = "engineering"
  }
