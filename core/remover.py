"""
Module: remover
Description: File remover for ROM files and associated images.

Author: Ihor Cheberiak (Groomsha) (c) 2025
Project: RetroROMCleaner
"""

# Built-in imports
import os
import shutil
from typing import List, Optional

# Third-party imports

# Project imports


class FileRemover:
    """Клас для видалення файлів та пов'язаних ресурсів"""

    def __init__(self, roms_dir: str, imgs_dir: Optional[str] = None, log_file: str = "deleted_log.txt"):
        """Ініціалізація видаляча файлів"""

        self.roms_dir = roms_dir
        self.imgs_dir = imgs_dir
        self.log_file = log_file