import json
import os
import subprocess
from PyQt5.QtCore import Qt, QTranslator, QLocale, QLibraryInfo, QPropertyAnimation
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QVBoxLayout, QWidget, QDialog, QLabel, QPushButton, \
    QMessageBox, QMenu, QComboBox, QStatusBar, QStackedWidget

# from ...ModulesUI.adsPro.installwhattsaping.invisibleQT import InvisibleInstance
# from ...ModulesUI.adsPro.installwhattsaping.jsontorobot import JsonToRobot
# from ...ModulesUI.adsPro.installwhattsaping.majenvqt import MajEnv
# from ...ModulesUI.adsPro.installwhattsaping.supprimBon import DeleteBon
# from ...ModulesUI.adsPro.installwhattsaping.updateInstanceQt import UpdateInstance
# from ...ModulesUI.adsPro.wp_robot_install import WpRobot
# from ...ModulesUI.tiktok.group_manager import GroupTable
# from ...ModulesUI.tiktok.instances_table import InstanceTable
# from ...ModulesUI.tiktok.media_manager import MediaTable
# from ...imports import *
# from ...installFBrobotPy.demarrageAuto import InstallerApp
# from ...statistique.stat import Dashboard
# from ...translation import TranslatorManager

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About AI AdsPro ROBOT Pro")
        layout = QVBoxLayout()
        label = QLabel(
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
            )
        layout.addWidget(label)
        close_button = QPushButton("Close")
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
        self.setWindowTitle("Certificate")
        layout = QVBoxLayout()
        label = QLabel(
                "<div style='background-color:#FAF3E0; padding:15px; border-radius:8px;'>"
                "<h2 style='color:#D35400; font-size:20px; text-align:center;'>License Expiration</h2>"

                "<p style='font-size:14px; color:#4A4A4A; line-height:1.6;'>"
                "Your license is currently valid until <strong style='color:#D35400;'>December 31, 202x</strong>.<br>"
                "To continue enjoying all the premium features of <strong>Nova360.ai</strong>, please consider renewing your license before this date.<br>"
                "</p><br>"

                "<div style='padding: 10px; border-left: 4px solid #D35400; margin: 10px 0;'>"
                "<p style='font-size:13px; color:#7F8C8D; margin:0 20px;'>"
                "After this date, your access to premium features will be restricted. You will still be able to access your account but with limited functionality until you renew your license."
                "</p>"
                "</div><br>"

                "<h3 style='color:#D35400; font-size:16px;'>In Case of Issues</h3>"

                "<ul style='font-size:13px; color:#4A4A4A; padding-left: 40px;'>"
                "<li style='margin-bottom:10px;'>If your instance stops working, check your internet connection and ensure the license is active.</li><br>"
                "<li>Contact our technical support if you encounter further difficulties.</li>"
                "</ul><br>"

                "<p style='font-size:12px; color:gray; text-align:center;'>"
                "For any assistance, please visit <a href='https://support.nova360pro.com' style='color:#D35400; text-decoration:none;'>our support center</a>."
                "</p>"
                "</div>"
            )
        layout.addWidget(label)
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.setLayout(layout)

        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

class AdsManagerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('AI AdsPro ROBOT Pro')

        main_layout = QVBoxLayout(self)

        menubar_font = QFont("Arial", 10, QFont.Bold)
        menubar = QMenuBar()
        menubar.setFont(menubar_font)
        main_layout.setMenuBar(menubar)

        self.instance_action = QAction(QIcon("ressources/icons/facebook-icon-png-745.png"), 'Instance', self)
        self.instance_action.setToolTip('Display instance list')
        self.instance_action.triggered.connect(self.open_instance)
        menubar.addAction(self.instance_action)

        self.media_action = QAction(QIcon("ressources/icons/facebook-icon-png-745.png"), 'Media', self)
        self.media_action.setToolTip('Display media list')
        self.media_action.triggered.connect(self.open_media)
        menubar.addAction(self.media_action)

        self.group_action = QAction(QIcon("ressources/icons/facebook-icon-png-745.png"), 'Groups', self)
        self.group_action.setToolTip('Display group list')
        self.group_action.triggered.connect(self.open_group)
        menubar.addAction(self.group_action)

        self.about_action = QAction(QIcon("ressources/icons/facebook-icon-png-745.png"), 'About', self)
        self.about_action.setToolTip('Application information')
        self.about_action.triggered.connect(self.open_about)
        menubar.addAction(self.about_action)

        self.certificate_action = QAction(QIcon("ressources/icons/facebook-icon-png-745.png"), 'Certificate', self)
        self.certificate_action.setToolTip('Certificate information')
        self.certificate_action.triggered.connect(self.open_certificate)
        menubar.addAction(self.certificate_action)

        self.settings_menu = menubar.addMenu(QIcon("ressources/icons/settings.png"), 'Settings')
        self.dark_mode_action = QAction('Enable dark mode', self, checkable=True)
        self.dark_mode_action.setToolTip('Switch to dark mode')
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        self.settings_menu.addAction(self.dark_mode_action)
        self.theme_action = QAction('Customize theme', self)
        self.theme_action.setToolTip('Change theme colors')
        self.theme_action.triggered.connect(self.customize_theme)
        self.settings_menu.addAction(self.theme_action)

        self.instance_install = QAction(QIcon("ressources/icons/install.png"), 'Install', self)
        self.instance_install.setToolTip('Install instances')
        self.instance_install.triggered.connect(self.open_install)
        menubar.addAction(self.instance_install)

        self.language_menu = QMenu('Language', self)
        switch_language_en = QAction('English', self)
        switch_language_en.triggered.connect(lambda: self.switch_language("en"))
        self.language_menu.addAction(switch_language_en)
        switch_language_fr = QAction('French', self)
        switch_language_fr.triggered.connect(lambda: self.switch_language("fr"))
        self.language_menu.addAction(switch_language_fr)
        switch_language_tr = QAction('Turkish', self)
        switch_language_tr.triggered.connect(lambda: self.switch_language("tr"))
        self.language_menu.addAction(switch_language_tr)
        switch_language_ar = QAction('Arabic', self)
        switch_language_ar.triggered.connect(lambda: self.switch_language("ar"))
        self.language_menu.addAction(switch_language_ar)
        menubar.addMenu(self.language_menu)

        self.tools_menu = menubar.addMenu("Tools")
        self.tools_menu.addAction(QAction("Start Time", self, triggered=self.show_start_time))
        self.tools_menu.addAction(QAction("Uninstall Instances", self, triggered=self.uninstall_instances))
        self.tools_menu.addAction(QAction("Invisible Instances", self, triggered=self.show_invisible_instances))
        self.tools_menu.addAction(QAction("Environment", self, triggered=self.update_env))
        self.tools_menu.addAction(QAction("Text to Robot", self, triggered=self.update_text))
        self.tools_menu.addAction(QAction("Delete Instance", self, triggered=self.delete_instance))
        self.tools_menu.addAction(QAction("Update Instance", self, triggered=self.update_instance))

        self.status_bar = QStatusBar()
        main_layout.addWidget(self.status_bar)

        self.content_stack = QStackedWidget(self)
        main_layout.addWidget(self.content_stack)

    def open_media(self):
        # self.content_stack.setCurrentWidget(self.media_table)
        pass

    def open_instance(self):
        # self.content_stack.setCurrentWidget(self.instance_table)
        pass

    def open_install(self):
        # self.content_stack.setCurrentWidget(self.wp_robot)
        pass

    def open_group(self):
        # self.content_stack.setCurrentWidget(self.group_table)
        pass

    def open_about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def open_certificate(self):
        certificate_dialog = CertificateDialog(self)
        certificate_dialog.exec_()

    def toggle_dark_mode(self):
        pass

    def customize_theme(self):
        QMessageBox.information(self, "Customize Theme", "This feature will be available soon.")

    def show_start_time(self):
        pass

    def uninstall_instances(self):
        pass

    def show_invisible_instances(self):
        pass

    def update_env(self):
        pass

    def update_text(self):
        pass

    def delete_instance(self):
        pass

    def update_instance(self):
        pass

    def switch_language(self, lang):
        pass
