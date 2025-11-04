"""
Тести для Finder.
"""

# Built-in imports
from unittest.mock import patch, MagicMock

# Third-party imports
import pytest

# Project imports
from core.finder import Finder


class TestFinder:
    """Тестування класу Finder"""

    def test_init_default_values(self):
        """Тест ініціалізації з значеннями за замовчуванням"""
        finder = Finder(cfg={"ROMS_DIR": "/test/roms", "IGNORE_CASE": True, "USE_HASH": True})

        assert finder.roms_dir == "/test/roms"
        assert finder.ignore_case is True
        assert finder.use_hash is True

    def test_init_custom_values(self):
        """Тест ініціалізації з власними значеннями"""
        finder = Finder(cfg={"ROMS_DIR": "/custom/roms", "IGNORE_CASE": False, "USE_HASH": False})

        assert finder.roms_dir == "/custom/roms"
        assert finder.ignore_case is False
        assert finder.use_hash is False

    def test_init_with_none_dir(self):
        """Тест ініціалізації з None директорією"""
        finder = Finder(cfg={"ROMS_DIR": None, "IGNORE_CASE": True, "USE_HASH": True})
        assert finder.roms_dir is None

    def test_init_with_empty_dir(self):
        """Тест ініціалізації з пустою директорією"""
        finder = Finder(cfg={"ROMS_DIR": "", "IGNORE_CASE": True, "USE_HASH": True})
        assert finder.roms_dir == ""