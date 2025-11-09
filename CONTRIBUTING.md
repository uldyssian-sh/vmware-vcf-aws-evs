# Contributing to VMware VCF AWS EVS Integration

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use issue templates** when available
3. **Provide detailed information**:
   - Environment details (OS, Python version, Terraform version)
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages and logs

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following our coding standards
4. **Test your changes** thoroughly
5. **Commit with clear messages**:
   ```bash
   git commit -m "feat: add EVS cluster scaling automation"
   ```
6. **Push to your fork** and **create a pull request**

## 📝 Coding Standards

### Python Code

- Follow **PEP 8** style guidelines
- Use **type hints** for function parameters and return values
- Write **docstrings** for all functions and classes
- Maximum line length: **88 characters** (Black formatter)
- Use **meaningful variable names**

Example:
```python
def create_evs_cluster(
    cluster_name: str,
    instance_type: str,
    cluster_size: int
) -> Dict[str, Any]:
    """
    Create an EVS cluster with specified configuration.

    Args:
        cluster_name: Name for the EVS cluster
        instance_type: EC2 instance type for cluster nodes
        cluster_size: Number of nodes in the cluster

    Returns:
        Dictionary containing cluster creation response

    Raises:
        EVSClusterError: If cluster creation fails
    """
    # Implementation here
    pass
```

### Terraform Code

- Use **consistent naming conventions**
- Add **descriptions** to all variables and outputs
- Use **locals** for computed values
- Follow **HCL formatting** standards
- Include **examples** for modules

Example:
```hcl
variable "evs_cluster_name" {
  description = "Name of the EVS cluster to create"
  type        = string
  validation {
    condition     = length(var.evs_cluster_name) > 0
    error_message = "EVS cluster name cannot be empty."
  }
}
```

### Documentation

- Use **clear, concise language**
- Include **code examples** where appropriate
- Update **README.md** if adding new features
- Add **inline comments** for complex logic
- Create **tutorials** for new workflows

## 🧪 Testing Requirements

### Before Submitting

1. **Run all tests**:
   ```bash
   python -m pytest tests/
   ```

2. **Check code formatting**:
   ```bash
   black --check .
   flake8 .
   ```

3. **Validate Terraform**:
   ```bash
   terraform fmt -check
   terraform validate
   ```

4. **Test documentation**:
   ```bash
   mkdocs serve
   ```

### Writing Tests

- **Unit tests** for all new functions
- **Integration tests** for workflows
- **Mock external dependencies** (AWS APIs, vCenter)
- Use **descriptive test names**
- Aim for **>80% code coverage**

Example:
```python
def test_create_evs_cluster_success():
    """Test successful EVS cluster creation."""
    # Arrange
    mock_client = Mock()
    mock_client.create_cluster.return_value = {"ClusterId": "cluster-123"}

    # Act
    result = create_evs_cluster("test-cluster", "i3.metal", 3)

    # Assert
    assert result["ClusterId"] == "cluster-123"
    mock_client.create_cluster.assert_called_once()
```

## 🏗️ Development Setup

### Local Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/uldyssian-sh/vmware-vcf-aws-evs.git
   cd vmware-vcf-aws-evs
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

### Development Tools

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing framework
- **Pre-commit**: Git hooks

## 📋 Pull Request Guidelines

### PR Checklist

- [ ] **Descriptive title** and detailed description
- [ ] **Tests added/updated** for new functionality
- [ ] **No merge conflicts** with main branch
- [ ] **All CI checks passing**
- [ ] **Follows coding standards**

### PR Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Documentation
- [ ] README updated
- [ ] API docs updated
- [ ] Tutorial created/updated
```

## 🔒 Security Guidelines

- **Never commit secrets** or credentials
- **Use environment variables** for configuration
- **Follow AWS security best practices**
- **Validate all inputs** in functions
- **Use IAM roles** instead of access keys
- **Report security issues** privately

## 📞 Getting Help

- **GitHub Discussions**: General questions and ideas
- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Check existing docs first
- **Code Review**: Ask for feedback on complex changes

## 🎯 Contribution Areas

We welcome contributions in these areas:

### High Priority
- **Bug fixes** and stability improvements
- **Performance optimizations**
- **Security enhancements**
- **Documentation improvements**

### Medium Priority
- **New automation scripts**
- **Additional Terraform modules**
- **Monitoring enhancements**
- **Test coverage improvements**

### Low Priority
- **Code refactoring**
- **UI/UX improvements**
- **Additional examples**
- **Translation support**

## 🏆 Recognition

Contributors will be recognized in:
- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page

Thank you for helping make this project better! 🚀