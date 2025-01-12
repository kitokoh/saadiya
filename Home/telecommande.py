import json
import logging
import os
import platform
import requests
import subprocess
import sys
import webbrowser
import win32con
import win32gui
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtCore import QPropertyAnimation, pyqtProperty
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import Qt, QTimer, QTime, QDateTime, QProcess, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QPixmap
from PyQt5.QtGui import QMovie, QColor
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QSplitter, QTabWidget, QHBoxLayout,
    QPushButton, QLabel, QSizePolicy, QGraphicsDropShadowEffect, QDesktopWidget,
    QMainWindow, QTextEdit, QMessageBox, QDialog
)
from PyQt5.QtWidgets import QGraphicsOpacityEffect

try:
    import pygetwindow as gw
except ImportError:
    gw = None  # Pour gérer Windows uniquement

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler("fb_robot_log.txt"),  # Log file
#         logging.StreamHandler()  # Console output
#     ]
# )

from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtGui import QColor, QMovie
from PyQt5.QtWidgets import QGraphicsOpacityEffect


from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtGui import QColor, QMovie
from PyQt5.QtWidgets import QGraphicsOpacityEffect



from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QColor, QFont, QMovie
from PyQt5.QtWidgets import (
    QApplication, QLabel, QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QVBoxLayout, 
    QWidget, QProgressBar, QPushButton, QHBoxLayout
)

import json
import os
from PyQt5.QtCore import Qt, QPoint, QRect, QPropertyAnimation
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog, QPushButton, QHBoxLayout, QWidget, QMessageBox


class FirstTimeGuide(QDialog):
    SETTINGS_PATH = (
        os.path.expanduser("~/AppData/Roaming/saadiya/resources/settings.json")
        if os.name == "nt"
        else os.path.expanduser("~/.saadiya/resources/settings.json")
    )

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Leopardo AI - First Time Guide")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(parent.size())

        self.settings = self.load_settings()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.init_ui()
        self.setLayout(self.layout)

        self.steps = self.get_steps()
        self.current_step = 0

        self.highlight_overlay = QLabel(self)
        self.init_highlight_overlay()

        self.show_step()

    def init_ui(self):
        self.overlay_label = QLabel()
        self.overlay_label.setAlignment(Qt.AlignCenter)
        self.overlay_label.setStyleSheet(self.get_label_stylesheet())
        self.layout.addWidget(self.overlay_label)

        nav_layout = QHBoxLayout()
        self.next_button = self.create_button("Next", "#3498db", "#2980b9", self.next_step)
        nav_layout.addWidget(self.next_button)

        self.close_button = self.create_button("Skip", "#e74c3c", "#c0392b", self.skip_guide)
        nav_layout.addWidget(self.close_button)

        self.layout.addLayout(nav_layout)

    def create_button(self, text, bg_color, hover_color, callback):
        button = QPushButton(text)
        button.setStyleSheet(self.get_button_stylesheet(bg_color, hover_color))
        button.clicked.connect(callback)
        return button

    def init_highlight_overlay(self):
        self.highlight_overlay.setStyleSheet(self.get_highlight_stylesheet())
        self.highlight_overlay.hide()

    def load_settings(self):
        try:
            if os.path.exists(self.SETTINGS_PATH):
                with open(self.SETTINGS_PATH, "r") as file:
                    return json.load(file)
            return {"remotefirst": "False"}
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Error", "Invalid settings file. Recreating default settings.")
            return {"remotefirst": "False"}

    def save_settings(self):
        os.makedirs(os.path.dirname(self.SETTINGS_PATH), exist_ok=True)
        with open(self.SETTINGS_PATH, "w") as file:
            json.dump(self.settings, file)

    def get_steps(self):
        return [
            {
                "text": "Cliquez sur le bouton circulaire au centre pour accéder au panneau de contrôle.",
                "target": self.parent.open_panel_btn,
            },
            {
                "text": "Cliquez sur le bouton rectangulaire à gauche pour démarrer le robot FB.",
                "target": self.parent.button_tabs.widget(0) if self.parent.button_tabs.count() > 0 else None,
            },
        ]

    def show_step(self):
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self.overlay_label.setText(step["text"])
            self.highlight_widget(step["target"])
        else:
            QMessageBox.information(self, "Guide Complete", "Vous avez terminé le guide initial.")
            self.close()

    def highlight_widget(self, widget):
        if not widget or not widget.isVisible():
            return

        rect = widget.geometry()
        offset = widget.mapToGlobal(QPoint(0, 0))
        self.highlight_overlay.setGeometry(QRect(offset.x(), offset.y(), rect.width(), rect.height()))

        animation = QPropertyAnimation(self.highlight_overlay, b"geometry")
        animation.setDuration(500)
        animation.setStartValue(QRect(offset.x(), offset.y(), 0, 0))
        animation.setEndValue(QRect(offset.x(), offset.y(), rect.width(), rect.height()))
        animation.start()

        self.highlight_overlay.show()

    def next_step(self):
        self.highlight_overlay.hide()
        self.current_step += 1
        self.show_step()

    def skip_guide(self):
        self.settings["remotefirst"] = "True"
        self.save_settings()
        self.close()

    @staticmethod
    def get_label_stylesheet():
        return (
            "QLabel {"
            "    color: white;"
            "    font-size: 18px;"
            "    font-weight: bold;"
            "    background-color: rgba(0, 0, 0, 0.7);"
            "    border-radius: 10px;"
            "    padding: 15px;"
            "    font-family: Arial, sans-serif;"
            "}"
        )

    @staticmethod
    def get_button_stylesheet(bg_color, hover_color):
        return (
            f"QPushButton {{"
            f"    background-color: {bg_color};"
            f"    color: white;"
            f"    font-size: 14px;"
            f"    border-radius: 10px;"
            f"    padding: 10px 20px;"
            f"    font-family: Arial, sans-serif;"
            f"}}"
            f"QPushButton:hover {{"
            f"    background-color: {hover_color};"
            f"}}"
        )

    @staticmethod
    def get_highlight_stylesheet():
        return (
            "QLabel {"
            "    border: 3px solid #f39c12;"
            "    background-color: rgba(0, 0, 0, 0.5);"
            "}"
        )


class AnimatedScreen(QLabel):
    def __init__(self, text="Ready to Control", parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(200)

                # Digital screen with modern styling
        self.setStyleSheet(self.get_screen_stylesheet())


        # Ajout des animations et effets
        self.apply_shadow_effect()
        self.add_text_glow_animation()
        self.add_pulsing_border_animation()

        # Initialisation du GIF
        self.background_movie = None

        # Initialisation de l'opacité du texte
        self._text_opacity = 1.0  # Définir la valeur initiale de l'opacité

        # Transition de texte
        self.text_animation = QPropertyAnimation(self, b"textOpacity")

    def get_text_opacity(self):
        return self._text_opacity

    def set_text_opacity(self, opacity):
        self._text_opacity = opacity
        self.setStyleSheet(
            f"""
            QLabel {{
                color: rgba(0, 255, 136, {int(opacity * 255)});
                font-size: 24px;
                font-weight: bold;
            }}
            """
        )

    textOpacity = pyqtProperty(float, get_text_opacity, set_text_opacity)

  


    textOpacity = pyqtProperty(float, get_text_opacity, set_text_opacity)

    def apply_shadow_effect(self):
        """Ajoute une ombre portée au texte."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(3, 3)
        shadow.setColor(QColor(0, 0, 0, 200))  # Noir semi-transparent
        self.setGraphicsEffect(shadow)

    def get_screen_stylesheet(self):
        """Renvoie le style CSS pour le QLabel."""
        return """
            QLabel {
                background-color: rgba(45, 45, 45, 180);  /* Arrière-plan semi-transparent */
                color: #00ff88;  /* Couleur du texte */
                font-size: 24px;  /* Taille du texte */
                font-weight: bold;  /* Texte en gras */
                border-radius: 15px;  /* Coins arrondis */
                padding: 15px;  /* Espacement intérieur */
                border: 2px solid #00ff88;  /* Bordure verte */
            }
        """

    def add_text_glow_animation(self):
        """Ajoute une animation de glow au texte."""
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)

        self.glow_animation = QPropertyAnimation(effect, b"opacity")
        self.glow_animation.setDuration(2000)  # Durée de l'animation en ms
        self.glow_animation.setStartValue(0.8)
        self.glow_animation.setKeyValueAt(0.5, 1.0)
        self.glow_animation.setEndValue(0.8)
        self.glow_animation.setLoopCount(-1)  # Animation infinie
        self.glow_animation.start()

    def add_pulsing_border_animation(self):
        """Ajoute une animation pulsante à la bordure."""
        self.border_animation = QPropertyAnimation(self, b"styleSheet")
        self.border_animation.setDuration(1500)
        self.border_animation.setLoopCount(-1)  # Animation infinie

        # Définition des styles pour l'animation
        start_style = """
            QLabel {
                background-color: rgba(45, 45, 45, 180);
                color: #00ff88;
                font-size: 24px;
                font-weight: bold;
                border-radius: 15px;
                padding: 15px;
                border: 3px solid #00ff88;  /* Bordure verte */
            }
        """
        end_style = """
            QLabel {
                background-color: rgba(45, 45, 45, 180);
                color: #00ff88;
                font-size: 24px;
                font-weight: bold;
                border-radius: 15px;
                padding: 15px;
                border: 3px solid #8800ff;  /* Bordure violette */
            }
        """

        self.border_animation.setStartValue(start_style)
        self.border_animation.setEndValue(end_style)
        self.border_animation.start()

    def set_background_gif(self, gif_path):
        """Ajoute ou change le GIF animé comme arrière-plan."""
        if self.background_movie:
            self.background_movie.stop()  # Arrête l'ancien GIF

        self.background_movie = QMovie(gif_path)
        if self.background_movie.isValid():
            self.setMovie(self.background_movie)
            self.background_movie.start()
        else:
            print(f"Erreur : Le fichier GIF '{gif_path}' est introuvable ou invalide.")

    def add_typing_text(self, text, interval=100):
        """Affiche un texte avec un effet dactylographique."""
        self.current_text = ""
        self.full_text = text
        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self._append_next_char)
        self.typing_timer.start(interval)

    def _append_next_char(self):
        """Ajoute le caractère suivant au texte."""
        if len(self.current_text) < len(self.full_text):
            self.current_text += self.full_text[len(self.current_text)]
            self.setText(self.current_text)
        else:
            self.typing_timer.stop()

    def add_progress_bar(self):
        """Ajoute une barre de progression sous le texte."""
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(10, self.height() - 30, self.width() - 20, 20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(45, 45, 45, 180);
                border: 1px solid #00ff88;
                border-radius: 10px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #00ff88;
                border-radius: 10px;
            }
        """)
        self.progress_bar.setValue(50)  # Par exemple, pourcentage actuel




class RemoteControl(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark_theme = True  # Default to dark mode
        self.settings = self.load_settings()  # Chargez les paramètres avant d'initialiser l'interface

        self.initUI()
    def load_settings(self):
        """
        Charge le fichier settings.json. Si le fichier n'existe pas, crée un fichier par défaut.
        """
        settings_path = os.path.expanduser(
            "~/AppData/Roaming/saadiya/resources/settings.json" if os.name == "nt" else "~/.saadiya/resources/settings.json"
        )
        if not os.path.exists(settings_path):
            # Si le fichier n'existe pas, créez un fichier par défaut
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            default_settings = {
                "language": "en",
                "fb_robot": "False",
                "multi_fb": "False",
                "walplus": "False",
                "wa_crm": "False",
                "fb_comment": "False",
                "insta": "False",
                "in_job": "False",
                "blog": "False",
                "ytb": "False",
                "pin": "False",
                "x": "False",
                "tok": "False",
                "remotefirst": "False",
                "pannel": "first"
            }
            with open(settings_path, "w") as file:
                json.dump(default_settings, file)
            return default_settings
        else:
            # Charger les paramètres existants
            with open(settings_path, "r") as file:
                return json.load(file)

    def save_settings(self):
        """
        Sauvegarde les paramètres dans le fichier settings.json.
        """
        settings_path = os.path.expanduser(
            "~/AppData/Roaming/saadiya/resources/settings.json" if os.name == "nt" else "~/.saadiya/resources/settings.json"
        )
        with open(settings_path, "w") as file:
            json.dump(self.settings, file)



    def initUI(self):
        # Vérifiez si c'est la première exécution



        self.setWindowTitle("Leopardo AI - Remote Control")
        self.setWindowIcon(QIcon('../resources/icons/robot-icons-30504-Windows.ico'))  # Assurez-vous que le chemin de l'icône est correct

        self.setFixedSize(450, 730)  # Set fixed size for the window

        # Make the window always stay on top
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Positionner la fenêtre à droite de l'écran
        screen_geometry = QDesktopWidget().availableGeometry()
        window_width = 450  # Largeur de la fenêtre
        window_height = 700  # Hauteur de la fenêtre

        # Calculer les coordonnées pour aligner à droite
        x = screen_geometry.width() - window_width - 10
        y = (screen_geometry.height() - window_height) // 2 - 70 # Centré verticalement

        self.move(x, y)


    # Vérification de la première utilisation
# Vérifiez si c'est la première exécution
        # if self.settings.get("remotefirst", "False") == "False":
        #     guide = FirstTimeGuide(self)
        #     guide.exec_()

                # Digital screen with modern styling
#         self.screen = QLabel("Ready to Control")
#         self.screen.setFixedHeight(self.height() // 5)
#         self.screen.setAlignment(Qt.AlignCenter)
#         self.apply_shadow_effect 1()
#         self.screen.setStyleSheet(self.get_screen_stylesheet())

# # Ajout de l'animation de glow
#         self.add_text_glow_animation()
#         self.set_background_gif("path/to/your/background.gif")  # Exemple : 'assets/animated-bg.gif'
#         self.screen.add_pulsing_border_animation()
#         main_layout.addWidget(self.screen)




        # Initialisation de l'écran principal
        self.screen = AnimatedScreen("Ready to Contro2222l", self)
        # Définir un GIF en arrière-plan
        self.screen.set_background_gif("resources/gifs/1.gif")  # Par exemple : 'assets/animated-bg.gif'
        self.screen.get_screen_stylesheet()

        # Ajout d'une animation de bordure pulsante
        self.screen.add_pulsing_border_animation()

        # Ajout de l'écran au layout principal
        main_layout.addWidget(self.screen)

        #self.activate_light("Module Chosen")
        lambda: self.activate_light1("Stategie Marketing School ")

        # Bouton pour changer le GIF d'arrière-plan
        gif_path = "resources/gifs/1.gif"  # Chemin du GIF sélectionné
        self.change_background_gif(gif_path)
        # Central area: circular buttons and small buttons
        central_layout = QHBoxLayout()

        # Small buttons on the left
            #         "Fb Robot": lambda: self.execute_fb_robot_in_tab(),
            # "Multi Fb": lambda: self.on_button_click("fb_robot.exe", "Fb Robot Log"),
            # "WA": self.run_fb_robot,
            # "Insta": lambda: self.open_terminal_tab("Insta", "insta_tool.exe"),
        left_buttons = QVBoxLayout()

        button_actions = {
            "FB Robot": lambda: self.execute_robot_in_tab("FB Robot","Robot satarting","resources/gifs/fb_robot.gif"),
            "Multi FB": lambda: self.execute_robot_in_tab("Multi FB","Robot satarting","resources/gifs/multi_fb.gif"),
            "WA +": lambda: self.execute_robot_in_tab("WA +","Robot satarting","resources/gifs/wa.gif"),
            "WA CRM": lambda: self.execute_robot_in_tab("WA CRM","Robot satarting","resources/gifs/wa_crm.gif"),
            "FB Comment": lambda: self.execute_robot_in_tab("FB Comment","Robot satarting","resources/gifs/fb_comment.gif"),
            "Insta": lambda: self.execute_robot_in_tab("Insta","Robot satarting","resources/gifs/insta.gif"),

        }
        self.button_states = {
            "FB Robot": False  # True signifie que le bouton est activé
            
        }
        for name, icon in [("FB Robot", "resources/icons/fb_robot.ico"), ("Multi FB", "resources/icons/multi_fb.ico"),
                        ("WA +", "resources/icons/wa.png"), ("WA CRM", "resources/icons/wa_crm.png"),("FB Comment", "resources/icons/fb_comment.png"),("Insta", "resources/icons/insta.ico")]:
            btn = self.create_small_button(name, icon)
            self.apply_shadow_effect(btn)
            left_buttons.addWidget(btn)

            if name in button_actions:
                btn.clicked.connect(button_actions[name])
        # Vérification de l'état de Nova360
        self.nova360_installed = self.is_nova360_installed()
        self.button_text = "Panel" if self.nova360_installed else "Installing..."
        # Circular buttons in the center
        circle_buttons_layout = QVBoxLayout()
        self.open_panel_btn = self.create_circular_button2(self.button_text , "resources/icons/openpanel.png")
        self.start_robots_btn = self.create_circular_button2("Start All", "resources/icons/pannel.png")
        self.choice_module_btn = self.create_circular_button2("Strategie", "resources/icons/school.png")







        button_actions2 = {
            "IN Job": lambda: self.execute_robot_in_tab("IN Job","Robot satarting","resources/gifs/in_job.gif"),
            "Blog": lambda: self.execute_robot_in_tab("Blog","Robot satarting","resources/gifs/blog.gif"),
            "YTB": lambda: self.execute_robot_in_tab("YTB","Robot satarting","resources/gifs/ytb.gif"),
            "PIN": lambda: self.execute_robot_in_tab("PIN","Robot satarting","resources/gifs/pin.gif"),
            "X": lambda: self.execute_robot_in_tab("X","Robot satarting","resources/gifs/x.gif"),
            "TOK": lambda: self.execute_robot_in_tab("TOK","Robot satarting","resources/gifs/tok.gif"),

        }

        #pour le buttons executle all 
        self.button_actionss = {
            "FB Robot": lambda: self.execute_robot_in_tab("FB Robot","Robot satarting","resources/gifs/fb_robot.gif"),
            "WA +": lambda: self.execute_robot_in_tab("WA +","Robot satarting","resources/gifs/1.gif"),
            "WA CRM": lambda: self.execute_robot_in_tab("WA CRM","Robot satarting","resources/gifs/1.gif"),
            "FB Comment": lambda: self.execute_robot_in_tab("FB Comment","Robot satarting","resources/gifs/1.gif"),
            "Insta": lambda: self.execute_robot_in_tab("Insta","Robot satarting","resources/gifs/1.gif"),
            "IN Job": lambda: self.execute_robot_in_tab("IN Job","Robot satarting","resources/gifs/1.gif"),
            "Blog": lambda: self.execute_robot_in_tab("Blog","Robot satarting","resources/gifs/1.gif"),
            "YTB": lambda: self.execute_robot_in_tab("YTB","Robot satarting","resources/gifs/1.gif"),
            "PIN": lambda: self.execute_robot_in_tab("PIN","Robot satarting","resources/gifs/1.gif"),
            "X": lambda: self.execute_robot_in_tab("X","Robot satarting","resources/gifs/1.gif"),
            "TOK": lambda: self.execute_robot_in_tab("TOK","Robot satarting","resources/gifs/1.gif"),
        }
        for btn in [self.open_panel_btn, self.start_robots_btn, self.choice_module_btn]:
            self.apply_shadow_effect(btn)
            circle_buttons_layout.addWidget(btn)

        # Small buttons on the right
        right_buttons = QVBoxLayout()
        for name, icon in [("IN Job", "resources/icons/in_job.ico"), ("Blog", "resources/icons/blog.png"),
                        ("YTB", "resources/icons/ytb.ico"), ("PIN", "resources/icons/pin.png"),("X", "resources/icons/x.png"),
                        ("TOK", "resources/icons/tok.ico")]:
            btn = self.create_small_button(name, icon)
            self.apply_shadow_effect(btn)
            right_buttons.addWidget(btn)

            if name in button_actions2:
                btn.clicked.connect(button_actions2[name])

        # Add layouts to the central layout
        central_layout.addLayout(left_buttons)
        central_layout.addLayout(circle_buttons_layout)
        central_layout.addLayout(right_buttons)


        main_layout.addLayout(central_layout)
  # Sub-layout for the first button
        button_layout = QHBoxLayout()

        # Theme toggle button
        self.theme_button = QPushButton("Theme")
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setStyleSheet(self.get_button_stylesheet())
        button_layout.addWidget(self.theme_button)

        # LED indicators
        self.leds_layout = QHBoxLayout()
        self.green_led = self.create_led("green")
        self.yellow_led = self.create_led("yellow")
        self.red_led = self.create_led("red")
        self.leds_layout.addWidget(self.green_led)
        self.leds_layout.addWidget(self.yellow_led)
        self.leds_layout.addWidget(self.red_led)
        button_layout.addLayout(self.leds_layout)

        # Radio switch button
        self.radio_button = QPushButton("Off")
        self.radio_button.setCheckable(True)
        self.radio_button.clicked.connect(self.toggle_radio)
        self.radio_button.setStyleSheet(self.get_radio_stylesheet())
        button_layout.addWidget(self.radio_button)

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Connect main buttons for light effect
         #self.open_panel_btn.clicked.connect(lambda: self.activate_light("Open Panel Activated"))
        self.open_panel_btn.clicked.connect(self.handle_button_click)

      #   self.start_robots_btn.clicked.connect(lambda: self.activate_light("Robots Started"))
# Intégration avec le bouton Start All
        #self.start_robots_btn = self.create_circular_button2("Start All", "resources/icons/pannel.png")
        self.start_robots_btn.clicked.connect(self.handle_start_all_robots)


        self.choice_module_btn.clicked.connect(self.start_countdown)
        # Buttons to trigger the execution of external programs
        self.fb_robot_btn = self.create_small_button("FB Robot", "resources/icons/fb.ico")
        self.pin_btn = self.create_small_button("Pin", "resources/icons/pin.ico")
        self.fb_robot_btn.clicked.connect(self.run_fb_robot)
        self.pin_btn.clicked.connect(self.run_pin)

                # Footer with dynamic time
        footer_layout = QHBoxLayout()

        # Footer with dynamic time
        self.footer = QLabel()
        self.footer.setAlignment(Qt.AlignLeft)  # Align footer to the left
        self.footer.setStyleSheet("""
            QLabel {
                color: #aaa;
                font-size: 12px;
                font-style: italic;
                margin-top: 10px;
            }
        """)
        self.apply_shadow_effect(self.footer)
        footer_layout.addWidget(self.footer)

        # Update the footer text with the current time
        self.update_footer()
        timer = QTimer(self)
        timer.timeout.connect(self.update_footer)
        timer.start(1000)  # Update every second

        # Create a label to show time remaining
        self.timer_label = QLabel("Time : 00:00:00")
        self.timer_label.setAlignment(Qt.AlignRight)  # Align timer to the right
        self.timer_label.setStyleSheet("""
            QLabel {
                color: #ff6347;  # Tomato red color for the timer
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
        """)
        self.apply_shadow_effect(self.timer_label)
        footer_layout.addWidget(self.timer_label)
 
    # Add the footer layout to the main layout


        # Initialize the timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time_remaining = QTime(0, 5, 0)  # Example: Start a 5-minute countdown

        # Splitter principal
        self.splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(self.splitter)

        # Section des boutons
        self.button_tabs = QTabWidget()
        self.splitter.addWidget(self.button_tabs)

        # Section des terminaux
        # self.terminal_tabs = QTabWidget()
        # self.terminal_tabs.setTabsClosable(True)
        # self.terminal_tabs.tabCloseRequested.connect(self.close_terminal_tab)
        #self.splitter.addWidget(self.terminal_tabs)

        self.processes = {}
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_terminal_tab)

        main_layout.addLayout(footer_layout) 

        self.splitter.addWidget(self.tab_widget)

        # Initialiser le dictionnaire pour les processus

        #main_layout.addWidget(self.tab_widget)

        # # First-time guide check
        # if self.settings.get("remotefirst", "True") == "True":
        #     guide = FirstTimeGuide(self)  # Create guide instance
        #     guide.exec_()  # Show the guide modally
        #     self.settings["remotefirst"] = "True"  # Update setting to prevent guide from showing again
        #     self.save_settings()  # Save the updated setting


    #     # Apply the main layout
        self.setLayout(main_layout)




    def activate_light1(self, message):
        """Simule un effet lumineux rouge sur l'écran."""
        self.screen.change_style(message, self.get_light_stylesheet1())
        QTimer.singleShot(20000, self.reset_light1)  # Réinitialisation après 2 secondes

    def reset_light1(self):
        """Réinitialise le style par défaut."""
        self.screen.change_style("Ready to Control11", self.screen.get_screen_stylesheet())

    def get_light_stylesheet1(self):
        """Renvoie le style pour l'écran lorsque la lumière est activée."""
        return """
            QLabel {
                background-color: #ff4500;  /* Rouge lumineux */
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: 2px solid #8b0000;
                border-radius: 15px;
                padding: 15px;
            }
        """

    def change_background_gif(self, gif_path):
        """Change dynamiquement le GIF d'arrière-plan selon le chemin fourni."""
        if gif_path:  # Vérifie si un chemin est fourni
            if self.screen.background_movie:
                current_gif = self.screen.background_movie.fileName()
                if current_gif != gif_path:  # Vérifie si le GIF est déjà en cours
                    self.screen.set_background_gif(gif_path)  # Définit le nouveau GIF
                else:
                    print("Le GIF sélectionné est déjà en cours d'affichage.")
            else:
                # Si aucun GIF n'est actuellement affiché, on en affiche un nouveau
                self.screen.set_background_gif(gif_path)
        else:
            print("Erreur : Aucun chemin de GIF valide n'a été fourni.")
        
    # # Vérification si c'est la première exécution (après la définition des boutons)
    #     if self.settings.get("remotefirst", "False") == "False":
    #         guide = FirstTimeGuide(self)
    #         guide.exec_()
    #         # Mettez à jour la variable "remotefirst" pour qu'elle ne s'affiche qu'une fois
    #         self.settings["remotefirst"] = "True"
    #         self.save_settings()


    def apply_shadow_effect1(self):
        """Applique un effet d'ombre au widget."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(3, 3)
        shadow.setColor(QColor(0, 0, 0, 200))  # Noir semi-transparent
        self.setGraphicsEffect(shadow)

    def get_screen_stylesheet(self):
        """Renvoie le style CSS pour l'écran numérique."""
        return """
            QLabel {
                background-color: rgba(45, 45, 45, 180);  /* Transparence légère */
                color: #00ff88;  /* Vert néon */
                font-size: 22px;
                font-weight: bold;
                border-radius: 15px;
                padding: 15px;
                border: 2px solid #888;  /* Bordure gris clair */
            }
        """

    def add_text_glow_animation(self):
        """Ajoute une animation subtile de lueur au texte."""
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)

        self.glow_animation = QPropertyAnimation(effect, b"opacity")
        self.glow_animation.setDuration(2000)  # Durée de l'animation (ms)
        self.glow_animation.setStartValue(0.8)
        self.glow_animation.setKeyValueAt(0.5, 1.0)  # Brillance maximale au milieu
        self.glow_animation.setEndValue(0.8)
        self.glow_animation.setLoopCount(-1)  # Animation infinie
        self.glow_animation.start()

    def set_background_gif(self, gif_path):
        """Ajoute un GIF animé comme fond d'écran pour l'écran numérique."""
        self.background_movie = QMovie(gif_path)
        self.setMovie(self.background_movie)
        self.background_movie.start()

    def add_pulsing_border_animation(self):
        """Ajoute une animation de bordure pulsante autour de l'écran."""
        self.border_animation = QPropertyAnimation(self, b"styleSheet")
        self.border_animation.setDuration(1500)  # Durée de l'animation
        self.border_animation.setLoopCount(-1)  # Animation infinie

        start_style = """
            QLabel {
                background-color: rgba(45, 45, 45, 180);
                color: #00ff88;
                font-size: 22px;
                font-weight: bold;
                border-radius: 15px;
                padding: 15px;
                border: 3px solid #00ff88;  /* Bordure verte */
            }
        """
        end_style = """
            QLabel {
                background-color: rgba(45, 45, 45, 180);
                color: #00ff88;
                font-size: 22px;
                font-weight: bold;
                border-radius: 15px;
                padding: 15px;
                border: 3px solid #8800ff;  /* Bordure violette */
            }
        """

        self.border_animation.setStartValue(start_style)
        self.border_animation.setEndValue(end_style)
        self.border_animation.start()







    def create_new_tab_for_robot(self, robot_name):
        """Create a new tab for the given robot."""
        # Create the new widget for the robot tab
        robot_widget = QWidget()
        layout = QVBoxLayout(robot_widget)
        
        # Example content for the robot tab (you can customize this as needed)
        robot_label = QLabel(f"Executing {robot_name} robot")
        layout.addWidget(robot_label)
        
        # Add the robot tab to the tab widget
        tab_index = self.tab_widget.addTab(robot_widget, robot_name)
        
        return tab_index

    def execute_robot_in_tab(self, robot_name,message,gif_path):
        """
        Create a new tab to execute a specific robot and display its output,
        after checking the necessary conditions.
        
        :param robot_name: Name of the robot to execute (used for the button and tab).
        """
        message = message
        #self.activate_light("Module Chosen")
        lambda: self.activate_light1(message)

        # Bouton pour changer le GIF d'arrière-plan
        gif_path = gif_path  # Chemin du GIF sélectionné
        self.change_background_gif(gif_path)


        if not hasattr(self, 'tab_widget') or self.tab_widget is None:
            logging.error("tab_widget is not initialized.")
            return

        if self.button_states.get(robot_name, False):
            logging.warning(f"{robot_name} is already running.")
            return

        if not self.can_execute_program(robot_name):
            logging.warning(f"Cannot execute {robot_name}. Required folder conditions are not met.")
            return

        robot_path = self.get_robot_path(robot_name)
        if not robot_path or not os.path.exists(robot_path):
            logging.error(f"Executable not found: {robot_path}")
            return

        button = self.find_button_by_name(robot_name)
        if button:
            button.setEnabled(False)
        self.button_states[robot_name] = True

        terminal_output = QTextEdit()
        terminal_output.setReadOnly(True)

        tab_title = f"{robot_name} "
        index = self.tab_widget.addTab(terminal_output, tab_title)
        self.tab_widget.setCurrentIndex(index)

        process = self.run_executable_in_tab(robot_path, terminal_output)

        def on_process_finished():
            self.button_states[robot_name] = False
            if button:
                button.setEnabled(True)
            logging.info(f"{robot_name} execution finished.")

        process.finished.connect(on_process_finished)

        # After creating the tab, check if the radio button is off
        if not self.radio_button.isChecked():
            # If radio button is off, close the newly created tab immediately
            self.close_terminal_tab(index)

    def toggle_radio(self):
        """Toggles the radio button's state."""
        if self.radio_button.isChecked():
            lambda: self.activate_light1("feu Marketing  ")

        # Bouton pour changer le GIF d'arrière-plan
            gif_path = "resources/gifs/on.gif"  # Chemin du GIF sélectionné
            self.change_background_gif(gif_path)
            self.radio_button.setText("On")
            self.green_led.setStyleSheet("background-color: green; border-radius: 15px;")
            self.yellow_led.setStyleSheet("background-color: gray; border-radius: 15px;")
            self.red_led.setStyleSheet("background-color: gray; border-radius: 15px;")
        else:
            self.radio_button.setText("Off")
            self.green_led.setStyleSheet("background-color: gray; border-radius: 15px;")
            # The next line handles closing tabs when radio button is "off"
            self.close_all_tabs()  # Optional: If you want to close all tabs when radio is off

    def close_terminal_tab(self, index):
        """Close the terminal tab and terminate the associated process."""
        widget = self.tab_widget.widget(index)
        if widget:
            # Ensure the process is properly terminated
            if index in self.processes:  # Check if the process exists
                process = self.processes[index]
                try:
                    if process.state() != QProcess.NotRunning:
                        logging.info(f"Closing process for tab {index}")
                        process.terminate()
                        if not process.waitForFinished(5000):  # Wait for up to 5 seconds
                            logging.warning(f"Process for tab {index} is not responding. Forcing termination.")
                            process.kill()
                    else:
                        logging.info(f"Process for tab {index} is already stopped.")
                except Exception as e:
                    logging.error(f"Error closing process: {e}")
                finally:
                    del self.processes[index]  # Remove the process from the dictionary

            # Remove the tab from the QTabWidget
            self.tab_widget.removeTab(index)
        else:
            logging.warning(f"No widget found for tab at index {index}")

    def close_all_tabs(self):
        """Close all tabs when the radio button is turned off."""
        for index in range(self.tab_widget.count()):
            self.close_terminal_tab(index)



    def handle_start_all_robots(self):
        """Gestion de clic sur le bouton Start All."""
        # Désactiver le bouton et afficher "Starting..."
        self.start_robots_btn.setText("Starting...")
        self.start_robots_btn.setEnabled(False)

        # Afficher l'effet lumineux de démarrage
        #self.activate_light("Starting all robotss...")
        lambda: self.activate_light1("Start All robot!")

        # Bouton pour changer le GIF d'arrière-plan
        gif_path = "resources/gifs/start_all.gif"  # Chemin du GIF sélectionné
        self.change_background_gif(gif_path)

        # Créer et afficher le popup
        dialog = self.create_popup()
        if dialog.exec_() == QDialog.Accepted:
            self.start_all_robots()  # Lancer tous les robots si confirmé
        else:
            # Réactiver le bouton en cas d'annulation
            self.reset_start_button()

    def reset_start_button(self):
        """Réinitialise le bouton Start All."""
        self.start_robots_btn.setText("Start All")
        self.start_robots_btn.setEnabled(True)

    def start_all_robots(self):
        """Démarre tous les robots en parallèle."""
        try:
            # Afficher l'effet lumineux de démarrage
            self.activate_light("Robots Started")

            # Lancer chaque robot dans le groupe
            for action_name, action_func in self.button_actionss.items():
                action_func()  # Lancer chaque robot

            print("Tous les robots ont été démarrés.")
        except Exception as e:
            print(f"Erreur lors du démarrage des robots : {e}")
        finally:
            # Réinitialiser le bouton après 5 secondes
            QTimer.singleShot(5000, lambda: self.reset_start_button())
            # Réinitialiser l'effet lumineux après 1 seconde
            QTimer.singleShot(1000, self.reset_light)

    def create_popup(self):
        """Crée un popup moderne pour demander confirmation."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Confirmation")
        dialog.setWindowIcon(QIcon("resources/icons/confirmation.ico"))
        dialog.setFixedSize(400, 200)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #222831;
                border-radius: 10px;
            }
            QLabel {
                color: #eeeeee;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton {
                border: 1px solid #00adb5;
                border-radius: 5px;
                color: #eeeeee;
                padding: 8px 15px;
                background-color: #00adb5;
            }
            QPushButton:hover {
                background-color: #393e46;
            }
            QPushButton:pressed {
                background-color: #007b83;
            }
        """)

        # Ajouter des widgets
        layout = QVBoxLayout(dialog)

        label = QLabel("Do you want to start all the robots?")
        label.setFont(QFont("Arial", 14))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Boutons
        button_layout = QVBoxLayout()
        confirm_button = QPushButton("yes, Start ")
        cancel_button = QPushButton("Cancel")

        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        # Connecter les boutons
        confirm_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        return dialog

    def activate_light(self, message):
        """Simule un effet lumineux rouge sur l'écran."""
        self.screen.setText(message)
        self.screen.setStyleSheet(self.get_light_stylesheet())
        QTimer.singleShot(2000, self.reset_light)

    def reset_light(self):
        """Réinitialise l'effet lumineux après 1 seconde."""
        self.screen.setText("")
        self.screen.setStyleSheet("")



    def is_nova360_installed(self):
        """Vérifie si Nova360 est installé sur le système."""
        if platform.system() == "Windows":
            return os.path.exists("C:\\Program Files\\Nova360 AI\\main.exe")
        elif platform.system() == "Darwin":
            return os.path.exists("/Applications/Nova360.app")
        elif platform.system() == "Linux":
            return subprocess.call(["which", "nova360"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0
        return False

    def is_nova360_running(self):
        """Vérifie si Nova360 est déjà en cours d'exécution."""
        try:
            if platform.system() == "Windows":
                output = subprocess.check_output('tasklist', shell=True).decode()
                return "main.exe" in output
            elif platform.system() == "Darwin" or platform.system() == "Linux":
                output = subprocess.check_output(['ps', 'aux']).decode()
                return "nova360" in output
        except Exception as e:
            print(f"Erreur lors de la vérification du processus : {e}")
        return False


    def handle_button_click(self):
        """Gestion de clic sur le bouton principal."""
        lambda: self.activate_light1("Light Activated!")

        # Bouton pour changer le GIF d'arrière-plan
        gif_path = "resources/gifs/pannel.gif"  # Chemin du GIF sélectionné
        self.change_background_gif(gif_path)


        if self.nova360_installed:
            self.open_nova360()
        else:
            self.install_nova360()
    def open_nova360(self):
        """Ouvre Nova360, ou affiche la fenêtre si elle est déjà en cours d'exécution."""
        if self.is_nova360_running():
            print("Nova360 est déjà en cours d'exécution.")
            self.open_panel_btn.setText("Program opened")
            self.bring_nova360_to_front()  # Ramène la fenêtre au premier plan
            QTimer.singleShot(2000, lambda: self.open_panel_btn.setText("Open Panel"))
            return

        # Désactiver le bouton temporairement
        self.open_panel_btn.setText("Opening...")
        self.open_panel_btn.setEnabled(False)

        QTimer.singleShot(30000, lambda: self.open_panel_btn.setEnabled(True))  # Réactiver après 30s
        QTimer.singleShot(30000, lambda: self.open_panel_btn.setText("Open Panel"))

        try:
            if platform.system() == "Windows":
                subprocess.Popen(
                    ["C:\\Program Files\\Nova360 AI\\main.exe"],
                    cwd="C:\\Program Files\\Nova360 AI\\"
                )
            elif platform.system() == "Darwin":
                subprocess.Popen(
                    ["open", "/Applications/Nova360.app"],
                    cwd="/Applications/"
                )
            elif platform.system() == "Linux":
                subprocess.Popen(
                    ["nova360"],
                    cwd="/usr/share/nova360/"  # Remplacez par le chemin réel si connu
                )
        except Exception as e:
            print(f"Erreur lors du lancement de Nova360 : {e}")

    def bring_nova360_to_front(self):
        """Ramène la fenêtre Nova360 au premier plan selon le système d'exploitation."""
        try:
            if platform.system() == "Windows":
                import win32gui
                import win32con

                def enum_windows_callback(hwnd, results):
                    # Vérifie si la fenêtre contient "Nova360" dans son titre
                    if win32gui.IsWindowVisible(hwnd) and "Nova360" in win32gui.GetWindowText(hwnd):
                        results.append(hwnd)

                windows = []
                win32gui.EnumWindows(enum_windows_callback, windows)

                if windows:
                    hwnd = windows[0]  # Supposons qu'une seule fenêtre correspond
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restaurer si minimisé
                    win32gui.SetForegroundWindow(hwnd)  # Amener au premier plan
                else:
                    print("Fenêtre Nova360 non trouvée.")

            elif platform.system() == "Darwin":
                # macOS : Utilise AppleScript via subprocess
                script = """
                tell application "System Events"
                    set appProcess to first application process whose name is "Nova360"
                    set frontmost of appProcess to true
                end tell
                """
                subprocess.run(["osascript", "-e", script], check=True)

            elif platform.system() == "Linux":
                # Linux : Utilise xdotool pour interagir avec les fenêtres
                result = subprocess.run(["xdotool", "search", "--name", "Nova360"], capture_output=True, text=True)
                window_id = result.stdout.strip()
                if window_id:
                    subprocess.run(["xdotool", "windowactivate", window_id])
                else:
                    print("Fenêtre Nova360 non trouvée.")

            else:
                print(f"Système d'exploitation {platform.system()} non pris en charge pour ramener la fenêtre au premier plan.")

        except Exception as e:
            print(f"Erreur lors de la mise au premier plan : {e}")

    # def open_nova360(self):
    #     """Ouvre Nova360, ou affiche la fenêtre si elle est déjà en cours d'exécution."""
    #     if self.is_nova360_running():
    #         print("Nova360 est déjà en cours d'exécution.")
    #         self.open_panel_btn.setText("Programme ouvert")
    #         self.bring_nova360_to_front()
    #         QTimer.singleShot(2000, lambda: self.open_panel_btn.setText("Open Panel"))
    #         return

    #     # Désactiver le bouton temporairement
    #     self.open_panel_btn.setText("Ouverture en cours...")
    #     self.open_panel_btn.setEnabled(False)

    #     QTimer.singleShot(30000, lambda: self.open_panel_btn.setEnabled(True))  # Réactiver après 30s
    #     QTimer.singleShot(30000, lambda: self.open_panel_btn.setText("Open Panel"))

    #     try:
    #         if platform.system() == "Windows":
    #             subprocess.Popen(["C:\\Program Files\\Nova360 AI\\main.exe"])
    #         elif platform.system() == "Darwin":
    #             subprocess.Popen(["open", "/Applications/Nova360.app"])
    #         elif platform.system() == "Linux":
    #             subprocess.Popen(["nova360"])
    #     except Exception as e:
    #         print(f"Erreur lors du lancement de Nova360 : {e}")

    def install_nova360(self):
        """Télécharge et installe Nova360."""
        download_url = ""
        installer_path = ""

        if platform.system() == "Windows":
            download_url = "https://nova360.turknovatech.com/storage/themes/2.0.0/Nova360.exe"
            installer_path = "nova360_installer.exe"
        elif platform.system() == "Darwin":
            download_url = "https://nova360.turknovatech.com/storage/themes/2.0.0/Nova360.dmg"
            installer_path = "nova360_installer.dmg"
        elif platform.system() == "Linux":
            print("Nova360 n'est pas disponible pour Linux.")
            return

        # Télécharger l'installateur
        self.open_panel_btn.setText("Downloading...")
        try:
            response = requests.get(download_url, stream=True, verify=False)  # SSL verification disabled
            with open(installer_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        except Exception as e:
            print(f"Erreur lors du téléchargement : {e}")
            return

        # Installer Nova360
        self.open_panel_btn.setText("Installing...")
        try:
            if platform.system() == "Windows":
                subprocess.run([installer_path, "/S"])  # Mode silencieux
            elif platform.system() == "Darwin":
                subprocess.run(["hdiutil", "attach", installer_path])
                subprocess.run(["cp", "-R", "/Volumes/Nova360/Nova360.app", "/Applications/"])
                subprocess.run(["hdiutil", "detach", "/Volumes/Nova360/"])
        except Exception as e:
            print(f"Erreur lors de l'installation : {e}")
            return

        # Nettoyage et lancement
        os.remove(installer_path)
        self.open_panel_btn.setText("Open Panel")
        self.nova360_installed = True
        self.open_nova360()

    # def is_nova360_installed(self):
    #     """Vérifie si Nova360 est installé sur le système."""
    #     if platform.system() == "Windows":
    #         return os.path.exists("C:\\Program Files\\Nova360 AI\\main.exe")
    #     elif platform.system() == "Darwin":
    #         return os.path.exists("/Applications/Nova360.app")
    #     elif platform.system() == "Linux":
    #         return subprocess.call(["which", "nova360"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0
    #     return False

    # def is_nova360_running(self):
    #     """Vérifie si Nova360 est déjà en cours d'exécution."""
    #     try:
    #         if platform.system() == "Windows":
    #             output = subprocess.check_output('tasklist', shell=True).decode()
    #             return "nova360.exe" in output
    #         elif platform.system() == "Darwin" or platform.system() == "Linux":
    #             output = subprocess.check_output(['ps', 'aux']).decode()
    #             return "nova360" in output
    #     except Exception as e:
    #         print(f"Erreur lors de la vérification du processus : {e}")
    #     return False

    # def handle_button_click(self):
    #     """Gestion de clic sur le bouton principal."""
    #     if self.nova360_installed:
    #         self.open_nova360()
    #     else:
    #         self.install_nova360()

    # def open_nova360(self):
    #     """Ouvre Nova360, ou affiche la fenêtre si elle est déjà en cours d'exécution."""
    #     if self.is_nova360_running():
    #         print("Nova360 est déjà en cours d'exécution.")
    #         self.open_panel_btn.setText("Déjà ouvert")
    #         QTimer.singleShot(2000, lambda: self.open_panel_btn.setText("Open Panel"))
    #         return

    #     # Désactiver le bouton temporairement
    #     self.open_panel_btn.setText("Ouverture en cours...")
    #     self.open_panel_btn.setEnabled(False)

    #     QTimer.singleShot(30000, lambda: self.open_panel_btn.setEnabled(True))  # Réactiver après 30s
    #     QTimer.singleShot(30000, lambda: self.open_panel_btn.setText("Open Panel"))

    #     try:
    #         if platform.system() == "Windows":
    #             subprocess.Popen(["C:\\Program Files\\Nova360 AI\\main.exe"])
    #         elif platform.system() == "Darwin":
    #             subprocess.Popen(["open", "/Applications/Nova360.app"])
    #         elif platform.system() == "Linux":
    #             subprocess.Popen(["nova360"])
    #     except Exception as e:
    #         print(f"Erreur lors du lancement de Nova360 : {e}")

    # def install_nova360(self):
    #     """Télécharge et installe Nova360."""
    #     download_url = ""
    #     installer_path = ""

    #     if platform.system() == "Windows":
    #         download_url = "https://nova360.turknovatech.com/storage/themes/2.0.0/Nova360.exe"
    #         installer_path = "nova360_installer.exe"
    #     elif platform.system() == "Darwin":
    #         download_url = "https://nova360.turknovatech.com/storage/themes/2.0.0/Nova360.dmg"
    #         installer_path = "nova360_installer.dmg"
    #     elif platform.system() == "Linux":
    #         print("Nova360 n'est pas disponible pour Linux.")
    #         return

    #     # Télécharger l'installateur
    #     self.open_panel_btn.setText("Downloading...")
    #     try:
    #         response = requests.get(download_url, stream=True)
    #         with open(installer_path, "wb") as file:
    #             for chunk in response.iter_content(chunk_size=8192):
    #                 file.write(chunk)
    #     except Exception as e:
    #         print(f"Erreur lors du téléchargement : {e}")
    #         return

    #     # Installer Nova360
    #     self.open_panel_btn.setText("Installing...")
    #     try:
    #         if platform.system() == "Windows":
    #             subprocess.run([installer_path, "/S"])  # Mode silencieux
    #         elif platform.system() == "Darwin":
    #             subprocess.run(["hdiutil", "attach", installer_path])
    #             subprocess.run(["cp", "-R", "/Volumes/Nova360/Nova360.app", "/Applications/"])
    #             subprocess.run(["hdiutil", "detach", "/Volumes/Nova360/"])
    #     except Exception as e:
    #         print(f"Erreur lors de l'installation : {e}")
    #         return

    #     # Nettoyage et lancement
    #     os.remove(installer_path)
    #     self.open_panel_btn.setText("Open Panel")
    #     self.nova360_installed = True
    #     self.open_nova360()


    # def run_executable_in_tab(self, executable_path, output_widget, tab_title):
    #     """Exécute un programme et redirige sa sortie vers un QTextEdit dans un onglet."""
    #     process = QProcess(self)

    #     # Capture la sortie standard et l'erreur
    #     process.readyReadStandardOutput.connect(
    #         lambda: output_widget.append(process.readAllStandardOutput().data().decode("utf-8", errors="ignore"))
    #     )
    #     process.readyReadStandardError.connect(
    #         lambda: output_widget.append(process.readAllStandardError().data().decode("utf-8", errors="ignore"))
    #     )

    #     # Connexion du signal 'finished' pour gérer la fin du processus
    #     process.finished.connect(lambda: self.on_process_finished(executable_path, output_widget, process))

    #     # Démarrer le processus
    #     process.start(executable_path)

    #     # Stocker le processus dans le dictionnaire pour le gérer
    #     self.processes[executable_path] = process

    #     # Créer un nouvel onglet pour afficher la sortie du processus
    #     self.open_terminal_tab(tab_title, output_widget)

    #     logging.info(f"Process started: {executable_path}")
    # def run_executable_in_tab(self, executable_path, output_widget):
    #     """Exécute un programme et redirige sa sortie vers un QTextEdit."""
    #     process = QProcess(self)

    #     # Capture la sortie standard et l'erreur
    #     process.readyReadStandardOutput.connect(
    #         lambda: output_widget.append(process.readAllStandardOutput().data().decode("utf-8", errors="ignore"))
    #     )
    #     process.readyReadStandardError.connect(
    #         lambda: output_widget.append(process.readAllStandardError().data().decode("utf-8", errors="ignore"))
    #     )

    #     # Démarrer le processus avec le chemin d'exécutable
    #     try:
    #         process.start(executable_path)  # Assurez-vous que executable_path est un chemin de fichier valide
    #         logging.info(f"Process started: {executable_path}")
    #     except Exception as e:
    #         logging.error(f"Failed to start process: {e}")
    #         output_widget.append(f"\n[Erreur] Impossible de démarrer le processus : {e}\n")
    def run_executable_in_tab(self, executable_path, output_widget):
        """Exécute un programme et redirige sa sortie vers un QTextEdit."""
        if not os.path.exists(executable_path):
            output_widget.append(f"[Erreur] Le fichier exécutable est introuvable : {executable_path}")
            logging.error(f"Executable not found: {executable_path}")
            return None

        process = QProcess(self)

        # Capture la sortie standard et les erreurs
        process.readyReadStandardOutput.connect(
            lambda: output_widget.append(
                process.readAllStandardOutput().data().decode("utf-8", errors="ignore")
            )
        )
        process.readyReadStandardError.connect(
            lambda: output_widget.append(
                f"[Erreur] {process.readAllStandardError().data().decode('utf-8', errors='ignore')}"
            )
        )

        # Connectez des signaux pour surveiller les erreurs et la fin
        def handle_error(error):
            error_messages = {
                QProcess.FailedToStart: "Le processus n'a pas pu démarrer.",
                QProcess.Crashed: "Le processus a crashé.",
                QProcess.Timedout: "Le processus a expiré.",
                QProcess.WriteError: "Erreur lors de l'écriture dans le processus.",
                QProcess.ReadError: "Erreur lors de la lecture depuis le processus.",
            }
            message = error_messages.get(error, "Erreur inconnue.")
            output_widget.append(f"[Erreur] {message}")
            logging.error(f"Process error: {message}")

        process.errorOccurred.connect(handle_error)

        def handle_finished(exit_code, exit_status):
            status_message = (
                "Terminé avec succès." if exit_status == QProcess.NormalExit else "Le processus s'est arrêté de manière anormale."
            )
            output_widget.append(f"[Info] Processus terminé avec le code {exit_code}: {status_message}")
            logging.info(f"Process finished: {status_message} (Exit code: {exit_code})")

        process.finished.connect(handle_finished)

        # Démarrer le processus
        try:
            process.start(executable_path)
            logging.info(f"Process started: {executable_path}")
            output_widget.append(f"[Info] Processus démarré : {executable_path}")
        except Exception as e:
            logging.error(f"Failed to start process: {e}")
            output_widget.append(f"[Erreur] Impossible de démarrer le processus : {e}")
            return None

        return process

    def on_process_finished(self, executable_path, output_widget, process):
        """Gérer la fin du processus."""
        exit_code = process.exitCode()
        exit_status = process.exitStatus()
        logging.info(f"Process {executable_path} finished with exit code {exit_code} and status {exit_status}")

        # Fermer l'onglet et nettoyer les ressources
        self.close_terminal_tab(output_widget)

        # Supprimer le processus du dictionnaire
        del self.processes[executable_path]


    # def close_terminal_tab(self, output_widget):
    #     """Fermer l'onglet de terminal et nettoyer les ressources."""
    #     index = self.tab_widget.indexOf(output_widget)
    #     if index != -1:
    #         # Fermer l'onglet
    #         self.tab_widget.removeTab(index)

    #         # Nettoyer le QTextEdit
    #         output_widget.clear()

    #         logging.info("Tab closed and resources cleaned.")

    def get_tab_widget(self):
        """Retourne l'onglet de terminal pour un accès à l'interface."""
        return self.tab_widget

  
    # def execute_fb_robot_in_tab(self):
    #     """Crée un onglet pour exécuter le Fb Robot et afficher sa sortie."""
    #     # Vérifier si tab_widget est bien initialisé
    #     if not hasattr(self, 'tab_widget') or self.tab_widget is None:
    #         print("tab_widget is not initialized.")
    #         return

    #     # Définir le chemin de l'exécutable (exemple)
    #     fb_robot_path = "C:\\Users\\cheic\\AppData\\Roaming\\saadiya\\resources\\tools\\fb_robot.exe"
        
    #     # Vérifier si le fichier existe
    #     if not os.path.exists(fb_robot_path):
    #         print(f"Executable not found: {fb_robot_path}")
    #         return

    #     # Créer un widget QTextEdit pour afficher la sortie
    #     terminal_output = QTextEdit(self)
    #     terminal_output.setReadOnly(True)

    #     # Ajouter un nouvel onglet
    #     tab_title = "Fb Robot Terminal"
    #     index = self.tab_widget.addTab(terminal_output, tab_title)
    #     self.tab_widget.setCurrentIndex(index)

    #     # Exécuter l'exécutable et rediriger la sortie
    #     self.run_executable_in_tab(fb_robot_path, terminal_output)        
   
    # def execute_fb_robot_in_tab(self):
    #     """Crée un onglet pour exécuter le Fb Robot et afficher sa sortie."""
    #     # Vérifier si tab_widget est bien initialisé
    #     if not hasattr(self, 'tab_widget') or self.tab_widget is None:
    #         print("tab_widget is not initialized.")
    #         return

    #     # Vérifier si le bouton est déjà en cours d'utilisation
    #     if getattr(self, "button_states", {}).get("Fb Robot", False):
    #         print("Fb Robot is already running.")
    #         return

    #     # Définir le chemin de l'exécutable
    #     fb_robot_path = self.get_fb_robot_path()
    #     if not fb_robot_path or not os.path.exists(fb_robot_path):
    #         print(f"Executable not found: {fb_robot_path}")
    #         return

    #     # Désactiver le bouton pour éviter les clics multiples
    #     button = self.find_button_by_name("Fb Robot")  # Implémentez cette méthode pour récupérer le bouton par son nom
    #     if button:
    #         button.setEnabled(False)
    #     self.button_states = self.button_states or {}
    #     self.button_states["Fb Robot"] = True

    #     # Créer un widget QTextEdit pour afficher la sortie
    #     terminal_output = QTextEdit(self)
    #     terminal_output.setReadOnly(True)

    #     # Ajouter un nouvel onglet
    #     tab_title = "Fb Robot"
    #     index = self.tab_widget.addTab(terminal_output, tab_title)
    #     self.tab_widget.setCurrentIndex(index)

    #     # Exécuter l'exécutable et rediriger la sortie
    #     process = self.run_executable_in_tab(fb_robot_path, terminal_output)

    #     # Surveiller la fin du processus pour réactiver le bouton
    #     def on_process_finished():
    #         self.button_states["Fb Robot"] = False
    #         if button:
    #             button.setEnabled(True)

    #     process.finished.connect(on_process_finished)
    # def execute_robot_in_tab(self, robot_name):
    #     """
    #     Crée un onglet pour exécuter un robot spécifique et afficher sa sortie.
        
    #     :param robot_name: Nom du robot à exécuter (utilisé pour le bouton et l'onglet).
    #     """
    #     # Vérifier si tab_widget est bien initialisé
    #     if not hasattr(self, 'tab_widget') or self.tab_widget is None:
    #         print("tab_widget is not initialized.")
    #         return

    #     # Vérifier si le bouton est déjà en cours d'utilisation
    #     if getattr(self, "button_states", {}).get(robot_name, False):
    #         print(f"{robot_name} is already running.")
    #         return

    #     # Définir le chemin de l'exécutable
    #     robot_path = self.get_robot_path(robot_name)  # Remplacez par une méthode dynamique
    #     if not robot_path or not os.path.exists(robot_path):
    #         print(f"Executable not found: {robot_path}")
    #         return

    #     # Désactiver le bouton pour éviter les clics multiples
    #     button = self.find_button_by_name(robot_name)  # Implémentez cette méthode pour récupérer le bouton par son nom
    #     if button:
    #         button.setEnabled(False)
    #     self.button_states = self.button_states or {}
    #     self.button_states[robot_name] = True

    #     # Créer un widget QTextEdit pour afficher la sortie
    #     terminal_output = QTextEdit(self)
    #     terminal_output.setReadOnly(True)

    #     # Ajouter un nouvel onglet
    #     tab_title = f"{robot_name} Terminal"
    #     index = self.tab_widget.addTab(terminal_output, tab_title)
    #     self.tab_widget.setCurrentIndex(index)

    #     # Exécuter l'exécutable et rediriger la sortie
    #     process = self.run_executable_in_tab(robot_path, terminal_output)

    #     # Surveiller la fin du processus pour réactiver le bouton
    #     def on_process_finished():
    #         self.button_states[robot_name] = False
    #         if button:
    #             button.setEnabled(True)

    #     process.finished.connect(on_process_finished)


    def can_execute_program(self ,program_name):
        """
        Vérifie si un programme peut être exécuté en fonction de l'existence de dossiers spécifiques.

        :param program_name: Nom du programme à exécuter (par exemple, "fb robot" ou "wa").
        :return: Booléen indiquant si le programme peut être exécuté.
        """
        print(f"Vérification de l'exécution du programme : {program_name}")

        # Définir les chemins requis pour chaque programme
        program_conditions = {
            "fb robot": os.path.join("bon", "robot1"),
            "multi fb": os.path.join("bon", "robot1"),
            "wa +": os.path.join("wabon", "robot1"),
            "wa crm": os.path.join("wabon", "robot1"),
            "fb comment": os.path.join("bon", "robot1"),
            "insta": os.path.join("instabon", "robot1"),
            "in job": os.path.join("inbon", "robot1"),
            "blog": os.path.join("blogbon", "robot1"),
            "ytb": os.path.join("ytbon", "robot1"),
            "pin": os.path.join("pinbon", "robot1"),
            "x": os.path.join("xbon", "robot1"),
            "tok": os.path.join("tokbon", "robot1"),

        }

        # Récupérer le chemin requis pour le programme demandé
        required_path = program_conditions.get(program_name.lower())
        if not required_path:
            print(f"Programme non supporté : {program_name}")
            return False

        print(f"Chemin requis pour {program_name} : {required_path}")

        # Déterminer le chemin de base en fonction du système d'exploitation
        if platform.system() == "Windows":
            base_path = os.getenv("SystemDrive", "C:\\")  # Par défaut, "C:\\" pour Windows
            print(f"Système d'exploitation détecté : Windows, base_path = {base_path}")
        else:
            base_path = os.path.expanduser("~")  # Dossier "bon" dans le HOME pour Linux/Mac
            print(f"Système d'exploitation détecté : {platform.system()}, base_path = {base_path}")

        # Combiner le chemin de base avec le chemin requis
        full_path = os.path.join(base_path, required_path)
        print(f"Chemin complet calculé : {full_path}")

        # Vérification de l'existence et du contenu du dossier
        if os.path.exists(full_path):
            print(f"Le dossier '{full_path}' existe.")
            if os.path.isdir(full_path):
                print(f"'{full_path}' est un dossier.")
                try:
                    entries = list(os.scandir(full_path))
                    if not entries:
                        print(f"Le dossier '{full_path}' est vide.")
                        return False

                    for entry in entries:
                        print(f"Entrée trouvée : {entry.name} (Type : {'Fichier' if entry.is_file() else 'Dossier'})")

                    if any(entry for entry in entries if entry.is_file() or entry.is_dir()):
                        print(f"Le dossier '{full_path}' contient des fichiers ou des dossiers valides.")
                        return True
                    else:
                        print(f"Aucun fichier ou dossier valide trouvé dans '{full_path}'.")
                except Exception as e:
                    print(f"Erreur lors de l'accès au dossier '{full_path}' : {e}")
            else:
                print(f"'{full_path}' n'est pas un dossier.")
        else:
            print(f"Le dossier '{full_path}' n'existe pas.")

        return False

    def execute_robot_in_tab1(self, robot_name):
        """
        Crée un onglet pour exécuter un robot spécifique et afficher sa sortie,
        après vérification des conditions nécessaires.

        :param robot_name: Nom du robot à exécuter (utilisé pour le bouton et l'onglet).
        """
        if not hasattr(self, 'tab_widget') or self.tab_widget is None:
            logging.error("tab_widget is not initialized.")
            return

        if self.button_states.get(robot_name, False):
            logging.warning(f"{robot_name} is already running.")
            return

        if not self.can_execute_program(robot_name):
            logging.warning(f"Cannot execute {robot_name}. Required folder conditions are not met.")
            return

        robot_path = self.get_robot_path(robot_name)
        if not robot_path or not os.path.exists(robot_path):
            logging.error(f"Executable not found: {robot_path}")
            return

        button = self.find_button_by_name(robot_name)
        if button:
            button.setEnabled(False)
        self.button_states[robot_name] = True

        terminal_output = QTextEdit()
        terminal_output.setReadOnly(True)

        tab_title = f"{robot_name} "
        index = self.tab_widget.addTab(terminal_output, tab_title)
        self.tab_widget.setCurrentIndex(index)

        process = self.run_executable_in_tab(robot_path, terminal_output)

        def on_process_finished():
            self.button_states[robot_name] = False
            if button:
                button.setEnabled(True)
            logging.info(f"{robot_name} execution finished.")

        process.finished.connect(on_process_finished)

    
    # def find_button_by_name(self, name):
    #     """Retourne un bouton en fonction de son nom."""
    #     for button in self.findChildren(QPushButton):
    #         if button.text() == name:
    #             return button
    #     return None
    def find_button_by_name(self, name):
        """Retourne un bouton en fonction de son nom."""
        for button in self.findChildren(QPushButton):
            if button.text() == name:
                return button
        return None
                        
    def apply_shadow_effect(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)  # Adjust the blur radius
        shadow.setOffset(2, 2)  # Offset for the shadow (x, y)
        shadow.setColor(QColor(0, 0, 0, 160))  # Semi-transparent black
        widget.setGraphicsEffect(shadow)

    def update_footer(self):
        current_time = QDateTime.currentDateTime().toString("hh:mm:ss AP")
        footer_text = f"©2025 Nova360 AI - Remote Control | {current_time}"
        self.footer.setText(footer_text)

    
    def create_led(self, color):
        led = QLabel()
        led.setFixedSize(30, 30)
        led.setStyleSheet(f"background-color: gray; border-radius: 15px;")
        return led

    def toggle_theme(self):
        print("Theme toggled!")
    def toggle_radio1(self):
        if self.radio_button.isChecked():
            self.radio_button.setText("On")
            lambda: self.activate_light1("feu Marketing  ")

        # Bouton pour changer le GIF d'arrière-plan
            gif_path = "resources/gifs/off.gif"  # Chemin du GIF sélectionné
            self.change_background_gif(gif_path)
            self.green_led.setStyleSheet("background-color: green; border-radius: 15px;")
            self.yellow_led.setStyleSheet("background-color: gray; border-radius: 15px;")
            self.red_led.setStyleSheet("background-color: gray; border-radius: 15px;")
        else:
            self.radio_button.setText("Off")
            self.green_led.setStyleSheet("background-color: gray; border-radius: 15px;")

   
    def toggle_switch(self):
        if self.switch_button.isChecked():
            self.switch_button.setStyleSheet(self.get_switch_stylesheet(True))
            self.green_led.setStyleSheet("background-color: green; border-radius: 15px;")
            self.yellow_led.setStyleSheet("background-color: gray; border-radius: 15px;")
            self.red_led.setStyleSheet("background-color: gray; border-radius: 15px;")
        else:
            self.switch_button.setStyleSheet(self.get_switch_stylesheet(False))
            self.green_led.setStyleSheet("background-color: gray; border-radius: 15px;")

    def get_button_stylesheet(self):
        return """
            QPushButton {
                background-color: lightblue;
                padding: 10px;
                border: 2px solid darkblue;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: skyblue;
            }
        """

    def get_switch_stylesheet(self, checked=False):
        if checked:
            return """
                QPushButton {
                    background-color: green;
                    border: 2px solid darkgreen;
                    border-radius: 20px;
                    width: 60px;
                    height: 30px;
                }
                QPushButton::after {
                    content: '';
                    background-color: white;
                    width: 25px;
                    height: 25px;
                    border-radius: 12px;
                    margin-left: 30px;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: gray;
                    border: 2px solid darkgray;
                    border-radius: 20px;
                    width: 60px;
                    height: 30px;
                }
                QPushButton::after {
                    content: '';
                    background-color: white;
                    width: 25px;
                    height: 25px;
                    border-radius: 12px;
                    margin-left: 2px;
                }
            """
  
    def add_terminal_tab(self, title):
        terminal = QTextEdit()
        terminal.setReadOnly(True)
        self.tab_widget.addTab(terminal, title)
        return terminal

    def on_button_click(self, command, tab_title):
        """Créer un terminal et exécuter une commande."""
        terminal = self.add_terminal_tab(tab_title)
        terminal.append(f"Lancement de la commande : {command}")
        self.run_command(command, terminal)

    def run_command(self,command, output_widget):
        """Exécute une commande et affiche la sortie dans un QTextEdit."""
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        for line in process.stdout:
            output_widget.append(line.strip())  # Ajouter chaque ligne de sortie
        process.wait()
        if process.returncode != 0:
            output_widget.append(f"Erreur: {process.stderr.read()}")

    # def apply_shadow_effect(self, widget):
    #     """Applique un effet d'ombre à un widget."""
    #     shadow = QGraphicsDropShadowEffect()
    #     shadow.setBlurRadius(10)
    #     shadow.setOffset(2, 2)
    #     shadow.setColor(QColor(0, 0, 0, 150))  # Couleur noire semi-transparente
    #     widget.setGraphicsEffect(shadow)
    # def get_screen_stylesheet(self):
    #     """Renvoie un style CSS plus moderne et professionnel pour l'écran numérique."""
    #     return """
    #         QLabel {
    #             background: qradialgradient(
    #                 cx: 0.5, cy: 0.5, radius: 0.8,
    #                 fx: 0.5, fy: 0.5,
    #                 stop: 0 rgba(45, 45, 45, 255),
    #                 stop: 1 rgba(20, 20, 20, 255)
    #             );
    #             color: #32CD32;  /* Vert néon */
    #             font-size: 22px;
    #             font-family: 'Roboto Mono', 'Courier New', monospace;
    #             font-weight: bold;
    #             letter-spacing: 1px;  /* Espacement entre les lettres */
    #             text-shadow: 0 0 8px #32CD32, 0 0 16px #00FF00;  /* Effet lumineux */
    #             border-radius: 15px;
    #             padding: 15px;
    #             border: 2px solid #444;
    #         }
    #     """

   
   
    # def run_executable_in_tab(self, executable_path, output_widget):
    #     """Exécute un programme et redirige sa sortie vers un QTextEdit."""
    #     process = QProcess(self)

    #     # Capture la sortie standard et l'erreur
    #     process.readyReadStandardOutput.connect(
    #         lambda: output_widget.append(process.readAllStandardOutput().data().decode("utf-8"))
    #     )
    #     process.readyReadStandardError.connect(
    #         lambda: output_widget.append(process.readAllStandardError().data().decode("utf-8"))
    #     )

    #     # Démarrer le processus
    #     process.start(executable_path)

    #     # Stocker le processus dans un dictionnaire pour le gérer
    #     self.processes[executable_path] = process
   

    # def run_executable_in_tab(self, executable_path, output_widget):
    #     """Exécute un programme et redirige sa sortie vers un QTextEdit."""
    #     process = QProcess(self)

    #     # Capture la sortie standard et les erreurs
    #     process.readyReadStandardOutput.connect(
    #         lambda: output_widget.append(process.readAllStandardOutput().data().decode("utf-8"))
    #     )
    #     process.readyReadStandardError.connect(
    #         lambda: output_widget.append(process.readAllStandardError().data().decode("utf-8"))
    #     )

    #     # Démarrer le processus
    #     process.start(executable_path)

    #     # Stocker le processus dans un dictionnaire
    #     self.processes[executable_path] = process

    def open_terminal_tab(self, title, executable_path):
        """Ouvre un onglet terminal pour exécuter un fichier exécutable et capturer sa sortie."""
        logging.info(f"Opening terminal tab with title: {title} and executable: {executable_path}")

        # Crée un widget pour afficher la sortie
        terminal_output = QTextEdit()
        terminal_output.setReadOnly(True)
        terminal_output.setStyleSheet("""
            QTextEdit {
                background-color: #000;
                color: #0f0;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
        """)

        # Ajoute l'onglet avec le titre
        index = self.tab_widget.addTab(terminal_output, title)
        self.tab_widget.setCurrentIndex(index)

        # Configure le processus
        process = QProcess(self)
        process.setProcessChannelMode(QProcess.MergedChannels)

        # Connecte la sortie du processus au widget
        process.readyReadStandardOutput.connect(
            lambda: terminal_output.append(process.readAllStandardOutput().data().decode("utf-8", errors="ignore"))
        )
        process.readyReadStandardError.connect(
            lambda: terminal_output.append(process.readAllStandardError().data().decode("utf-8", errors="ignore"))
        )

        # Connecte un message si le processus se termine
        def on_process_finished():
            terminal_output.append("\n[Processus terminé]\n")
            self.clean_up_after_process(process, index)  # Nettoyage après la fin du processus

        process.finished.connect(on_process_finished)

        # Exécute le fichier exécutable
        try:
            process.start(executable_path)
            logging.info(f"Started process: {executable_path}")
        except Exception as e:
            logging.error(f"Failed to start process: {e}")
            terminal_output.append(f"\n[Erreur] Impossible de démarrer le processus : {e}\n")

    def clean_up_after_process(self, process, index):
        """Fait le nettoyage après la fin du processus et ferme l'onglet."""
        logging.info("Cleaning up after process and closing tab.")
        if process:
            process.terminate()  # Tente de terminer le processus
            process.waitForFinished()  # Attend que le processus soit vraiment terminé

        # Supprimer l'onglet correspondant au processus
        if self.tab_widget.count() > index:
            self.tab_widget.removeTab(index)

        logging.info(f"Tab {index} closed and resources cleaned up.")   

    def update_logs():
        output = process.stdout.readline()
        if output:
            terminal_output.append(output.decode().strip())
        elif process.poll() is not None:
            timer.stop()

    timer = QTimer()
    timer.timeout.connect(update_logs)
    timer.start(100)
    def closeEvent(self, event):
        """Gérer la fermeture de l'application et terminer tous les processus en cours."""
        for index, process in list(self.processes.items()):
            try:
                if process.state() != QProcess.NotRunning:
                    logging.info(f"Fermeture du processus pour l'onglet {index}")
                    process.terminate()
                    if not process.waitForFinished(5000):  # Attendre jusqu'à 5 secondes
                        logging.warning(f"Le processus pour l'onglet {index} ne répond pas. Terminaison forcée.")
                        process.kill()
                else:
                    logging.info(f"Le processus pour l'onglet {index} est déjà arrêté.")
            except Exception as e:
                logging.error(f"Erreur lors de la fermeture du processus {index}: {e}")
            finally:
                del self.processes[index]  # Supprimer chaque processus du dictionnaire

        super().closeEvent(event)  # Appeler la méthode de fermeture parente


    # def close_terminal_tab(self, index):
    #     """Fermer un onglet de terminal et terminer le processus associé."""
    #     widget = self.tab_widget.widget(index)
    #     if widget:
    #         # Assurez-vous d'avoir une structure pour stocker les processus
    #         if index in self.processes:  # Si le processus est dans le dictionnaire
    #             process = self.processes[index]
    #             try:
    #                 process.terminate()  # Tentative de fermeture propre
    #                 process.waitForFinished(5000)  # Attendre jusqu'à 5 secondes pour une fermeture propre
    #             except Exception as e:
    #                 logging.error(f"Erreur lors de la fermeture du processus: {e}")
    #             del self.processes[index]  # Supprimer l'entrée du processus dans le dictionnaire

    #         # Retirer l'onglet du QTabWidget
    #         self.tab_widget.removeTab(index)
    #     else:
    #         logging.warning(f"Aucun widget trouvé pour l'onglet à l'index {index}")
    def close_terminal_tab1(self, index):
        """Fermer un onglet de terminal et terminer le processus associé."""
        widget = self.tab_widget.widget(index)
        if widget:
            # Assurez-vous d'avoir une structure pour stocker les processus
            if index in self.processes:  # Si le processus est dans le dictionnaire
                process = self.processes[index]
                try:
                    if process.state() != QProcess.NotRunning:
                        logging.info(f"Fermeture du processus pour l'onglet {index}")
                        process.terminate()  # Tentative de fermeture propre
                        if not process.waitForFinished(5000):  # Attendre jusqu'à 5 secondes
                            logging.warning(f"Le processus pour l'onglet {index} ne répond pas. Terminaison forcée.")
                            process.kill()  # Forcer la fermeture si le processus ne répond pas
                    else:
                        logging.info(f"Le processus pour l'onglet {index} est déjà arrêté.")
                except Exception as e:
                    logging.error(f"Erreur lors de la fermeture du processus: {e}")
                finally:
                    del self.processes[index]  # Supprimer l'entrée du processus dans le dictionnaire

            # Retirer l'onglet du QTabWidget
            self.tab_widget.removeTab(index)
        else:
            logging.warning(f"Aucun widget trouvé pour l'onglet à l'index {index}")


    def start_countdown(self):
        """Start the countdown when 'Choice Module' button is clicked and open a website after 3 seconds."""
        self.time_remaining = QTime(0, 5, 0)  # Reset to 5 minutes
        self.timer.start(1000)  # Update every second
        self.timer_label.setText(f"Temps restant: {self.time_remaining.toString('hh:mm:ss')}")
        #self.activate_light("Module Chosen")
        lambda: self.activate_light1("Stategie Marketing School ")

        # Bouton pour changer le GIF d'arrière-plan
        gif_path = "resources/gifs/strategie.gif"  # Chemin du GIF sélectionné
        self.change_background_gif(gif_path)

        # Set up a QTimer to open the website after 3 seconds
        QTimer.singleShot(3000, self.open_website)

    def open_website(self):
        """Open the specified website in the default browser."""
        website_url = "https://nova360.turknovatech.com/"  # Replace with the desired URL
        webbrowser.open(website_url)

    def update_timer(self):
        """Update the countdown timer every second."""
        if self.time_remaining > QTime(0, 0, 0):
            self.time_remaining = self.time_remaining.addSecs(-1)  # Decrease by 1 second
            self.timer_label.setText(f"Temps restant: {self.time_remaining.toString('hh:mm:ss')}")
        else:
            self.timer.stop()
            self.timer_label.setText("Exécution du programme!")


    # def apply_shadow_effect(self, widget):
    #     """Apply shadow effect to widgets."""
    #     # Placeholder for your actual shadow effect code
    #     pass

    def get_screen_stylesheet(self):
        """Return stylesheet for the screen."""
        return "font-size: 20px; color: white; background-color: #333;"


    def create_small_button(self, text, icon_path):
        """Create a small button with text and icon."""
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        return button


    # def get_fb_robot_path(self):
    #     """Détecte le chemin du programme Fb Robot en fonction du système d'exploitation."""
    #     logging.info("Determining the path for Fb Robot.")

    #     if platform.system() == "Windows":
    #         logging.debug("Detected Windows OS.")
    #         user_profile = os.getenv('APPDATA')
    #         if not user_profile:
    #             logging.error("APPDATA environment variable not found.")
    #             return None
            
    #         fb_robot_path = os.path.join(user_profile, 'saadiya', 'resources', 'tools', 'fb_robot.exe')
    #         logging.debug(f"Constructed path for Windows: {fb_robot_path}")
    #     elif platform.system() == "Darwin":
    #         logging.debug("Detected macOS.")
    #         user_profile = os.getenv('HOME')
    #         if not user_profile:
    #             logging.error("HOME environment variable not found.")
    #             return None
            
    #         fb_robot_path = os.path.join(user_profile, 'Library', 'Application Support', 'saadiya', 'resources', 'tools', 'fb_robot')
    #         logging.debug(f"Constructed path for macOS: {fb_robot_path}")
    #     else:
    #         logging.error(f"Unsupported OS detected: {platform.system()}")
    #         return None

    #     if os.path.exists(fb_robot_path):
    #         logging.info(f"Executable found: {fb_robot_path}")
    #         return fb_robot_path
    #     else:
    #         logging.warning(f"Executable not found: {fb_robot_path}")
    #         return None
    def get_robot_path(self, robot_name):
        """
        Détecte le chemin du programme spécifié en fonction du système d'exploitation et du robot.

        :param robot_name: Nom du robot (par exemple, "FB Robot").
        :return: Chemin complet du programme ou None.
        """
        logging.info(f"Determining the path for {robot_name}.")

        # Nom du fichier basé sur le robot
        executable_name = {
            "FB Robot": "fb_robot.exe",
            "Multi FB": "multi_fb.exe",
            "WA +": "wa.exe",
            "WA CRM": "wa_crm.exe",
            "FB Comment": "fb_comment.exe",
            "Insta": "insta.exe",
            "IN Job": "in_job.exe",
            "Blog": "blog.exe",
            "YTB": "ytb.exe",
            "PIN": "pin.exe",
            "X": "x.exe",
            "TOK": "tok.exe",
            "Mail": "mail.exe",
            "Reddit": "reddit.exe",
            "Snap": "snap.exe",


            "Other Robot": "other_robot.exe",  # Ajoutez d'autres robots ici
        }.get(robot_name)

        if not executable_name:
            logging.error(f"No executable defined for robot: {robot_name}")
            return None

        # Détecter le système d'exploitation
        if platform.system() == "Windows":
            logging.debug("Detected Windows OS.")
            user_profile = os.getenv('APPDATA')
            if not user_profile:
                logging.error("APPDATA environment variable not found.")
                return None
            robot_path = os.path.join(user_profile, 'saadiya', 'resources', 'tools', executable_name)
        elif platform.system() == "Darwin":
            logging.debug("Detected macOS.")
            user_profile = os.getenv('HOME')
            if not user_profile:
                logging.error("HOME environment variable not found.")
                return None
            robot_path = os.path.join(user_profile, 'Library', 'Application Support', 'saadiya', 'resources', 'tools', executable_name.replace(".exe", ""))
        else:
            logging.error(f"Unsupported OS detected: {platform.system()}")
            return None

        # Vérification de l'existence du fichier
        if os.path.exists(robot_path):
            logging.info(f"Executable found: {robot_path}")
            return robot_path
        else:
            logging.warning(f"Executable not found: {robot_path}")
            return None


    def run_fb_robot(self):
        """Execute the Fb Robot program based on OS."""
        logging.info("Starting run_fb_robot function.")

        # Determine the OS and set the path accordingly
        if platform.system() == "Windows":
            logging.debug("Detected Windows OS.")
            user_profile = os.getenv('APPDATA')
            if user_profile:
                logging.debug(f"APPDATA environment variable: {user_profile}")
            else:
                logging.error("APPDATA environment variable not found.")
                return
            
            fb_robot_path = os.path.join(user_profile, 'saadiya', 'resources', 'tools', 'fb_robot.exe')
            logging.debug(f"Constructed path for Windows: {fb_robot_path}")
        elif platform.system() == "Darwin":
            logging.debug("Detected macOS.")
            user_profile = os.getenv('HOME')
            if user_profile:
                logging.debug(f"HOME environment variable: {user_profile}")
            else:
                logging.error("HOME environment variable not found.")
                return
            
            fb_robot_path = os.path.join(user_profile, 'Library', 'Application Support', 'saadiya', 'resources', 'tools', 'fb_robot')
            logging.debug(f"Constructed path for macOS: {fb_robot_path}")
        else:
            logging.error(f"Unsupported OS detected: {platform.system()}")
            return

        # Log the path and check if it exists
        logging.debug(f"Final path to execute: {fb_robot_path}")
        if os.path.exists(fb_robot_path):
            logging.info(f"File found at path: {fb_robot_path}")
            try:
                logging.debug("Attempting to execute the file.")
                subprocess.Popen(fb_robot_path, shell=True)
                logging.info(f"Successfully launched: {fb_robot_path}")
            except Exception as e:
                logging.error(f"Exception occurred while launching the file: {e}")
        else:
            logging.warning(f"File not found: {fb_robot_path}. Please verify the path.")
    
    def run_pin(self):
        """Execute the Pin program based on OS."""
        if platform.system() == "Windows":
            # Path for Windows (Roaming)
            user_profile = os.getenv('APPDATA')
            pin_path = os.path.join(user_profile, 'saadiya','resources', 'tools', 'pin.exe')
        elif platform.system() == "Darwin":  # macOS
            # Path for macOS (Library)
            user_profile = os.getenv('HOME')
            pin_path = os.path.join(user_profile, 'Library', 'Application Support', 'saadiya','resources', 'tools', 'pin')
        else:
            print("Unsupported OS.")
            return

        if os.path.exists(pin_path):
            subprocess.Popen(pin_path)
        else:
            print(f"File not found: {pin_path}")

    # def start_countdown(self):
    #     """Start the countdown when 'Choice Module' button is clicked."""
    #     self.time_remaining = QTime(0, 5, 0)  # Reset to 5 minutes
    #     self.timer.start(1000)  # Update every second
    #     self.timer_label.setText(f"Temps restant: {self.time_remaining.toString('hh:mm:ss')}")
    #     self.activate_light("Module Chosen")

    def update_timer(self):
        """Update the countdown timer every second."""
        if self.time_remaining > QTime(0, 0, 0):
            self.time_remaining = self.time_remaining.addSecs(-1)  # Decrease by 1 second
            self.timer_label.setText(f"Temps restant: {self.time_remaining.toString('hh:mm:ss')}")
        else:
            self.timer.stop()
            self.timer_label.setText("Exécution du programme!")



    # def apply_shadow_effect(self, widget):
    #     """Apply shadow effect to widgets."""
    #     # Placeholder for your actual shadow effect code
    #     pass

    def get_screen_stylesheet(self):
        """Return stylesheet for the screen."""
        return "font-size: 20px; color: white; background-color: #333;"



    def create_small_button(self, text, icon_path):
        """Create a small button with text and icon."""
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        return button

    def create_circular_button(self, name, icon_path):
        """Create a circular button with an icon and sleek futuristic styling"""
        button = QPushButton(name)
        button.setFixedSize(100, 100)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(50, 50))  # Taille ajustée de l'icône
        button.setStyleSheet(self.get_circular_button_stylesheet(name))
        return button

    def get_circular_button_stylesheet(self, button_name):
        """Generate a futuristic stylesheet for circular buttons."""
        return f"""
        QPushButton {{
            background-color: qradialgradient(
                cx: 0.5, cy: 0.5, radius: 0.6,
                fx: 0.5, fy: 0.5,
                stop: 0 #3e3e3e, stop: 1 #2a2a2a
            );
            color: white;
            border-radius: 50px;  /* Makes it circular */
            border: 2px solid #4caf50;  /* Green futuristic border */
            font-size: 12px;
            font-weight: bold;
            text-align: center;
        }}
        QPushButton:hover {{
            background-color: qradialgradient(
                cx: 0.5, cy: 0.5, radius: 0.6,
                fx: 0.5, fy: 0.5,
                stop: 0 #4caf50, stop: 1 #3e3e3e
            );
            color: #ffffff;
            border: 2px solid #76ff03;
            transform: scale(1.1);  /* Slight zoom effect */
        }}
        QPushButton:pressed {{
            background-color: qradialgradient(
                cx: 0.5, cy: 0.5, radius: 0.6,
                fx: 0.5, fy: 0.5,
                stop: 0 #76ff03, stop: 1 #4caf50
            );
            border: 2px solid #1b5e20;
            color: #ffffff;
        }}
        """
    def create_circular_button2(self, name, icon_path):
        """Create a circular button with the icon as a background and styled text."""
        button = QPushButton(name)
        button.setFixedSize(100, 100)
        button.setStyleSheet(self.get_circular_button_stylesheet2(name, icon_path))
        return button

    def get_circular_button_stylesheet2(self, button_name, icon_path):
        """Generate a futuristic stylesheet for circular buttons with background image and styled text."""
        return f"""
        QPushButton {{
            background-color: transparent;
            background-image: url({icon_path});
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;  /* Ensure the image covers the button */
            color: #00ff00;  /* Green text color */
            font-size: 14px;
            font-weight: bold;  /* Make text bold */
            text-align: center;
            border-radius: 50px;  /* Makes it circular */
            border: 2px solid #4caf50;  /* Green futuristic border */
            padding-top: 65px;  /* Adjust text position */
        }}
        QPushButton:hover {{
            background-color: transparent;
            background-image: url({icon_path});
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
            color: #007BFF;  /* Blue text color on hover */
            border: 2px solid #76ff03;  /* Lighter green border */
            transform: scale(1.1);  /* Slight zoom effect */
        }}
        QPushButton:pressed {{
            background-color: transparent;
            background-image: url({icon_path});
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
            color: #ffffff;  /* White text color on press */
            border: 2px solid #1b5e20;  /* Dark green border */
        }}
        """

    def create_small_button(self, name, icon_path):
        """Create a small rectangular button with a polished design"""
        button = QPushButton(name)
        button.setFixedSize(90, 40)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(button.size() * 0.5)
        button.setStyleSheet(self.get_small_button_stylesheet())
        return button

    def activate_light(self, message):
        """Simulate a red light effect on the screen"""
        self.screen.setText(message)
        self.screen.setStyleSheet(self.get_light_stylesheet())
        QTimer.singleShot(1000, self.reset_light)

    def reset_light(self):
        """Reset the screen after the light effect"""
        self.screen.setText("Ready to Control")
        self.screen.setStyleSheet(self.get_screen_stylesheet())

    def toggle_theme(self):
        """Toggle between dark and light modes"""
        self.is_dark_theme = not self.is_dark_theme
        self.setStyleSheet(self.get_app_stylesheet())

    # def apply_shadow_effect(self, widget):
    #     """Apply a shadow effect to a widget"""
    #     shadow = QGraphicsDropShadowEffect()
    #     shadow.setColor(QColor(0, 0, 0, 160))
    #     shadow.setOffset(0, 4)
    #     shadow.setBlurRadius(10)
    #     widget.setGraphicsEffect(shadow)

    def get_screen_stylesheet(self):
        """Return the style for the screen"""
        return """
            QLabel {




                background-color: #2d2d3f;
                color: #00ff7f;
                font-size: 20px;
                font-weight: bold;
                border: 2px solid #00ff7f;
                border-radius: 15px;
                padding: 15px;
            }
        """

    def get_light_stylesheet(self):
        """Return the style for the screen when light is activated"""
        return """
            QLabel {

                            background-color: #4CAF50;
                background-image: url('images/back.webp');
                background-position: center;
                background-repeat: no-repeat;


                background-color: #ff4500;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: 2px solid #8b0000;
                border-radius: 15px;
                padding: 15px;
            }
        """
  
    def get_button_stylesheet(self):
        return """
            QPushButton {
                background-color: lightblue;
                padding: 10px;
                border: 2px solid darkblue;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: skyblue;
            }
        """

    def get_radio_stylesheet(self):
        return """
            QPushButton {
                background-color: lightgray;
                padding: 10px;
                border: 2px solid gray;
                border-radius: 15px;
            }
            QPushButton:checked {
                background-color: green;
                color: white;
            }
        """
    def get_circular_button_stylesheet1(self):
        """Style for circular buttons"""
        return """
            QPushButton {


            
                border-radius: 50px;
                background-color: #0078d7;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border: 3px solid #005bb5;
            }
            QPushButton:hover {
                background-color: #005bb5;
                border-color: #003f91;
            }
            QPushButton:pressed {
                background-color: #003f91;
                border-color: #ff4500;
            }
        """

    def get_small_button_stylesheet(self):
        """Style for small buttons"""
        return """
            QPushButton {
                background-color: #3a3a4f;
                color: #ffffff;
                font-size: 12px;
                border-radius: 5px;
                border: 2px solid #444;
            }
            QPushButton:hover {
                background-color: #444;
                border-color: #555;
            }
            QPushButton:pressed {
                background-color: #555;
                border-color: #ff4500;
            }
        """

    def get_toggle_button_stylesheet(self):
        """Style for the toggle theme button"""
        return """
            QPushButton {
                background-color: #444;
                color: #fff;
                font-size: 14px;
                padding: 10px;
                border: 2px solid #666;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #555;
                border-color: #777;
            }
            QPushButton:pressed {
                background-color: #222;
                border-color: #ff4500;
            }
        """

    def get_app_stylesheet(self):
        """Return the style for the current theme"""
        if self.is_dark_theme:
            return """
                QWidget { 
                background-color: #2d2d3f; 
                color: #ffffff;
                 
                   }
            """
        return """
            QWidget { background-color: #ffffff; color: #000000; }
        """


# Test the application
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    remote = RemoteControl()
    remote.show()
    sys.exit(app.exec_())
