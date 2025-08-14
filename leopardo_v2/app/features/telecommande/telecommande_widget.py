import json
import logging
import os
import platform
import requests
import subprocess
import sys
import webbrowser
from PyQt5.QtCore import QPropertyAnimation, pyqtProperty, QSettings, Qt, QTimer, QTime, QDateTime, QProcess, QSize, QPoint, QRect
from PyQt5.QtGui import QFont, QIcon, QColor, QPixmap, QMovie
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QSplitter, QTabWidget, QHBoxLayout,
    QPushButton, QLabel, QSizePolicy, QGraphicsDropShadowEffect, QDesktopWidget,
    QMainWindow, QTextEdit, QMessageBox, QDialog, QGraphicsOpacityEffect, QProgressBar,
    QToolButton, QWidgetAction, QListWidget, QListWidgetItem, QFrame, QMenu, QCheckBox,
    QDialogButtonBox, QFormLayout, QRadioButton
)

class FirstTimeGuide(QDialog):
    # ... (omitted for brevity) ...

class AnimatedScreen(QLabel):
    # ... (omitted for brevity) ...

class TelecommandeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark_theme = True
        self.settings = self.load_settings()
        self.chrome_profiles = self.detect_chrome_profiles()
        self.initUI()

    def load_settings(self):
        # ... (omitted for brevity) ...

    def save_settings(self):
        # ... (omitted for brevity) ...

    def detect_chrome_profiles(self):
        """Détecte les profils Chrome disponibles"""
        profiles = ["Default"]
        chrome_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")

        try:
            if os.path.exists(chrome_path):
                for item in os.listdir(chrome_path):
                    if item.startswith("Profile ") or item == "Default":
                        profiles.append(item)
        except Exception as e:
            print(f"Erreur détection profils Chrome: {str(e)}")

        return list(set(profiles))

    def initUI(self):
        self.setWindowTitle("Leopardo AI - Remote Control")
        self.setWindowIcon(QIcon('../resources/icons/robot-icons-30504-Windows.ico'))
        self.setFixedSize(450, 730)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(5, 5, 5, 5)

        screen_geometry = QDesktopWidget().availableGeometry()
        window_width = 450
        window_height = 700
        x = screen_geometry.width() - window_width - 10
        y = (screen_geometry.height() - window_height) // 2 - 70
        self.move(x, y)

        self.screen = AnimatedScreen("Ready to Control", self)
        main_layout.addWidget(self.screen)

        # Browser settings
        browser_group = QGroupBox("Browser Settings")
        browser_layout = QHBoxLayout(browser_group)
        self.chrome_radio = QRadioButton("Chrome")
        self.chrome_radio.setChecked(True)
        self.firefox_radio = QRadioButton("Firefox")
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(self.chrome_profiles)
        self.profile_combo.setCurrentText("Default")
        self.chrome_radio.toggled.connect(lambda: self.profile_combo.setEnabled(self.chrome_radio.isChecked()))
        browser_layout.addWidget(QLabel("Browser:"))
        browser_layout.addWidget(self.chrome_radio)
        browser_layout.addWidget(self.firefox_radio)
        browser_layout.addWidget(QLabel("Chrome Profile:"))
        browser_layout.addWidget(self.profile_combo)
        main_layout.addWidget(browser_group)

        central_layout = QHBoxLayout()
        left_buttons = QVBoxLayout()

        button_actions = {
            "FB Robot": lambda: self.execute_robot_in_tab("FB Robot","Robot satarting","resources/gifs/fb_robot.gif"),
            "Multi FB": lambda: self.execute_robot_in_tab("Multi FB","Robot satarting","resources/gifs/multi_fb.gif"),
            "WA +": lambda: self.execute_robot_in_tab("WA +","Robot satarting","resources/gifs/wa.gif"),
            "WA CRM": lambda: self.execute_robot_in_tab("WA CRM","Robot satarting","resources/gifs/wa_crm.gif"),
            "FB Semi-Auto": lambda: self.execute_robot_in_tab("FB Semi-Auto","Robot satarting","resources/gifs/fb_comment.gif"),
            "Insta": lambda: self.execute_robot_in_tab("Insta","Robot satarting","resources/gifs/insta.gif"),
        }
        self.button_states = {}
        for name, icon in [("FB Robot", "resources/icons/fb_robot.ico"), ("Multi FB", "resources/icons/multi_fb.ico"),
                        ("WA +", "resources/icons/wa.png"), ("WA CRM", "resources/icons/wa_crm.png"),("FB Semi-Auto", "resources/icons/fb_comment.png"),("Insta", "resources/icons/insta.ico")]:
            btn = self.create_small_button(name, icon)
            left_buttons.addWidget(btn)
            if name in button_actions:
                btn.clicked.connect(button_actions[name])

        central_layout.addLayout(left_buttons)
        main_layout.addLayout(central_layout)

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_terminal_tab)
        main_layout.addWidget(self.tab_widget)
        self.processes = {}

        self.setLayout(main_layout)

    def create_small_button(self, text, icon_path):
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        return button

    def execute_robot_in_tab(self, robot_name, message, gif_path):
        # ... (omitted for brevity) ...
        robot_path = self.get_robot_path(robot_name)
        # ... (omitted for brevity) ...

        if self.chrome_radio.isChecked():
            profile = self.profile_combo.currentText()
            chrome_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
            command = [chrome_path, f"--profile-directory={profile}", robot_path]
        else:
            command = [robot_path]

        process = self.run_executable_in_tab(command, terminal_output)
        # ... (omitted for brevity) ...

    # ... (the rest of the class methods) ...
    def get_robot_path(self, robot_name):
        # ... (omitted for brevity) ...
        return None

    def run_executable_in_tab(self, command, output_widget):
        # ... (omitted for brevity) ...
        process = QProcess(self)
        process.start(command[0], command[1:])
        return process

    def close_terminal_tab(self, index):
        # ... (omitted for brevity) ...
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    remote = TelecommandeWidget()
    remote.show()
    sys.exit(app.exec_())
