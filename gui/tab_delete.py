"""
Module: gui.tab_delete
Description: Delete Files tab for RetroROMCleaner GUI.

Author: Ihor Cheberiak (Groomsha) (c) 2025
Project: RetroROMCleaner
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Callable, Optional


class TabDelete(ctk.CTkFrame):
    """Вкладка 'Delete Files'"""

    def __init__(self, master, lang: dict, on_delete: Optional[Callable] = None):
        super().__init__(master)
        self.lang = lang
        self.on_delete = on_delete  # callback у core/remover
        self.build()

    def build(self):
        """Створення віджетів"""
        ctk.CTkLabel(self, text=self.lang["delete_tab"]).pack(anchor="w", padx=10, pady=(10, 5))

        # Кнопки
        frame_btns = ctk.CTkFrame(self)
        frame_btns.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(frame_btns, text=self.lang["start"], command=self.start_delete).pack(side="left", padx=10)
        ctk.CTkButton(frame_btns, text=self.lang["stop"], command=self.stop_delete).pack(side="left", padx=5)

        # Лог
        frame_log = ctk.CTkFrame(self)
        frame_log.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(frame_log, text=self.lang["log"]).pack(anchor="w")
        self.logbox = ctk.CTkTextbox(frame_log, height=200)
        self.logbox.pack(fill="both", expand=True)
        self.progress = ctk.CTkProgressBar(frame_log)
        self.progress.pack(fill="x", pady=5)
        self.progress.set(0)

    def start_delete(self):
        """Тимчасовий обробник кнопки 'Start'"""
        self.logbox.insert("end", "[INFO] Deletion started...\n")
        self.logbox.see("end")
        if self.on_delete:
            self.on_delete()  # пізніше виклик remover.run()

    def stop_delete(self):
        """Зупинка процесу"""
        messagebox.showinfo("Info", "Deletion stopped.")
        self.logbox.insert("end", "[INFO] Deletion stopped.\n")
        self.logbox.see("end")