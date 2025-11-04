"""
Конфігурація для тестів RetroROMCleaner.
"""

# Built-in imports
import os
import sys
import tempfile
import json
from pathlib import Path

# Third-party imports
import pytest

# Project imports


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Налаштування тестового середовища"""
    # Додати кореневу директорію проекту до sys.path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

    yield

    # Очищення після тестів
    pass


@pytest.fixture
def temp_config_file():
    """Створення тимчасового файлу конфігурації"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        test_config = {
            "ROMS_DIR": "/test/roms",
            "IMGS_DIR": "/test/imgs",
            "IGNORE_CASE": True,
            "USE_HASH": True,
            "LANGUAGE": "en",
            "THEME": "Dark",
        }
        json.dump(test_config, f, indent=4)
        config_file = f.name

    yield config_file

    # Очищення
    try:
        os.unlink(config_file)
    except:
        pass


@pytest.fixture
def temp_languages_dir():
    """Створення тимчасової директорії з мовами"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Створити тестові файли мов
        en_lang = {"title": "Test App", "language": "Language"}
        uk_lang = {"title": "Тестовий додаток", "language": "Мова"}

        with open(os.path.join(temp_dir, 'en.json'), 'w', encoding='utf-8') as f:
            json.dump(en_lang, f, ensure_ascii=False, indent=4)

        with open(os.path.join(temp_dir, 'uk.json'), 'w', encoding='utf-8') as f:
            json.dump(uk_lang, f, ensure_ascii=False, indent=4)

        yield temp_dir