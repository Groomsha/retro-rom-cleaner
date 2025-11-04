"""
Тести для SettingsManager.
"""

# Built-in imports
import os
import json
import tempfile
from unittest.mock import patch, mock_open

# Third-party imports
import pytest

# Project imports
from core.settings_manager import SettingsManager


class TestSettingsManager:
    """Тестування класу SettingsManager"""

    def test_init_default_config_file(self):
        """Тест ініціалізації з файлом конфігурації за замовчуванням"""
        manager = SettingsManager()
        assert manager.config_file == "config.json"
        assert hasattr(manager, 'DEFAULT_CONFIG')
        assert isinstance(manager.DEFAULT_CONFIG, dict)

    def test_init_custom_config_file(self):
        """Тест ініціалізації з власним файлом конфігурації"""
        custom_file = "custom_config.json"
        manager = SettingsManager(custom_file)
        assert manager.config_file == custom_file

    @patch('os.path.exists')
    def test_load_config_file_not_exists(self, mock_exists):
        """Тест завантаження конфігурації коли файл не існує"""
        mock_exists.return_value = False

        manager = SettingsManager()
        config = manager.load_config()

        assert config == manager.DEFAULT_CONFIG.copy()
        mock_exists.assert_called_once_with("config.json")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='{"ROMS_DIR": "/test"}')
    def test_load_config_file_exists_valid(self, mock_file, mock_exists):
        """Тест завантаження конфігурації з валідного файлу"""
        mock_exists.return_value = True

        manager = SettingsManager()
        config = manager.load_config()

        assert config["ROMS_DIR"] == "/test"
        # Перевірити що відсутні ключі додані з DEFAULT_CONFIG
        for key, value in manager.DEFAULT_CONFIG.items():
            if key != "ROMS_DIR":
                assert key in config
                assert config[key] == value

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('json.load')
    def test_load_config_file_corrupted(self, mock_json_load, mock_file, mock_exists):
        """Тест завантаження конфігурації з пошкодженого файлу"""
        mock_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

        manager = SettingsManager()
        config = manager.load_config()

        assert config == manager.DEFAULT_CONFIG.copy()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_config(self, mock_json_dump, mock_file, mock_exists):
        """Тест збереження конфігурації"""
        mock_exists.return_value = True

        manager = SettingsManager()
        test_config = {"test_key": "test_value"}

        manager.save_config(test_config)

        mock_file.assert_called_once_with("config.json", "w", encoding="utf-8")
        mock_json_dump.assert_called_once_with(test_config, mock_file(), indent=4)

    def test_default_config_structure(self):
        """Тест структури конфігурації за замовчуванням"""
        manager = SettingsManager()

        expected_keys = [
            "ROMS_DIR", "IMGS_DIR", "IGNORE_CASE",
            "USE_HASH", "LANGUAGE", "THEME"
        ]

        for key in expected_keys:
            assert key in manager.DEFAULT_CONFIG

        # Перевірити типи значень
        assert isinstance(manager.DEFAULT_CONFIG["ROMS_DIR"], str)
        assert isinstance(manager.DEFAULT_CONFIG["IMGS_DIR"], str)
        assert isinstance(manager.DEFAULT_CONFIG["IGNORE_CASE"], bool)
        assert isinstance(manager.DEFAULT_CONFIG["USE_HASH"], bool)
        assert isinstance(manager.DEFAULT_CONFIG["LANGUAGE"], str)
        assert isinstance(manager.DEFAULT_CONFIG["THEME"], str)

    def test_load_config_merges_with_defaults(self):
        """Тест що load_config об'єднує завантажені налаштування з дефолтними"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            partial_config = {"ROMS_DIR": "/custom/roms", "LANGUAGE": "uk"}
            json.dump(partial_config, f)
            temp_file = f.name

        try:
            manager = SettingsManager(temp_file)
            config = manager.load_config()

            # Перевірити що кастомні значення збереглися
            assert config["ROMS_DIR"] == "/custom/roms"
            assert config["LANGUAGE"] == "uk"

            # Перевірити що інші значення взяті з DEFAULT_CONFIG
            assert config["IMGS_DIR"] == manager.DEFAULT_CONFIG["IMGS_DIR"]
            assert config["THEME"] == manager.DEFAULT_CONFIG["THEME"]
            assert config["IGNORE_CASE"] == manager.DEFAULT_CONFIG["IGNORE_CASE"]
            assert config["USE_HASH"] == manager.DEFAULT_CONFIG["USE_HASH"]

        finally:
            os.unlink(temp_file)

    def test_load_config_handles_file_not_found_error(self):
        """Тест обробки FileNotFoundError при завантаженні"""
        with patch('builtins.open') as mock_file:
            mock_file.side_effect = FileNotFoundError()

            manager = SettingsManager()
            config = manager.load_config()

            assert config == manager.DEFAULT_CONFIG.copy()