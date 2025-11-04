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

    def __init__(self, config_file: str = "config.json"):
        """Ініціалізація менеджера налаштувань

        Args:
            config_file: Шлях до файлу конфігурації
        """
        self.config_file = config_file