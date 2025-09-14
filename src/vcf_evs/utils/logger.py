"""Logging utilities for VCF EVS integration."""

import logging
import sys
import os
from pathlib import Path
from typing import Optional


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """Set up logging configuration."""
    
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
    # Remove any shell metacharacters and path traversal attempts
    safe_name = os.path.basename(log_file)
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '.-_')
    
    # Ensure .log extension
    if not safe_name.endswith('.log'):
        safe_name += '.log'
    
    # Create logs directory if it doesn't exist
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    return str(logs_dir / safe_name)