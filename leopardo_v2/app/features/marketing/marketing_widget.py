import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

class MarketingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        title = QLabel("Marketing Automation Modules")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        main_layout.addSpacing(20)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(20)

        self.add_marketing_button("FB Grup Robot", "", self.open_facebook_robot)
        self.add_marketing_button("WhatsApping", "", self.open_whatsapp_robot)
        self.add_marketing_button("Blogging", "", self.open_blogging_robot)
        self.add_marketing_button("Insta Pro", "", self.open_insta_robot)
        self.add_marketing_button("Telegram Bot", "", self.open_telegram_robot)
        self.add_marketing_button("Status", "", self.open_status_robot)
        self.add_marketing_button("Emailing", "", self.open_emailing_robot)
        self.add_marketing_button("Twitter Bot", "", self.open_twitter_robot)
        self.add_marketing_button("LinkedIn Job", "", self.open_linkedin_robot)
        self.add_marketing_button("Reddit Group", "", self.open_reddit_robot)
        self.add_marketing_button("Snapchat", "", self.open_snapchat_robot)
        self.add_marketing_button("TikTok Pro", "", self.open_tiktok_robot)
        self.add_marketing_button("Discord Grup", "", self.open_discord_robot)
        self.add_marketing_button("YouTube Pro", "", self.open_youtube_robot)

        main_layout.addLayout(self.grid_layout)
        main_layout.addStretch()

    def add_marketing_button(self, text, icon_path, function):
        button = QPushButton(text)
        button.setFont(QFont("Arial", 14))
        button.setStyleSheet("""
            QPushButton {
                background-color: #E91E63;
                color: white;
                border: 2px solid #CCCCCC;
                border-radius: 15px;
                padding: 10px;
                min-width: 150px;
                min-height: 150px;
            }
        """)
        button.clicked.connect(function)

        row = self.grid_layout.rowCount()
        col = self.grid_layout.columnCount()
        if col == 4:
            col = 0
            row += 1

        self.grid_layout.addWidget(button, row, col)

    def open_facebook_robot(self):
        self.open_placeholder_tab("FB Robot")

    def open_whatsapp_robot(self):
        self.open_placeholder_tab("WhatsApp Robot")

    def open_blogging_robot(self):
        self.open_placeholder_tab("Blogging Robot")

    def open_insta_robot(self):
        self.open_placeholder_tab("Insta Pro Robot")

    def open_telegram_robot(self):
        self.open_placeholder_tab("Telegram Bot")

    def open_status_robot(self):
        self.open_placeholder_tab("Status Robot")

    def open_emailing_robot(self):
        self.open_placeholder_tab("Emailing Robot")

    def open_twitter_robot(self):
        self.open_placeholder_tab("Twitter Bot")

    def open_linkedin_robot(self):
        self.open_placeholder_tab("LinkedIn Job Robot")

    def open_reddit_robot(self):
        self.open_placeholder_tab("Reddit Group Robot")

    def open_snapchat_robot(self):
        self.open_placeholder_tab("Snapchat Robot")

    def open_tiktok_robot(self):
        self.open_placeholder_tab("TikTok Pro Robot")

    def open_discord_robot(self):
        self.open_placeholder_tab("Discord Grup Robot")

    def open_youtube_robot(self):
        self.open_placeholder_tab("YouTube Pro Robot")

    def open_placeholder_tab(self, name):
        if hasattr(self.parent(), 'add_feature_tab'):
            self.parent().add_feature_tab(QLabel(f"{name} Placeholder"), name)
        elif hasattr(self, 'parent') and hasattr(self.parent(), 'parent') and hasattr(self.parent().parent(), 'add_feature_tab'):
            self.parent().parent().add_feature_tab(QLabel(f"{name} Placeholder"), name)

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    widget = MarketingWidget()
    widget.show()
    sys.exit(app.exec_())
