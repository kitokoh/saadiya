import os
import json
from PyQt5.QtCore import QTranslator, QLocale, QCoreApplication

class LanguageManager:
    def __init__(self, app):
        self.app = app
        self.translator = QTranslator()
        self.init_language()

    def switch_language(self, language):
        # Assuming .qm files are in resources/lang/<language>/
        translator_path = os.path.join('resources', 'lang', language, 'app.qm')

        if os.path.exists(translator_path):
            self.translator.load(translator_path)
            QCoreApplication.installTranslator(self.translator)
        else:
            # Fallback to English or remove translator if not found
            QCoreApplication.removeTranslator(self.translator)

        self.save_language_choice(language)
        # The UI needs to be re-translated, which is handled in the main app

    def save_language_choice(self, language):
        preferences = {'language': language}
        # Assuming settings are stored in a file
        with open('settings.json', 'w') as f:
            json.dump(preferences, f)

    def init_language(self):
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    preferences = json.load(f)
                    selected_language = preferences.get('language', 'en')
            else:
                system_locale = QLocale.system().name()[:2]
                language_map = {'en': 'en', 'fr': 'fr', 'tr': 'tr', 'ar': 'ar', 'pt': 'pt'}
                selected_language = language_map.get(system_locale, 'en')
        except (FileNotFoundError, json.JSONDecodeError):
            selected_language = 'en'

        self.switch_language(selected_language)
