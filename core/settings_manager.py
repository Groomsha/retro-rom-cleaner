"""
Module: settings_manager
Description: JSON settings manager for application configuration.

Author: Ihor Cheberiak (Groomsha) (c) 2025
Project: RetroROMCleaner
"""

# Built-in imports
import json
import os
from typing import Dict, Any, Optional

# Third-party imports

# Project imports


class SettingsManager:
    """Клас для управління налаштуваннями"""

    DEFAULT_CONFIG = {
        "ROMS_DIR": "",
        "IMGS_DIR": "",
        "IGNORE_CASE": True,
        "USE_HASH": True,
        "LANGUAGE": "en",
        "THEME": "Dark",
    }

    def __init__(self, config_file: str = "config.json"):
        """Ініціалізація менеджера налаштувань"""

        self.config_file = config_file

    def load_config(self) -> Dict[str, Any]:
        """Завантаження конфігурації з файлу"""

        if not os.path.exists(self.config_file):
            return self.DEFAULT_CONFIG.copy()

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                # Merge with defaults for missing keys
                for key, value in self.DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
        except (json.JSONDecodeError, FileNotFoundError):
            return self.DEFAULT_CONFIG.copy()

    def save_config(self, config: Dict[str, Any]):
        """Збереження конфігурації у файл"""

        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)