"""
Тести для FileRemover.
"""

# Built-in imports

# Third-party imports
import pytest

# Project imports
from core.remover import FileRemover


class TestFileRemover:
    """Тестування класу FileRemover"""

    def test_init_default_values(self):
        """Тест ініціалізації з значеннями за замовчуванням"""
        remover = FileRemover("/test/roms")

        assert remover.roms_dir == "/test/roms"
        assert remover.imgs_dir is None
        assert remover.log_file == "deleted_log.txt"

    def test_init_custom_values(self):
        """Тест ініціалізації з власними значеннями"""
        remover = FileRemover("/custom/roms", "/custom/imgs", "custom_log.txt")

        assert remover.roms_dir == "/custom/roms"
        assert remover.imgs_dir == "/custom/imgs"
        assert remover.log_file == "custom_log.txt"

    def test_init_with_none_imgs_dir(self):
        """Тест ініціалізації з None директорією зображень"""
        remover = FileRemover("/test/roms", None)
        assert remover.imgs_dir is None

    def test_init_with_empty_log_file(self):
        """Тест ініціалізації з пустим лог-файлом"""
        remover = FileRemover("/test/roms", log_file="")
        assert remover.log_file == ""