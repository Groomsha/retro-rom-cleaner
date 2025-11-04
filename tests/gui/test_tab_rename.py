"""
Тести для TabRename.
"""

# Built-in imports

# Third-party imports
import pytest

# Project imports
from gui.tab_rename import TabRename


class TestTabRename:
    """Тестування класу TabRename"""

    def test_init(self):
        """Тест ініціалізації TabRename"""
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        try:
            lang = {
                "rename_tab": "Rename Files",
                "start": "Start",
                "stop": "Stop",
                "log": "Log"
            }

            tab = TabRename(root, lang)
            assert tab.lang == lang
            assert tab.on_rename is None
            assert hasattr(tab, 'build')
        finally:
            root.destroy()

    def test_init_with_callback(self):
        """Тест ініціалізації TabRename з callback"""
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()

        try:
            lang = {"rename_tab": "Rename Files"}
            callback_called = False

            def test_callback():
                nonlocal callback_called
                callback_called = True

            tab = TabRename(root, lang, test_callback)
            assert tab.on_rename == test_callback
        finally:
            root.destroy()

    def test_start_rename_without_callback(self):
        """Тест start_rename без callback"""
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()

        try:
            lang = {"rename_tab": "Rename Files"}
            tab = TabRename(root, lang)

            # Не повинно викликати помилку
            tab.start_rename()
            # Callback не встановлений, тому нічого не повинно статися
        finally:
            root.destroy()

    def test_start_rename_with_callback(self):
        """Тест start_rename з callback"""
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()

        try:
            lang = {"rename_tab": "Rename Files"}
            callback_called = False

            def test_callback():
                nonlocal callback_called
                callback_called = True

            tab = TabRename(root, lang, test_callback)
            tab.start_rename()

            assert callback_called
        finally:
            root.destroy()