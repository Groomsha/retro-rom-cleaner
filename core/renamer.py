"""
Module: renamer
Description: File renamer for ROM files and associated images.

Author: Ihor Cheberiak (Groomsha) (c) 2025
Project: RetroROMCleaner
"""

# Built-in imports
import os
import re
from typing import List, Optional

# Third-party imports

# Project imports


class FileRenamer:
    """Клас для перейменування файлів"""

    def __init__(self, roms_dir: str, imgs_dir: Optional[str] = None, log_file: str = "renamed_log.txt"):
        """Ініціалізація перейменувача файлів

        Args:
            roms_dir: Шлях до директорії з ROM-файлами
            imgs_dir: Шлях до директорії з зображеннями (опціонально)
            log_file: Шлях до файлу логу перейменувань
        """
        self.roms_dir = roms_dir
        self.imgs_dir = imgs_dir
        self.log_file = log_file