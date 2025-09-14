"""Configuration management utilities."""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """Configuration manager for VCF EVS integration."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager."""
        self.config_path = config_path or "config/config.yaml"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        config_file = Path(self.config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Override with environment variables
        config = self._apply_env_overrides(config)
        
        return config
    
    def _apply_env_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides."""
        # AWS configuration
        if os.getenv('AWS_REGION'):
            config.setdefault('aws', {})['region'] = os.getenv('AWS_REGION')
        
        if os.getenv('AWS_PROFILE'):
            config.setdefault('aws', {})['profile'] = os.getenv('AWS_PROFILE')
        
        # VMware configuration
        if os.getenv('VCENTER_SERVER'):
            config.setdefault('vmware', {})['vcenter_server'] = os.getenv('VCENTER_SERVER')
        
        if os.getenv('VCENTER_USERNAME'):
            config.setdefault('vmware', {})['username'] = os.getenv('VCENTER_USERNAME')
        
        if os.getenv('VCENTER_PASSWORD'):
            config.setdefault('vmware', {})['password'] = os.getenv('VCENTER_PASSWORD')
        
        # EVS configuration
        if os.getenv('EVS_CLUSTER_NAME'):
            config.setdefault('evs', {})['default_cluster_name'] = os.getenv('EVS_CLUSTER_NAME')
        
        return config
    
    def get_aws_config(self) -> Dict[str, Any]:
        """Get AWS configuration."""
        return self.config.get('aws', {})
    
    def get_vmware_config(self) -> Dict[str, Any]:
        """Get VMware configuration."""
        return self.config.get('vmware', {})
    
    def get_evs_config(self) -> Dict[str, Any]:
        """Get EVS configuration."""
        return self.config.get('evs', {})
    
    def get_security_config(self) -> Dict[str, Any]:
        """Get security configuration."""
        return self.config.get('security', {})
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """Get monitoring configuration."""
        return self.config.get('monitoring', {})
    
    def get_migration_config(self) -> Dict[str, Any]:
        """Get migration configuration."""
        return self.config.get('migration', {})
    
    def get_tags(self) -> Dict[str, str]:
        """Get resource tags."""
        return self.config.get('tags', {})