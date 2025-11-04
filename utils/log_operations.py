"""
Модуль: utils.log_operations
Опис: Операції з логуванням для проекту RetroROMCleaner.

Автор: Ihor Cheberiak (Groomsha) (c) 2025
Project: RetroROMCleaner
"""

# Built-in imports
import os

# Third-party imports

# Project imports


class LogOperations:
    """Клас для операцій з логуванням."""

    @staticmethod
    def write_log(file_path: str, text: str):
        """Додати текст до файлу логу."""
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(text + "\\n")