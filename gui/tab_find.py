"""
Module: gui.tab_find
Description: GUI tab for finding duplicate ROMs in RetroROMCleaner.
"""

import customtkinter as ctk
import threading
from core.finder import Finder


class TabFind(ctk.CTkFrame):
    """Find Duplicates tab — runs Finder in a background thread."""

    def __init__(self, master, lang, settings_manager):
        super().__init__(master)
        self.lang = lang
        self.settings_manager = settings_manager
        self.finder_thread = None
        self.is_running = False
        self.build()

    # -------------------------------------------------------------------------
    def build(self):
        """Create UI elements for Find Duplicates tab."""

        # Directories
        frame_dirs = ctk.CTkFrame(self)
        frame_dirs.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(frame_dirs, text=self.lang["roms_dir"]).grid(row=0, column=0, sticky="w")
        self.roms_entry = ctk.CTkEntry(frame_dirs, width=500)
        self.roms_entry.insert(0, self.settings_manager.config.get("ROMS_DIR", ""))
        self.roms_entry.grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_dirs, text=self.lang["browse"], command=lambda: self.select_folder(self.roms_entry)).grid(row=0, column=2, padx=5)

        ctk.CTkLabel(frame_dirs, text=self.lang["imgs_dir"]).grid(row=2, column=0, sticky="w", pady=(20, 0))
        self.imgs_entry = ctk.CTkEntry(frame_dirs, width=500)
        self.imgs_entry.insert(0, self.settings_manager.config.get("IMGS_DIR", ""))
        self.imgs_entry.grid(row=2, column=1, padx=5, pady=(20, 0))
        ctk.CTkButton(frame_dirs, text=self.lang["browse"], command=lambda: self.select_folder(self.imgs_entry)).grid(row=2, column=2, padx=5, pady=(20, 0))

        # Options
        frame_opts = ctk.CTkFrame(self)
        frame_opts.pack(fill="x", padx=10, pady=(20, 5))
        self.var_ignore = ctk.BooleanVar(value=self.settings_manager.config.get("IGNORE_CASE", True))
        self.var_md5 = ctk.BooleanVar(value=self.settings_manager.config.get("USE_HASH", True))

        ctk.CTkCheckBox(frame_opts, text=self.lang["ignore_case"], variable=self.var_ignore).pack(side="left", padx=10)
        ctk.CTkCheckBox(frame_opts, text=self.lang["use_md5"], variable=self.var_md5).pack(side="left", padx=10)

        # Buttons
        frame_btns = ctk.CTkFrame(self)
        frame_btns.pack(fill="x", padx=10, pady=5)

        self.start_btn = ctk.CTkButton(frame_btns, text=self.lang["start"], command=self.start_find)
        self.start_btn.pack(side="left", padx=10)

        self.stop_btn = ctk.CTkButton(frame_btns, text=self.lang["stop"], command=self.stop_find, state="disabled")
        self.stop_btn.pack(side="left", padx=5)

        # Log + progress frame
        frame_log = ctk.CTkFrame(self)
        frame_log.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame_log, text=self.lang["log"]).pack(anchor="w")

        self.logbox = ctk.CTkTextbox(frame_log, height=220)
        self.logbox.pack(fill="both", expand=True)

        self.progressbar = ctk.CTkProgressBar(frame_log)
        self.progressbar.pack(fill="x", pady=5)
        self.progressbar.set(0)

    # -------------------------------------------------------------------------
    def start_find(self):
        """Start Finder in a separate thread."""
        if self.is_running:
            self._log("[WARN] Finder is already running.")
            return

        self.is_running = True
        self.progressbar.set(0)
        self.logbox.delete("1.0", "end")
        self._log("[INFO] Starting duplicate search...")

        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")

        cfg = self.settings_manager.config

        # Run Finder in separate thread
        self.finder_thread = threading.Thread(
            target=self._run_finder_thread, args=(cfg,), daemon=True
        )
        self.finder_thread.start()

    def _run_finder_thread(self, cfg):
        """Actual Finder execution in background thread."""
        try:
            finder = Finder(cfg=cfg, log_widget=self, progress=self)
            finder.run()
        except Exception as e:
            self._log(f"[ERROR] Finder failed: {e}")
        finally:
            self._on_find_complete()

    def stop_find(self):
        """Stop the running thread (not forcefully, just flag)."""
        if not self.is_running:
            return
        self._log("[INFO] Finder stopped manually (next file will end loop).")
        self.is_running = False

    def _on_find_complete(self):
        """Executed when Finder finishes or stops."""
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self._log("[INFO] Finder completed.")

    # -------------------------------------------------------------------------
    def select_folder(self, entry_widget):
        """Select folder via dialog."""
        import tkinter.filedialog as filedialog
        folder = filedialog.askdirectory()
        if folder:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, folder)

    # -------------------------------------------------------------------------
    # Helper functions for thread-safe logging and progress update
    def _log(self, message: str):
        """Thread-safe GUI logging."""
        def append():
            self.logbox.insert("end", message + "\n")
            self.logbox.see("end")
        self.after(0, append)

    def set(self, value: float):
        """Thread-safe progress update (Finder calls this)."""
        self.after(0, lambda: self.progressbar.set(value))