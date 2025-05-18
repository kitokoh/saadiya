import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, 
                            QPushButton, QProgressBar, QTextEdit, QMessageBox, QCheckBox)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QDialog

# Import existing update functions (they should be in a separate module)
from AutoUpdater.autoupdatefonctionnelle1 import perform_update, is_admin, elevate_privileges, load_app_info, fetch_update_info
import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QProgressBar, QTextEdit, QMessageBox, 
                            QCheckBox, QFrame, QSizePolicy, QSpacerItem)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QLinearGradient, QPainter
from PyQt5.QtSvg import QSvgWidget
import sqlite3
from datetime import datetime

# Import existing update functions

import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QProgressBar, QTextEdit, QMessageBox, 
                            QCheckBox, QFrame, QSizePolicy, QSpacerItem, QDialog)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QLinearGradient, QPainter
from PyQt5.QtSvg import QSvgWidget
import sqlite3
from datetime import datetime

# Import existing update functions

# Database setup
DB_FILE = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'leopardo_updater.db')
# DB_FILE = "leopardo_updater.db"

# Style constants
PRIMARY_COLOR = "#6E48AA"
SECONDARY_COLOR = "#9D50BB"
ACCENT_COLOR = "#4776E6"
DARK_COLOR = "#2D2D39"
LIGHT_COLOR = "#F8F9FA"
TEXT_COLOR = "#FFFFFF"
SUCCESS_COLOR = "#4CAF50"
WARNING_COLOR = "#FFC107"
ERROR_COLOR = "#F44336"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS settings_updates
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  auto_check INTEGER DEFAULT 1,
                  notify_beta INTEGER DEFAULT 0,
                  last_check TEXT,
                  theme TEXT DEFAULT 'dark')''')
    
    c.execute("SELECT COUNT(*) FROM settings_updates")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO settings_updates (auto_check, notify_beta, theme) VALUES (1, 0, 'dark')")
    conn.commit()
    conn.close()

def get_setting(setting_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(f"SELECT {setting_name} FROM settings_updates WHERE id=1")
    result = c.fetchone()[0]
    conn.close()
    return result

def update_setting(setting_name, value):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(f"UPDATE settings_updates SET {setting_name}=? WHERE id=1", (value,))
    conn.commit()
    conn.close()

def update_last_check():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("UPDATE settings_updates SET last_check=? WHERE id=1", (now,))
    conn.commit()
    conn.close()

class GradientButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(40)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Use protected attributes instead of properties to avoid recursion
        self._color1 = QColor(PRIMARY_COLOR)
        self._color2 = QColor(SECONDARY_COLOR)
        
        # Animation
        self.animation = QPropertyAnimation(self, b"_color1")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        
        self.animation2 = QPropertyAnimation(self, b"_color2")
        self.animation2.setDuration(300)
        self.animation2.setEasingCurve(QEasingCurve.OutQuad)
    
    def enterEvent(self, event):
        self.animation.stop()
        self.animation.setEndValue(QColor(ACCENT_COLOR))
        self.animation.start()
        
        self.animation2.stop()
        self.animation2.setEndValue(QColor(PRIMARY_COLOR))
        self.animation2.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.animation.stop()
        self.animation.setEndValue(QColor(PRIMARY_COLOR))
        self.animation.start()
        
        self.animation2.stop()
        self.animation2.setEndValue(QColor(SECONDARY_COLOR))
        self.animation2.start()
        super().leaveEvent(event)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create gradient
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, self._color1)
        gradient.setColorAt(1, self._color2)
        
        # Draw rounded rectangle
        rect = self.rect()
        radius = min(rect.width(), rect.height()) / 2
        
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, radius, radius)
        
        # Draw text
        painter.setPen(QColor(TEXT_COLOR))
        painter.drawText(rect, Qt.AlignCenter, self.text())
    
    def _get_color1(self):
        return self._color1
    
    def _set_color1(self, color):
        self._color1 = color
        self.update()
    
    def _get_color2(self):
        return self._color2
    
    def _set_color2(self, color):
        self._color2 = color
        self.update()
    
    # Use property correctly without causing recursion
    color1 = property(_get_color1, _set_color1)
    color2 = property(_get_color2, _set_color2)

class UpdateWorker(QThread):
    update_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.check_only = False
    
    def set_check_only(self, check_only):
        self.check_only = check_only
    
    def run(self):
        try:
            app_info = load_app_info()
            if not app_info:
                self.error_signal.emit("Failed to load application info")
                return
            
            update_info = fetch_update_info()
            if not update_info:
                self.error_signal.emit("Failed to fetch update information")
                return
            
            current_version = app_info.get('current_version', '0.0.0')
            new_version = update_info['latest_version']
            
            result = {
                'current_version': current_version,
                'new_version': new_version,
                'update_available': False,
                'release_notes': update_info.get('release_notes', 'No release notes available'),
                'check_only': self.check_only
            }
            
            if tuple(map(int, current_version.split('.'))) < tuple(map(int, new_version.split('.'))):
                result['update_available'] = True
                result['download_url'] = update_info['url']
                result['file_hash'] = update_info.get('sha256')
            
            self.update_signal.emit(result)
            update_last_check()
            
            if not self.check_only and result['update_available']:
                self.perform_update(app_info, update_info)
        except Exception as e:
            self.error_signal.emit(str(e))
    
    def perform_update(self, app_info, update_info):
        perform_update()

class AnimatedProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animation = QPropertyAnimation(self, b"value")
        self._animation.setDuration(1000)
        self._animation.setEasingCurve(QEasingCurve.OutQuad)
        
        self.setTextVisible(False)
        self.setStyleSheet(f"""
            QProgressBar {{
                border-radius: 6px;
                background-color: {DARK_COLOR};
                height: 12px;
            }}
            QProgressBar::chunk {{
                border-radius: 6px;
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 {PRIMARY_COLOR}, stop:1 {ACCENT_COLOR});
            }}
        """)
    
    def setValueAnimated(self, value):
        self._animation.stop()
        self._animation.setStartValue(self.value())
        self._animation.setEndValue(value)
        self._animation.start()

class UpdaterWindow(QMainWindow):
    def __init__(self, parent=None):        

        super().__init__(parent)
        self.setWindowTitle("Leopardo AI Updater")
        self.setWindowIcon(QIcon("leopardo_icon.ico"))
        self.setMinimumSize(600, 600)
        
        # Initialize database
        init_db()
        
        # Set theme
        self.current_theme = get_setting('theme')
        self.apply_theme()
        
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Header
        self.create_header()
        
        # Status card
        self.create_status_card()
        
        # Release notes card
        self.create_release_notes_card()
        
        # Progress bar
        self.progress_bar = AnimatedProgressBar()
        self.progress_bar.setVisible(False)
        self.main_layout.addWidget(self.progress_bar)
        
        # Buttons
        self.create_button_row()
        
        # Spacer
        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Footer
        self.create_footer()
        
        # Initialize worker thread
        self.worker = UpdateWorker()
        self.worker.update_signal.connect(self.handle_update_info)
        self.worker.error_signal.connect(self.handle_error)
        self.worker.progress_signal.connect(self.update_progress)
        
        # Check for updates on startup if auto-check is enabled
        if get_setting('auto_check'):
            self.check_for_updates()
    
    def apply_theme(self):
        palette = QPalette()
        
        if self.current_theme == 'dark':
            palette.setColor(QPalette.Window, QColor(DARK_COLOR))
            palette.setColor(QPalette.WindowText, QColor(TEXT_COLOR))
            palette.setColor(QPalette.Base, QColor("#3D3D4A"))
            palette.setColor(QPalette.AlternateBase, QColor(DARK_COLOR))
            palette.setColor(QPalette.ToolTipBase, QColor(TEXT_COLOR))
            palette.setColor(QPalette.ToolTipText, QColor(TEXT_COLOR))
            palette.setColor(QPalette.Text, QColor(TEXT_COLOR))
            palette.setColor(QPalette.Button, QColor("#3D3D4A"))
            palette.setColor(QPalette.ButtonText, QColor(TEXT_COLOR))
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Highlight, QColor(ACCENT_COLOR))
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            palette.setColor(QPalette.Window, QColor(LIGHT_COLOR))
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.AlternateBase, QColor(LIGHT_COLOR))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, QColor("#E0E0E0"))
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Highlight, QColor(ACCENT_COLOR))
            palette.setColor(QPalette.HighlightedText, Qt.white)
        
        QApplication.setPalette(palette)
    
    def create_header(self):
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Logo and title
        logo_title = QWidget()
        logo_layout = QHBoxLayout(logo_title)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(15)
        
        # Logo placeholder (replace with actual logo)
        self.logo = QLabel()
        self.logo.setPixmap(QIcon("leopardo_icon.ico").pixmap(40, 40))
        logo_layout.addWidget(self.logo)
        
        title = QLabel("Leopardo AI")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setWeight(QFont.Bold)
        title.setFont(title_font)
        logo_layout.addWidget(title)
        
        logo_layout.addStretch()
        header_layout.addWidget(logo_title)
        
        # Theme toggle button
        self.theme_button = QPushButton()
        self.theme_button.setIcon(QIcon.fromTheme("color-management" if self.current_theme == 'dark' else "color-management"))
        self.theme_button.setFlat(True)
        self.theme_button.setFixedSize(30, 30)
        self.theme_button.setCursor(Qt.PointingHandCursor)
        self.theme_button.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_button)
        
        self.main_layout.addWidget(header)
    
    def create_status_card(self):
        self.status_card = QFrame()
        self.status_card.setFrameShape(QFrame.StyledPanel)
        self.status_card.setStyleSheet(f"""
            QFrame {{
                background-color: {'#3D3D4A' if self.current_theme == 'dark' else '#FFFFFF'};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        
        card_layout = QVBoxLayout(self.status_card)
        card_layout.setSpacing(10)
        
        self.status_title = QLabel("Checking for updates...")
        status_font = QFont()
        status_font.setPointSize(14)
        status_font.setWeight(QFont.Bold)
        self.status_title.setFont(status_font)
        self.status_title.setAlignment(Qt.AlignCenter)
        
        self.version_label = QLabel()
        self.version_label.setAlignment(Qt.AlignCenter)
        
        card_layout.addWidget(self.status_title)
        card_layout.addWidget(self.version_label)
        
        self.main_layout.addWidget(self.status_card)
    
    def create_release_notes_card(self):
        self.release_notes_card = QFrame()
        self.release_notes_card.setFrameShape(QFrame.StyledPanel)
        self.release_notes_card.setStyleSheet(f"""
            QFrame {{
                background-color: {'#3D3D4A' if self.current_theme == 'dark' else '#FFFFFF'};
                border-radius: 10px;
                padding: 15px;
            }}
            QTextEdit {{
                background-color: transparent;
                border: none;
                color: {TEXT_COLOR if self.current_theme == 'dark' else 'black'};
            }}
        """)
        self.release_notes_card.setVisible(False)
        
        card_layout = QVBoxLayout(self.release_notes_card)
        
        notes_title = QLabel("Release Notes")
        notes_title_font = QFont()
        notes_title_font.setPointSize(12)
        notes_title_font.setWeight(QFont.Bold)
        notes_title.setFont(notes_title_font)
        
        self.release_notes = QTextEdit()
        self.release_notes.setReadOnly(True)
        
        card_layout.addWidget(notes_title)
        card_layout.addWidget(self.release_notes)
        
        self.main_layout.addWidget(self.release_notes_card)
    
    def create_button_row(self):
        button_row = QWidget()
        button_layout = QHBoxLayout(button_row)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(15)
        
        self.update_button = GradientButton("Install Update")
        self.update_button.setVisible(False)
        self.update_button.clicked.connect(self.start_update)
        
        self.check_button = GradientButton("Check for Updates")
        self.check_button.clicked.connect(self.check_for_updates)
        
        self.settings_button = QPushButton("Settings")
        self.settings_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#3D3D4A' if self.current_theme == 'dark' else '#E0E0E0'};
                color: {TEXT_COLOR if self.current_theme == 'dark' else 'black'};
                border-radius: 6px;
                padding: 8px 15px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {'#4D4D5A' if self.current_theme == 'dark' else '#D0D0D0'};
            }}
        """)
        self.settings_button.setCursor(Qt.PointingHandCursor)
        self.settings_button.clicked.connect(self.show_settings)
        
        button_layout.addWidget(self.check_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.settings_button)
        
        self.main_layout.addWidget(button_row)
    
    def create_footer(self):
        footer = QLabel("© 2023 Leopardo AI. All rights reserved.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #888; font-size: 10px;")
        self.main_layout.addWidget(footer)
    
    def toggle_theme(self):
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        update_setting('theme', self.current_theme)
        self.apply_theme()
        self.update_ui_colors()
    
    def update_ui_colors(self):
        # Update status card
        self.status_card.setStyleSheet(f"""
            QFrame {{
                background-color: {'#3D3D4A' if self.current_theme == 'dark' else '#FFFFFF'};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        
        # Update release notes card
        self.release_notes_card.setStyleSheet(f"""
            QFrame {{
                background-color: {'#3D3D4A' if self.current_theme == 'dark' else '#FFFFFF'};
                border-radius: 10px;
                padding: 15px;
            }}
            QTextEdit {{
                background-color: transparent;
                border: none;
                color: {TEXT_COLOR if self.current_theme == 'dark' else 'black'};
            }}
        """)
        
        # Update settings button
        self.settings_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#3D3D4A' if self.current_theme == 'dark' else '#E0E0E0'};
                color: {TEXT_COLOR if self.current_theme == 'dark' else 'black'};
                border-radius: 6px;
                padding: 8px 15px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {'#4D4D5A' if self.current_theme == 'dark' else '#D0D0D0'};
            }}
        """)
    
    def check_for_updates(self):
        self.status_title.setText("Checking for updates...")
        self.version_label.setText("")
        self.release_notes_card.setVisible(False)
        self.update_button.setVisible(False)
        self.progress_bar.setVisible(False)
        
        self.worker.set_check_only(True)
        self.worker.start()
    
    def start_update(self):
        if not is_admin():
            elevate_privileges()
            return
        
        self.status_title.setText("Preparing update...")
        self.update_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValueAnimated(0)
        
        self.worker.set_check_only(False)
        self.worker.start()
    
    def handle_update_info(self, info):
        current = info['current_version']
        new = info['new_version']
        
        self.version_label.setText(f"Current version: {current}\nLatest version: {new}")
        
        if info['update_available']:
            self.status_title.setText("Update Available!")
            self.status_title.setStyleSheet(f"color: {SUCCESS_COLOR};")
            
            self.release_notes.setPlainText(info['release_notes'])
            self.release_notes_card.setVisible(True)
            
            if not info['check_only']:
                self.update_button.setVisible(True)
            else:
                self.update_button.setVisible(True)
                self.update_button.setText("Install Update")
        else:
            self.status_title.setText("You're up to date!")
            self.status_title.setStyleSheet(f"color: {SUCCESS_COLOR};")
            
            if info['check_only']:
                self.release_notes.setPlainText(info['release_notes'])
                self.release_notes_card.setVisible(True)
    
    def handle_error(self, error_msg):
        self.status_title.setText("Update Error")
        self.status_title.setStyleSheet(f"color: {ERROR_COLOR};")
        
        QMessageBox.critical(self, "Error", 
                           f"<b>An error occurred during update:</b><br><br>{error_msg}",
                           QMessageBox.Ok)
    
    def update_progress(self, value):
        self.progress_bar.setValueAnimated(value)
    
    def show_settings(self):
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle("Settings")
        settings_dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout(settings_dialog)
        
        # Add a header
        header = QLabel("Updater Settings")
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setWeight(QFont.Bold)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Settings options
        auto_check = QCheckBox("Automatically check for updates on startup")
        auto_check.setChecked(get_setting('auto_check'))
        
        notify_beta = QCheckBox("Notify me about beta releases")
        notify_beta.setChecked(get_setting('notify_beta'))
        
        last_check = get_setting('last_check')
        last_check_label = QLabel(f"Last checked: {last_check if last_check else 'Never'}")
        last_check_label.setStyleSheet("color: #888;")
        
        layout.addWidget(auto_check)
        layout.addWidget(notify_beta)
        layout.addWidget(last_check_label)
        
        # Add spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Save button
        save_button = GradientButton("Save Settings")
        save_button.clicked.connect(lambda: self.save_settings(
            auto_check.isChecked(),
            notify_beta.isChecked(),
            settings_dialog
        ))
        layout.addWidget(save_button)
        
        settings_dialog.exec_()
    
    def save_settings(self, auto_check, notify_beta, dialog):
        update_setting('auto_check', 1 if auto_check else 0)
        update_setting('notify_beta', 1 if notify_beta else 0)
        
        # Show confirmation
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Settings Saved")
        msg.setText("Your settings have been saved successfully.")
        msg.setStandardButtons(QMessageBox.Ok)
        
        # Apply theme to message box
        if self.current_theme == 'dark':
            msg.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {DARK_COLOR};
                    color: {TEXT_COLOR};
                }}
                QLabel {{
                    color: {TEXT_COLOR};
                }}
            """)
        
        msg.exec_()
        dialog.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = UpdaterWindow()
    window.show()
    
    sys.exit(app.exec_())