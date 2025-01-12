import json
import os
import subprocess
from PyQt5.QtCore import Qt, QTranslator, QLocale, QLibraryInfo, QPropertyAnimation
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QVBoxLayout, QWidget, QDialog, QLabel, QPushButton, \
    QMessageBox, QMenu, QComboBox, QStatusBar
from PyQt5.QtCore import Qt, QTimer

from ModulesUI.whasapping.group_manager import ContactTable
from ModulesUI.whasapping.installwhattsaping.invisibleQT import InvisibleInstance
from ModulesUI.whasapping.installwhattsaping.jsontorobot import JsonToRobot
from ModulesUI.whasapping.installwhattsaping.majenvqt import MajEnv
from ModulesUI.whasapping.installwhattsaping.supprimBon import DeleteBon
from ModulesUI.whasapping.installwhattsaping.updateInstanceQt import UpdateInstance
from ModulesUI.whasapping.instances_table import InstanceTable
from ModulesUI.whasapping.media_manager import MediaTable
# from fb_robot_install import FbRobot
from ModulesUI.whasapping.wp_robot_install import WpRobot
from imports import *
from installFBrobotPy.demarrageAuto import InstallerApp
from statistique.stat import Dashboard
from translation import TranslatorManager  # Importer le gestionnaire de traductions


# from ModulesUI.whasapping.installwhattsaping..majenvqt import AppEnv
# from ModulesUI.whasapping.installwhattsaping..updatejson import InstallerApp
# from ModulesUI.whasapping.installwhattsaping..installGithub import InstallerApp
# from ModulesUI.whasapping.installwhattsaping..installpython import InstallerApp
class AboutDialog(QDialog):
    """Boîte de dialogue pour 'À propos'."""
    def __init__(self, parent=None):
        super().__init__(parent)

                # Initialiser et charger les traductions
        # self.translator_manager = TranslatorManager()
        # self.translator_manager.load_translations()


        self.setWindowTitle(self.tr("À propos de AI WP ROBOT Pro"))
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

class LoadingScreen(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
                border-radius: 10px;
            }
            QLabel {
                color: white;
                font-size: 16px;
            }
        """)

        layout = QVBoxLayout()
        self.label = QLabel("Loading in progress, please wait...")

        layout.addWidget(self.label)
        self.setLayout(layout)
        self.resize(300, 100)


class WhatsMainWindow(QMainWindow):
    def __iniiit__(self):
        super().__init__()
        self.setWindowTitle(self.tr('AI WP ROBOT Pro'))
        
        self.setGeometry(100, 210, 900, 600)
        self.setWindowIcon(QIcon('resources/icons/whatsapp-512.png'))  # Icône de la fenêtre

    
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

        self.group_action = QAction(QIcon("ressources/icons/facebook-icon-png-745.png"), self.tr('Contacts'), self)
        self.group_action.setToolTip(self.tr('Afficher la liste des groupes'))
        self.group_action.triggered.connect(self.open_contacts)
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
        license_checker = LicenseChecker(license_dir="C:\\wabon")  # Passez le chemin ici
        
        file_path = 'C:\\wabon\\robot1\\data.json'  # Spécifiez le chemin vers votre fichier data.json
        group_counter = GroupCounter(file_path)   
        self.Nombregroup =group_counter.count_groups()
        # url = "C:\\wabon\\robot1\\log.txt"
        # self.totalshare = LogLineCounter(url)
        # program_name = "FB-ROBOT.exe"
        # task_checker = ScheduledTaskChecker(program_name)
        # self.nexttimeshare = task_checker.check_task()
        print(license_checker.is_license_valid())
        self.instance_table = Dashboard(title="AI WA ROBOT PRO", subtitle="Analytics Overview", validiter=license_checker.is_license_valid(),Nombregroupes=self.Nombregroup, totalshare="Nombre total" ,nexttimeshare="none")
        layout.addWidget(self.instance_table)
   


    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr('AI WP ROBOT Pro'))
        self.setGeometry(100, 210, 900, 600)
        self.setWindowIcon(QIcon('resources/icons/whatsapp-512.png'))  # Icône de la fenêtre

        # Configuration de la barre de menus
        menubar_font = QFont("Arial", 10, QFont.Bold)
        menubar = self.menuBar()
        menubar.setFont(menubar_font)

        # Configuration de la barre de menus avec style personnalisé pour Médias et Contacts
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #1E1E2F;  /* Couleur de fond sombre */
                color: #ECEFF4;            /* Couleur du texte */
                padding: 5px;
            }
            QMenuBar::item {
                padding: 8px 25px;
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #4C566A;  /* Couleur de fond au survol */
            }
            QMenu {
                background-color: #3B4252;  /* Couleur de fond du menu */
                color: #ECEFF4;             /* Couleur du texte */
                padding: 10px;
                border: 1px solid #4C566A;  /* Bordure du menu */
            }
            QMenu::item:selected {
                background-color: #4C566A;  /* Couleur de fond au survol */
            }

            /* Style personnalisé pour Médias */
            QMenuBar::item#media_action {
                background-color: #1E90FF;  /* Bleu vif */
                color: #FFFFFF;             /* Texte blanc */
                border-radius: 5px;         /* Coins arrondis */
                padding: 8px 25px;
            }
            QMenuBar::item#media_action:selected {
                background-color: #00BFFF;  /* Bleu plus clair au survol */
            }

            /* Style personnalisé pour Contacts */
            QMenuBar::item#contacts_action {
                background-color: #32CD32;  /* Vert vif */
                color: #FFFFFF;             /* Texte blanc */
                border-radius: 5px;         /* Coins arrondis */
                padding: 8px 25px;
            }
            QMenuBar::item#contacts_action:selected {
                background-color: #00FF7F;  /* Vert plus clair au survol */
            }
        """)

        # Menu "Médias" avec style personnalisé
        self.media_action = QAction(QIcon("resources/icons/media.png"), self.tr('Médias'), self)
        self.media_action.setToolTip(self.tr('Afficher la liste des médias'))
        self.media_action.triggered.connect(self.open_media)
        self.media_action.setObjectName("media_action")  # Identifiant pour le style CSS
        menubar.addAction(self.media_action)

        # Menu "Contacts" avec style personnalisé
        self.contacts_action = QAction(QIcon("resources/icons/contacts.png"), self.tr('Contacts'), self)
        self.contacts_action.setToolTip(self.tr('Afficher la liste des contacts'))
        self.contacts_action.triggered.connect(self.open_contacts)
        self.contacts_action.setObjectName("contacts_action")  # Identifiant pour le style CSS
        menubar.addAction(self.contacts_action)




        # Menu "Tools" (regroupe "Certif", "About" et d'autres outils)
        self.tools_menu = menubar.addMenu(QIcon("resources/icons/tools.png"), self.tr('Tools'))
        
        # Sous-menu "Certif"
        self.certificate_action = QAction(QIcon("resources/icons/certificate.png"), self.tr('Certif'), self)
        self.certificate_action.setToolTip(self.tr('Informations sur votre certificat'))
        self.certificate_action.triggered.connect(self.open_certificate)
        self.tools_menu.addAction(self.certificate_action)

        # Sous-menu "About"
        self.about_action = QAction(QIcon("resources/icons/about.png"), self.tr('About'), self)
        self.about_action.setToolTip(self.tr('Informations sur l\'application'))
        self.about_action.triggered.connect(self.open_about)
        self.tools_menu.addAction(self.about_action)

        # Séparateur
        self.tools_menu.addSeparator()

        # Sous-menu "Heure de démarrage"
        self.scheduling_action = QAction(QIcon("resources/icons/schedule.png"), self.tr('Heure de démarrage'), self)
        self.scheduling_action.setToolTip(self.tr('Planifier des tâches'))
        self.scheduling_action.triggered.connect(self.show_start_time)
        self.tools_menu.addAction(self.scheduling_action)

        # Sous-menu "Uninstall Instances"
        self.uninstall_action = QAction(QIcon("resources/icons/uninstall.png"), self.tr('Uninstall Instances'), self)
        self.uninstall_action.setToolTip(self.tr('Désinstaller des instances'))
        self.uninstall_action.triggered.connect(self.uninstall_instances)
        self.tools_menu.addAction(self.uninstall_action)

        # Sous-menu "Invisible Instances"
        self.invisible_action = QAction(QIcon("resources/icons/invisible.png"), self.tr('Invisible Instances'), self)
        self.invisible_action.setToolTip(self.tr('Afficher les instances invisibles'))
        self.invisible_action.triggered.connect(self.show_invisible_instances)
        self.tools_menu.addAction(self.invisible_action)

        # Sous-menu "Environement"
        self.environment_action = QAction(QIcon("resources/icons/environment.png"), self.tr('Environement'), self)
        self.environment_action.setToolTip(self.tr('Mettre à jour l\'environnement'))
        self.environment_action.triggered.connect(self.update_env)
        self.tools_menu.addAction(self.environment_action)

        # Sous-menu "Text to Robot"
        self.text_to_robot_action = QAction(QIcon("resources/icons/text.png"), self.tr('Text to Robot'), self)
        self.text_to_robot_action.setToolTip(self.tr('Mettre à jour le texte du robot'))
        self.text_to_robot_action.triggered.connect(self.update_text)
        self.tools_menu.addAction(self.text_to_robot_action)

        # Sous-menu "Delete Instance"
        self.delete_instance_action = QAction(QIcon("resources/icons/delete.png"), self.tr('Delete Instance'), self)
        self.delete_instance_action.setToolTip(self.tr('Supprimer une instance'))
        self.delete_instance_action.triggered.connect(self.delete_instance)
        self.tools_menu.addAction(self.delete_instance_action)

        # Sous-menu "Update Instance"
        self.update_instance_action = QAction(QIcon("resources/icons/update.png"), self.tr('Update Instance'), self)
        self.update_instance_action.setToolTip(self.tr('Mettre à jour l\'instance'))
        self.update_instance_action.triggered.connect(self.update_instance)
        self.tools_menu.addAction(self.update_instance_action)
        # Menu "Insight" (anciennement "Instance")
        self.insight_action = QAction(QIcon("resources/icons/insight.png"), self.tr('Insight'), self)
        self.insight_action.setToolTip(self.tr('Afficher les insights'))
        self.insight_action.triggered.connect(self.open_dashboard)
        menubar.addAction(self.insight_action)

        # Menu "Paramètres"
        self.settings_menu = menubar.addMenu(QIcon("resources/icons/settings.png"), self.tr('Theme'))
        
        # Option "Mode sombre"
        self.dark_mode_action = QAction(QIcon("resources/icons/dark_mode.png"), self.tr('Activer le mode sombre'), self, checkable=True)
        self.dark_mode_action.setToolTip(self.tr('Basculer vers le mode sombre'))
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        self.settings_menu.addAction(self.dark_mode_action)

        # Option "Personnaliser le thème"
        self.theme_action = QAction(QIcon("resources/icons/theme.png"), self.tr('Personnaliser le thème'), self)
        self.theme_action.setToolTip(self.tr('Changer les couleurs du thème'))
        self.theme_action.triggered.connect(self.customize_theme)
        self.settings_menu.addAction(self.theme_action)

        # Barre d'état
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Exemple de contenu central (à adapter)
        license_checker = LicenseChecker(license_dir="C:\\wabon")
        file_path = 'C:\\wabon\\robot1\\data.json'
        group_counter = GroupCounter(file_path)
        self.Nombregroup = group_counter.count_groups()

        # self.instance_table = Dashboard(
        #     title="AI WA ROBOT PRO",
        #     subtitle="Analytics Overview",
        #     validiter=license_checker.is_license_valid(),
        #     Nombregroupes=self.Nombregroup,
        #     totalshare="Nombre total",
        #     nexttimeshare="none"
        # )
        # layout.addWidget(self.instance_table)
        self.contacts = ContactTable(self)
        layout.addWidget(self.contacts)
    # # Méthodes pour les actions du menu
    def open_dashboard(self):
        # Afficher un écran de chargement
        loading_screen = LoadingScreen(self)
        loading_screen.show()

        # license_checker = LicenseChecker(license_dir="C:\\wabon")
        # file_path = 'C:\\wabon\\robot1\\data.json'
        # group_counter = GroupCounter(file_path)
        # Nombregroup = group_counter.count_groups()
        # dash = Dashboard(
        #     title="AI FB ROBOT PRO",
        #     subtitle="Analytics Overview",
        #     validiter=license_checker.is_license_valid(),
        #     Nombregroupes=Nombregroup,
        #     totalshare="Nombre total",
        #     nexttimeshare="none"
        # )
        # self.setCentralWidget(dash)
        # Simuler un chargement avec QTimer
        QTimer.singleShot(1, lambda: self.finish_loading(loading_screen))

    def finish_loading(self, loading_screen):
        # Fermer l'écran de chargement
    

        # Continuer avec le chargement du tableau de bord
        license_checker = LicenseChecker(license_dir="C:\\wabon")
        file_path = 'C:\\wabon\\robot1\\data.json'
        group_counter = GroupCounter(file_path)
        Nombregroup = group_counter.count_groups()

        dash = Dashboard(
            title="wa+ CRM",
            subtitle="Analytics Overview",
            validiter=license_checker.is_license_valid(),
            Nombregroupes=Nombregroup,
            totalshare=" total",
            nexttimeshare="none"
        )
        self.setCentralWidget(dash)
        loading_screen.close()
  
  
    def open_insight(self):
        QMessageBox.information(self, "Insight", "Fonctionnalité Insight")

    # def open_media(self):
    #     QMessageBox.information(self, "Médias", "Fonctionnalité Médias")

    # def open_contacts(self):
    #     QMessageBox.information(self, "Contacts", "Fonctionnalité Contacts")

    # def open_certificate(self):
    #     QMessageBox.information(self, "Certif", "Fonctionnalité Certif")

    # def open_about(self):
    #     QMessageBox.information(self, "About", "Fonctionnalité About")

    # def show_start_time(self):
    #     QMessageBox.information(self, "Heure de démarrage", "Fonctionnalité Heure de démarrage")

    # def uninstall_instances(self):
    #     QMessageBox.information(self, "Uninstall Instances", "Fonctionnalité Uninstall Instances")

    # def show_invisible_instances(self):
    #     QMessageBox.information(self, "Invisible Instances", "Fonctionnalité Invisible Instances")

    # def update_env(self):
    #     QMessageBox.information(self, "Environement", "Fonctionnalité Environement")

    # def update_text(self):
    #     QMessageBox.information(self, "Text to Robot", "Fonctionnalité Text to Robot")

    # def delete_instance(self):
    #     QMessageBox.information(self, "Delete Instance", "Fonctionnalité Delete Instance")

    # def update_instance(self):
    #     QMessageBox.information(self, "Update Instance", "Fonctionnalité Update Instance")

    # def toggle_dark_mode(self):
    #     QMessageBox.information(self, "Mode sombre", "Mode sombre activé/désactivé")

    # def customize_theme(self):
    #     QMessageBox.information(self, "Personnaliser le thème", "Fonctionnalité Personnaliser le thème")



    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','whatssappro','main_wp_robot_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','whatssappro','main_wp_robot_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','whatssappro','main_wp_robot_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','whatssappro','main_wp_robot_translated.qm'))

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
        self.setWindowTitle(self.tr('AI WP ROBOT Pro'))
        # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # Par exemple, pour les actions du menu :
        self.instance_action.setText(self.tr('Instance'))
        # self.instance_action.setText(self.tr('Home'))
        # self.instance_action.setText(self.tr('Installer'))

        self.media_action.setText(self.tr('Médias'))
        self.group_action.setText(self.tr('Contacts'))
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

    def open_contacts(self):
        self.setCentralWidget(ContactTable(self))

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
            self.tr("Êtes-vous sûr de vouloir désinstaller toutes les instances de Whatsapp Robot ? Cela retirera toutes vos instances."),
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
    window = WhatsMainWindow()
    window.show()
    sys.exit(app.exec_())
