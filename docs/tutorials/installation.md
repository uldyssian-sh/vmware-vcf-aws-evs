# Installation Guide

This guide will walk you through installing and configuring the VMware VCF AWS EVS Integration toolkit.

## Prerequisites

Before you begin, ensure you have the following:

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: Version 3.8 or higher
- **Terraform**: Version 1.0 or higher
- **AWS CLI**: Version 2.0 or higher
- **Git**: For cloning the repository

### Access Requirements

- **AWS Account** with EVS service enabled
- **VMware vCenter** access with administrative privileges
- **Network connectivity** between your environment and AWS

## Step 1: Clone the Repository

```bash
git clone https://github.com/uldyssian-sh/vmware-vcf-aws-evs.git
cd vmware-vcf-aws-evs
```

## Step 2: Set Up Python Environment

### Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# For development (optional)
pip install -r requirements-dev.txt
```

### Install the Package

```bash
# Install in development mode
pip install -e .

# Or install from PyPI (when available)
pip install vmware-vcf-aws-evs
```

## Step 3: Configure AWS CLI

```bash
# Configure AWS CLI with your credentials
aws configure

# Verify configuration
aws sts get-caller-identity
```

## Step 4: Set Up Configuration

### Create Configuration File

```bash
# Copy example configuration
cp config/config.example.yaml config/config.yaml
```

### Edit Configuration

Edit `config/config.yaml` with your environment details:

```yaml
# AWS Configuration
aws:
  region: us-west-2
  profile: default

# VMware Configuration
vmware:
  vcenter_server: <your-vcenter-server>
  username: <username>
  # Note: Use environment variables for sensitive data

# EVS Configuration
evs:
  default_cluster_name: production-cluster
  default_instance_type: i3.metal
  default_node_count: 3

# Network Configuration
network:
  vpc_cidr: 10.0.0.0/16
  allowed_cidrs:
    - 10.0.0.0/8
    - 192.168.0.0/16

# Logging
logging:
  level: INFO
  file: logs/vcf-evs.log
```

### Set Environment Variables

Create a `.env` file for sensitive information:

```bash
# AWS Configuration
AWS_REGION=us-west-2
AWS_PROFILE=default

# VMware Configuration
VCENTER_SERVER=<your-vcenter-server>
VCENTER_USERNAME=<username>
VCENTER_PASSWORD=<password>

# EVS Configuration
EVS_CLUSTER_NAME=<cluster-name>
```

**Important**: Never commit the `.env` file to version control.

## Step 5: Initialize Terraform

```bash
cd terraform/examples/basic
terraform init
```

### Configure Terraform Variables

Create `terraform.tfvars`:

```hcl
# AWS Settings
aws_region = "us-west-2"

# EVS Configuration
evs_cluster_name = "my-evs-cluster"
evs_instance_type = "i3.metal"
evs_node_count = 3

# Network Configuration
allowed_cidr_blocks = ["10.0.0.0/8"]

# Environment
environment = "production"
```

## Step 6: Verify Installation

### Test CLI Tool

```bash
# Check version
vcf-evs --version

# Test configuration
vcf-evs status --config config/config.yaml
```

### Test Python Import

```python
from vcf_evs import EVSClient, VCenterClient, ConfigManager

# Test configuration loading
config = ConfigManager("config/config.yaml")
print("Configuration loaded successfully")
```

### Validate Terraform

```bash
cd terraform/examples/basic
terraform validate
terraform plan
```

## Step 7: Run Tests

```bash
# Run unit tests
python -m pytest tests/unit/ -v

# Run integration tests (requires AWS access)
python -m pytest tests/integration/ -v

# Run all tests with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Step 8: Set Up Development Tools (Optional)

If you plan to contribute to the project:

```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files
```

## Troubleshooting

### Common Issues

#### Python Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall package
pip install -e .
```

#### AWS Authentication Issues

```bash
# Check AWS credentials
aws sts get-caller-identity

# Verify region configuration
aws configure get region
```

#### Terraform Issues

```bash
# Reinitialize Terraform
rm -rf .terraform
terraform init

# Check provider versions
terraform version
```

#### VMware Connection Issues

- Verify vCenter server URL and credentials
- Check network connectivity to vCenter
- Ensure user has required permissions

### Getting Help

- Check the [troubleshooting guide](../troubleshooting.md)
- Review [GitHub Issues](https://github.com/uldyssian-sh/vmware-vcf-aws-evs/issues)
- Join [GitHub Discussions](https://github.com/uldyssian-sh/vmware-vcf-aws-evs/discussions)

## Next Steps

After successful installation:

1. Follow the [Migration Tutorial](migration.md) to migrate your first VM
2. Set up [Monitoring](monitoring.md) for your EVS clusters
3. Review [Best Practices](../best-practices.md) for production deployments

## Uninstallation

To remove the toolkit:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Remove configuration files (optional)
rm -rf config/config.yaml .env

# Remove Terraform state (if applicable)
cd terraform/examples/basic
terraform destroy
```