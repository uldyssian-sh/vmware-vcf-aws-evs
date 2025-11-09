"""Setup configuration for VMware VCF AWS EVS Integration."""

from setuptools import setup, find_packages

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "VMware VCF AWS EVS Integration Toolkit"

try:
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
except FileNotFoundError:
    requirements = []

setup(
    name="vmware-vcf-aws-evs",
    version="1.0.0",
    author="VMware VCF EVS Team",
    author_email="25517637+uldyssian-sh@users.noreply.github.com",
    description="VMware Cloud Foundation AWS EVS Integration Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uldyssian-sh/vmware-vcf-aws-evs",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Systems Administration",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.12.0",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "vcf-evs=vcf_evs.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)# Updated Sun Nov  9 12:49:45 CET 2025
