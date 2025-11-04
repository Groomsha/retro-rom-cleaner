"""
Модуль: utils.file_operations
Опис: Операції з файлами для проекту RetroROMCleaner.

Автор: Ihor Cheberiak (Groomsha) (c) 2025
Project: RetroROMCleaner
"""

# Built-in imports
import os
import re
from typing import List

# Third-party imports

# Project imports


class FileOperations:
    """Клас для операцій з файлами."""

    @staticmethod
    def normalize_name(filename: str) -> str:
        """
        Нормалізувати ім'я файлу: видалити спеціальні символи, дужки, кілька пробілів.
        Вихід у нижньому регістрі для відповідності без урахування регістру.
        """
        
        name, _ = os.path.splitext(filename)
        cleaned = re.sub(r"[^a-zA-Z0-9\\s_-]", "", name)
        cleaned = re.sub(r"\\s+", " ", cleaned)
        return cleaned.strip().lower()

    @staticmethod
    def safe_list_files(root_dir: str) -> List[str]:
        """
        Повернути всі шляхи до файлів усередині заданого каталогу.
        Пропускає каталоги або записи з відмовами в доступі.
        """
        
        file_paths = []
        for root, _, files in os.walk(root_dir):
            for name in files:
                full_path = os.path.join(root, name)
                if os.path.isfile(full_path):
                    file_paths.append(full_path)
        return file_paths