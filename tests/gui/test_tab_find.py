"""
Тести для TabFind.
"""

# Built-in imports

# Third-party imports
import pytest

# Project imports
from gui.tab_find import TabFind


class TestTabFind:
    """Тестування класу TabFind"""

    def test_init(self):
        """Тест ініціалізації TabFind"""
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        try:
            lang = {
                "roms_dir": "ROMs Dir:",
                "imgs_dir": "Images Dir:",
                "browse": "Browse",
                "ignore_case": "Ignore Case",
                "use_md5": "Use MD5",
                "start": "Start",
                "stop": "Stop",
                "log": "Log"
            }

            cfg = {
                "ROMS_DIR": "/test/roms",
                "IMGS_DIR": "/test/imgs",
                "IGNORE_CASE": True,
                "USE_HASH": True
            }

            tab = TabFind(root, lang, cfg)
            assert tab.lang == lang
            assert tab.cfg == cfg
            assert hasattr(tab, 'build')
        finally:
            root.destroy()

    def test_select_folder_with_valid_path(self):
        """Тест вибору папки з валідним шляхом"""
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()

        try:
            lang = {"browse": "Browse"}
            cfg = {}
            tab = TabFind(root, lang, cfg)

            # Mock для entry
            class MockEntry:
                def __init__(self):
                    self.value = ""

                def delete(self, start, end):
                    pass

                def insert(self, pos, text):
                    self.value = text

            entry = MockEntry()

            # Mock filedialog
            import unittest.mock as mock
            with mock.patch('tkinter.filedialog.askdirectory', return_value='/selected/path'):
                tab.select_folder(entry)
                assert entry.value == '/selected/path'
        finally:
            root.destroy()

    def test_select_folder_cancel(self):
        """Тест вибору папки з скасуванням"""
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()

        try:
            lang = {"browse": "Browse"}
            cfg = {}
            tab = TabFind(root, lang, cfg)

            class MockEntry:
                def __init__(self):
                    self.value = "original"

                def delete(self, start, end):
                    self.value = ""

                def insert(self, pos, text):
                    self.value = text

            entry = MockEntry()

            import unittest.mock as mock
            with mock.patch('tkinter.filedialog.askdirectory', return_value=''):
                tab.select_folder(entry)
                assert entry.value == "original"  # Не повинно змінюватися
        finally:
            root.destroy()