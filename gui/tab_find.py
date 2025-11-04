"""
Module: gui.tab_find
Description: Find Duplicates tab for RetroROMCleaner GUI.

Author: Ihor Cheberiak (Groomsha) (c) 2025
Project: RetroROMCleaner
"""

import customtkinter as ctk
from tkinter import filedialog
from typing import Callable, Optional


class TabFind(ctk.CTkFrame):
    """Вкладка 'Find Duplicates'"""

    def __init__(self, master, lang: dict, cfg: dict, on_find: Optional[Callable] = None):
        super().__init__(master)
        self.lang = lang
        self.cfg = cfg
        self.on_find = on_find  # callback у core/finder
        self.build()

    def build(self):
        """Створення віджетів"""

        # Папки
        frame_dirs = ctk.CTkFrame(self)
        frame_dirs.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(frame_dirs, text=self.lang["roms_dir"]).grid(row=0, column=0, sticky="w")
        self.roms_entry = ctk.CTkEntry(frame_dirs, width=500)
        self.roms_entry.insert(0, self.cfg.get("ROMS_DIR", ""))
        self.roms_entry.grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_dirs, text=self.lang["browse"], command=lambda: self.select_folder(self.roms_entry)).grid(row=0, column=2, padx=5)

        ctk.CTkLabel(frame_dirs, text=self.lang["imgs_dir"]).grid(row=2, column=0, sticky="w", pady=(20, 0))
        self.imgs_entry = ctk.CTkEntry(frame_dirs, width=500)
        self.imgs_entry.insert(0, self.cfg.get("IMGS_DIR", ""))
        self.imgs_entry.grid(row=2, column=1, padx=5, pady=(20, 0))
        ctk.CTkButton(frame_dirs, text=self.lang["browse"], command=lambda: self.select_folder(self.imgs_entry)).grid(row=2, column=2, padx=5, pady=(20, 0))

        # Опції
        frame_opts = ctk.CTkFrame(self)
        frame_opts.pack(fill="x", padx=10, pady=(20, 5))
        self.var_ignore = ctk.BooleanVar(value=self.cfg.get("IGNORE_CASE", True))
        self.var_md5 = ctk.BooleanVar(value=self.cfg.get("USE_HASH", True))

        ctk.CTkCheckBox(frame_opts, text=self.lang["ignore_case"], variable=self.var_ignore).pack(side="left", padx=10)
        ctk.CTkCheckBox(frame_opts, text=self.lang["use_md5"], variable=self.var_md5).pack(side="left", padx=10)

        # Кнопки
        frame_btns = ctk.CTkFrame(self)
        frame_btns.pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(frame_btns, text=self.lang["start"], command=self.start_find).pack(side="left", padx=10)
        ctk.CTkButton(frame_btns, text=self.lang["stop"], command=self.stop_find).pack(side="left")

        # Лог
        frame_log = ctk.CTkFrame(self)
        frame_log.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(frame_log, text=self.lang["log"]).pack(anchor="w")
        self.logbox = ctk.CTkTextbox(frame_log, height=200)
        self.logbox.pack(fill="both", expand=True)
        self.progress = ctk.CTkProgressBar(frame_log)
        self.progress.pack(fill="x", pady=5)
        self.progress.set(0)

    def select_folder(self, entry_widget):
        """Вибір папки через діалог"""
        
        folder = filedialog.askdirectory()
        if folder:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, folder)

    def start_find(self):
        """Тимчасовий обробник кнопки 'Start'"""
        
        self.logbox.insert("end", "[INFO] Finding duplicates started...\n")
        self.logbox.see("end")
        if self.on_find:
            self.on_find()  # пізніше виклик finder.run()

    def stop_find(self):
        """Зупинка процесу"""
        
        self.logbox.insert("end", "[INFO] Finding stopped.\n")
        self.logbox.see("end")