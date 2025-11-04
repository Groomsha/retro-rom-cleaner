"""
Тести для TabDelete.
"""

# Built-in imports

# Third-party imports
import pytest

# Project imports
from gui.tab_delete import TabDelete


class TestTabDelete:
    """Тестування класу TabDelete"""

    def test_init(self):
        """Тест ініціалізації TabDelete"""
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        try:
            lang = {
                "delete_tab": "Delete Files",
                "start": "Start",
                "stop": "Stop",
                "log": "Log"
            }

            tab = TabDelete(root, lang)
            assert tab.lang == lang
            assert tab.on_delete is None
            assert hasattr(tab, 'build')
        finally:
            root.destroy()

    def test_init_with_callback(self):
        """Тест ініціалізації TabDelete з callback"""
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()

        try:
            lang = {"delete_tab": "Delete Files"}
            callback_called = False

            def test_callback():
                nonlocal callback_called
                callback_called = True

            tab = TabDelete(root, lang, test_callback)
            assert tab.on_delete == test_callback
        finally:
            root.destroy()

    def test_start_delete_without_callback(self):
        """Тест start_delete без callback"""
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()

        try:
            lang = {"delete_tab": "Delete Files"}
            tab = TabDelete(root, lang)

            # Не повинно викликати помилку
            tab.start_delete()
            # Callback не встановлений, тому нічого не повинно статися
        finally:
            root.destroy()

    def test_start_delete_with_callback(self):
        """Тест start_delete з callback"""
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()

        try:
            lang = {"delete_tab": "Delete Files"}
            callback_called = False

            def test_callback():
                nonlocal callback_called
                callback_called = True

            tab = TabDelete(root, lang, test_callback)
            tab.start_delete()

            assert callback_called
        finally:
            root.destroy()