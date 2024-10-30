import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QComboBox,
    QMessageBox, QProgressBar, QHBoxLayout, QFormLayout, QPushButton, QTimeEdit, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ui.header import HeaderSection
from ui.footer import FooterSection
from imports import * 

user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

class InstallerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI FB ROBOT PRO - Setup Assistant")
        self.setGeometry(600, 300, 800, 500)  # Ajustement de la taille pour le nouvel élément
        self.current_language = "en"
        self.translations = self.load_translations()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        header = HeaderSection(self, title="AI FBK Marketing Instances", app_name="Nova360 AI", slogan="AI Marketing & Management Auto")
        main_layout.addWidget(header)

        content_layout = QHBoxLayout()
        form_layout = QFormLayout()

        header_label = QLabel(self.trans("title"))
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #0078D7;")
        form_layout.addRow(header_label)

        subheader_label = QLabel("Follow the steps to set up your AI FB Robot.")
        subheader_label.setStyleSheet("font-size: 18px; color: #555;")
        form_layout.addRow(subheader_label)

        self.auto_start_label = QLabel(self.trans("auto_start_prompt"))
        self.auto_start_combo = QComboBox(self)
        self.auto_start_combo.addItems([self.trans("yes"), self.trans("no")])
        form_layout.addRow(self.auto_start_label, self.auto_start_combo)

        self.start_type_label = QLabel(self.trans("start_type_prompt"))
        self.start_type_combo = QComboBox(self)
        self.start_type_combo.addItems([self.trans("startup"), self.trans("specific_time")])
        self.start_type_combo.currentIndexChanged.connect(self.toggle_time_input)
        form_layout.addRow(self.start_type_label, self.start_type_combo)

        self.schedule_label = QLabel(self.trans("schedule_prompt"))
        self.schedule_input = QTimeEdit(self)
        self.schedule_input.setDisplayFormat("HH:mm")
        self.schedule_input.setEnabled(False)
        form_layout.addRow(self.schedule_label, self.schedule_input)

        # Ajout des cases à cocher pour les jours de la semaine
        self.days_checkboxes = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days:
            checkbox = QCheckBox(day)
            self.days_checkboxes[day] = checkbox
            form_layout.addRow(checkbox)

        button_layout = QHBoxLayout()
        install_button = QPushButton(self.trans("install_button"))
        install_button.clicked.connect(self.run_installation)
        button_layout.addWidget(install_button)

        form_layout.addRow(button_layout)
        self.progress_bar = QProgressBar(self)
        form_layout.addRow(self.progress_bar)

        content_layout.addLayout(form_layout)
        promo_image_label = QLabel()
        pixmap = QPixmap("resources/images/5.jpg")
        promo_image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        promo_image_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(promo_image_label)

        main_layout.addLayout(content_layout)
        nav_layout = QHBoxLayout()
        home_button = QPushButton("Home")
        about_button = QPushButton("About")
        nav_layout.addWidget(home_button)
        nav_layout.addWidget(about_button)
        main_layout.addLayout(nav_layout)

        footer = FooterSection(self)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)
        self.setStyleSheet("""
            QWidget {
                font-family: 'Arial';
                font-size: 14px;
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
            }
            QProgressBar {
                background-color: #e0e0e0;
                border-radius: 8px;
            }
            QProgressBar::chunk {
                background-color: #0078D7;
                border-radius: 8px;
            }
        """)

    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load("resources/lang/en_US/modules/main_fb_robot_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/modules/main_fb_robot_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/modules/main_fb_robot_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/modules/main_fb_robot_translated.qm")
        QApplication.instance().installTranslator(self.translator)
        self.save_language_choice(language)
        self.retranslateUi()

    def save_language_choice(self, language):
        preferences = {'language': language}
        with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'w') as f:
            json.dump(preferences, f)

    def retranslateUi(self):
        self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        self.instance_action.setText(self.tr('Instance'))
        self.media_action.setText(self.tr('Médias'))
        self.group_action.setText(self.tr('Groupes'))
        self.about_action.setText(self.tr('About'))
        self.certificate_action.setText(self.tr('Certif'))
        self.language_menu.setTitle(self.tr('Langue'))

    def init_language(self):
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')
        else:
            system_locale = QLocale.system().name()[:2]
            language_map = {
                'en': 'en',
                'fr': 'fr',
                'tr': 'tr',
                'ar': 'ar',
            }
            selected_language = language_map.get(system_locale, 'en')
        self.switch_language(selected_language)

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
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "FB-Robot.exe")
            days_selected = [day for day, checkbox in self.days_checkboxes.items() if checkbox.isChecked()]

            if not days_selected:
                self.show_message("Error", "Please select at least one day.")
                return
            
            self.schedule_task(desktop_path, schedule_time, days_selected)

        self.progress_bar.setValue(100)
        self.show_message(self.trans("installation_complete"), self.trans("installation_complete_message"))

    def schedule_task(self, program_path, time, days):
        days_string = ','.join(days).lower()
        command = f'schtasks /create /tn "FB-Robot" /tr "{program_path}" /sc weekly /d {days_string} /st {time} /f'
        try:
            subprocess.run(command, check=True, shell=True)
            print(f"Tâche planifiée créée pour {days_string} à {time}")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la création de la tâche planifiée: {e}")

    def trans(self, key):
        return self.translations[self.current_language].get(key, key)

    def load_translations(self):
        return {
            "en": {
                "title": "AI FB ROBOT PRO - Setup Assistant",
                "auto_start_prompt": "Do you want Facebook Robot to start automatically?",
                "start_type_prompt": "When should it start?",
                "schedule_prompt": "Select the time to start (e.g. 15:00):",
                "install_button": "Programmer demarrage automatique ",
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
        QMessageBox.information(self, title, message)

def main():
    app = QApplication(sys.argv)
    installer = InstallerApp()
    installer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()  # Appelle la fonction main si le script est exécuté directement
