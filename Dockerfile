# Multi-stage build for production-ready container
FROM python:3.11-slim as builder

# Set build arguments
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

# Add metadata
LABEL maintainer="25517637+uldyssian-sh@users.noreply.github.com" \
      org.opencontainers.image.title="VMware VCF AWS EVS Integration" \
      org.opencontainers.image.description="VMware Cloud Foundation AWS EVS Integration Toolkit" \
      org.opencontainers.image.version="${VERSION:-1.0.1}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.source="https://github.com/uldyssian-sh/vmware-vcf-aws-evs" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.vendor="uldyssian-sh"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Create non-root user
RUN groupadd -r vcfevs && useradd -r -g vcfevs -s /bin/bash vcfevs

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/
COPY setup.py pyproject.toml ./

# Install the application
RUN pip install --no-cache-dir -e .

# Create directories and set permissions
RUN mkdir -p /app/logs /app/data && \
    chown -R vcfevs:vcfevs /app

# Switch to non-root user
USER vcfevs

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import vcf_evs; print('OK')" || exit 1

# Set environment variables
ENV PYTHONPATH=/app/src \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose port (if needed)
EXPOSE 8080

# Default command
