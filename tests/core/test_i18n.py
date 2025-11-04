"""
Тести для LanguageManager.
"""

# Built-in imports
import os
import json
import tempfile
from unittest.mock import patch, mock_open

# Third-party imports
import pytest

# Project imports
from core.i18n import LanguageManager


class TestLanguageManager:
    """Тестування класу LanguageManager"""

    def test_init_default_languages_dir(self):
        """Тест ініціалізації з директорією мов за замовчуванням"""
        manager = LanguageManager()
        assert manager.languages_dir == "languages"
        assert isinstance(manager.languages, dict)

    def test_init_custom_languages_dir(self):
        """Тест ініціалізації з власною директорією мов"""
        custom_dir = "custom_languages"
        manager = LanguageManager(custom_dir)
        assert manager.languages_dir == custom_dir

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_load_languages_no_directory(self, mock_listdir, mock_exists):
        """Тест завантаження мов коли директорія не існує"""
        mock_exists.return_value = False

        manager = LanguageManager()
        manager.load_languages()

        assert manager.languages == {}
        mock_exists.assert_called_once_with("languages")

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_load_languages_empty_directory(self, mock_listdir, mock_exists):
        """Тест завантаження мов з пустої директорії"""
        mock_exists.return_value = True
        mock_listdir.return_value = []

        manager = LanguageManager()
        manager.load_languages()

        assert manager.languages == {}

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_languages_valid_files(self, mock_file, mock_listdir, mock_exists):
        """Тест завантаження мов з валідними файлами"""
        mock_exists.return_value = True
        mock_listdir.return_value = ['en.json', 'uk.json', 'invalid.txt']

        manager = LanguageManager()
        manager.load_languages()

        assert 'en' in manager.languages
        assert 'uk' in manager.languages
        assert 'invalid' not in manager.languages  # Не .json файл
        assert manager.languages['en'] == {"key": "value"}
        assert manager.languages['uk'] == {"key": "value"}

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('json.load')
    def test_load_languages_corrupted_file(self, mock_json_load, mock_file, mock_listdir, mock_exists):
        """Тест завантаження мов з пошкодженим файлом"""
        mock_exists.return_value = True
        mock_listdir.return_value = ['en.json']
        mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

        manager = LanguageManager()
        manager.load_languages()

        assert manager.languages == {}

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('builtins.open')
    def test_load_languages_file_not_found(self, mock_file, mock_listdir, mock_exists):
        """Тест завантаження мов коли файл не знайдено"""
        mock_exists.return_value = True
        mock_listdir.return_value = ['en.json']
        mock_file.side_effect = FileNotFoundError()

        manager = LanguageManager()
        manager.load_languages()

        assert manager.languages == {}

    def test_get_language_existing(self):
        """Тест отримання існуючої мови"""
        manager = LanguageManager()
        manager.languages = {'en': {'title': 'App'}, 'uk': {'title': 'Додаток'}}

        lang = manager.get_language('en')
        assert lang == {'title': 'App'}

        lang = manager.get_language('uk')
        assert lang == {'title': 'Додаток'}

    def test_get_language_non_existing_fallback_to_en(self):
        """Тест отримання неіснуючої мови з fallback до 'en'"""
        manager = LanguageManager()
        manager.languages = {'en': {'title': 'App'}}

        lang = manager.get_language('uk')
        assert lang == {'title': 'App'}

    def test_get_language_non_existing_no_en_fallback(self):
        """Тест отримання неіснуючої мови без 'en'"""
        manager = LanguageManager()
        manager.languages = {'uk': {'title': 'Додаток'}}

        lang = manager.get_language('fr')
        assert lang == {}

    def test_get_available_languages(self):
        """Тест отримання списку доступних мов"""
        manager = LanguageManager()
        manager.languages = {'en': {}, 'uk': {}, 'fr': {}}

        available = manager.get_available_languages()
        assert set(available) == {'en', 'uk', 'fr'}

    def test_get_available_languages_empty(self):
        """Тест отримання списку доступних мов коли мов немає"""
        manager = LanguageManager()
        manager.languages = {}

        available = manager.get_available_languages()
        assert available == []

    def test_init_calls_load_languages(self):
        """Тест що __init__ викликає load_languages"""
        with patch.object(LanguageManager, 'load_languages') as mock_load:
            manager = LanguageManager()
            mock_load.assert_called_once()

    def test_get_language_case_sensitive(self):
        """Тест що get_language чутливий до регістру"""
        manager = LanguageManager()
        manager.languages = {'EN': {'title': 'App'}, 'en': {'title': 'App Lower'}}

        lang = manager.get_language('en')
        assert lang == {'title': 'App Lower'}

        lang = manager.get_language('EN')
        assert lang == {'title': 'App'}

    def test_load_languages_multiple_files(self, temp_languages_dir):
        """Тест завантаження кількох файлів мов з fixtures"""
        manager = LanguageManager(temp_languages_dir)
        manager.load_languages()

        assert len(manager.languages) == 2
        assert 'en' in manager.languages
        assert 'uk' in manager.languages
        assert manager.languages['en']['title'] == 'Test App'
        assert manager.languages['uk']['title'] == 'Тестовий додаток'

    def test_get_language_fallback_chain(self):
        """Тест ланцюжка fallback для мов"""
        manager = LanguageManager()

        # Немає мов зовсім
        lang = manager.get_language('any')
        assert lang == {}

        # Є тільки 'en'
        manager.languages = {'en': {'key': 'en_value'}}
        lang = manager.get_language('uk')
        assert lang == {'key': 'en_value'}

        # Є кілька мов
        manager.languages = {'en': {'key': 'en_value'}, 'uk': {'key': 'uk_value'}}
        lang = manager.get_language('uk')
        assert lang == {'key': 'uk_value'}