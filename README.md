# VMware Cloud Foundation AWS EVS Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=flat&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![VMware](https://img.shields.io/badge/VMware-607078?style=flat&logo=vmware&logoColor=white)](https://www.vmware.com/)

A comprehensive toolkit for integrating VMware Cloud Foundation (VCF) with Amazon Elastic VMware Service (EVS), providing automation scripts, Terraform modules, and detailed documentation for seamless hybrid cloud operations.

**Author**: LT - [GitHub Profile](https://github.com/uldyssian-sh)

> **Based on official AWS documentation**: This toolkit implements best practices from the [AWS EVS User Guide](https://docs.aws.amazon.com/pdfs/evs/latest/userguide/evs-ug.pdf) and [Re:Invent 2024 Deep Dive](https://reinvent.awsevents.com/content/dam/reinvent/2024/slides/mam/MAM237-NEW_Deep-dive-into-Amazon-Elastic-VMware-Service.pdf).

## 🚀 Features

- **Automated Deployment**: Complete infrastructure as code using Terraform
- **Migration Tools**: Scripts for workload migration between on-premises VCF and AWS EVS
- **Monitoring & Observability**: CloudWatch integration and custom dashboards
- **Security Best Practices**: IAM roles, security groups, and encryption configurations
- **Cost Optimization**: Resource tagging and cost monitoring tools
- **Disaster Recovery**: Automated backup and recovery procedures

## 📋 Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform >= 1.0
- Python 3.8+
- VMware vSphere PowerCLI
- Valid AWS account with EVS service enabled
- VMware Cloud Foundation environment

## 🛠️ Quick Start

Get running in under 30 minutes following AWS best practices:

```bash
# 1. Clone and setup
git clone https://github.com/uldyssian-sh/vmware-vcf-aws-evs.git
cd vmware-vcf-aws-evs
pip install -r requirements.txt

# 2. Configure (edit with your settings)
cp config/config.example.yaml config/config.yaml

# 3. Deploy your first EVS cluster
cd terraform/examples/basic
terraform init && terraform apply

# 4. Verify deployment
vcf-evs status --config ../../config/config.yaml
```

> **💡 Tip**: See the [Quick Start Guide](docs/tutorials/quickstart.md) for detailed instructions and troubleshooting.

## 📁 Project Structure

```
vmware-vcf-aws-evs/
├── docs/                    # Comprehensive documentation
│   ├── architecture/        # Architecture diagrams and designs
│   ├── tutorials/          # Step-by-step guides
│   └── api/               # API documentation
├── terraform/              # Infrastructure as Code
│   ├── modules/           # Reusable Terraform modules
│   ├── environments/      # Environment-specific configurations
│   └── examples/         # Example deployments
├── scripts/               # Automation scripts
│   ├── migration/        # Migration utilities
│   ├── monitoring/       # Monitoring setup
│   └── backup/          # Backup and recovery
├── config/               # Configuration templates
├── tests/               # Automated tests
└── wiki/               # Additional documentation
```

## 🔧 Supported EVS Instance Types

Based on [AWS EVS documentation](https://docs.aws.amazon.com/pdfs/evs/latest/userguide/evs-ug.pdf):

| Instance Type | vCPU | Memory | Storage | Best For |
|---------------|------|--------|---------|----------|
| **i3.metal** | 72 | 512 GB | 8×1.9TB NVMe | General workloads |
| **i3en.metal** | 96 | 768 GB | 8×7.5TB NVMe | Storage-intensive |
| **r5.metal** | 96 | 768 GB | EBS only | Memory-intensive |
| **m5.metal** | 96 | 384 GB | EBS only | Balanced compute |

### Configuration Example

```yaml
# config/config.yaml
aws:
  region: us-west-2
  profile: default

evs:
  default_cluster_name: production-evs
  default_instance_type: i3.metal  # See table above
  default_node_count: 3

security:
  allowed_cidr_blocks:
    - 10.0.0.0/8
```

## 📚 Documentation

### Official AWS Resources
- **[AWS EVS User Guide (PDF)](https://docs.aws.amazon.com/pdfs/evs/latest/userguide/evs-ug.pdf)** - Complete EVS documentation
- **[Getting Started Guide](https://docs.aws.amazon.com/evs/latest/userguide/getting-started.html)** - Official AWS tutorial
- **[EVS FAQs](https://aws.amazon.com/evs/faqs/)** - Frequently asked questions
- **[Re:Invent 2024 Deep Dive](https://reinvent.awsevents.com/content/dam/reinvent/2024/slides/mam/MAM237-NEW_Deep-dive-into-Amazon-Elastic-VMware-Service.pdf)** - Technical presentation

### Toolkit Documentation
- [Architecture Overview](docs/architecture/overview.md)
- [Quick Start Guide](docs/tutorials/quickstart.md)
- [Installation Guide](docs/tutorials/installation.md)
- [Migration Tutorial](docs/tutorials/migration.md)
- [Monitoring Setup](docs/tutorials/monitoring.md)
- [API Reference](docs/api/README.md)

## 🧪 Testing

Run the test suite:

```bash
# Unit tests
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/

# Terraform validation
cd terraform/
terraform validate
terraform fmt -check
```

## 🔒 Security

- All sensitive data is managed through AWS Secrets Manager
- IAM roles follow principle of least privilege
- Network security groups restrict access appropriately
- Encryption at rest and in transit is enabled by default

## 📊 Monitoring

The solution includes:

- CloudWatch dashboards for EVS metrics
- Custom alarms for critical thresholds
- Log aggregation and analysis
- Performance monitoring tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and development process.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 [Documentation](https://github.com/uldyssian-sh/vmware-vcf-aws-evs/wiki)
- 🐛 [Issue Tracker](https://github.com/uldyssian-sh/vmware-vcf-aws-evs/issues)
- 💬 [Discussions](https://github.com/uldyssian-sh/vmware-vcf-aws-evs/discussions)

## 🙏 Acknowledgments

- AWS EVS Team for comprehensive documentation
- VMware Cloud Foundation community
- Open source contributors

---

**Note**: This project is not officially affiliated with AWS or VMware.
It's a community-driven initiative to simplify VCF-EVS integration.
## 📦 Documentation Notice

Large PDF documentation files are available in the [Releases](https://github.com/uldyssian-sh/vmware-vcf-aws-evs/releases) section 
to keep the repository lightweight and fast to clone.


