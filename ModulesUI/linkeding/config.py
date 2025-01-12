import json
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QCheckBox, QComboBox, QTabWidget, QPushButton, QGroupBox, QHBoxLayout, QLabel, QFileDialog
)


class ConfigWindow(QMainWindow):
    def __init__(self, config_path="data.json"):
        super().__init__()
        self.config_path = config_path
        self.config = self.load_config()
        self.setWindowTitle("Paramétrage des configurations")
        self.setGeometry(200, 100, 600, 600)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Création des onglets
        tabs = QTabWidget()
        tabs.addTab(self.create_general_tab(), "Général")
        tabs.addTab(self.create_linkedin_tab(), "LinkedIn")
        tabs.addTab(self.create_angelco_tab(), "AngelCo")
        tabs.addTab(self.create_global_logic_tab(), "GlobalLogic")
        
        main_layout.addWidget(tabs)
        
        # Boutons de contrôle
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Sauvegarder")
        save_btn.clicked.connect(self.save_config)
        load_btn = QPushButton("Charger")
        load_btn.clicked.connect(self.reload_config)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(load_btn)
        
        main_layout.addLayout(btn_layout)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_general_tab(self):
        general_tab = QWidget()
        layout = QFormLayout()
        
        # Champ pour le navigateur
        self.browser_combo = QComboBox()
        self.browser_combo.addItems(["Chrome", "Firefox"])
        self.browser_combo.setCurrentText(self.config.get("browser", ["Chrome"])[0])
        layout.addRow("Navigateur :", self.browser_combo)

        # Champ pour le mode headless
        self.headless_checkbox = QCheckBox("Mode Headless")
        self.headless_checkbox.setChecked(self.config.get("headless", False))
        layout.addRow("Mode sans interface graphique :", self.headless_checkbox)
        
        general_tab.setLayout(layout)
        return general_tab

    def create_linkedin_tab(self):
        linkedin_tab = QWidget()
        layout = QFormLayout()
        
        # Champs pour l'email et le mot de passe LinkedIn
        self.email_edit = QLineEdit(self.config.get("email", ""))
        self.password_edit = QLineEdit(self.config.get("password", ""))
        self.password_edit.setEchoMode(QLineEdit.Password)
        
        layout.addRow("Email LinkedIn :", self.email_edit)
        layout.addRow("Mot de passe LinkedIn :", self.password_edit)
        
        linkedin_tab.setLayout(layout)
        return linkedin_tab

    def create_angelco_tab(self):
        angelco_tab = QWidget()
        layout = QFormLayout()
        
        # Champs pour les informations d'AngelCo
        self.angelco_email_edit = QLineEdit(self.config.get("AngelCoEmail", ""))
        self.angelco_password_edit = QLineEdit(self.config.get("AngelCoPassword", ""))
        self.angelco_password_edit.setEchoMode(QLineEdit.Password)
        
        layout.addRow("Email AngelCo :", self.angelco_email_edit)
        layout.addRow("Mot de passe AngelCo :", self.angelco_password_edit)
        
        angelco_tab.setLayout(layout)
        return angelco_tab

    def create_global_logic_tab(self):
        global_logic_tab = QWidget()
        layout = QFormLayout()
        
        # Champs pour les informations de GlobalLogic
        self.globallogic_email_edit = QLineEdit(self.config.get("GlobalLogicEmail", ""))
        self.globallogic_password_edit = QLineEdit(self.config.get("GlobalLogicPassword", ""))
        self.globallogic_password_edit.setEchoMode(QLineEdit.Password)
        
        layout.addRow("Email GlobalLogic :", self.globallogic_email_edit)
        layout.addRow("Mot de passe GlobalLogic :", self.globallogic_password_edit)
        
        global_logic_tab.setLayout(layout)
        return global_logic_tab

    def load_config(self):
        try:
            with open(self.config_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_config(self):
        # Mettre à jour les valeurs de config depuis l'interface
        self.config["browser"] = [self.browser_combo.currentText()]
        self.config["headless"] = self.headless_checkbox.isChecked()
        self.config["email"] = self.email_edit.text()
        self.config["password"] = self.password_edit.text()
        self.config["AngelCoEmail"] = self.angelco_email_edit.text()
        self.config["AngelCoPassword"] = self.angelco_password_edit.text()
        self.config["GlobalLogicEmail"] = self.globallogic_email_edit.text()
        self.config["GlobalLogicPassword"] = self.globallogic_password_edit.text()
        
        with open(self.config_path, 'w') as file:
            json.dump(self.config, file, indent=4)
        self.show_message("Configuration sauvegardée avec succès!")

    def reload_config(self):
        self.config = self.load_config()
        self.update_ui_from_config()
        self.show_message("Configuration rechargée avec succès!")

    def update_ui_from_config(self):
        # Mettre à jour les champs de l'interface avec les valeurs de config
        self.browser_combo.setCurrentText(self.config.get("browser", ["Chrome"])[0])
        self.headless_checkbox.setChecked(self.config.get("headless", False))
        self.email_edit.setText(self.config.get("email", ""))
        self.password_edit.setText(self.config.get("password", ""))
        self.angelco_email_edit.setText(self.config.get("AngelCoEmail", ""))
        self.angelco_password_edit.setText(self.config.get("AngelCoPassword", ""))
        self.globallogic_email_edit.setText(self.config.get("GlobalLogicEmail", ""))
        self.globallogic_password_edit.setText(self.config.get("GlobalLogicPassword", ""))

    def show_message(self, message):
        msg = QLabel(message)
        msg.setStyleSheet("color: green; font-weight: bold;")
        self.statusBar().addWidget(msg, 0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConfigWindow()
    window.show()
    sys.exit(app.exec_())
