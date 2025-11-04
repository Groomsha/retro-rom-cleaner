"""
Модуль: utils.hash_operations
Опис: Операції з хешуванням для проекту RetroROMCleaner.

Автор: Ihor Cheberiak (Groomsha) (c) 2025
Project: RetroROMCleaner
"""

# Built-in imports
import hashlib

# Third-party imports

# Project imports


class HashOperations:
    """Клас для операцій з хешуванням."""

    @staticmethod
    def get_md5(path: str) -> str:
        """Обчислити MD5 хеш для файлу. Повертає порожній рядок, якщо файл недоступний."""
        
        try:
            with open(path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""