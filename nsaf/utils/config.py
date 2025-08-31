"""
Configuration management for NSAF
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class NSAFConfig:
    """NSAF Configuration Manager"""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration manager"""
        self.config_file = config_file or "nsaf_config.yaml"
        self.config = self._load_default_config()
        self._load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            'scanner': {
                'timeout': 3,
                'max_threads': 100,
                'default_ports': '1-1000',
                'discovery_method': 'ping'
            },
            'vulnerability_scanner': {
                'timeout': 10,
                'enable_ssl_checks': True,
                'enable_web_checks': True,
                'enable_service_detection': True
            },
            'reporting': {
                'default_format': 'html',
                'output_directory': 'reports',
                'template_directory': 'templates',
                'include_recommendations': True
            },
            'logging': {
                'level': 'INFO',
                'log_directory': 'logs',
                'max_log_files': 10
            },
            'targets': {
                'exclude_hosts': [],
                'exclude_ports': [],
                'include_private_ranges': True
            }
        }
    
    def _load_config(self) -> None:
        """Load configuration from file"""
        config_path = Path(self.config_file)
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    if config_path.suffix.lower() == '.yaml' or config_path.suffix.lower() == '.yml':
                        file_config = yaml.safe_load(f)
                    else:
                        file_config = json.load(f)
                
                # Merge with default config
                self._merge_config(self.config, file_config)
                
            except Exception as e:
                print(f"Error loading config file {config_path}: {e}")
    
    def _merge_config(self, default: Dict[str, Any], override: Dict[str, Any]) -> None:
        """Recursively merge configuration dictionaries"""
        for key, value in override.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self._merge_config(default[key], value)
            else:
                default[key] = value
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any) -> None:
        """Set configuration value using dot notation"""
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def save(self, filename: Optional[str] = None) -> None:
        """Save configuration to file"""
        save_path = filename or self.config_file
        
        with open(save_path, 'w') as f:
            if Path(save_path).suffix.lower() in ['.yaml', '.yml']:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            else:
                json.dump(self.config, f, indent=2)
    
    def create_sample_config(self, filename: str = "nsaf_config.yaml") -> None:
        """Create a sample configuration file"""
        sample_config = {
            'scanner': {
                'timeout': 3,
                'max_threads': 100,
                'default_ports': '1-1000',
                'discovery_method': 'ping'
            },
            'vulnerability_scanner': {
                'timeout': 10,
                'enable_ssl_checks': True,
                'enable_web_checks': True,
                'enable_service_detection': True
            },
            'reporting': {
                'default_format': 'html',
                'output_directory': 'reports',
                'template_directory': 'templates',
                'include_recommendations': True
            },
            'logging': {
                'level': 'INFO',
                'log_directory': 'logs',
                'max_log_files': 10
            },
            'targets': {
                'exclude_hosts': ['192.168.1.1'],
                'exclude_ports': [22, 3389],
                'include_private_ranges': True
            }
        }
        
        with open(filename, 'w') as f:
            yaml.dump(sample_config, f, default_flow_style=False, indent=2)
        
        print(f"Sample configuration created: {filename}")

# Global configuration instance
config = NSAFConfig()
