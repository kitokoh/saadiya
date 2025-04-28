import json
import os
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QSize
from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPainter
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QFrame, QToolButton, 
    QSizePolicy, QMenu
)

from translation import TranslatorManager

user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

class HeaderSection(QFrame):
    menu_toggled = pyqtSignal()
    quick_action_triggered = pyqtSignal(str)
    language_changed = pyqtSignal(str)

    def __init__(self, parent=None, title="AI Marketing Automation", 
                 app_name="Leopardo AI", slogan="AI Marketing & Management Auto"):
        super().__init__(parent)
        self.translator = QTranslator()
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        
        self.dynamic_title = title
        self.app_name = app_name
        self.slogan = slogan
        
        self.setup_ui()
        self.init_language()
        self.setup_animations()

    def setup_ui(self):
        """Configuration de l'interface sobre et professionnelle"""
        self.setMinimumHeight(100)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(10, 5, 10, 0)

        # 1. Barre supérieure (Logo + Titre)
        top_bar = QHBoxLayout()
        
        # Bouton menu
        self.menu_button = QToolButton()
        self.menu_button.setText("☰")
        self.menu_button.setFont(QFont("Arial", 16))
        self.menu_button.setCursor(Qt.PointingHandCursor)
        self.menu_button.clicked.connect(self.toggle_side_menu)
        top_bar.addWidget(self.menu_button)
        
        # Logo
        self.logo_label = QLabel()
        pixmap = QPixmap("resources/icons/robot-256.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(pixmap)
        top_bar.addWidget(self.logo_label)
        
        # Titre et slogan
        title_layout = QVBoxLayout()
        self.title_label = QLabel(self.dynamic_title)
        self.title_label.setFont(QFont("Arial", 14, QFont.Bold))
        
        self.slogan_label = QLabel(self.slogan)
        self.slogan_label.setFont(QFont("Arial", 10))
        
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.slogan_label)
        top_bar.addLayout(title_layout, stretch=1)
        
        # Bouton utilisateur
        self.user_button = QToolButton()
        self.user_button.setText("👤")
        self.user_button.setPopupMode(QToolButton.InstantPopup)
        
        user_menu = QMenu()
        user_menu.addAction("🔧 Paramètres")
        user_menu.addAction("❓ Aide")
        user_menu.addSeparator()
        user_menu.addAction("🚪 Quitter")
        
        self.user_button.setMenu(user_menu)
        top_bar.addWidget(self.user_button)
        
        main_layout.addLayout(top_bar)

        # 2. Barre d'actions rapides (comme Word/Excel)
        self.quick_actions_bar = QFrame()
        quick_layout = QHBoxLayout(self.quick_actions_bar)
        quick_layout.setContentsMargins(5, 5, 5, 5)
        quick_layout.setSpacing(10)
        
        # Boutons d'actions rapides avec emojis
        actions = [
            ("📝 Nouveau", "new"),
            ("📂 Ouvrir", "open"),
            ("💾 Enregistrer", "save"),
            ("🖨️ Imprimer", "print"),
            ("📊 Statistiques", "stats"),
            ("⚙️ Paramètres", "settings")
        ]
        
        for text, action in actions:
            btn = QToolButton()
            btn.setText(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, a=action: self.quick_action_triggered.emit(a))
            quick_layout.addWidget(btn)
        
        quick_layout.addStretch()
        main_layout.addWidget(self.quick_actions_bar)

        # 3. Menu latéral
        self.side_menu = QWidget(self)
        self.side_menu.setFixedWidth(200)
        self.side_menu.move(-200, 0)
        self.side_menu.setStyleSheet("background-color: #f5f5f5; border-right: 1px solid #e0e0e0;")
        
        side_layout = QVBoxLayout(self.side_menu)
        side_layout.setContentsMargins(5, 20, 5, 5)
        
        menu_items = [
            "🏠 Accueil",
            "📊 Tableau de bord",
            "📈 Analytics",
            "📋 Rapports",
            "🔔 Notifications",
            "🛠️ Outils"
        ]
        
        for item in menu_items:
            btn = QPushButton(item)
            btn.setStyleSheet("text-align: left; padding: 8px; border: none;")
            btn.setCursor(Qt.PointingHandCursor)
            side_layout.addWidget(btn)
        
        side_layout.addStretch()
        self.side_menu.hide()

        # Appliquer le style global
        self.setStyleSheet("""
            HeaderSection {
                background-color: #ffffff;
                border-bottom: 1px solid #e0e0e0;
            }
            QLabel {
                color: #333333;
            }
            #quick_actions_bar {
                background-color: #f8f8f8;
                border-top: 1px solid #e0e0e0;
                border-bottom: 1px solid #e0e0e0;
            }
            QToolButton {
                border: none;
                padding: 5px 8px;
                background: transparent;
                font-size: 12px;
            }
            QToolButton:hover {
                background-color: #eaeaea;
                border-radius: 4px;
            }
        """)

    def setup_animations(self):
        """Configure l'animation du menu latéral"""
        self.menu_animation = QPropertyAnimation(self.side_menu, b"pos")
        self.menu_animation.setDuration(250)
        self.menu_animation.setEasingCurve(QEasingCurve.InOutQuad)

    def toggle_side_menu(self):
        """Bascule le menu latéral"""
        if self.side_menu.isVisible():
            self.menu_animation.setStartValue(QPoint(-200, 0))
            self.menu_animation.setEndValue(QPoint(-200, 0))
            self.menu_animation.finished.connect(lambda: self.side_menu.hide())
        else:
            self.side_menu.show()
            self.menu_animation.setStartValue(QPoint(-200, 0))
            self.menu_animation.setEndValue(QPoint(0, 0))
            self.menu_animation.finished.disconnect()
        
        self.menu_animation.start()

    # ... (conservez vos méthodes existantes switch_language, save_language_choice, etc.)

    def update_title(self, new_title):
        """Méthode pour changer dynamiquement le titre."""
        self.title_label.setText(new_title)
        self.dynamic_title = new_title


class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.header = HeaderSection()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.header)
        
        # Connecter les signaux
        self.header.quick_action_triggered.connect(lambda action: print(f"Action: {action}"))
        self.header.language_changed.connect(lambda lang: print(f"Langue changée: {lang}"))


if __name__ == "__main__":
    app = QApplication([])
    window = TestWindow()
    window.resize(800, 600)
    window.show()
    app.exec_()