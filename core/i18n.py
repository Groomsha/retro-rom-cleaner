"""
Module: i18n
Description: Internationalization and localization support.

Author: Ihor Cheberiak (Groomsha) (c) 2025
Project: RetroROMCleaner
"""

# Built-in imports
import json
import os
from typing import Dict, Any

# Third-party imports

# Project imports


class LanguageManager:
    """Клас для управління мовами інтерфейсу"""

    def __init__(self, languages_dir: str = "languages"):
        """Ініціалізація менеджера мов"""

        self.languages_dir = languages_dir
        self.languages: Dict[str, Dict[str, str]] = {}
        self.load_languages()

    def load_languages(self):
        """Завантаження всіх доступних мов"""

        if not os.path.exists(self.languages_dir):
            return

        for filename in os.listdir(self.languages_dir):
            if filename.endswith('.json'):
                lang_code = filename[:-5]  # Remove .json extension
                filepath = os.path.join(self.languages_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.languages[lang_code] = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    continue

    def get_language(self, lang_code: str) -> Dict[str, str]:
        """Отримання словника для конкретної мови"""

        return self.languages.get(lang_code, self.languages.get('en', {}))

    def get_available_languages(self) -> list[str]:
        """Отримання списку доступних мов"""

        return list(self.languages.keys())