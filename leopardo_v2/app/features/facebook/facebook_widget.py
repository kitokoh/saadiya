import json
import os
import subprocess
from PyQt5.QtCore import Qt, QTranslator, QLocale, QLibraryInfo, QPropertyAnimation, QTimer
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QVBoxLayout, QWidget, QDialog, QLabel, QPushButton, \
    QMessageBox, QMenu, QComboBox, QStatusBar

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


class FacebookWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.translator = QTranslator()
        self.init_language()
        self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        self.setGeometry(100, 210, 900, 600)
        self.setWindowIcon(QIcon('resources/icons/facebook-icon-png-770-Windows.ico'))

        menubar_font = QFont("Arial", 10, QFont.Bold)
        menubar = self.menuBar()
        menubar.setFont(menubar_font)
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #2E3440;
                color: #ECEFF4;
                padding: 5px;
            }
            QMenuBar::item {
                padding: 8px 25px;
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #4C566A;
            }
            QMenu {
                background-color: #3B4252;
                color: #ECEFF4;
                padding: 10px;
                border: 1px solid #4C566A;
            }
            QMenu::item:selected {
                background-color: #4C566A;
            }
        """)

        self.media_action = QAction(QIcon("resources/icons/media.png"), self.tr('Médias'), self)
        self.media_action.setToolTip(self.tr('Afficher la liste des médias'))
        self.media_action.triggered.connect(self.open_media)
        menubar.addAction(self.media_action)

        self.group_action = QAction(QIcon("resources/icons/group.png"), self.tr('Groupes'), self)
        self.group_action.setToolTip(self.tr('Afficher la liste des groupes'))
        self.group_action.triggered.connect(self.open_group)
        menubar.addAction(self.group_action)

        self.tools_menu = menubar.addMenu(QIcon("resources/icons/tools.png"), self.tr('Tools'))

        self.certificate_action = QAction(QIcon("resources/icons/certificate.png"), self.tr('Certif'), self)
        self.certificate_action.setToolTip(self.tr('Informations sur votre certificat'))
        self.certificate_action.triggered.connect(self.open_certificate)
        self.tools_menu.addAction(self.certificate_action)

        self.about_action = QAction(QIcon("resources/icons/about.png"), self.tr('About'), self)
        self.about_action.setToolTip(self.tr('Informations sur l\'application'))
        self.about_action.triggered.connect(self.open_about)
        self.tools_menu.addAction(self.about_action)

        self.tools_menu.addSeparator()

        self.scheduling_action = QAction(QIcon("resources/icons/schedule.png"), self.tr('Scheduling'), self)
        self.scheduling_action.setToolTip(self.tr('Planifier des tâches'))
        self.scheduling_action.triggered.connect(self.show_start_time)
        self.tools_menu.addAction(self.scheduling_action)

        self.uninstall_action = QAction(QIcon("resources/icons/uninstall.png"), self.tr('Uninstall Instances'), self)
        self.uninstall_action.setToolTip(self.tr('Désinstaller des instances'))
        self.uninstall_action.triggered.connect(self.uninstall_instances)
        self.tools_menu.addAction(self.uninstall_action)

        self.update_robot_action = QAction(QIcon("resources/icons/update.png"), self.tr('Update Robot'), self)
        self.update_robot_action.setToolTip(self.tr('Mettre à jour le robot'))
        self.update_robot_action.triggered.connect(self.update_text)
        self.tools_menu.addAction(self.update_robot_action)

        self.update_instance_action = QAction(QIcon("resources/icons/update.png"), self.tr('Update Instance'), self)
        self.update_instance_action.setToolTip(self.tr('Mettre à jour l\'instance'))
        self.update_instance_action.triggered.connect(self.update_instance)
        self.tools_menu.addAction(self.update_instance_action)

        self.insight_action = QAction(QIcon("resources/icons/insight.png"), self.tr('Insight'), self)
        self.insight_action.setToolTip(self.tr('Afficher les insights'))
        self.insight_action.triggered.connect(self.open_dashboard)
        menubar.addAction(self.insight_action)

        self.Instances_action = QAction(QIcon("resources/icons/insight.png"), self.tr('Instance'), self)
        self.Instances_action.setToolTip(self.tr('Afficher les insights'))
        self.Instances_action.triggered.connect(self.open_install)
        menubar.addAction(self.Instances_action)

        self.settings_menu = menubar.addMenu(QIcon("resources/icons/settings.png"), self.tr('Theme'))

        self.dark_mode_action = QAction(QIcon("resources/icons/dark_mode.png"), self.tr('Activer le mode sombre'), self, checkable=True)
        self.dark_mode_action.setToolTip(self.tr('Basculer vers le mode sombre'))
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        self.settings_menu.addAction(self.dark_mode_action)

        self.theme_action = QAction(QIcon("resources/icons/theme.png"), self.tr('Personnaliser le thème'), self)
        self.theme_action.setToolTip(self.tr('Changer les couleurs du thème'))
        self.theme_action.triggered.connect(self.customize_theme)
        self.settings_menu.addAction(self.theme_action)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.group = QWidget(self)
        layout.addWidget(self.group)

    def switch_language(self, language):
        translator_path = os.path.join('resources', 'lang', language, 'modules', 'main_fb_robot_translated.qm')

        if os.path.exists(translator_path):
            self.translator.load(translator_path)
        else:
            self.translator.load("")

        QApplication.instance().installTranslator(self.translator)
        self.save_language_choice(language)
        self.retranslateUi()

        self.show_success_message("Langue changée avec succès !")

    def show_success_message(self, message):
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

        label.move(
            (self.width() - label.width()) // 2,
            (self.height() - label.height()) // 2
        )
        label.show()

        QTimer.singleShot(3000, label.close)

    def save_language_choice(self, language):
        preferences = {'language': language}
        with open(os.path.join('resources', 'settings.json'), 'w') as f:
            json.dump(preferences, f)

    def retranslateUi(self):
        self.setWindowTitle(self.tr('AI FB ROBOT Pro'))

    def init_language(self):
        if os.path.exists(os.path.join('resources', 'settings.json')):
            with open(os.path.join('resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')
        else:
            system_locale = QLocale.system().name()[:2]
            language_map = {'en': 'en', 'fr': 'fr', 'tr': 'tr', 'ar': 'ar'}
            selected_language = language_map.get(system_locale, 'en')
        self.switch_language(selected_language)

    def open_media(self):
        print("Open Media")

    def open_dashboard(self):
        print("Open Dashboard")

    def open_instance(self):
        print("Open Instance")

    def open_install(self):
        print("Open Install")

    def open_group(self):
        print("Open Group")

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
        print("Show Start Time")

    def uninstall_instances(self):
        reply = QMessageBox.question(
            self,
            self.tr("confirmez la désinstallation"),
            self.tr("Êtes-vous sûr de vouloir désinstaller toutes les instances de Facebook Robot ? Cela retirera toutes vos instances."),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            uninstall_exe_path = os.path.join("resources", "tools", "uninstall.exe")
            if os.path.exists(uninstall_exe_path):
                try:
                    subprocess.Popen([uninstall_exe_path], shell=True)
                    QMessageBox.information(self, self.tr("Désinstallation"), self.tr("Instances désinstallées avec succès."))
                except Exception as e:
                    QMessageBox.critical(self, self.tr("Erreur"), self.tr(f"Impossible d'exécuter uninstall.exe : {str(e)}"))
            else:
                QMessageBox.critical(self, self.tr("Erreur"), self.tr(f"Le fichier {uninstall_exe_path} est introuvable."))
        else:
            QMessageBox.information(self, self.tr("Annulé"), self.tr("Désinstallation annulée."))

    def update_text(self):
        QMessageBox.information(self, self.tr("MAJ Text"), self.tr("Texte mis à jour avec succès."))

    def update_instance(self):
        QMessageBox.information(self, self.tr("Update Instance"), self.tr("Instance mise à jour avec succès."))
