from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,QSplitter , QTabWidget, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSplitter, QTabWidget, QTextEdit
import subprocess
from PyQt5.QtCore import QProcess


import os
import subprocess
import sys
from PyQt5.QtCore import QTimer, QTime,QDateTime
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import platform

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("fb_robot_log.txt"),  # Log file
        logging.StreamHandler()  # Console output
    ]
)
class RemoteControl(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark_theme = True  # Default to dark mode
        self.initUI()




    def initUI(self):
        self.setWindowTitle("Nova360 AI - Remote Control")
        self.setWindowIcon(QIcon('../resources/icons/robot-icons-30504-Windows.ico'))  # Assurez-vous que le chemin de l'icône est correct

        self.setFixedSize(450, 700)  # Set fixed size for the window


        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(5, 5, 5, 5)


        # Digital screen with modern styling
        self.screen = QLabel("Ready to Control")
        self.screen.setFixedHeight(self.height() // 5)
        self.screen.setAlignment(Qt.AlignCenter)
        self.apply_shadow_effect(self.screen)
        self.screen.setStyleSheet(self.get_screen_stylesheet())
        main_layout.addWidget(self.screen)

        # Central area: circular buttons and small buttons
        central_layout = QHBoxLayout()

        # Small buttons on the left
            #         "Fb Robot": lambda: self.execute_fb_robot_in_tab(),
            # "Multi Fb": lambda: self.on_button_click("fb_robot.exe", "Fb Robot Log"),
            # "WA": self.run_fb_robot,
            # "Insta": lambda: self.open_terminal_tab("Insta", "insta_tool.exe"),
        left_buttons = QVBoxLayout()
        button_actions = {
            "FB Robot": lambda: self.execute_robot_in_tab("FB Robot"),
            "Multi FB": lambda: self.execute_robot_in_tab("Multi FB"),
            "WA +": lambda: self.execute_robot_in_tab("WA +"),
            "WA CRM": lambda: self.execute_robot_in_tab("WA CRM"),
            "Fb Comment": lambda: self.execute_robot_in_tab("Fb Comment"),
            "Insta": lambda: self.execute_robot_in_tab("Insta"),

        }
        self.button_states = {
            "Fb Robot": False  # True signifie que le bouton est activé
            
        }
        for name, icon in [("Fb Robot", "icons/fb.png"), ("Multi Fb", "icons/multi_fb.png"),
                        ("WA +", "icons/wa.png"), ("COMMENT", "icons/insta.png"),("COMMENT", "icons/insta.png"),("Insta", "icons/insta.png")]:
            btn = self.create_small_button(name, icon)
            self.apply_shadow_effect(btn)
            left_buttons.addWidget(btn)

            if name in button_actions:
                btn.clicked.connect(button_actions[name])

        # Circular buttons in the center
        circle_buttons_layout = QVBoxLayout()
        self.open_panel_btn = self.create_circular_button("Open Panel", "icons/panel.png")
        self.start_robots_btn = self.create_circular_button("Start Robots", "icons/robot.png")
        self.choice_module_btn = self.create_circular_button("Choice Module", "icons/module.png")

        for btn in [self.open_panel_btn, self.start_robots_btn, self.choice_module_btn]:
            self.apply_shadow_effect(btn)
            circle_buttons_layout.addWidget(btn)

        # Small buttons on the right
        right_buttons = QVBoxLayout()
        for name, icon in [("Pin", "icons/pin.png"), ("X", "icons/x.png"),
                        ("In", "icons/linkedin.png"), ("YTB", "icons/ytb.png"),("X", "icons/x.png"),
                        ("In", "icons/linkedin.png")]:
            btn = self.create_small_button(name, icon)
            self.apply_shadow_effect(btn)
            right_buttons.addWidget(btn)

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
        self.open_panel_btn.clicked.connect(lambda: self.activate_light("Open Panel Activated"))
        self.start_robots_btn.clicked.connect(lambda: self.activate_light("Robots Started"))
        self.choice_module_btn.clicked.connect(self.start_countdown)
        # Buttons to trigger the execution of external programs
        self.fb_robot_btn = self.create_small_button("Fb Robot", "icons/fb.png")
        self.pin_btn = self.create_small_button("Pin", "icons/pin.png")
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
        self.timer_label = QLabel("Temps restant : 00:00:00")
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


        # Apply the main layout
        self.setLayout(main_layout)



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
    def execute_robot_in_tab(self, robot_name):
        """
        Crée un onglet pour exécuter un robot spécifique et afficher sa sortie.
        
        :param robot_name: Nom du robot à exécuter (utilisé pour le bouton et l'onglet).
        """
        # Vérifier si tab_widget est bien initialisé
        if not hasattr(self, 'tab_widget') or self.tab_widget is None:
            print("tab_widget is not initialized.")
            return

        # Vérifier si le bouton est déjà en cours d'utilisation
        if getattr(self, "button_states", {}).get(robot_name, False):
            print(f"{robot_name} is already running.")
            return

        # Définir le chemin de l'exécutable
        robot_path = self.get_robot_path(robot_name)  # Remplacez par une méthode dynamique
        if not robot_path or not os.path.exists(robot_path):
            print(f"Executable not found: {robot_path}")
            return

        # Désactiver le bouton pour éviter les clics multiples
        button = self.find_button_by_name(robot_name)  # Implémentez cette méthode pour récupérer le bouton par son nom
        if button:
            button.setEnabled(False)
        self.button_states = self.button_states or {}
        self.button_states[robot_name] = True

        # Créer un widget QTextEdit pour afficher la sortie
        terminal_output = QTextEdit(self)
        terminal_output.setReadOnly(True)

        # Ajouter un nouvel onglet
        tab_title = f"{robot_name} Terminal"
        index = self.tab_widget.addTab(terminal_output, tab_title)
        self.tab_widget.setCurrentIndex(index)

        # Exécuter l'exécutable et rediriger la sortie
        process = self.run_executable_in_tab(robot_path, terminal_output)

        # Surveiller la fin du processus pour réactiver le bouton
        def on_process_finished():
            self.button_states[robot_name] = False
            if button:
                button.setEnabled(True)

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
    def toggle_radio(self):
        if self.radio_button.isChecked():
            self.radio_button.setText("On")
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

    def apply_shadow_effect(self, widget):
        """Applique un effet d'ombre à un widget."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(2, 2)
        shadow.setColor(QColor(0, 0, 0, 150))  # Couleur noire semi-transparente
        widget.setGraphicsEffect(shadow)
    def get_screen_stylesheet(self):
        """Renvoie le style CSS pour l'écran numérique."""
        return """
            QLabel {
                background-color: #2d2d2d;
                color: #00ff00;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid #555;
            }
        """
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
    def close_terminal_tab(self, index):
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
        """Start the countdown when 'Choice Module' button is clicked."""
        self.time_remaining = QTime(0, 5, 0)  # Reset to 5 minutes
        self.timer.start(1000)  # Update every second
        self.timer_label.setText(f"Temps restant: {self.time_remaining.toString('hh:mm:ss')}")
        self.activate_light("Module Chosen")

    def update_timer(self):
        """Update the countdown timer every second."""
        if self.time_remaining > QTime(0, 0, 0):
            self.time_remaining = self.time_remaining.addSecs(-1)  # Decrease by 1 second
            self.timer_label.setText(f"Temps restant: {self.time_remaining.toString('hh:mm:ss')}")
        else:
            self.timer.stop()
            self.timer_label.setText("Exécution du programme!")


    def apply_shadow_effect(self, widget):
        """Apply shadow effect to widgets."""
        # Placeholder for your actual shadow effect code
        pass

    def get_screen_stylesheet(self):
        """Return stylesheet for the screen."""
        return "font-size: 20px; color: white; background-color: #333;"

    def create_circular_button(self, text, icon_path):
        """Create a circular button with text and icon."""
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        button.setStyleSheet("border-radius: 50%; padding: 20px;")
        return button

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

        :param robot_name: Nom du robot (par exemple, "Fb Robot").
        :return: Chemin complet du programme ou None.
        """
        logging.info(f"Determining the path for {robot_name}.")

        # Nom du fichier basé sur le robot
        executable_name = {
            "Fb Robot": "fb_robot.exe",
            "Multi Fb": "multi_fb.exe",
            "WA": "wa.exe",
            "WA +": "wa_plus.exe",

            "Insta": "insta.exe",
            "In": "in.exe",

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

    def start_countdown(self):
        """Start the countdown when 'Choice Module' button is clicked."""
        self.time_remaining = QTime(0, 5, 0)  # Reset to 5 minutes
        self.timer.start(1000)  # Update every second
        self.timer_label.setText(f"Temps restant: {self.time_remaining.toString('hh:mm:ss')}")
        self.activate_light("Module Chosen")

    def update_timer(self):
        """Update the countdown timer every second."""
        if self.time_remaining > QTime(0, 0, 0):
            self.time_remaining = self.time_remaining.addSecs(-1)  # Decrease by 1 second
            self.timer_label.setText(f"Temps restant: {self.time_remaining.toString('hh:mm:ss')}")
        else:
            self.timer.stop()
            self.timer_label.setText("Exécution du programme!")



    def apply_shadow_effect(self, widget):
        """Apply shadow effect to widgets."""
        # Placeholder for your actual shadow effect code
        pass

    def get_screen_stylesheet(self):
        """Return stylesheet for the screen."""
        return "font-size: 20px; color: white; background-color: #333;"

    def create_circular_button(self, text, icon_path):
        """Create a circular button with text and icon."""
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        button.setStyleSheet("border-radius: 50%; padding: 20px;")
        return button

    def create_small_button(self, text, icon_path):
        """Create a small button with text and icon."""
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        return button

    def create_circular_button(self, name, icon_path):
        """Create a circular button with an icon and sleek styling"""
        button = QPushButton(name)
        button.setFixedSize(100, 100)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(button.size() * 0.5)
        button.setStyleSheet(self.get_circular_button_stylesheet())
        return button

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

    def apply_shadow_effect(self, widget):
        """Apply a shadow effect to a widget"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 4)
        shadow.setBlurRadius(10)
        widget.setGraphicsEffect(shadow)

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
    def get_circular_button_stylesheet(self):
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
