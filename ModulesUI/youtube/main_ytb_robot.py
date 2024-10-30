import os
import json

import subprocess
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QVBoxLayout, QWidget, QDialog, QLabel, QPushButton, QMessageBox, QMenu, QComboBox, QStatusBar
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTranslator, QLocale, QLibraryInfo, QPropertyAnimation

from media_manager import MediaTable
from group_manager import GroupTable
from instances_table import InstanceTable
from fb_robot_install import FbRobot

from installFBrobotPy.demarrageAuto import InstallerApp
#from installFBrobotPy.majenvqt import AppEnv 
#from installFBrobotPy.updatejson import InstallerApp
#from installFBrobotPy.installGithub import InstallerApp
#from installFBrobotPy.installpython import InstallerApp

from installFBrobotPy.invisibleQT import InvisibleInstance
from installFBrobotPy.majenvqt import MajEnv
from installFBrobotPy.jsontorobot import JsonToRobot
from installFBrobotPy.supprimBon import DeleteBon
from installFBrobotPy.updateInstanceQt import UpdateInstance

from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *
class AboutDialog(QDialog):
    """Boîte de dialogue pour 'À propos'."""
    def __init__(self, parent=None):
        super().__init__(parent)

                # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()


        self.setWindowTitle(self.tr("À propos de AI YTB ROBOT Pro"))
        layout = QVBoxLayout()
        label = QLabel(self.tr("AI YTB ROBOT Pro v1.0\n\nDéveloppé par Ibrahim MAX.\n\nCette application utilise des techniques d'automatisation IA pour faciliter la gestion des médias, groupes et instances dans les réseaux sociaux."))
        layout.addWidget(label)
        close_button = QPushButton(self.tr("Fermer"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)




        # Animation pour rendre l'ouverture plus fluide
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

class CertificateDialog(QDialog):
    """Boîte de dialogue pour 'Certificat'."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Certificat"))
        layout = QVBoxLayout()
        label = QLabel(self.tr("Votre certificat est valide jusqu'au 31 décembre 202x.\n\nAssurez-vous de le renouveler avant cette date pour maintenir l'accès aux fonctionnalités premium."))
        layout.addWidget(label)
        close_button = QPushButton(self.tr("Fermer"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)

        # Animation pour rendre l'ouverture plus fluide
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

class YtbMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr('AI YTB ROBOT Pro'))
        
        self.setGeometry(100, 210, 900, 600)
        self.setWindowIcon(QIcon('resources/icons/youtube-logo-png-3580.png'))  # Icône de la fenêtre

    
        menubar_font = QFont("Arial", 10, QFont.Bold)
        menubar = self.menuBar()
        menubar.setFont(menubar_font)
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #f0f0f0;
                padding: 5px;
            }
            QMenuBar::item {
                padding: 8px 25px;
            }
            QMenuBar::item:selected {
                background-color: #d3d3d3;
            }
            QMenu {
                padding: 10px;
            }
        """)

        # Actions du menu avec self.tr pour les traductions
        self.instance_action = QAction(QIcon("ressources/icons/facebook-icon-png-745.png"), self.tr('Instance'), self)
        self.instance_action.setToolTip(self.tr('Afficher la liste des instances'))
        self.instance_action.triggered.connect(self.open_instance)
        menubar.addAction(self.instance_action)

        self.media_action = QAction(QIcon("ressources/icons/facebook-icon-png-745.png"), self.tr('Médias'), self)
        self.media_action.setToolTip(self.tr('Afficher la liste des médias'))
        self.media_action.triggered.connect(self.open_media)
        menubar.addAction(self.media_action)

        self.group_action = QAction(QIcon("ressources/icons/facebook-icon-png-745.png"), self.tr('Groupes'), self)
        self.group_action.setToolTip(self.tr('Afficher la liste des groupes'))
        self.group_action.triggered.connect(self.open_group)
        menubar.addAction(self.group_action)

        self.about_action = QAction(QIcon("ressources/icons/facebook-icon-png-745.png"), self.tr('About'), self)
        self.about_action.setToolTip(self.tr('Informations sur l\'application'))
        self.about_action.triggered.connect(self.open_about)
        menubar.addAction(self.about_action)

        self.certificate_action = QAction(QIcon("ressources/icons/facebook-icon-png-745.png"), self.tr('Certif'), self)
        self.certificate_action.setToolTip(self.tr('Informations sur votre certificat'))
        self.certificate_action.triggered.connect(self.open_certificate)
        menubar.addAction(self.certificate_action)

        # Menu des paramètres
        self.settings_menu = menubar.addMenu(QIcon("ressources/icons/settings.png"), self.tr('Param'))

        self.dark_mode_action = QAction(self.tr('Activer le mode sombre'), self, checkable=True)
        self.dark_mode_action.setToolTip(self.tr('Basculer vers le mode sombre'))
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        self.settings_menu.addAction(self.dark_mode_action)

        self.theme_action = QAction(self.tr('Personnaliser le thème'), self)
        self.theme_action.setToolTip(self.tr('Changer les couleurs du thème'))
        self.theme_action.triggered.connect(self.customize_theme)
        self.settings_menu.addAction(self.theme_action)

        self.instance_install = QAction(QIcon("ressources/icons/install.png"), self.tr('Installer'), self)
        self.instance_install.setToolTip(self.tr('Installer des instances'))
        self.instance_install.triggered.connect(self.open_install)
        menubar.addAction(self.instance_install)

        # Menu des langues
        self.language_menu = QMenu(self.tr('Langue'), self)
        switch_language_en = QAction(self.tr('Anglais'), self)
        switch_language_en.triggered.connect(lambda: self.switch_language("en"))
        self.language_menu.addAction(switch_language_en)

        switch_language_fr = QAction(self.tr('Français'), self)
        switch_language_fr.triggered.connect(lambda: self.switch_language("fr"))
        self.language_menu.addAction(switch_language_fr)

        switch_language_tr = QAction(self.tr('Turc'), self)
        switch_language_tr.triggered.connect(lambda: self.switch_language("tr"))
        self.language_menu.addAction(switch_language_tr)

        switch_language_ar = QAction(self.tr('Arabe'), self)
        switch_language_ar.triggered.connect(lambda: self.switch_language("ar"))
        self.language_menu.addAction(switch_language_ar)

        menubar.addMenu(self.language_menu)


        # Menu Tools
        self.tools_menu = menubar.addMenu(self.tr("Tools"))
        self.tools_menu.addAction(QAction(self.tr("Heure de démarrage"), self, triggered=self.show_start_time))
        self.tools_menu.addAction(QAction(self.tr("Uninstall Instances"), self, triggered=self.uninstall_instances))
        self.tools_menu.addAction(QAction(self.tr("Invisible Instances"), self, triggered=self.show_invisible_instances))
        self.tools_menu.addAction(QAction(self.tr("Environement"), self, triggered=self.update_env))
        self.tools_menu.addAction(QAction(self.tr("Text to Robot"), self, triggered=self.update_text))
        self.tools_menu.addAction(QAction(self.tr("Delete Instance"), self, triggered=self.delete_instance))
        self.tools_menu.addAction(QAction(self.tr("Update Instance"), self, triggered=self.update_instance))
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        # Ajouter une barre de statut
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Ajouter une barre de statut
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Ajouter un widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.instance_table = FbRobot()
        layout.addWidget(self.instance_table)
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','main_wp_robot.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','main_wp_robot.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','main_wp_robot.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','main_wp_robot.qm'))

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
        self.setWindowTitle(self.tr('AI YTB ROBOT Pro'))
        # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # Par exemple, pour les actions du menu :
        self.instance_action.setText(self.tr('Instance'))
        self.media_action.setText(self.tr('Médias'))
        self.group_action.setText(self.tr('Groupes'))
        self.about_action.setText(self.tr('About'))
        self.certificate_action.setText(self.tr('Certif'))
        self.language_menu.setTitle(self.tr('Langue'))

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
            }

            # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)


    def open_media(self):
        self.setCentralWidget(MediaTable(self))

    def open_instance(self):
        self.setCentralWidget(InstanceTable(self))

    def open_install(self):
        self.setCentralWidget(FbRobot())

    def open_group(self):
        self.setCentralWidget(GroupTable(self))

    def open_about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def open_certificate(self):
        certificate_dialog = CertificateDialog(self)
        certificate_dialog.exec_()

    def toggle_dark_mode(self):
        if self.centralWidget().styleSheet() == "":
            self.centralWidget().setStyleSheet("background-color: #2e2e2e; color: white;")
        else:
            self.centralWidget().setStyleSheet("")

    def customize_theme(self):
        QMessageBox.information(self, self.tr("Personnaliser le thème"), self.tr("Cette fonctionnalité sera bientôt disponible."))


    def show_start_time(self):
        self.setCentralWidget(InstallerApp())

        QMessageBox.information(self, self.tr("Heure de démarrage"), self.tr("L'heure de démarrage est: ..."))

    def uninstall_instances(self):
        # Afficher un message de confirmation avant la désinstallation
        reply = QMessageBox.question(
            self, 
            self.tr("confirmez la désinstallation"), 
            self.tr("Êtes-vous sûr de vouloir désinstaller toutes les instances de YTB Robot ? Cela retirera toutes vos instances."),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Chemin vers le fichier uninstall.exe
            uninstall_exe_path = os.path.join("resources", "tools", "uninstall.exe")

            # Vérifier si le fichier uninstall.exe existe
            if os.path.exists(uninstall_exe_path):
                try:
                    # Exécuter uninstall.exe
                    subprocess.Popen([uninstall_exe_path], shell=True)

                    # Afficher un message de succès
                    QMessageBox.information(self, self.tr("Désinstallation"), self.tr("Instances desinstallation ...."))

                    # Optionnel : Rediriger vers une autre vue, si nécessaire
                    self.setCentralWidget(FbRobot())

                except Exception as e:
                    # Gestion des erreurs si l'exécution échoue
                    QMessageBox.critical(self, self.tr("Erreur"), self.tr(f"Impossible d'exécuter uninstall.exe : {str(e)}"))
            else:
                # Si le fichier n'existe pas
                QMessageBox.critical(self, self.tr("Erreur"), self.tr(f"Le fichier {uninstall_exe_path} est introuvable."))
        else:
            # L'utilisateur a annulé l'opération
            QMessageBox.information(self, self.tr("Annulé"), self.tr("Désinstallation annulée."))
    
    def show_invisible_instances(self):
        self.setCentralWidget(InvisibleInstance())

        QMessageBox.information(self, self.tr("Invisible Instances"), self.tr("Aucune instance invisible détectée."))

    def update_env(self):
        self.setCentralWidget(MajEnv())
        QMessageBox.information(self, self.tr("MAJ Env"), self.tr("Environnement mis à jour ...."))


    def update_text(self):
        self.setCentralWidget(JsonToRobot())

        QMessageBox.information(self, self.tr("MAJ Text"), self.tr("Texte mis à jour ..."))

    def delete_instance(self):
        QMessageBox.information(self, self.tr("Delete Instance"), self.tr("Instance supprimée ...."))
        self.setCentralWidget(DeleteBon())

    def update_instance(self):
        QMessageBox.information(self, self.tr("Update Instance"), self.tr("Instance mise à jour ...."))
        self.setCentralWidget(UpdateInstance())

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = YtbMainWindow()
    window.show()
    sys.exit(app.exec_())
