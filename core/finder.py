"""
Module: core.finder
Description: Duplicate finder for RetroROMCleaner project.

Author: Ihor Cheberiak (Groomsha) (c) 2025
Project: RetroROMCleaner
"""

import os
from typing import Dict, List, Optional
from utils import FileOperations, HashOperations, LogOperations


class Finder:
    """
    Клас для пошуку дублікатів ROM-файлів у зазначених каталогах.
    Використовує нормалізацію імен файлів та опціональне MD5 хешування.
    """

    def __init__(self, cfg: dict, log_widget=None, progress=None):
        """
        Аргументи:
            cfg: Завантажений словник конфігурації
            log_widget: Віджет GUI Textbox для живого логування
            progress: Віджет GUI ProgressBar для візуальних оновлень
        """
        self.cfg = cfg
        self.log_widget = log_widget
        self.progress = progress
        self.roms_dir = cfg.get("ROMS_DIR", "")
        self.use_hash = cfg.get("USE_HASH", True)
        self.ignore_case = cfg.get("IGNORE_CASE", True)
        self.duplicates_file = "duplicates.txt"
        self.file_ops = FileOperations()
        self.hash_ops = HashOperations()
        self.log_ops = LogOperations()

    # -------------------------------------------------------------------------
    def run(self):
        """Головний процес для пошуку дублікатів та запису звіту."""
        if not self.roms_dir or not os.path.exists(self.roms_dir):
            self._log("[ERROR] ROMS_DIR not found or invalid path.")
            return

        all_files = self.file_ops.safe_list_files(self.roms_dir)
        total_files = len(all_files)
        if total_files == 0:
            self._log("[INFO] No files found in ROMS_DIR.")
            return

        grouped: Dict[str, List[str]] = {}

        self._log(f"[INFO] Scanning {total_files} files...")
        for idx, file_path in enumerate(all_files, start=1):
            base_name = os.path.basename(file_path)
            norm_name = self.file_ops.normalize_name(base_name)
            if not norm_name:
                continue

            if self.ignore_case:
                norm_name = norm_name.lower()

            # Optional: add MD5 hash for extra grouping
            md5 = self.hash_ops.get_md5(file_path) if self.use_hash else ""
            key = f"{norm_name}|{md5}" if md5 else norm_name

            grouped.setdefault(key, []).append(file_path)

            # Update progress
            if self.progress:
                self.progress.set(idx / total_files)

        # Collect duplicates
        duplicates = {k: v for k, v in grouped.items() if len(v) > 1}
        if not duplicates:
            self._log("[INFO] No duplicates found.")
            return

        self._write_duplicates_file(duplicates)
        self._log(f"[SUCCESS] {len(duplicates)} duplicate groups saved to {self.duplicates_file}")

    # -------------------------------------------------------------------------
    def _write_duplicates_file(self, duplicates: Dict[str, List[str]]):
        """Зберегти знайдені дублікати до текстового файлу."""
        with open(self.duplicates_file, "w", encoding="utf-8") as f:
            for key, files in duplicates.items():
                name = key.split("|")[0]
                f.write(f"=== {name} ===\n")
                for path in files:
                    f.write(path + "\n")
                f.write("---\n")
        self._log(f"[INFO] Report saved: {self.duplicates_file}")

    # -------------------------------------------------------------------------
    def _log(self, text: str):
        """Логувати до GUI та до файлу duplicates.log."""
        log_line = text.strip()
        if self.log_widget:
            self.log_widget._log(log_line)
        self.log_ops.write_log("logs/finder.log", log_line)