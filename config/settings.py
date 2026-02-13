"""
Settings configuration
"""

from typing import Dict, Any, Optional
import os

try:
    import yaml
except ImportError:
    yaml = None


class Settings:
    """Application settings"""

    # Default settings
    DEFAULT_SETTINGS = {
        "log_format": "standard",
        "anomaly_threshold": 2.0,
        "error_rate_threshold": 10.0,
        "chunk_size": 100,
        "report_format": "json",
        "openai": {
            "enabled": True,
            "model": "gpt-3.5-turbo",
            "max_tokens": 500,
            "temperature": 0.3,
        },
        "detection": {
            "error_spike_enabled": True,
            "pattern_anomaly_enabled": True,
            "timing_anomaly_enabled": True,
        },
    }

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize settings
        
        Args:
            config_file: Path to YAML configuration file
        """
        self.settings = self.DEFAULT_SETTINGS.copy()
        
        if config_file and os.path.exists(config_file):
            self._load_from_file(config_file)

    def _load_from_file(self, file_path: str) -> None:
        """Load settings from YAML file"""
        if yaml is None:
            print("Warning: PyYAML not installed. Using default settings.")
            return
        
        try:
            with open(file_path, 'r') as f:
                custom_settings = yaml.safe_load(f) or {}
                self._merge_settings(custom_settings)
        except Exception as e:
            print(f"Warning: Could not load config file {file_path}: {e}")

    def _merge_settings(self, custom: Dict[str, Any]) -> None:
        """Merge custom settings with defaults"""
        for key, value in custom.items():
            if isinstance(value, dict) and key in self.settings:
                self.settings[key].update(value)
            else:
                self.settings[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        keys = key.split(".")
        value = self.settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value

    def to_dict(self) -> Dict[str, Any]:
        """Get all settings as dictionary"""
        return self.settings.copy()
