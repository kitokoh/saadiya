import os
import json

import subprocess
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QVBoxLayout, QWidget, QDialog, QLabel, QPushButton, QMessageBox, QMenu, QComboBox, QStatusBar
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTranslator, QLocale, QLibraryInfo, QPropertyAnimation

# from media_manager import MediaTable
# from group_manager import GroupTable
# from instances_table import InstanceTable
# from fb_robot_install import FbRobot

from ModulesUI.tiktok.media_manager import MediaTable
from ModulesUI.tiktok.group_manager import GroupTable
from ModulesUI.tiktok.instances_table import InstanceTable
#from fb_robot_install import FbRobot
from ModulesUI.chatBot.wp_robot_install import WpRobot
from statistique.stat import Dashboard


from ModulesUI.chatBot.installwhattsaping.demarrageAuto import InstallerApp
#from ModulesUI.chatBot.installwhattsaping.majenvqt import AppEnv 
#from ModulesUI.chatBot.installwhattsaping.updatejson import InstallerApp
#from ModulesUI.chatBot.installwhattsaping.installGithub import InstallerApp
#from ModulesUI.chatBot.installwhattsaping.installpython import InstallerApp

from ModulesUI.chatBot.installwhattsaping.invisibleQT import InvisibleInstance
from ModulesUI.chatBot.installwhattsaping.majenvqt import MajEnv
from ModulesUI.chatBot.installwhattsaping.jsontorobot import JsonToRobot
from ModulesUI.chatBot.installwhattsaping.supprimBon import DeleteBon
from ModulesUI.chatBot.installwhattsaping.updateInstanceQt import UpdateInstance

from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *
class AboutDialog(QDialog):
    """Boîte de dialogue pour 'À propos'."""
    def __init__(self, parent=None):
        super().__init__(parent)

                # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()


        self.setWindowTitle(self.tr("À propos de AI Chat ROBOT Pro"))
        layout = QVBoxLayout()
        label = QLabel(self.tr(
                "<div style='background-color:#F5F7FA; padding:15px; border-radius:10px;'>"
                "<h1 style='color:#1A5276; font-size:24px; font-weight:bold; text-align:center;'>Welcome to Nova360.ai</h1>"
                
                "<p style='font-size:16px; color:#333333; text-align:center;'>"
                "<strong>Your All-in-One AI-Powered Social Media Automation Solution</strong>"
                "</p><br>"
                
                "<div style='padding: 10px; border-left: 4px solid #1A5276;'>"
                "<p style='font-size:14px; color:#5D6D7E; line-height:1.6; margin:0 20px;'>"
                "Nova360.ai is the essential tool for entrepreneurs, brands, and influencers looking to simplify and scale their social media presence.<br>"
                "With advanced AI, Nova360.ai automates every aspect of your social media strategy, allowing you to engage effortlessly,<br>"
                "grow your influence, and remain at the forefront of your audience’s minds."
                "</p>"
                "</div><br>"
                
                "<h3 style='color:#1A5276; font-size:18px; margin-top:20px; text-align:center;'>Core Features</h3><br>"
                
                "<ul style='font-size:14px; color:#4A4A4A; padding-left: 40px;'>"
                "<li style='margin-bottom:10px;'><strong>🌐 Smart Scheduling:</strong> Plan and post content across platforms with precision timing for maximum reach.</li><br>"
                "<li style='margin-bottom:10px;'><strong>🤖 Automated Audience Engagement:</strong> Engage your audience with intelligent replies and dynamic comments.</li><br>"
                "<li><strong>📂 Comprehensive Media & Group Management:</strong> Manage media assets, groups, and instances seamlessly to optimize your workflow.</li>"
                "</ul><br>"
                
                "<p style='font-size:14px; color:#5D6D7E; line-height:1.6; text-align:center;'>"
                "Join a thriving community of brands and individuals who trust Nova360.ai to elevate their social media automation.<br>"
                "Save time, boost engagement, and focus on building your brand."
                "</p><br>"
                
                "<p style='font-size:11px; color:#888888; text-align:center; margin-top:20px;'>"
                "© 2024 Nova360 Pro | "
                "<a href='https://www.nova360pro.com' style='color:#1A5276; text-decoration:none;'>www.nova360pro.com</a>"
                "</p>"
                "</div>"
            ))
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
        label = QLabel(self.tr(
                "<div style='background-color:#FAF3E0; padding:15px; border-radius:8px;'>"
                "<h2 style='color:#D35400; font-size:20px; text-align:center;'>Expiration de Votre Licence</h2>"
                
                "<p style='font-size:14px; color:#4A4A4A; line-height:1.6;'>"
                "Votre licence est actuellement valide jusqu'au <strong style='color:#D35400;'>31 décembre 202x</strong>.<br>"
                "Pour continuer à profiter de toutes les fonctionnalités premium de <strong>Nova360.ai</strong>, veuillez penser à renouveler votre licence avant cette date.<br>"
                "</p><br>"
                
                "<div style='padding: 10px; border-left: 4px solid #D35400; margin: 10px 0;'>"
                "<p style='font-size:13px; color:#7F8C8D; margin:0 20px;'>"
                "Après cette date, votre accès aux fonctionnalités premium sera restreint. Vous pourrez toujours accéder à votre compte mais avec des fonctionnalités limitées jusqu'au renouvellement de votre licence."
                "</p>"
                "</div><br>"
                
                "<h3 style='color:#D35400; font-size:16px;'>En Cas de Problème</h3>"
                
                "<ul style='font-size:13px; color:#4A4A4A; padding-left: 40px;'>"
                "<li style='margin-bottom:10px;'>Si votre instance ne fonctionne plus, vérifiez la connexion Internet et assurez-vous que la licence est active.</li><br>"
                "<li>Contactez notre support technique si vous rencontrez des difficultés supplémentaires.</li>"
                "</ul><br>"
                
                "<p style='font-size:12px; color:gray; text-align:center;'>"
                "Pour toute assistance, veuillez visiter <a href='https://support.nova360pro.com' style='color:#D35400; text-decoration:none;'>notre centre de support</a>."
                "</p>"
                "</div>"
            ))
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

class ChatBotMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr('AI chatBot ROBOT Pro'))
        
        self.setGeometry(100, 210, 900, 600)
        self.setWindowIcon(QIcon('resources/icons/robot-icons-30497-Windows.ico'))  # Icône de la fenêtre

    
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
      # construction statistiques
        license_checker = LicenseChecker(license_dir="C:\\chatbotbon")  # Passez le chemin ici
        
        file_path = 'C:\\chatbotbon\\robot1\\data.json'  # Spécifiez le chemin vers votre fichier data.json
        group_counter = GroupCounter(file_path)   
        self.Nombregroup =group_counter.count_groups()
        # url = "C:\\chatbotbon\\robot1\\log.txt"
        # self.totalshare = LogLineCounter(url)
        # program_name = "FB-ROBOT.exe"
        # task_checker = ScheduledTaskChecker(program_name)
        # self.nexttimeshare = task_checker.check_task()
        print(license_checker.is_license_valid())
        self.instance_table = Dashboard(title="Chat Bot AI PRO", subtitle="Analytics Overview", validiter=license_checker.is_license_valid(),Nombregroupes=self.Nombregroup, totalshare="Nombre total" ,nexttimeshare="none")
        layout.addWidget(self.instance_table)
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_EN','chatBropro','main_chatbot_robot_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','chatBropro','main_chatbot_robot_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','chatBropro','main_chatbot_robot_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','chatBropro','main_chatbot_robot_translated.qm'))

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
        self.setWindowTitle(self.tr('AI Chat ROBOT Pro'))
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
        self.setCentralWidget(WpRobot())

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
            self.tr("Êtes-vous sûr de vouloir désinstaller toutes les instances de Chat Robot ? Cela retirera toutes vos instances."),
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
                    self.setCentralWidget(WpRobot())

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
    window = ChatBotMainWindow()
    window.show()
    sys.exit(app.exec_())
