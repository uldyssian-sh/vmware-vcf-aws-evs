"""Logging utilities for VCF EVS integration."""

import logging
import sys
import os
from pathlib import Path
from typing import Optional


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """Set up logging configuration."""
    
    # Validate log level
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if level.upper() not in valid_levels:
        level = 'INFO'
    
    # Create logger
    logger = logging.getLogger("vcf_evs")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        # Sanitize log file path to prevent path traversal
        safe_log_file = _safe_log_path(log_file)
        file_handler = logging.FileHandler(safe_log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def _safe_log_path(log_file: str) -> str:
    """Sanitize log file path to prevent path traversal and command injection."""
    if not log_file or not isinstance(log_file, str):
        log_file = 'default.log'
    
    # Remove any shell metacharacters and path traversal attempts
    safe_name = os.path.basename(log_file)
    # Allow alphanumeric, dots, hyphens, underscores, and spaces
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '.-_ ')
    safe_name = safe_name.strip()
    
    # Prevent empty names
    if not safe_name:
        safe_name = 'default'
    
    # Ensure .log extension
    if not safe_name.endswith('.log'):
        safe_name += '.log'
    
    # Create logs directory if it doesn't exist
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    # Resolve path and ensure it's within logs directory
    full_path = logs_dir / safe_name
    resolved_path = full_path.resolve()
    
    # Security check: ensure resolved path is within logs directory
    try:
        resolved_path.relative_to(logs_dir.resolve())
    except ValueError:
        raise ValueError("Invalid log file path")
    
    return str(resolved_path)