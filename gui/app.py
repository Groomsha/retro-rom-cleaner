"""
Module: app
Description: CustomTkinter GUI application for RetroROMCleaner.

Author: Ihor Cheberiak (Groomsha) (c) 2025
Project: RetroROMCleaner
"""

# Built-in imports
import os
import sys
from tkinter import filedialog
from typing import Dict, Any

# Third-party imports
import customtkinter as ctk

# Project imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.settings_manager import SettingsManager
from core.i18n import LanguageManager


class RetroROMCleanerGUI(ctk.CTk):
    """Графічний інтерфейс для RetroROMCleaner"""

    def __init__(self, config_file: str = "config.json"):
        """Ініціалізація графічного інтерфейсу

        Args:
            config_file: Шлях до файлу конфігурації
        """
        super().__init__()

        # Ініціалізація менеджерів
        self.settings_manager = SettingsManager(config_file)
        self.language_manager = LanguageManager()

        # Завантаження конфігурації
        self.cfg = self.settings_manager.load_config()

        # Налаштування мови
        self.lang_code = self.cfg.get("LANGUAGE", "en")
        self.lang = self.language_manager.get_language(self.lang_code)

        # Налаштування теми
        ctk.set_appearance_mode(self.cfg.get("THEME", "Dark"))
        self.title(self.lang["title"])
        self.geometry("900x600")
        self.minsize(800, 500)

        self.create_widgets()

    def create_widgets(self):
        """Створення всіх віджетів інтерфейсу"""
        # Створення вкладок
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_find = self.tabs.add(self.lang["find_tab"])
        self.tab_delete = self.tabs.add(self.lang["delete_tab"])
        self.tab_rename = self.tabs.add(self.lang["rename_tab"])
        self.tab_settings = self.tabs.add(self.lang["settings_tab"])

        self.create_tab_find()
        self.create_tab_delete()
        self.create_tab_rename()
        self.create_tab_settings()

    def create_tab_find(self):
        """Створення вкладки пошуку дублікатів"""
        t = self.tab_find

        # Папки
        frame_dirs = ctk.CTkFrame(t)
        frame_dirs.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(frame_dirs, text=self.lang["roms_dir"]).grid(row=0, column=0, sticky="w")
        self.roms_entry = ctk.CTkEntry(frame_dirs, width=500)
        self.roms_entry.insert(0, self.cfg.get("ROMS_DIR", ""))
        self.roms_entry.grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_dirs, text=self.lang["browse"], command=lambda: self.select_folder(self.roms_entry)).grid(row=0, column=2, padx=5)

        ctk.CTkLabel(frame_dirs, text=self.lang["imgs_dir"]).grid(row=1, column=0, sticky="w")
        self.imgs_entry = ctk.CTkEntry(frame_dirs, width=500)
        self.imgs_entry.insert(0, self.cfg.get("IMGS_DIR", ""))
        self.imgs_entry.grid(row=1, column=1, padx=5)
        ctk.CTkButton(frame_dirs, text=self.lang["browse"], command=lambda: self.select_folder(self.imgs_entry)).grid(row=1, column=2, padx=5)

        # Опції
        frame_opts = ctk.CTkFrame(t)
        frame_opts.pack(fill="x", padx=10, pady=5)
        self.var_ignore = ctk.BooleanVar(value=self.cfg.get("IGNORE_CASE", True))
        self.var_md5 = ctk.BooleanVar(value=self.cfg.get("USE_HASH", True))

        ctk.CTkCheckBox(frame_opts, text=self.lang["ignore_case"], variable=self.var_ignore).pack(side="left", padx=10)
        ctk.CTkCheckBox(frame_opts, text=self.lang["use_md5"], variable=self.var_md5).pack(side="left", padx=10)

        # Кнопки
        frame_btns = ctk.CTkFrame(t)
        frame_btns.pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(frame_btns, text=self.lang["start"], command=self.dummy_action).pack(side="left", padx=10)
        ctk.CTkButton(frame_btns, text=self.lang["stop"], command=self.dummy_action).pack(side="left")

        # Лог
        frame_log = ctk.CTkFrame(t)
        frame_log.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(frame_log, text=self.lang["log"]).pack(anchor="w")
        self.logbox = ctk.CTkTextbox(frame_log, height=200)
        self.logbox.pack(fill="both", expand=True)
        self.progress = ctk.CTkProgressBar(frame_log)
        self.progress.pack(fill="x", pady=5)
        self.progress.set(0)

    def create_tab_delete(self):
        """Створення вкладки видалення файлів"""
        pass

    def create_tab_rename(self):
        """Створення вкладки перейменування файлів"""
        pass

    def create_tab_settings(self):
        """Створення вкладки налаштувань"""
        t = self.tab_settings
        ctk.CTkLabel(t, text=self.lang["language"]).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.lang_option = ctk.CTkOptionMenu(t, values=self.language_manager.get_available_languages(), command=self.change_language)
        self.lang_option.set(self.lang_code)
        self.lang_option.grid(row=0, column=1, padx=10)

        ctk.CTkLabel(t, text=self.lang["theme"]).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.theme_option = ctk.CTkOptionMenu(t, values=["Dark", "Light", "System"], command=self.change_theme)
        self.theme_option.set(self.cfg.get("THEME", "Dark"))
        self.theme_option.grid(row=1, column=1, padx=10)

        ctk.CTkButton(t, text=self.lang["save"], command=self.save_current_settings).grid(row=3, column=0, padx=10, pady=20)
        ctk.CTkButton(t, text=self.lang["restore"], command=self.restore_defaults).grid(row=3, column=1, padx=10, pady=20)

    def select_folder(self, entry_widget):
        """Вибір папки через діалог

        Args:
            entry_widget: Віджет поля введення для оновлення
        """
        folder = filedialog.askdirectory()
        if folder:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, folder)

    def dummy_action(self):
        """Тестова дія"""
        self.logbox.insert("end", "[INFO] Placeholder action executed.\n")
        self.logbox.see("end")

    def change_language(self, lang_code: str):
        """Зміна мови інтерфейсу

        Args:
            lang_code: Код нової мови
        """
        self.cfg["LANGUAGE"] = lang_code
        self.settings_manager.save_config(self.cfg)
        self.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def change_theme(self, theme_name: str):
        """Зміна теми інтерфейсу

        Args:
            theme_name: Назва нової теми
        """
        ctk.set_appearance_mode(theme_name)
        self.cfg["THEME"] = theme_name
        self.settings_manager.save_config(self.cfg)

    def save_current_settings(self):
        """Збереження поточних налаштувань"""
        self.cfg["ROMS_DIR"] = self.roms_entry.get()
        self.cfg["IMGS_DIR"] = self.imgs_entry.get()
        self.cfg["IGNORE_CASE"] = self.var_ignore.get()
        self.cfg["USE_HASH"] = self.var_md5.get()
        self.settings_manager.save_config(self.cfg)
        if hasattr(self, 'logbox'):
            self.logbox.insert("end", "[INFO] Settings saved.\n")
            self.logbox.see("end")

    def restore_defaults(self):
        """Відновлення налаштувань за замовчуванням"""
        self.settings_manager.save_config(self.settings_manager.DEFAULT_CONFIG)
        if hasattr(self, 'logbox'):
            self.logbox.insert("end", "[INFO] Defaults restored. Restart app.\n")
            self.logbox.see("end")

