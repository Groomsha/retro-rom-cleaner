"""
Module: main
Description: Main entry point for RetroROMCleaner application.

Author: Ihor Cheberiak (Groomsha) (c) 2025
Project: RetroROMCleaner
"""

# Built-in imports
import sys
import os
from typing import Optional

# Third-party imports

# Project imports

# Додати поточну директорію до sys.path для коректних імпортів
sys.path.insert(0, os.path.dirname(__file__))


def main():
    """Головна функція додатку"""

    # Запуск графічного інтерфейсу
    try:
        import gui.app
        app = gui.app.RetroROMCleanerGUI()
        app.mainloop()
    except ImportError as e:
        print(f"Помилка імпорту GUI: {e}")
        print("GUI залежності не встановлені або відсутні.")


if __name__ == "__main__":
    main()