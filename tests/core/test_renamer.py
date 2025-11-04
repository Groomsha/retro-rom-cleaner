"""
Тести для FileRenamer.
"""

# Built-in imports

# Third-party imports
import pytest

# Project imports
from core.renamer import FileRenamer


class TestFileRenamer:
    """Тестування класу FileRenamer"""

    def test_init_default_values(self):
        """Тест ініціалізації з значеннями за замовчуванням"""
        renamer = FileRenamer("/test/roms")

        assert renamer.roms_dir == "/test/roms"
        assert renamer.imgs_dir is None
        assert renamer.log_file == "renamed_log.txt"

    def test_init_custom_values(self):
        """Тест ініціалізації з власними значеннями"""
        renamer = FileRenamer("/custom/roms", "/custom/imgs", "custom_log.txt")

        assert renamer.roms_dir == "/custom/roms"
        assert renamer.imgs_dir == "/custom/imgs"
        assert renamer.log_file == "custom_log.txt"

    def test_init_with_none_imgs_dir(self):
        """Тест ініціалізації з None директорією зображень"""
        renamer = FileRenamer("/test/roms", None)
        assert renamer.imgs_dir is None

    def test_init_with_empty_log_file(self):
        """Тест ініціалізації з пустим лог-файлом"""
        renamer = FileRenamer("/test/roms", log_file="")
        assert renamer.log_file == ""