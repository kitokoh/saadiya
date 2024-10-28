import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QComboBox, 
    QMessageBox, QProgressBar, QHBoxLayout, QFormLayout,QPushButton, QTimeEdit
)
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QFont

class InstallerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI FB ROBOT PRO - Setup Assistant")
        self.setGeometry(600, 300, 600, 400)  # Taille ajustée
        self.current_language = "en"
        self.translations = self.load_translations()

        # Initialiser l'interface utilisateur
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Style général
        self.setStyleSheet("""
            QWidget {
                font-family: 'Arial';
                font-size: 14px;
            }
            QLineEdit, QComboBox, QPushButton, QTimeEdit {
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .header {
                font-size: 24px;
                font-weight: bold;
                color: #0078D7;
                margin-bottom: 5px;
            }
            .subheader {
                font-size: 18px;
                font-weight: normal;
                color: #555;
                margin-bottom: 20px;
            }
        """)

        # En-tête
        header_label = QLabel(self.trans("title"))
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #0078D7;")
        layout.addWidget(header_label)

        subheader_label = QLabel("Follow the steps to set up your AI FB Robot.")
        subheader_label.setStyleSheet("font-size: 18px; color: #555;")
        layout.addWidget(subheader_label)

        # Formulaire principal
        form_layout = QFormLayout()

        # Auto démarrage
        self.auto_start_label = QLabel(self.trans("auto_start_prompt"))
        self.auto_start_combo = QComboBox(self)
        self.auto_start_combo.addItems([self.trans("yes"), self.trans("no")])
        form_layout.addRow(self.auto_start_label, self.auto_start_combo)

        # Type de démarrage
        self.start_type_label = QLabel(self.trans("start_type_prompt"))
        self.start_type_combo = QComboBox(self)
        self.start_type_combo.addItems([self.trans("startup"), self.trans("specific_time")])
        self.start_type_combo.currentIndexChanged.connect(self.toggle_time_input)
        form_layout.addRow(self.start_type_label, self.start_type_combo)

        # Sélecteur d'heure pour planifier l'exécution
        self.schedule_label = QLabel(self.trans("schedule_prompt"))
        self.schedule_input = QTimeEdit(self)
        self.schedule_input.setDisplayFormat("HH:mm")
        self.schedule_input.setEnabled(False)
        form_layout.addRow(self.schedule_label, self.schedule_input)

        layout.addLayout(form_layout)

        # Boutons et barre de progression
        button_layout = QHBoxLayout()

        install_button = QPushButton(self.trans("install_button"))
        install_button.clicked.connect(self.run_installation)
        button_layout.addWidget(install_button)

        layout.addLayout(button_layout)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        # Pied de page
        footer_label = QLabel("AI FB Robot Pro © 2024 - All Rights Reserved")
        footer_label.setStyleSheet("font-size: 12px; color: grey;")
        footer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer_label)

        self.setLayout(layout)

    def toggle_time_input(self):
        """Activer/désactiver l'entrée de temps selon le type de démarrage"""
        if self.start_type_combo.currentText() == self.trans("specific_time"):
            self.schedule_input.setEnabled(True)
        else:
            self.schedule_input.setEnabled(False)

    def run_installation(self):
        """Lancer l'installation et planifier le démarrage du programme"""
        auto_start = self.auto_start_combo.currentText()
        start_type = self.start_type_combo.currentText()
        schedule_time = self.schedule_input.time().toString("HH:mm")

        if auto_start == self.trans("yes") and start_type == self.trans("specific_time"):
            # Planifier l'exécution de FB-Robot.exe à l'heure choisie
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "FB-Robot.exe")
            self.schedule_task(desktop_path, schedule_time)

        self.progress_bar.setValue(100)
        self.show_message(self.trans("installation_complete"), self.trans("installation_complete_message"))

    def schedule_task(self, program_path, time):
        """Créer une tâche planifiée pour exécuter le programme à une heure spécifique chaque jour"""
        command = f'schtasks /create /tn "FB-Robot" /tr "{program_path}" /sc daily /st {time} /f'
        try:
            subprocess.run(command, check=True, shell=True)
            print(f"Tâche planifiée créée pour {time}")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la création de la tâche planifiée: {e}")

    def trans(self, key):
        """Récupère la traduction en fonction de la langue"""
        return self.translations[self.current_language].get(key, key)

    def load_translations(self):
        """Charge les traductions disponibles"""
        return {
            "en": {
                "title": "AI FB ROBOT PRO - Setup Assistant",
                "auto_start_prompt": "Do you want Facebook Robot to start automatically?",
                "start_type_prompt": "When should it start?",
                "schedule_prompt": "Select the time to start (e.g. 15:00):",
                "install_button": "Install",
                "yes": "Yes",
                "no": "No",
                "startup": "Startup",
                "specific_time": "Specific Time",
                "installation_complete": "Installation complete!",
                "installation_complete_message": "Check info.txt and journalInstallation.txt for details."
            },
            "tr": {
                "title": "AI FB ROBOT PRO - Kurulum Asistanı",
                "auto_start_prompt": "Facebook Robotu otomatik başlatılsın mı?",
                "start_type_prompt": "Ne zaman başlatılsın?",
                "schedule_prompt": "Başlatma zamanı seçin (örn: 15:00):",
                "install_button": "Yükle",
                "yes": "Evet",
                "no": "Hayır",
                "startup": "Başlangıç",
                "specific_time": "Belirli Zaman",
                "installation_complete": "Kurulum tamamlandı!",
                "installation_complete_message": "Ayrıntılar için info.txt ve journalInstallation.txt dosyalarını kontrol edin."
            }
        }

    def show_message(self, title, message):
        """Affiche une boîte de dialogue"""
        #QMessageBox.information(self, title, message)
        pass





def main():
    app = QApplication(sys.argv)
    installer = InstallerApp()
    installer.show()
    sys.exit(app.exec_())


    
if __name__ == "__main__":
    main()  # Appelle la fonction main si le script est exécuté directement



