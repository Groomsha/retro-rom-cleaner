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
        """Ініціалізація перейменувача файлів"""

        self.roms_dir = roms_dir
        self.imgs_dir = imgs_dir
        self.log_file = log_file