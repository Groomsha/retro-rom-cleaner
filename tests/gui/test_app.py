"""
Тести для RetroROMCleanerGUI.
"""

# Built-in imports
from unittest.mock import patch, MagicMock

# Third-party imports
import pytest

# Project imports
from gui.app import RetroROMCleanerGUI


class TestRetroROMCleanerGUI:
    """Тестування класу RetroROMCleanerGUI"""

    @patch('gui.app.ctk.CTk')
    @patch('core.settings_manager.SettingsManager')
    @patch('core.i18n.LanguageManager')
    def test_init(self, mock_lang_manager, mock_settings_manager, mock_ctk):
        """Тест ініціалізації GUI"""
        # Налаштування mock'ів
        mock_settings = MagicMock()
        mock_settings.load_config.return_value = {
            "LANGUAGE": "en",
            "THEME": "Dark"
        }
        mock_settings_manager.return_value = mock_settings

        mock_lang = MagicMock()
        mock_lang.get_language.return_value = {"title": "Test App"}
        mock_lang_manager.return_value = mock_lang

        # Створення екземпляру
        gui = RetroROMCleanerGUI()

        # Перевірки
        mock_settings_manager.assert_called_once_with("config.json")
        mock_lang_manager.assert_called_once()
        mock_settings.load_config.assert_called_once()
        mock_lang.get_language.assert_called_once_with("en")

        assert gui.cfg == mock_settings.load_config.return_value
        assert gui.lang_code == "en"
        assert gui.lang == mock_lang.get_language.return_value

    @patch('gui.app.ctk.CTk')
    @patch('core.settings_manager.SettingsManager')
    @patch('core.i18n.LanguageManager')
    def test_init_custom_config_file(self, mock_lang_manager, mock_settings_manager, mock_ctk):
        """Тест ініціалізації з власним файлом конфігурації"""
        custom_file = "custom.json"

        with patch('gui.app.ctk.CTk') as mock_ctk:
            gui = RetroROMCleanerGUI(custom_file)

            mock_settings_manager.assert_called_once_with(custom_file)

    @patch('gui.app.ctk.CTk')
    @patch('core.settings_manager.SettingsManager')
    @patch('core.i18n.LanguageManager')
    def test_create_widgets_calls(self, mock_lang_manager, mock_settings_manager, mock_ctk):
        """Тест що create_widgets створює всі вкладки"""
        mock_settings = MagicMock()
        mock_settings.load_config.return_value = {
            "LANGUAGE": "en",
            "THEME": "Dark"
        }
        mock_settings_manager.return_value = mock_settings

        mock_lang = MagicMock()
        mock_lang.get_language.return_value = {
            "find_tab": "Find",
            "delete_tab": "Delete",
            "rename_tab": "Rename",
            "settings_tab": "Settings"
        }
        mock_lang_manager.return_value = mock_lang

        gui = RetroROMCleanerGUI()

        # Виклик create_widgets
        with patch.object(gui, 'create_tab_find'), \
             patch.object(gui, 'create_tab_delete'), \
             patch.object(gui, 'create_tab_rename'), \
             patch.object(gui, 'create_tab_settings'):

            gui.create_widgets()

            # Перевірки що всі методи вкладок були викликані
            gui.create_tab_find.assert_called_once()
            gui.create_tab_delete.assert_called_once()
            gui.create_tab_rename.assert_called_once()
            gui.create_tab_settings.assert_called_once()

    @patch('gui.app.ctk.CTk')
    @patch('core.settings_manager.SettingsManager')
    @patch('core.i18n.LanguageManager')
    @patch('gui.app.ctk.CTkTabview')
    def test_create_tab_find_widgets(self, mock_tabview, mock_lang_manager, mock_settings_manager, mock_ctk):
        """Тест створення віджетів вкладки пошуку"""
        mock_settings = MagicMock()
        mock_settings.load_config.return_value = {
            "ROMS_DIR": "/test/roms",
            "IMGS_DIR": "/test/imgs",
            "IGNORE_CASE": True,
            "USE_HASH": True,
            "LANGUAGE": "en",
            "THEME": "Dark"
        }
        mock_settings_manager.return_value = mock_settings

        mock_lang = MagicMock()
        mock_lang.get_language.return_value = {
            "roms_dir": "ROMs Dir:",
            "imgs_dir": "Images Dir:",
            "browse": "Browse",
            "ignore_case": "Ignore Case",
            "use_md5": "Use MD5",
            "start": "Start",
            "stop": "Stop",
            "log": "Log"
        }
        mock_lang_manager.return_value = mock_lang

        gui = RetroROMCleanerGUI()

        # Mock для віджетів
        with patch('gui.app.ctk.CTkFrame') as mock_frame, \
             patch('gui.app.ctk.CTkLabel'), \
             patch('gui.app.ctk.CTkEntry') as mock_entry, \
             patch('gui.app.ctk.CTkButton'), \
             patch('gui.app.ctk.CTkCheckBox'), \
             patch('gui.app.ctk.CTkTextbox') as mock_textbox, \
             patch('gui.app.ctk.CTkProgressBar') as mock_progress:

            gui.create_tab_find()

            # Перевірки що віджети були створені
            assert mock_frame.call_count >= 3  # dirs, opts, btns, log frames
            assert mock_entry.call_count >= 2  # roms та imgs entries
            assert mock_textbox.call_count >= 1  # log box
            assert mock_progress.call_count >= 1  # progress bar

    @patch('gui.app.ctk.CTk')
    @patch('core.settings_manager.SettingsManager')
    @patch('core.i18n.LanguageManager')
    def test_select_folder(self, mock_lang_manager, mock_settings_manager, mock_ctk):
        """Тест вибору папки"""
        mock_settings = MagicMock()
        mock_settings.load_config.return_value = {"LANGUAGE": "en", "THEME": "Dark"}
        mock_settings_manager.return_value = mock_settings
        mock_lang_manager.return_value.get_language.return_value = {}

        gui = RetroROMCleanerGUI()

        mock_entry = MagicMock()

        with patch('gui.app.filedialog.askdirectory', return_value='/selected/path'):
            gui.select_folder(mock_entry)

            mock_entry.delete.assert_called_once_with(0, "end")
            mock_entry.insert.assert_called_once_with(0, '/selected/path')

    @patch('gui.app.ctk.CTk')
    @patch('core.settings_manager.SettingsManager')
    @patch('core.i18n.LanguageManager')
    def test_select_folder_cancel(self, mock_lang_manager, mock_settings_manager, mock_ctk):
        """Тест вибору папки з скасуванням"""
        mock_settings = MagicMock()
        mock_settings.load_config.return_value = {"LANGUAGE": "en", "THEME": "Dark"}
        mock_settings_manager.return_value = mock_settings
        mock_lang_manager.return_value.get_language.return_value = {}

        gui = RetroROMCleanerGUI()

        mock_entry = MagicMock()

        with patch('gui.app.filedialog.askdirectory', return_value=''):
            gui.select_folder(mock_entry)

            # Якщо скасовано, методи не повинні викликатися
            mock_entry.delete.assert_not_called()
            mock_entry.insert.assert_not_called()

    @patch('gui.app.ctk.CTk')
    @patch('core.settings_manager.SettingsManager')
    @patch('core.i18n.LanguageManager')
    def test_dummy_action(self, mock_lang_manager, mock_settings_manager, mock_ctk):
        """Тест тестованої дії"""
        mock_settings = MagicMock()
        mock_settings.load_config.return_value = {"LANGUAGE": "en", "THEME": "Dark"}
        mock_settings_manager.return_value = mock_settings
        mock_lang_manager.return_value.get_language.return_value = {}

        gui = RetroROMCleanerGUI()

        gui.logbox = MagicMock()

        gui.dummy_action()

        gui.logbox.insert.assert_called_once_with("end", "[INFO] Placeholder action executed.\n")
        gui.logbox.see.assert_called_once_with("end")

    @patch('gui.app.ctk.CTk')
    @patch('core.settings_manager.SettingsManager')
    @patch('core.i18n.LanguageManager')
    @patch('gui.app.sys')
    @patch('gui.app.os.execl')
    def test_change_language(self, mock_execl, mock_sys, mock_lang_manager, mock_settings_manager, mock_ctk):
        """Тест зміни мови"""
        mock_settings = MagicMock()
        mock_settings.load_config.return_value = {"LANGUAGE": "en", "THEME": "Dark"}
        mock_settings_manager.return_value = mock_settings
        mock_lang_manager.return_value.get_language.return_value = {}

        gui = RetroROMCleanerGUI()

        with patch.object(gui, 'destroy'):
            gui.change_language("uk")

            mock_settings.save_config.assert_called_once_with({"LANGUAGE": "uk", "THEME": "Dark"})
            gui.destroy.assert_called_once()
            mock_execl.assert_called_once()

    @patch('gui.app.ctk.CTk')
    @patch('core.settings_manager.SettingsManager')
    @patch('core.i18n.LanguageManager')
    @patch('gui.app.ctk.set_appearance_mode')
    def test_change_theme(self, mock_set_mode, mock_lang_manager, mock_settings_manager, mock_ctk):
        """Тест зміни теми"""
        mock_settings = MagicMock()
        mock_settings.load_config.return_value = {"LANGUAGE": "en", "THEME": "Dark"}
        mock_settings_manager.return_value = mock_settings
        mock_lang_manager.return_value.get_language.return_value = {}

        gui = RetroROMCleanerGUI()

        gui.change_theme("Light")

        mock_set_mode.assert_called_once_with("Light")
        mock_settings.save_config.assert_called_once_with({"LANGUAGE": "en", "THEME": "Light"})

    @patch('gui.app.ctk.CTk')
    @patch('core.settings_manager.SettingsManager')
    @patch('core.i18n.LanguageManager')
    def test_save_current_settings(self, mock_lang_manager, mock_settings_manager, mock_ctk):
        """Тест збереження поточних налаштувань"""
        mock_settings = MagicMock()
        mock_settings.load_config.return_value = {"LANGUAGE": "en", "THEME": "Dark"}
        mock_settings_manager.return_value = mock_settings
        mock_lang_manager.return_value.get_language.return_value = {}

        gui = RetroROMCleanerGUI()

        # Mock entries та checkboxes
        gui.roms_entry = MagicMock()
        gui.roms_entry.get.return_value = "/new/roms"
        gui.imgs_entry = MagicMock()
        gui.imgs_entry.get.return_value = "/new/imgs"
        gui.var_ignore = MagicMock()
        gui.var_ignore.get.return_value = False
        gui.var_md5 = MagicMock()
        gui.var_md5.get.return_value = False

        gui.logbox = MagicMock()

        gui.save_current_settings()

        expected_config = {
            "LANGUAGE": "en",
            "THEME": "Dark",
            "ROMS_DIR": "/new/roms",
            "IMGS_DIR": "/new/imgs",
            "IGNORE_CASE": False,
            "USE_HASH": False
        }
        mock_settings.save_config.assert_called_once_with(expected_config)
        gui.logbox.insert.assert_called_once_with("end", "[INFO] Settings saved.\n")
        gui.logbox.see.assert_called_once_with("end")

    @patch('gui.app.ctk.CTk')
    @patch('core.settings_manager.SettingsManager')
    @patch('core.i18n.LanguageManager')
    def test_restore_defaults(self, mock_lang_manager, mock_settings_manager, mock_ctk):
        """Тест відновлення налаштувань за замовчуванням"""
        mock_settings = MagicMock()
        mock_settings.DEFAULT_CONFIG = {"default": "config"}
        mock_settings.load_config.return_value = {"LANGUAGE": "en", "THEME": "Dark"}
        mock_settings_manager.return_value = mock_settings
        mock_lang_manager.return_value.get_language.return_value = {}

        gui = RetroROMCleanerGUI()

        gui.logbox = MagicMock()

        gui.restore_defaults()

        mock_settings.save_config.assert_called_once_with({"default": "config"})
        gui.logbox.insert.assert_called_once_with("end", "[INFO] Defaults restored. Restart app.\n")
        gui.logbox.see.assert_called_once_with("end")