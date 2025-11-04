"""
Тести для FileUtils.
"""

# Built-in imports

# Third-party imports
import pytest

# Project imports
from core.utils import FileUtils


class TestFileUtils:
    """Тестування класу FileUtils"""

    def test_init(self):
        """Тест ініціалізації FileUtils"""
        utils = FileUtils()
        assert utils is not None
        assert isinstance(utils, FileUtils)