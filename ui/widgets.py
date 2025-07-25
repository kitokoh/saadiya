from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialog, QPushButton
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtGui import QPixmap

class AccueilWidget(QWidget):
    """Widget for the 'Accueil' tab."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(self.tr("Welcome to the Accueil tab"))
        layout.addWidget(label)
        self.setLayout(layout)


class SearchWidget(QWidget):
    """Widget for the 'Search' tab."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(self.tr("Search Page"))
        layout.addWidget(label)
        self.setLayout(layout)


class SettingsWidget(QWidget):
    """Widget for the 'Settings' tab."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(self.tr("Settings Page"))
        layout.addWidget(label)
        self.setLayout(layout)


class HelpWidget(QWidget):
    """Widget for the 'Help' tab."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(self.tr("Help Page"))
        layout.addWidget(label)
        self.setLayout(layout)


class AboutDialog(QDialog):
    """Generic dialog for 'About' Leopardo AI."""
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize and load translations
        # self.translator_manager = TranslatorManager()
        # self.translator_manager.load_translations()

        # Window configuration
        self.setWindowTitle(self.tr("About Leopardo AI"))
        layout = QVBoxLayout()

        # Main content
        label = QLabel(self.tr(
            """
            <div style='background-color:#F5F7FA; padding:15px; border-radius:10px;'>
                <h1 style='color:#1A5276; font-size:24px; font-weight:bold; text-align:center;'>
                    Welcome to Leopardo AI
                </h1>

                <p style='font-size:16px; color:#333333; text-align:center;'>
                    <strong>Your All-in-One AI-Powered Automation Solution</strong>
                </p><br>

                <div style='padding: 10px; border-left: 4px solid #1A5276;'>
                    <p style='font-size:14px; color:#5D6D7E; line-height:1.6; margin:0 20px;'>
                        Leopardo AI is the ultimate tool for businesses, brands, and creators looking to simplify and scale their online presence.<br>
                        Harnessing advanced AI, Leopardo AI automates social media, content creation, engagement, and growth strategies.<br>
                        Focus on what matters most while Leopardo AI handles the execution.
                    </p>
                </div><br>

                <h3 style='color:#1A5276; font-size:18px; margin-top:20px; text-align:center;'>Core Features</h3><br>

                <ul style='font-size:14px; color:#4A4A4A; padding-left: 40px;'>
                    <li style='margin-bottom:10px;'><strong>🌐 Smart Scheduling:</strong> Plan and post across multiple platforms for maximum efficiency.</li><br>
                    <li style='margin-bottom:10px;'><strong>🤖 AI-Driven Engagement:</strong> Automate replies, comments, and audience interactions seamlessly.</li><br>
                    <li><strong>📂 Integrated Management:</strong> Organize media, campaigns, and teams with ease.</li>
                </ul><br>

                <p style='font-size:14px; color:#5D6D7E; line-height:1.6; text-align:center;'>
                    Join a growing community of professionals who trust Leopardo AI to optimize their automation journey.<br>
                    Save time, grow faster, and achieve more with AI at your fingertips.
                </p><br>

                <p style='font-size:11px; color:#888888; text-align:center; margin-top:20px;'>
                    © 2024 Leopard AI |
                    <a href='https://www.Leopardopro.com' style='color:#1A5276; text-decoration:none;'>www.Leopardopro.com</a>
                </p>
            </div>
            """
        ))
        layout.addWidget(label)

        # Close button
        close_button = QPushButton(self.tr("Close"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        # Apply the layout
        self.setLayout(layout)

        # Animation for smooth transition
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()


class CertificateDialog(QDialog):
    """Dialog for 'Certificate' (adapted for Leopard AI)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Certificate"))
        layout = QVBoxLayout()

        # Label with content adapted for Leopard AI
        label = QLabel(self.tr(
                "<div style='background-color:#FAF3E0; padding:15px; border-radius:8px;'>"
                "<h2 style='color:#D35400; font-size:20px; text-align:center;'>Your License Expiration</h2>"

                "<p style='font-size:14px; color:#4A4A4A; line-height:1.6;'>"
                "Your license is currently valid until <strong style='color:#D35400;'>December 31, 202x</strong>.<br>"
                "To continue enjoying all the premium features of <strong>Leopardo I</strong>, please consider renewing your license before this date.<br>"
                "</p><br>"

                "<div style='padding: 10px; border-left: 4px solid #D35400; margin: 10px 0;'>"
                "<p style='font-size:13px; color:#7F8C8D; margin:0 20px;'>"
                "After this date, your access to premium features will be restricted. You will still be able to access your account but with limited features until your license is renewed."
                "</p>"
                "</div><br>"

                "<h3 style='color:#D35400; font-size:16px;'>In Case of Issues</h3>"

                "<ul style='font-size:13px; color:#4A4A4A; padding-left: 40px;'>"
                "<li style='margin-bottom:10px;'>If your instance stops working, check the internet connection and ensure the license is active.</li><br>"
                "<li>Contact our technical support if you encounter additional difficulties.</li>"
                "</ul><br>"

                "<p style='font-size:12px; color:gray; text-align:center;'>"
                "For any assistance, please visit <a href='https://support.leopardai.com' style='color:#D35400; text-decoration:none;'>our support center</a>."
                "</p>"
                "</div>"
            ))
        layout.addWidget(label)

        # Close button
        close_button = QPushButton(self.tr("Close"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)

        # Animation for smooth opening
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()
