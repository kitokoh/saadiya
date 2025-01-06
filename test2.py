import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QWidget, QScrollArea, QLineEdit, QMessageBox, QComboBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class Nova360Setup(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nova360 - Configuration")
        self.setGeometry(100, 100, 1200, 800)

        # Variables JSON structure
        self.user_data = {
            "bots": {
                "twitter_bot": False,
                "linkedin_bot": False,
                "pinterest_bot": False,
                "snapchat_bot": False,
                "tiktok_bot": False,
                "reddit_bot": False,
                "youtube_bot": False,
                "facebook_bot": False,
                "whatsapp_bot": False,
                "blogging_bot": False,
                "instagram_bot": False,
                "telegram_bot": False,
                "branding_bot": False,
                "emailing_bot": False,
            },
            "modules": {},
            "info": {
                "name": "",
                "email": "",
                "role": ""
            }
        }

        self.current_platform = None
        self.platforms = {
            "Facebook": ["Group Share", "Auto Comment", "Page Management"],
            "Twitter": ["Auto Tweet", "Hashtag Tracker", "Analytics"],
            "LinkedIn": ["Connection Manager", "Message Automation", "Profile Insights"],
            "Instagram": ["Auto Post", "Story Scheduler", "Hashtag Analyzer"],
            "Pinterest": ["Pin Manager", "Board Insights", "Scheduler"],
            "Snapchat": ["Story Auto Post", "Audience Insights"],
            "TikTok": ["Video Auto Post", "Trend Tracker"],
            "Reddit": ["Post Scheduler", "Subreddit Insights"],
            "YouTube": ["Channel Manager", "Comment Moderator", "Analytics Tracker"],
            "WhatsApp": ["WA CRM", "WA Plus", "Bulk Messaging"],
            "Telegram": ["Group Manager", "Channel Insights"],
            "Blogging": ["Content Scheduler", "SEO Insights"],
            "Branding": ["Logo Generator", "Brand Kit Manager"],
            "Emailing": ["Newsletter Scheduler", "Email Analytics"],
        }

        # UI setup
        self.setup_ui()

    def setup_ui(self):
        """Setup the main UI layout."""
        main_layout = QVBoxLayout()

        # Dynamic green bar to show selected modules
        self.selection_bar = QLabel("Modules sélectionnés : Aucun")
        self.selection_bar.setFont(QFont("Arial", 12, QFont.Bold))
        self.selection_bar.setStyleSheet(
            "padding: 10px; background-color: #28a745; color: white; border-radius: 5px; margin-bottom: 10px;"
        )
        main_layout.addWidget(self.selection_bar)

        # Scroll area for platform selection
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        content_layout = QVBoxLayout()

        title = QLabel("Quels réseaux sociaux souhaitez-vous configurer ?")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title)

        for platform in self.platforms.keys():
            button = QPushButton(platform)
            button.setFont(QFont("Arial", 14))
            button.setStyleSheet(
                "padding: 15px; margin: 10px; background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 5px;"
            )
            button.clicked.connect(lambda _, p=platform: self.show_module_selection(p))
            content_layout.addWidget(button)

        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Finalize button
        finalize_button = QPushButton("Finaliser la configuration")
        finalize_button.setFont(QFont("Arial", 14))
        finalize_button.setStyleSheet(
            "padding: 15px; background-color: #007bff; color: white; border-radius: 5px;"
        )
        finalize_button.clicked.connect(self.finalize_setup)
        main_layout.addWidget(finalize_button)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def update_selection_bar(self):
        """Update the green bar with the currently selected platforms."""
        selected_platforms = [
            platform for platform, selected in self.user_data["bots"].items() if selected
        ]
        text = (
            "Modules sélectionnés : " + ", ".join(selected_platforms)
            if selected_platforms
            else "Aucun"
        )
        self.selection_bar.setText(text)

    def show_module_selection(self, platform):
        """Display the modules for the selected platform."""
        self.current_platform = platform
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel(f"Modules disponibles pour {platform}")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        for module in self.platforms[platform]:
            button = QPushButton(module)
            button.setFont(QFont("Arial", 14))
            button.setStyleSheet(
                "padding: 15px; margin: 10px; background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 5px;"
            )
            button.clicked.connect(lambda _, m=module: self.add_module(m))
            layout.addWidget(button)

        back_button = QPushButton("Retour")
        back_button.setFont(QFont("Arial", 14))
        back_button.setStyleSheet(
            "padding: 15px; margin: 10px; background-color: #d9534f; color: white; border-radius: 5px;"
        )
        back_button.clicked.connect(self.setup_ui)
        layout.addWidget(back_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def add_module(self, module):
        """Add the selected module to the JSON structure."""
        self.user_data["bots"][f"{self.current_platform.lower()}_bot"] = True
        if self.current_platform not in self.user_data["modules"]:
            self.user_data["modules"][self.current_platform] = []
        self.user_data["modules"][self.current_platform].append(module)
        self.update_selection_bar()

    def finalize_setup(self):
        """Finalize the setup and save the user data to a JSON file."""
        try:
            with open("settings.json", "w") as file:
                json.dump(self.user_data, file, indent=4)
            QMessageBox.information(self, "Succès", "Vos paramètres ont été enregistrés avec succès !")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Nova360Setup()
    window.show()
    sys.exit(app.exec_())
