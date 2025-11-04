"""
Module: finder
Description: Duplicate ROM file finder with MD5 hashing support.

Author: Ihor Cheberiak (Groomsha) (c) 2025
Project: RetroROMCleaner
"""

# Built-in imports
import os
import hashlib
from typing import Dict, List, Set, Optional

# Third-party imports

# Project imports


class DuplicateFinder:
    """Клас для пошуку дублікатів ROM-файлів"""

    def __init__(self, roms_dir: str, ignore_case: bool = True, use_hash: bool = True):
        """Ініціалізація пошукача дублікатів

        Args:
            roms_dir: Шлях до директорії з ROM-файлами
            ignore_case: Ігнорувати регістр при порівнянні
            use_hash: Використовувати MD5-хеш для порівняння
        """
        self.roms_dir = roms_dir
        self.ignore_case = ignore_case
        self.use_hash = use_hash