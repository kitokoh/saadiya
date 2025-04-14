import json
import os
import subprocess
from PyQt5.QtCore import Qt, QTranslator, QLocale, QLibraryInfo, QPropertyAnimation
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QVBoxLayout, QWidget, QDialog, QLabel, QPushButton, \
    QMessageBox, QMenu, QComboBox, QStatusBar

from checklicence import LicenseChecker
from facebooksmodule.fb_robot_install import FbRobot
from facebooksmodule.group_manager import GroupTable
from imports import *
from installFBrobotPy.demarrageAuto import InstallerApp
from instances_table import InstanceTable
from facebooksmodule.media_manager import MediaTable
from statistique.nombredegrup import GroupCounter
from statistique.nombretotalShare import LogLineCounter
from statistique.prochainexecution import ScheduledTaskChecker
from statistique.stat import Dashboard
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from PyQt5.QtWidgets import QMessageBox, QLabel
from PyQt5.QtCore import Qt, QTimer
class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("À propos de AI FB ROBOT Pro"))
        layout = QVBoxLayout()
        label = QLabel(self.tr(
            "<div style='background-color:#F5F7FA; padding:15px; border-radius:10px;'>"
            "<h1 style='color:#1A5276; font-size:24px; font-weight:bold; text-align:center;'>Welcome to nova360.turknovatech.com</h1>"
            "<p style='font-size:16px; color:#333333; text-align:center;'><strong>Your All-in-One AI-Powered Social Media Automation Solution</strong></p><br>"
            "<div style='padding: 10px; border-left: 4px solid #1A5276;'><p style='font-size:14px; color:#5D6D7E; line-height:1.6; margin:0 20px;'>nova360.turknovatech.com is the essential tool for entrepreneurs, brands, and influencers looking to simplify and scale their social media presence. With advanced AI, nova360.turknovatech.com automates every aspect of your social media strategy, allowing you to engage effortlessly, grow your influence, and remain at the forefront of your audience’s minds.</p></div><br>"
            "<h3 style='color:#1A5276; font-size:18px; margin-top:20px; text-align:center;'>Core Features</h3><br>"
            "<ul style='font-size:14px; color:#4A4A4A; padding-left: 40px;'>"
            "<li style='margin-bottom:10px;'><strong>🌐 Smart Scheduling:</strong> Plan and post content across platforms with precision timing for maximum reach.</li><br>"
            "<li style='margin-bottom:10px;'><strong>🤖 Automated Audience Engagement:</strong> Engage your audience with intelligent replies and dynamic comments.</li><br>"
            "<li><strong>📂 Comprehensive Media & Media Management:</strong> Manage media assets, groups, and instances seamlessly to optimize your workflow.</li>"
            "</ul><br>"
            "<p style='font-size:14px; color:#5D6D7E; line-height:1.6; text-align:center;'>Join a thriving community of brands and individuals who trust nova360.turknovatech.com to elevate their social media automation. Save time, boost engagement, and focus on building your brand.</p><br>"
            "<p style='font-size:11px; color:#888888; text-align:center; margin-top:20px;'>© 2024 Nova360 Pro | <a href='https://www.nova360pro.com' style='color:#1A5276; text-decoration:none;'>www.nova360pro.com</a></p>"
            "</div>"
        ))
        layout.addWidget(label)
        close_button = QPushButton(self.tr("Fermer"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

class CertificateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Certificat"))
        layout = QVBoxLayout()
        label = QLabel(self.tr(
            "<div style='background-color:#FAF3E0; padding:15px; border-radius:8px;'>"
            "<h2 style='color:#D35400; font-size:20px; text-align:center;'>Expiration de Votre Licence</h2>"
            "<p style='font-size:14px; color:#4A4A4A; line-height:1.6;'>Votre licence est actuellement valide jusqu'au <strong style='color:#D35400;'>31 décembre 202x</strong>. Pour continuer à profiter de toutes les fonctionnalités premium de <strong>nova360.turknovatech.com</strong>, veuillez penser à renouveler votre licence avant cette date.</p><br>"
            "<div style='padding: 10px; border-left: 4px solid #D35400; margin: 10px 0;'><p style='font-size:13px; color:#7F8C8D; margin:0 20px;'>Après cette date, votre accès aux fonctionnalités premium sera restreint. Vous pourrez toujours accéder à votre compte mais avec des fonctionnalités limitées jusqu'au renouvellement de votre licence.</p></div><br>"
            "<h3 style='color:#D35400; font-size:16px;'>En Cas de Problème</h3>"
            "<ul style='font-size:13px; color:#4A4A4A; padding-left: 40px;'>"
            "<li style='margin-bottom:10px;'>Si votre instance ne fonctionne plus, vérifiez la connexion Internet et assurez-vous que la licence est active.</li><br>"
            "<li>Contactez notre support technique si vous rencontrez des difficultés supplémentaires.</li>"
            "</ul><br>"
            "<p style='font-size:12px; color:gray; text-align:center;'>Pour toute assistance, veuillez visiter <a href='https://support.nova360pro.com' style='color:#D35400; text-decoration:none;'>notre centre de support</a>.</p>"
            "</div>"
        ))
        layout.addWidget(label)
        close_button = QPushButton(self.tr("Fermer"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)
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


class FaceMainWindow(QMainWindow):
    def __iniiit__(self):
        super().__init__()
        self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        self.setGeometry(100, 210, 900, 600)
        self.setWindowIcon(QIcon('resources/icons/facebook-icon-png-770-Windows.ico'))
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
        self.home_action = QAction(QIcon("resources/icons/facebook-icon-png-745.png"), self.tr('Home'), self)
        self.home_action.setToolTip(self.tr('Afficher la liste des instances'))
        self.home_action.triggered.connect(self.open_dashboard)
        menubar.addAction(self.home_action)
        self.instance_action = QAction(QIcon("resources/icons/facebook-icon-png-745.png"), self.tr('Instance'), self)
        self.instance_action.setToolTip(self.tr('Afficher la liste des instances'))
        self.instance_action.triggered.connect(self.open_instance)
        menubar.addAction(self.instance_action)
        self.media_action = QAction(QIcon("resources/icons/facebook-icon-png-745.png"), self.tr('Médias'), self)
        self.media_action.setToolTip(self.tr('Afficher la liste des médias'))
        self.media_action.triggered.connect(self.open_media)
        menubar.addAction(self.media_action)
        self.group_action = QAction(QIcon("resources/icons/facebook-icon-png-745.png"), self.tr('Groupes'), self)
        self.group_action.setToolTip(self.tr('Afficher la liste des groupes'))
        self.group_action.triggered.connect(self.open_group)
        menubar.addAction(self.group_action)
        self.about_action = QAction(QIcon("resources/icons/facebook-icon-png-745.png"), self.tr('About'), self)
        self.about_action.setToolTip(self.tr('Informations sur l\'application'))
        self.about_action.triggered.connect(self.open_about)
        menubar.addAction(self.about_action)
        self.certificate_action = QAction(QIcon("resources/icons/facebook-icon-png-745.png"), self.tr('Certif'), self)
        self.certificate_action.setToolTip(self.tr('Informations sur votre certificat'))
        self.certificate_action.triggered.connect(self.open_certificate)
        menubar.addAction(self.certificate_action)
        self.settings_menu = menubar.addMenu(QIcon("resources/icons/settings.png"), self.tr('Param'))
        self.dark_mode_action = QAction(self.tr('Activer le mode sombre'), self, checkable=True)
        self.dark_mode_action.setToolTip(self.tr('Basculer vers le mode sombre'))
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        self.settings_menu.addAction(self.dark_mode_action)
        self.theme_action = QAction(self.tr('Personnaliser le thème'), self)
        self.theme_action.setToolTip(self.tr('Changer les couleurs du thème'))
        self.theme_action.triggered.connect(self.customize_theme)
        self.settings_menu.addAction(self.theme_action)
        self.instance_install = QAction(QIcon("resources/icons/install.png"), self.tr('Installer'), self)
        self.instance_install.setToolTip(self.tr('Installer des instances'))
        self.instance_install.triggered.connect(self.open_install)
        menubar.addAction(self.instance_install)
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
        self.tools_menu = menubar.addMenu(self.tr("Tools"))
        self.tools_menu.addAction(QAction(self.tr("Scheduling"), self, triggered=self.show_start_time))
        self.tools_menu.addAction(QAction(self.tr("Uninstall Instances"), self, triggered=self.uninstall_instances))
        self.tools_menu.addAction(QAction(self.tr("Update Robot"), self, triggered=self.update_text))
        self.tools_menu.addAction(QAction(self.tr("Update Instance"), self, triggered=self.update_instance))
        self.translator = QTranslator()
        self.init_language()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        license_checker = LicenseChecker(license_dir="C:\\bon")
        file_path = 'C:\\bon\\robot1\\data.json'
        group_counter = GroupCounter(file_path)
        self.Nombregroup = group_counter.count_groups()
        self.instance_table = Dashboard(
            title="AI FB ROBOT PRO",
            subtitle="Analytics Overview",
            validiter=license_checker.is_license_valid(),
            Nombregroupes=self.Nombregroup,
            totalshare="Nombre total",
            nexttimeshare="none"
        )
        layout.addWidget(self.instance_table)

    def __init__(self):
        super().__init__()
        self.translator = QTranslator()
        self.init_language()
        self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        self.setGeometry(100, 210, 900, 600)
        self.setWindowIcon(QIcon('resources/icons/facebook-icon-png-770-Windows.ico'))

        # Configuration de la barre de menus
        menubar_font = QFont("Arial", 10, QFont.Bold)
        menubar = self.menuBar()
        menubar.setFont(menubar_font)
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #2E3440;  /* Couleur de fond sombre */
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
        """)



        # Menu "Médias"
        self.media_action = QAction(QIcon("resources/icons/media.png"), self.tr('Médias'), self)
        self.media_action.setToolTip(self.tr('Afficher la liste des médias'))
        self.media_action.triggered.connect(self.open_media)
        menubar.addAction(self.media_action)

        # Menu "Groupes"
        self.group_action = QAction(QIcon("resources/icons/group.png"), self.tr('Groupes'), self)
        self.group_action.setToolTip(self.tr('Afficher la liste des groupes'))
        self.group_action.triggered.connect(self.open_group)
        menubar.addAction(self.group_action)

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

        # Sous-menu "Scheduling"
        self.scheduling_action = QAction(QIcon("resources/icons/schedule.png"), self.tr('Scheduling'), self)
        self.scheduling_action.setToolTip(self.tr('Planifier des tâches'))
        self.scheduling_action.triggered.connect(self.show_start_time)
        self.tools_menu.addAction(self.scheduling_action)

        # Sous-menu "Uninstall Instances"
        self.uninstall_action = QAction(QIcon("resources/icons/uninstall.png"), self.tr('Uninstall Instances'), self)
        self.uninstall_action.setToolTip(self.tr('Désinstaller des instances'))
        self.uninstall_action.triggered.connect(self.uninstall_instances)
        self.tools_menu.addAction(self.uninstall_action)

        # Sous-menu "Update Robot"
        self.update_robot_action = QAction(QIcon("resources/icons/update.png"), self.tr('Update Robot'), self)
        self.update_robot_action.setToolTip(self.tr('Mettre à jour le robot'))
        self.update_robot_action.triggered.connect(self.update_text)
        self.tools_menu.addAction(self.update_robot_action)

        # Sous-menu "Update Instance"
        self.update_instance_action = QAction(QIcon("resources/icons/update.png"), self.tr('Update Instance'), self)
        self.update_instance_action.setToolTip(self.tr('Mettre à jour l\'instance'))
        self.update_instance_action.triggered.connect(self.update_instance)
        self.tools_menu.addAction(self.update_instance_action)

        # Menu "Insight" (anciennement "Home")
        self.insight_action = QAction(QIcon("resources/icons/insight.png"), self.tr('Insight'), self)
        self.insight_action.setToolTip(self.tr('Afficher les insights'))
        self.insight_action.triggered.connect(self.open_dashboard)
        menubar.addAction(self.insight_action)


        # Menu "Insight" (anciennement "Home")
        self.Instances_action = QAction(QIcon("resources/icons/insight.png"), self.tr('Instance'), self)
        self.Instances_action.setToolTip(self.tr('Afficher les insights'))
        self.Instances_action.triggered.connect(self.open_install)
        menubar.addAction(self.Instances_action)
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
        # self.instance_table = Dashboard(
        #     title="AI FB ROBOT PRO",
        #     subtitle="Analytics Overview",
        #     validiter=True,  # Remplacez par votre logique de licence
        #     Nombregroupes=10,  # Remplacez par votre logique de comptage
        #     totalshare="Nombre total",
        #     nexttimeshare="none"
        # )
        self.group = MediaTable(self)
        layout.addWidget(self.group)
       # layout.addWidget(self.instance_table)

    # Méthodes pour les actions du menu
    def open_insight(self):
        QMessageBox.information(self, "Insight", "Fonctionnalité Insight")



        


    def switch_language(self, language):
        translator_path = os.path.join(user_data_dir, 'resources', 'lang', language, 'modules', 'main_fb_robot_translated.qm')
        
        if os.path.exists(translator_path):
            self.translator.load(translator_path)
        else:
            self.translator.load("")
        
        QApplication.instance().installTranslator(self.translator)
        self.save_language_choice(language)
        self.retranslateUi()

        # Affichage d'un popup vert
        self.show_success_message("Langue changée avec succès !")

    def show_success_message(self, message):
        # Crée une étiquette flottante pour afficher le message
        label = QLabel(message, self)
        label.setStyleSheet("""
            QLabel {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        label.setAlignment(Qt.AlignCenter)
        label.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip)
        label.adjustSize()

        # Positionne l'étiquette au centre de la fenêtre principale
        label.move(
            (self.width() - label.width()) // 2,
            (self.height() - label.height()) // 2
        )
        label.show()

        # Disparition automatique après 3 secondes
        QTimer.singleShot(3000, label.close)

    def save_language_choice(self, language):
        preferences = {'language': language}
        with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'w') as f:
            json.dump(preferences, f)

    def retranslateUi(self):
        self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # self.home_action.setText(self.tr('Home'))
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.settings_menu.setTitle(self.tr('Param'))
        # self.dark_mode_action.setText(self.tr('Activer le mode sombre'))
        # self.theme_action.setText(self.tr('Personnaliser le thème'))
        # self.instance_install.setText(self.tr('Installer'))
        # self.language_menu.setTitle(self.tr('Langue'))
        # self.tools_menu.setTitle(self.tr("Tools"))
        # self.tools_menu.actions()[0].setText(self.tr("Scheduling"))
        # self.tools_menu.actions()[1].setText(self.tr("Uninstall Instances"))
        # self.tools_menu.actions()[2].setText(self.tr("Update Robot"))
        # self.tools_menu.actions()[3].setText(self.tr("Update Instance"))

    def init_language(self):
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')
        else:
            system_locale = QLocale.system().name()[:2]
            language_map = {'en': 'en', 'fr': 'fr', 'tr': 'tr', 'ar': 'ar'}
            selected_language = language_map.get(system_locale, 'en')
        self.switch_language(selected_language)

    def open_media(self):
        self.setCentralWidget(MediaTable(self))

    def open_dashboad(self):
        license_checker = LicenseChecker(license_dir="C:\\bon")
        file_path = 'C:\\bon\\robot1\\data.json'
        group_counter = GroupCounter(file_path)
        Nombregroup = group_counter.count_groups()
        dash = Dashboard(
            title="AI FB ROBOT PRO",
            subtitle="Analytics Overview",
            validiter=license_checker.is_license_valid(),
            Nombregroupes=Nombregroup,
            totalshare="Nombre total",
            nexttimeshare="none"
        )
        self.setCentralWidget(dash)
    def open_dashboard(self):
        # Afficher un écran de chargement
        loading_screen = LoadingScreen(self)
        loading_screen.show()

        # license_checker = LicenseChecker(license_dir="C:\\bon")
        # file_path = 'C:\\bon\\robot1\\data.json'
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
        license_checker = LicenseChecker(license_dir="C:\\bon")
        file_path = 'C:\\bon\\robot1\\data.json'
        group_counter = GroupCounter(file_path)
        Nombregroup = group_counter.count_groups()

        dash = Dashboard(
            title="FB Robot Pro",
            subtitle="Analytics Overview",
            validiter=license_checker.is_license_valid(),
            Nombregroupes=Nombregroup,
            totalshare=" total",
            nexttimeshare="none"
        )
        self.setCentralWidget(dash)
        loading_screen.close()
  
  
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

    def uninstall_instances(self):
        reply = QMessageBox.question(
            self,
            self.tr("confirmez la désinstallation"),
            self.tr("Êtes-vous sûr de vouloir désinstaller toutes les instances de Facebook Robot ? Cela retirera toutes vos instances."),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            uninstall_exe_path = os.path.join(user_data_dir, "resources", "tools", "uninstall.exe")
            if os.path.exists(uninstall_exe_path):
                try:
                    subprocess.Popen([uninstall_exe_path], shell=True)
                    QMessageBox.information(self, self.tr("Désinstallation"), self.tr("Instances désinstallées avec succès."))
                    self.setCentralWidget(FbRobot())
                except Exception as e:
                    QMessageBox.critical(self, self.tr("Erreur"), self.tr(f"Impossible d'exécuter uninstall.exe : {str(e)}"))
            else:
                QMessageBox.critical(self, self.tr("Erreur"), self.tr(f"Le fichier {uninstall_exe_path} est introuvable."))
        else:
            QMessageBox.information(self, self.tr("Annulé"), self.tr("Désinstallation annulée."))

    def update_text(self):
        QMessageBox.information(self, self.tr("MAJ Text"), self.tr("Texte mis à jour avec succès."))
        self.setCentralWidget(JsonToRobot())

    def update_instance(self):
        QMessageBox.information(self, self.tr("Update Instance"), self.tr("Instance mise à jour avec succès."))
        self.setCentralWidget(UpdateInstance())

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = FaceMainWindow()
    window.show()
    sys.exit(app.exec_())