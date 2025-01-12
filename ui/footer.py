import json
import os
import sys
from PyQt5.QtCore import Qt, QTranslator, QLocale, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QFrame, QPushButton, QApplication

# Define user data directory dynamically
USER_DATA_DIR = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "leopardo_ai")

class FooterSection(QFrame):
    # Signals emitted when buttons are clicked
    privacy_clicked = pyqtSignal()
    terms_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize translator
        self.translator = QTranslator()
        self.init_language()  # Initialize the language settings
        
        # Set up the UI
        self.setup_ui()

    def switch_language(self, language):
        """Switch the application's language."""
        lang_path = os.path.join(USER_DATA_DIR, 'resources', 'lang', language, 'ui', 'footer_translated.qm')
        if os.path.exists(lang_path):
            self.translator.load(lang_path)
            QApplication.instance().installTranslator(self.translator)
            self.save_language_choice(language)
            self.retranslate_ui()

    def save_language_choice(self, language):
        """Save the user's language choice in a JSON file."""
        preferences = {'language': language}
        settings_path = os.path.join(USER_DATA_DIR, 'resources', 'settings.json')
        os.makedirs(os.path.dirname(settings_path), exist_ok=True)
        with open(settings_path, 'w') as f:
            json.dump(preferences, f)

    def retranslate_ui(self):
        """Update all visible texts with translations."""
        self.privacy_button.setText(self.tr("Privacy Policy"))
        self.terms_button.setText(self.tr("Terms and Conditions"))
        self.footer_text.setText(self.tr("Visit www.leopardo.com | © 2025 by Leopardo - All rights reserved."))

    def init_language(self):
        """Initialize the language based on user preferences or system locale."""
        settings_path = os.path.join(USER_DATA_DIR, 'resources', 'settings.json')

        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')
        else:
            # Default to system locale or English
            system_locale = QLocale.system().name()[:2]  # e.g., 'en', 'fr'
            supported_languages = ['en', 'fr', 'tr', 'ar', 'pt']
            selected_language = system_locale if system_locale in supported_languages else 'en'

        self.switch_language(selected_language)

    def setup_ui(self):
        """Set up the UI elements."""
        self.setStyleSheet("""
            QFrame {
                border: none;
                background-color: #2E7D32;
            }
        """)

        layout = QHBoxLayout(self)

        # Create and configure buttons
        self.privacy_button = self.create_button(self.tr("Privacy Policy"))
        self.privacy_button.clicked.connect(self.on_privacy_clicked)

        self.terms_button = self.create_button(self.tr("Terms and Conditions"))
        self.terms_button.clicked.connect(self.on_terms_clicked)

        # Create footer text
        self.footer_text = QLabel(self.tr("Visit www.leopardo.com | © 2025 by Leopardo - All rights reserved."))
        self.footer_text.setFont(QFont("Arial", 10))
        self.footer_text.setAlignment(Qt.AlignCenter)
        self.footer_text.setStyleSheet("color: white;")

        # Add widgets to layout
        layout.addWidget(self.privacy_button)
        layout.addWidget(self.terms_button)
        layout.addWidget(self.footer_text)

    def create_button(self, text):
        """Helper method to create styled buttons."""
        button = QPushButton(text)
        button.setFont(QFont("Arial", 10))
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #81C784;
            }
        """)
        return button

    def on_privacy_clicked(self):
        self.privacy_clicked.emit()  # Emit the signal

    def on_terms_clicked(self):
        self.terms_clicked.emit()  # Emit the signal

# Example usage
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show the footer section
    footer = FooterSection()
    footer.show()

    sys.exit(app.exec_())
