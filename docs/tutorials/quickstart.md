# Quick Start Guide

Get up and running with VMware VCF AWS EVS integration in under 30 minutes. This guide follows the official AWS EVS documentation and best practices.

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] **AWS Account** with EVS service enabled in your target region
- [ ] **AWS CLI** configured with appropriate permissions
- [ ] **Terraform** v1.0+ installed
- [ ] **Python** 3.8+ with pip
- [ ] **VMware vCenter** access (for migration scenarios)
- [ ] **Network connectivity** between your environment and AWS

## Step 1: Quick Installation

```bash
# Clone and setup
git clone https://github.com/uldyssian-sh/vmware-vcf-aws-evs.git
cd vmware-vcf-aws-evs

# Install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

## Step 2: Configure Environment

Create your configuration file:

```bash
cp config/config.example.yaml config/config.yaml
```

Edit `config/config.yaml` with your settings:

```yaml
# Minimal configuration for quick start
aws:
  region: us-west-2
  profile: default

evs:
  default_cluster_name: quickstart-evs
  default_instance_type: i3.metal
  default_node_count: 3

security:
  allowed_cidr_blocks:
    - 10.0.0.0/8

tags:
  Environment: development
  Project: evs-quickstart
```

## Step 3: Deploy Your First EVS Cluster

### Using Terraform (Recommended)

```bash
cd terraform/examples/basic

# Initialize Terraform
terraform init

# Create terraform.tfvars
cat > terraform.tfvars << EOF
aws_region = "us-west-2"
evs_cluster_name = "quickstart-evs"
evs_instance_type = "i3.metal"
evs_node_count = 3
environment = "development"
EOF

# Plan and apply
terraform plan
terraform apply
```

### Using CLI Tool

```bash
# Check EVS service status
vcf-evs status

# Create cluster
vcf-evs create \
  --name quickstart-evs \
  --instance-type i3.metal \
  --size 3 \
  --config config/config.yaml
```

## Step 4: Verify Deployment

### Check Cluster Status

```bash
# Using CLI
vcf-evs status --config config/config.yaml

# Using AWS CLI
aws evs describe-clusters --region us-west-2
```

### Access vCenter

Once the cluster is ready (typically 45-60 minutes):

1. **Get vCenter URL** from AWS Console or CLI:
   ```bash
   aws evs describe-cluster --cluster-id <cluster-id> --query 'Cluster.VcenterEndpoint'
   ```

2. **Access vCenter Web Client**:
   - URL: `https://<vcenter-endpoint>/ui`
   - Username: `cloudadmin@vmc.local`
   - Password: Retrieved from AWS Secrets Manager

3. **Verify Cluster Health**:
   - Check all ESXi hosts are connected
   - Verify vSAN datastore (if applicable)
   - Confirm network connectivity

## Step 5: Test Basic Operations

### Create a Test VM

Using the vCenter Web Client:

1. Right-click on the cluster → **New Virtual Machine**
2. Select **Create a new virtual machine**
3. Configure basic settings:
   - Name: `test-vm-01`
   - Guest OS: `Ubuntu Linux (64-bit)`
   - Storage: Default vSAN datastore
   - Network: Default VM network

### Test Network Connectivity

```bash
# Test connectivity to vCenter
curl -k https://<vcenter-endpoint>/ui

# Test SSH access to management network (if configured)
ssh -i <your-key> root@<esxi-host-ip>
```

## Step 6: Set Up Monitoring (Optional)

Enable basic monitoring:

```bash
# Deploy CloudWatch dashboard
cd scripts/monitoring
python setup_monitoring.py --cluster-name quickstart-evs
```

## Common Instance Types and Use Cases

Based on [AWS EVS documentation](https://docs.aws.amazon.com/pdfs/evs/latest/userguide/evs-ug.pdf):

| Instance Type | Best For | vCPU | Memory | Storage |
|---------------|----------|------|--------|---------|
| **i3.metal** | General workloads, development | 72 | 512 GB | 8x1.9TB NVMe |
| **i3en.metal** | Storage-intensive workloads | 96 | 768 GB | 8x7.5TB NVMe |
| **r5.metal** | Memory-intensive applications | 96 | 768 GB | EBS only |
| **m5.metal** | Balanced compute workloads | 96 | 384 GB | EBS only |

## Troubleshooting Quick Fixes

### Cluster Creation Fails

```bash
# Check AWS service limits
aws service-quotas get-service-quota \
  --service-code evs \
  --quota-code L-12345678

# Verify IAM permissions
aws sts get-caller-identity
aws iam simulate-principal-policy \
  --policy-source-arn $(aws sts get-caller-identity --query Arn --output text) \
  --action-names evs:CreateCluster \
  --resource-arns "*"
```

### Network Connectivity Issues

```bash
# Check security groups
aws ec2 describe-security-groups \
  --filters "Name=group-name,Values=*evs*"

# Verify VPC configuration
aws ec2 describe-vpcs
aws ec2 describe-subnets
```

### vCenter Access Problems

1. **Check cluster status**: Must be `ACTIVE`
2. **Verify security groups**: Port 443 must be open
3. **Check DNS resolution**: Use IP if DNS fails
4. **Validate credentials**: Check AWS Secrets Manager

## Cost Estimation

Approximate monthly costs for quick start configuration:

| Component | Quantity | Unit Cost | Monthly Cost |
|-----------|----------|-----------|--------------|
| i3.metal instances | 3 | $4.992/hour | ~$10,783 |
| EBS storage | 1TB | $0.10/GB | $100 |
| Data transfer | 100GB | $0.09/GB | $9 |
| **Total** | | | **~$10,892** |

> **Note**: Use [AWS Pricing Calculator](https://calculator.aws) for accurate estimates based on your usage patterns.

## Next Steps

Now that you have a running EVS cluster:

1. **[Migrate a VM](migration.md)** - Move your first workload from on-premises
2. **[Set up monitoring](monitoring.md)** - Implement comprehensive observability
3. **[Configure backup](backup.md)** - Protect your workloads
4. **[Review security](../architecture/security.md)** - Harden your environment

## Cleanup

To avoid ongoing charges:

```bash
# Using Terraform
cd terraform/examples/basic
terraform destroy

# Using CLI
vcf-evs delete --cluster-id <cluster-id>

# Verify cleanup
aws evs describe-clusters --region us-west-2
```

## Official Resources

- **[AWS EVS User Guide (PDF)](https://docs.aws.amazon.com/pdfs/evs/latest/userguide/evs-ug.pdf)** - Complete documentation
- **[Getting Started Guide](https://docs.aws.amazon.com/evs/latest/userguide/getting-started.html)** - Official AWS tutorial
- **[EVS FAQs](https://aws.amazon.com/evs/faqs/)** - Common questions and answers
- **[Re:Invent Deep Dive](https://reinvent.awsevents.com/content/dam/reinvent/2024/slides/mam/MAM237-NEW_Deep-dive-into-Amazon-Elastic-VMware-Service.pdf)** - Technical presentation