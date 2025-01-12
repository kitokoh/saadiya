import os
import sys
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEvent
from PyQt5.QtGui import QFont, QMovie, QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout, QApplication, QPushButton, QProgressBar

user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
import json 
from PyQt5.QtCore import Qt, QTranslator, QLocale

class WelcomeDialog(QDialog):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle(self.tr("🎉 Welcome to Leopardo.ai! 🎉"))

        # Configuration principale de la fenêtre
        self.setGeometry(100, 100, 1320, 900)  # Taille de la fenêtre
        self.setWindowIcon(QIcon('resources/icons/robot-icons-30497.png'))

        self.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #F9FAFB, stop:1 #E3EAFD); border-radius: 10px;")
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        # Load welcome sound
        self.welcome_sound = QSound("resources/sounds/welcome_sound.wav")
        self.welcome_sound.play()

        # First confetti GIF
        self.confetti_label1 = QLabel(self)
        confetti_movie1 = QMovie("resources/sounds/confetti2.gif")
        self.confetti_label1.setMovie(confetti_movie1)
        confetti_movie1.start()

        # Header with pulsing animation
        self.welcome_message = QLabel(f"<h1 style='color:#2E86C1;'>{self.tr('Hello,')} {username}!</h1>", self)
        self.welcome_message.setAlignment(Qt.AlignCenter)
        self.welcome_message.setStyleSheet("font-weight: bold; font-size: 24px;")
        self.pulse_effect(self.welcome_message)

        # Second confetti GIF with delay
        self.confetti_label2 = QLabel(self)
        confetti_movie2 = QMovie("resources/sounds/confetti22.gif")
        self.confetti_label2.setMovie(confetti_movie2)
        QTimer.singleShot(confetti_movie1.frameCount() * confetti_movie1.nextFrameDelay(), confetti_movie2.start)

        # Main message and rotating tips
        self.main_text = QLabel(
            f"<p style='font-size:16px;'>"
            f"{self.tr('Welcome to')} <strong>Leopardo.ai</strong>, {self.tr('your AI-powered companion for next-level marketing automation.')}"
            "<br><br>{self.tr('Get ready to')} <em>automate</em>, <em>connect</em>, and <em>expand</em> your brand effortlessly with cutting-edge technology!</p>", self)
        self.main_text.setAlignment(Qt.AlignCenter)
        self.main_text.setStyleSheet("color: #34495E; font-size: 16px;")

        # Rotating tips below main text
        self.tip_label = QLabel("", self)
        self.tip_label.setAlignment(Qt.AlignCenter)
        self.tip_label.setStyleSheet("color: #4A4A4A; font-size: 12px; font-style: italic;")
        self.tips = [
            self.tr("💡 Tip: Schedule posts across multiple platforms with one click!"),
            self.tr("🚀 Feature: Use Leopardo.ai to engage your audience on autopilot."),
            self.tr("📈 Did you know? Leopardo.ai optimizes your marketing strategy with ease!")
        ]
        self.show_rotating_tips()

        # Animated "Get Started" Button with Tooltip and Sound
        self.get_started_button = QPushButton(self.tr("🚀 Get Started"), self)
        self.get_started_button.setToolTip(self.tr("Click to begin your journey with Leopardo.ai!"))
        self.get_started_button.setStyleSheet("""
            QPushButton {
                background-color: #2E86C1; color: white; font-size: 14px;
                padding: 10px 20px; border-radius: 5px; font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1C5F8A;
            }
        """)
        self.get_started_button.clicked.connect(self.on_get_started_click)
        self.add_hover_animation(self.get_started_button)

        # Progress bar to simulate loading
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #1C5F8A;
                border-radius: 5px;
                background-color: #E3EAFD;
            }
            QProgressBar::chunk {
                background-color: #2E86C1;
                width: 10px;
            }
        """)
        self.progress_bar.setFixedHeight(6)
        self.animate_progress()

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.confetti_label1, alignment=Qt.AlignCenter)
        layout.addWidget(self.welcome_message, alignment=Qt.AlignCenter)
        layout.addWidget(self.confetti_label2, alignment=Qt.AlignCenter)
        layout.addWidget(self.main_text, alignment=Qt.AlignCenter)
        layout.addWidget(self.tip_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)
        layout.addWidget(self.get_started_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)
    def switch_language(self, language):
        """Permet de changer la langue."""
        # if language == "en":
        #     self.translator.load("resources/lang/en_US/ui/welcomeStyle_translated.qm")
        # elif language == "fr":
        #     self.translator.load("resources/lang/fr_FR/ui/welcomeStyle_translated.qm")
        # elif language == "tr":
        #     self.translator.load("resources/lang/tr_TR/ui/welcomeStyle_translated.qm")
        # elif language == "ar":
        #     self.translator.load("resources/lang/ar_AR/ui/welcomeStyle_translated.qm")


        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','ui','welcomeStyle_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','ui','welcomeStyle_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','ui','welcomeStyle_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','ui','welcomeStyle_translated.qm'))
        elif language == "pt":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','pt_BR','ui','welcomeStyle_translated.qm'))

        # Installer le traducteur pour appliquer la nouvelle langue
        QApplication.instance().installTranslator(self.translator)
        
            # Sauvegarder le choix de l'utilisateur
        self.save_language_choice(language)


        # Réappliquer la traduction sur tous les éléments visibles de l'interface
        self.retranslateUi()

    def save_language_choice(self, language):
        """Sauvegarde le choix de langue de l'utilisateur dans un fichier JSON."""
        preferences = {'language': language}
        with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'w') as f:
            json.dump(preferences, f)
    def retranslateUi(self):
        """Recharge les textes traduits dans l'interface."""
        # self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # # Par exemple, pour les actions du menu :
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.language_menu.setTitle(self.tr('Langue'))
        pass
    def init_language(self):
        """Initialise la langue par défaut à celle du système ou à celle choisie par l'utilisateur."""
        # Vérifiez si le fichier de préférences existe
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')  # Par défaut à l'anglais si non trouvé
        else:
            # Obtenir le code de langue du système
            system_locale = QLocale.system().name()[:2]  # Par exemple: 'fr', 'en', 'tr', etc.

            # Dictionnaire pour mapper les codes de langue aux traductions
            language_map = {
                'en': 'en',
                'fr': 'fr',
                'tr': 'tr',
                'ar': 'ar',
                'pt': 'pt',

            }

            # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)


    def pulse_effect(self, widget):
        # Pulsing animation effect for welcome text
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(1000)
        animation.setStartValue(0.8)
        animation.setEndValue(1.0)
        animation.setLoopCount(-1)
        animation.start()

    def animate_progress(self):
        # Animate progress bar for loading effect
        self.progress_bar.setValue(0)
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.increment_progress)
        self.progress_timer.start(30)

    def increment_progress(self):
        value = self.progress_bar.value()
        if value < 100:
            self.progress_bar.setValue(value + 1)
        else:
            self.progress_timer.stop()

    def show_rotating_tips(self):
        # Rotating tips with timer
        self.tip_index = 0
        self.tip_timer = QTimer(self)
        self.tip_timer.timeout.connect(self.update_tip)
        self.tip_timer.start(3000)

    def update_tip(self):
        self.tip_label.setText(self.tips[self.tip_index])
        self.tip_index = (self.tip_index + 1) % len(self.tips)

    def on_get_started_click(self):
        # Play sound and close dialog on button click
        QSound.play("resources/sounds/click_sound.wav")
        self.accept()

    def add_hover_animation(self, button):
        # Create a subtle hover effect by changing the size
        button.installEventFilter(self)

    def eventFilter(self, source, event):
        if source == self.get_started_button:
            if event.type() == QEvent.Enter:
                self.get_started_button.setStyleSheet("""
                    QPushButton {
                        background-color: #2E86C1; color: white; font-size: 16px;
                        padding: 12px 24px; border-radius: 5px; font-weight: bold;
                    }
                """)
            elif event.type() == QEvent.Leave:
                self.get_started_button.setStyleSheet("""
                    QPushButton {
                        background-color: #2E86C1; color: white; font-size: 14px;
                        padding: 10px 20px; border-radius: 5px; font-weight: bold;
                    }
                """)
        return super().eventFilter(source, event)

def main():
    app = QApplication(sys.argv)
    username = "User"  
    dialog = WelcomeDialog(username)
    dialog.exec_()

if __name__ == "__main__":
    main()
