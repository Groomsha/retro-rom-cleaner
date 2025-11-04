"""
Тести для DuplicateFinder.
"""

# Built-in imports
from unittest.mock import patch, MagicMock

# Third-party imports
import pytest

# Project imports
from core.finder import DuplicateFinder


class TestDuplicateFinder:
    """Тестування класу DuplicateFinder"""

    def test_init_default_values(self):
        """Тест ініціалізації з значеннями за замовчуванням"""
        finder = DuplicateFinder("/test/roms")

        assert finder.roms_dir == "/test/roms"
        assert finder.ignore_case is True
        assert finder.use_hash is True

    def test_init_custom_values(self):
        """Тест ініціалізації з власними значеннями"""
        finder = DuplicateFinder("/custom/roms", ignore_case=False, use_hash=False)

        assert finder.roms_dir == "/custom/roms"
        assert finder.ignore_case is False
        assert finder.use_hash is False

    def test_init_with_none_dir(self):
        """Тест ініціалізації з None директорією"""
        finder = DuplicateFinder(None)
        assert finder.roms_dir is None

    def test_init_with_empty_dir(self):
        """Тест ініціалізації з пустою директорією"""
        finder = DuplicateFinder("")
        assert finder.roms_dir == ""