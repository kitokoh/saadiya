import sys
import os
import subprocess
import json
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit,
                             QHBoxLayout, QMessageBox, QDialog, QComboBox, QProgressBar)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtMultimedia import QSound
from datetime import datetime
from ui.header import HeaderSection  # Import du header
from ui.footer import FooterSection  # Import du footer

# Worker thread to execute scripts without blocking the GUI
class ScriptWorker(QThread):
    log_signal = pyqtSignal(str, str)  # message, level
    progress_signal = pyqtSignal(int)

    def __init__(self, scripts):
        super().__init__()
        self.scripts = scripts

    def run(self):
        total_scripts = len(self.scripts)
        for i, (friendly_message, script) in enumerate(self.scripts):
            if os.path.exists(script):
                self.log_signal.emit(friendly_message, "info")
                # Execute the script
                try:
                    subprocess.run(['python', script], check=True)
                    self.log_signal.emit(self.tr(f"Étape {i+1}/{total_scripts} : {friendly_message} réussie."), "success")
                except subprocess.CalledProcessError:
                    self.log_signal.emit(self.tr(f"Étape {i+1}/{total_scripts} : {friendly_message} échouée."), "error")
                # Update progress
                progress = int(((i + 1) / total_scripts) * 100)
                self.progress_signal.emit(progress)
            else:
                self.log_signal.emit(self.tr(f"Étape {i+1}/{total_scripts} : Le script {script} est introuvable."), "error")
                progress = int(((i + 1) / total_scripts) * 100)
                self.progress_signal.emit(progress)
        # Signal to indicate completion
        self.log_signal.emit(self.tr("Installation terminée avec succès."), "success")
        self.progress_signal.emit(100)

class LicenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Demander une licence"))
        self.setFixedSize(300, 150)
        layout = QVBoxLayout()

        label = QLabel(self.tr("Choisissez votre type de licence :"))
        layout.addWidget(label)

        self.combo_box = QComboBox()
        self.combo_box.addItems(["Mensuelle", "Annuelle", "Lifetime"])
        layout.addWidget(self.combo_box)

        submit_btn = QPushButton(self.tr("Envoyer la demande"))
        submit_btn.clicked.connect(self.submit_license_request)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_license_request(self):
        self.chosen_license = self.combo_box.currentText()
        self.accept()

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Aide"))
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()

        help_text = QLabel(f"""{self.tr('<h2>Aide et Tutoriels</h2>')}
            {self.tr('<p>Bienvenue dans le système de gestion automatisée. Voici quelques instructions pour vous aider :</p>')}
            <ul>
                <li><b>{self.tr("Démarrer Menu")}</b>: {self.tr("Lance le menu principal de l'application.")}</li>
                <li><b>{self.tr("Démarrer Système")}</b>: {self.tr("Initialise le système.")}</li>
                <li><b>{self.tr("Installer une autre instance")}</b>: {self.tr("Installe une nouvelle instance si le dossier 'robot1' existe.")}</li>
                <li><b>{self.tr("Demander votre licence")}</b>: {self.tr("Demande une licence en choisissant le type souhaité.")}</li>
            </ul>
            {self.tr('<p>Pour toute assistance supplémentaire, veuillez contacter le support technique.</p>')}
        """)
        help_text.setWordWrap(True)
        layout.addWidget(help_text)

        close_btn = QPushButton(self.tr("Fermer"))
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)

class WpRobot(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.settings_file = 'resources\data\settings.json'
        self.load_settings()
        self.initUI()

    def initUI(self):
        # Configuration de la fenêtre principale
        self.setWindowTitle(self.tr('Yönetim Uygulaması Pro'))
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowIcon(QIcon('resources/icons/robot-512.png'))  # Icône de la fenêtre

        # Layout principal
        main_layout = QVBoxLayout()
        # Ajouter le header
        header = HeaderSection(self)
        main_layout.addWidget(header)
        # Titre et sous-titre
        title_label = QLabel(self.tr("Système de Gestion Automatisée"))
        subtitle_label = QLabel(self.tr("Optimisez, installez et gérez vos environnements avec facilité."))
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        subtitle_label.setStyleSheet("font-size: 16px; color: #34495e;")
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(subtitle_label, alignment=Qt.AlignCenter)

        # Layout horizontal pour les boutons en haut
        btn_layout = QHBoxLayout()
# Ajouter les boutons conditionnels
        self.install_button = QPushButton(self)
        self.update_conditional_buttons()  # Mettez à jour les boutons en fonction des conditions
        self.install_button.setStyleSheet(""" 
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        self.install_button.setText(self.tr("Installer une instance de démo"))  # Utilisation de self.tr()
        self.install_button.clicked.connect(self.run_conditional_script)
        btn_layout.addWidget(self.install_button)  # Ajoutez le bouton au layout

        # Ajouter les boutons conditionnels supplémentaires
        self.conditional_btn_premium = QPushButton(self)
        self.update_conditional_premium()

        self.conditional_btn_premium.setStyleSheet(""" 
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ec7063;
            }
        """)
        self.conditional_btn_premium.setText(self.tr("Demande Licence"))  # Utilisation de self.tr()
        self.conditional_btn_premium.clicked.connect(self.request_license)

        btn_layout.addWidget(self.conditional_btn_premium)

        # Créer les boutons avec icônes et les ajouter au layout
        buttons = [
            (self.tr('Démarrer Menu'), 'Delacro-Id-Start-Menu.256.png', self.run_menu),
            (self.tr('Start Robot'), 'frpro-demoİnstall.png', self.run_system)
        ]

        for text, icon, function in buttons:
            btn = QPushButton(text)
            btn.setIcon(QIcon(f'resources/icons/{icon}'))
            btn.setStyleSheet(""" 
                QPushButton {
                    background-color: #2980b9;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #3498db;
                }
            """)
            btn.clicked.connect(function)
            btn_layout.addWidget(btn)

        # Ajouter un bouton d'aide
        help_btn = QPushButton(self.tr('Aide'), self)  # Utilisation de self.tr()
        help_btn.setIcon(QIcon('resources/icons/information-icon-6055-Windows.ico'))
        help_btn.setStyleSheet(""" 
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #bdc3c7;
            }
        """)
        help_btn.clicked.connect(self.show_help)
        btn_layout.addWidget(help_btn)

        # Ajouter un bouton de changement de thème

        main_layout.addLayout(btn_layout)

        # Barre de progression
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(""" 
            QProgressBar {
                border: 2px solid #ecf0f1;
                border-radius: 5px;
                text-align: center;
                color: #2c3e50;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
                width: 20px;
            }
        """)
        main_layout.addWidget(self.progress_bar)

        # Layout horizontal pour la console et l'image
        console_image_layout = QHBoxLayout()

        # Console de logs en bas (design amélioré)
        self.log_console = QTextEdit(self)
        self.log_console.setReadOnly(True)
        self.log_console.setStyleSheet(""" 
            font-size: 14px; 
            background-color: #2c3e50; 
            color: #ecf0f1; 
            padding: 10px;
            border: 1px solid #34495e;
            border-radius: 5px;
        """)
        console_image_layout.addWidget(self.log_console)

        # Image à droite de la console
        self.right_image_label = QLabel(self)
        self.right_image_label.setPixmap(QPixmap('resources/images/7.jpg').scaled(400, 700, Qt.KeepAspectRatio))
        console_image_layout.addWidget(self.right_image_label)

        main_layout.addLayout(console_image_layout)

        # Initialisation du système de notifications
        self.init_tray()

        # Charger les notifications sonores
        self.success_sound = QSound('resources/sounds/success.wav')
        self.error_sound = QSound('resources/sounds/error.wav')

        # Appliquer le thème initial
        if self.theme == 'dark':
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

        # Ajouter les notifications à la barre système
        self.tray_icon.show()

        # Ajouter un timer pour mettre à jour les boutons conditionnels
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_conditional_buttons)
        self.timer.start(5000)  # Mettre à jour toutes les 5 secondes

        # Ajouter sauvegarde automatique à la fermeture
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.destroyed.connect(self.save_settings)

        # Ajouter le footer
        footer = FooterSection(self)
        main_layout.addWidget(footer)

        # Définir la mise en page principale
        self.setLayout(main_layout)

    def update_conditional_premium(self):
        if os.path.exists(r'C:\Bon\robot1\python.txt'):
            self.conditional_btn_premium.setText(self.tr("Update licence"))  # Utilisation de self.tr()
        else: 
            self.conditional_btn_premium.setText(self.tr("Demande Licence"))  # Utilisation de self.tr()

    def update_conditional_buttons(self):
        if os.path.exists(r'C:\Bon\robot1'):
            self.install_button.setText(self.tr("Installer une autre instance"))  # Utilisation de self.tr()
        else:
            self.install_button.setText(self.tr("Installer une instance de démo"))  # Utilisation de self.tr()

    def init_tray(self):
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('resources/icons/robot-512.png'))
        self.tray_icon.setVisible(True)
        tray_menu = QtWidgets.QMenu()

        restore_action = tray_menu.addAction(self.tr("Restaurer"))  # Utilisation de self.tr()
        restore_action.triggered.connect(self.show_normal)

        quit_action = tray_menu.addAction(self.tr("Quitter"))  # Utilisation de self.tr()
        quit_action.triggered.connect(QtWidgets.qApp.quit)

        self.tray_icon.setContextMenu(tray_menu)

    def show_normal(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def toggle_theme(self):
        if self.theme == 'light':
            self.apply_dark_theme()
            self.theme = 'dark'
            self.theme_btn.setText(self.tr('Mode Clair'))  # Utilisation de self.tr()
        else:
            self.apply_light_theme()
            self.theme = 'light'
            self.theme_btn.setText(self.tr('Mode Sombre'))  # Utilisation de self.tr()
        self.save_settings()

    def apply_dark_theme(self):
        self.setStyleSheet(""" 
            QWidget {
                background-color: #34495e;
                color: #ecf0f1;
            }
            QPushButton {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 1px solid #2980b9;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QProgressBar {
                border: 2px solid #ecf0f1;
                border-radius: 5px;
                text-align: center;
                color: #ecf0f1;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
                width: 20px;
            }
            QTextEdit {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
        """)

    def apply_light_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #ecf0f1;
                color: #2c3e50;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: 1px solid #2980b9;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QProgressBar {
                border: 2px solid #2c3e50;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
                width: 20px;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #2c3e50;
            }
        """)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.theme = settings.get('theme', 'light')
                    self.license_type = settings.get('license_type', None)
            except json.JSONDecodeError:
                self.theme = 'light'
                self.license_type = None
        else:
            self.theme = 'light'
            self.license_type = None

    def save_settings(self):
        settings = {
            'theme': self.theme,
            'license_type': getattr(self, 'license_type', None)
        }
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            self.log(self.tr("Erreur lors de la sauvegarde des paramètres : {e}").format(e=e), "error")

    def log(self, message, level="info"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        colors = {
            "success": "#2ecc71",  # Vert
            "error": "#e74c3c",    # Rouge
            "info": "#3498db",     # Bleu
            "warning": "#f1c40f"   # Jaune
        }
        color = colors.get(level, "#ecf0f1")  # Couleur par défaut
        self.log_console.append(f"<span style='color: {color};'>{timestamp} - {self.tr(message)}</span>")

    # Fonctions pour les autres boutons
    def run_menu(self):
        self.log(self.tr('Lancement du menu principal...'), "info")
        # Simuler un démarrage avec un message utilisateur
        if os.path.exists('installwhattsaping/geninfo.py'):
            try:
                subprocess.run(['python', 'installwhattsaping/geninfo.py'], check=True)
                self.log(self.tr("Le menu a démarré avec succès !"), "success")
                self.show_notification(self.tr("Le menu a démarré avec succès !"), "success")
            except subprocess.CalledProcessError:
                self.log(self.tr("Erreur lors du démarrage du menu."), "error")
                self.show_notification(self.tr("Erreur lors du démarrage du menu."), "error")
        else:
            self.log(self.tr("Le fichier Menu est introuvable !"), "error")
            self.show_notification(self.tr("Le fichier Menu est introuvable !"), "error")

    def run_system(self):
        self.log(self.tr('Démarrage du système en cours...'), "info")
        if os.path.exists('installwhattsaping/start.py'):
            try:
                subprocess.run(['python', 'installwhattsaping/start.py'], check=True)
                self.log(self.tr("Le système a démarré avec succès !"), "success")
                self.show_notification(self.tr("Le système a démarré avec succès !"), "success")
            except subprocess.CalledProcessError:
                self.log(self.tr("Erreur lors du démarrage du système."), "error")
                self.show_notification(self.tr("Erreur lors du démarrage du système."), "error")
        else:
            self.log(self.tr("Le fichier Système est introuvable !"), "error")
            self.show_notification(self.tr("Le fichier Système est introuvable !"), "error")

    def run_conditional_script(self):
        # Liste des scripts à exécuter successivement avec des messages conviviaux
        scripts = [
            (self.tr('Création du dossier de l\'instance...'), 'installwhattsaping/createFolder.py'),
            (self.tr('Initialisation du système...'), 'installwhattsaping/system.py'),
            (self.tr('Organisation des fichiers...'), 'installwhattsaping/dossiers.py'),
            (self.tr('Copie des fichiers média...'), 'installwhattsaping/copieMediaDemo.py'),
            (self.tr('Mise à jour de l\'environnement...'), 'installwhattsaping/majenv.py'),
            (self.tr('Génération des informations...'), 'installwhattsaping/geninfo.py'),
            (self.tr('Installation de la licence de démo...'), 'installwhattsaping/generedemolicence.py'),
            (self.tr('Mise à jour des configurations...'), 'installwhattsaping/updatejson.py'),
            (self.tr('Finalisation de l\'installation...'), 'installwhattsaping/Visibleinstance.py'),
            (self.tr('Vérification du système...'), 'installwhattsaping/verificateur.py'),
            (self.tr('Configuration du bureau...'), 'installwhattsaping/cletobureau.py'),
            (self.tr('Démarrage automatique...'), 'installwhattsaping/demarrageauto.py'),
            (self.tr('Envoi des logs...'), 'installwhattsaping/sendlog.py'),
            (self.tr('Connexion au message...'), 'installwhattsaping/geninfo.py'),
            (self.tr('Visibilité du dossier...'), 'installwhattsaping/invisibleinstance.py'),
            (self.tr('Affichage du message...'), 'installwhattsaping/affiheMessage.py'), 
            (self.tr('Envoi du mail de succès...'), 'installwhattsaping/mailSucces.py'),
            (self.tr('Rendre invisible bon...'), 'installwhattsaping/invisibleinstance.py'),
            (self.tr('Suppression des dossiers d\'installation...'), 'installwhattsaping/secureChrome.py')
        ]

        # Initialize worker thread
        self.worker = ScriptWorker(scripts)
        self.worker.log_signal.connect(self.log)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.start()

    def request_license(self):
        # Affichage du formulaire pour demander la licence
        dialog = LicenseDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            chosen_license = dialog.chosen_license
            self.license_type = chosen_license
            self.log(self.tr(f"Licence {chosen_license} demandée."), "info")
            self.save_settings()
            self.show_notification(self.tr(f"Licence {chosen_license} demandée avec succès !"), "info")

    def show_help(self):
        # Affichage de la fenêtre d'aide
        help_dialog = HelpDialog(self)
        help_dialog.exec_()

    def show_notification(self, message, level="info"):
        if level == "info" or level == "success":
            icon = QtWidgets.QSystemTrayIcon.Information
        elif level == "error":
            icon = QtWidgets.QSystemTrayIcon.Critical
        else:
            icon = QtWidgets.QSystemTrayIcon.Information
        self.tray_icon.showMessage(self.tr('Notification'), self.tr(message), icon, 3000)

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        if value >= 100:
            self.log(self.tr("Installation terminée avec succès."), "success")
            self.show_notification(self.tr("Installation terminée avec succès !"), "success")
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = WpRobot()
    window.show()
    sys.exit(app.exec_())
