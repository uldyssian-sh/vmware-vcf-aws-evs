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
        return str(Path('logs') / 'default.log')
    
    # Remove any shell metacharacters and path traversal attempts
    safe_name = os.path.basename(log_file)
    # Allow only alphanumeric, dots, hyphens, and underscores
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '.-_')
    safe_name = safe_name.strip('.')
    
    # Prevent empty names and ensure valid filename
    if not safe_name or len(safe_name) < 1:
        safe_name = 'default'
    
    # Limit filename length
    if len(safe_name) > 100:
        safe_name = safe_name[:100]
    
    # Ensure .log extension
    if not safe_name.endswith('.log'):
        safe_name += '.log'
    
    # Create logs directory if it doesn't exist
    logs_dir = Path('logs')
    logs_dir.mkdir(mode=0o755, exist_ok=True)
    
    # Create safe path within logs directory
    safe_path = logs_dir / safe_name
    
    # Additional security validation
    if '..' in str(safe_path) or str(safe_path).startswith('/'):
        raise ValueError("Invalid log file path detected")
    
    return str(safe_path)# Updated Sun Nov  9 12:49:45 CET 2025
# Updated Sun Nov  9 12:52:32 CET 2025
# Updated Sun Nov  9 12:56:17 CET 2025
