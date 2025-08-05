import sys
import os
import sqlite3
import json
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTextEdit, QProgressBar, QScrollArea,
                             QGroupBox, QCheckBox, QFileDialog, QMessageBox, QStackedWidget,
                             QSizePolicy, QLineEdit, QGridLayout, QFrame, QSpacerItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel

# Corrected import paths for the new structure
from app.core.database import init_db, get_db_path
from app.core.constants import Constants
from app.core.action_handler import ActionHandler

class AnalysisThread(QThread):
    """Thread for asynchronous prompt analysis"""
    analysis_complete = pyqtSignal(str, list)
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int)

    def __init__(self, prompt_text, db_path):
        super().__init__()
        self.prompt_text = prompt_text
        self.db_path = db_path
        self._is_running = True

    def run(self):
        """Main execution of analysis thread"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            for i in range(1, 101):
                if not self._is_running:
                    return
                time.sleep(0.02)
                self.progress_updated.emit(i)

            prompt_lower = self.prompt_text.lower()
            detected = []

            cursor.execute('SELECT keyword, platform, response_template, action_type FROM detection_rules')
            rules = cursor.fetchall()

            for keyword, platform, template, action_type in rules:
                if not self._is_running:
                    return
                if keyword in prompt_lower:
                    detected.append((keyword, platform, template, action_type))

            analysis_text = self.generate_analysis_html(prompt_lower, detected)
            self.analysis_complete.emit(analysis_text, detected)

        except sqlite3.Error as e:
            self.error_occurred.emit(f"Database error: {e}")
        except Exception as e:
            self.error_occurred.emit(f"Analysis error: {e}")
        finally:
            if conn:
                conn.close()

    def stop(self):
        self._is_running = False
        self.wait()

    def generate_analysis_html(self, prompt, detected):
        # This HTML generation can be further improved, maybe with a template engine
        html = f"""
        <style>
            :root {{
                --primary: {Constants.PRIMARY_COLOR};
                --primary-hover: {Constants.PRIMARY_HOVER};
                --background: #ffffff;
                --text: {Constants.TEXT_COLOR};
                --text-secondary: {Constants.TEXT_SECONDARY};
                --card-bg: {Constants.CARD_BG};
                --card-border: {Constants.CARD_BORDER};
            }}
            body {{ font-family: sans-serif; padding: 20px; }}
            .option-card {{ border: 1px solid var(--card-border); border-radius: 8px; padding: 15px; margin-bottom: 10px; cursor: pointer; }}
            .option-card:hover {{ border-color: var(--primary); }}
        </style>
        <h2>Suggestions</h2>
        """
        if not detected:
            html += "<p>No specific actions detected. Try being more specific.</p>"
        else:
            for keyword, platform, template, action_type in detected:
                html += f"""
                <div class="option-card" onclick='pyHandler.handleAction(`{{
                    "type": "platform_action",
                    "platform": "{platform}",
                    "action": "{action_type}"
                }}`)'>
                    <h4>{template}</h4>
                    <p>Based on your mention of: <b>{keyword}</b></p>
                    <button>Execute</button>
                </div>
                """
        return html

class HomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_path = init_db()
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        header = QLabel("Leopardo AI Assistant")
        header.setObjectName("mainHeader")

        subheader = QLabel("Describe your marketing need to get customized solutions")
        subheader.setObjectName("mainSubheader")

        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Ex: I want to automate my WhatsApp posts...")

        self.analyze_button = QPushButton("Analyze")

        self.progress_bar = QProgressBar()
        self.progress_bar.hide()

        self.results_display = QWebEngineView()
        self.results_display.hide()

        self.channel = QWebChannel()
        self.handler = ActionHandler(self)
        self.channel.registerObject('pyHandler', self.handler)
        self.results_display.page().setWebChannel(self.channel)

        # Prompt suggestions
        self.suggestions_layout = self.create_prompt_suggestions()

        layout.addWidget(header)
        layout.addWidget(subheader)
        layout.addWidget(self.prompt_input)
        layout.addLayout(self.suggestions_layout)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.results_display)

        self.apply_styles()

    def create_prompt_suggestions(self):
        suggestions_layout = QVBoxLayout()
        title = QLabel("Example queries:")
        suggestions_grid = QGridLayout()

        suggestions = [
            ("Social media", "Create a strategy for Instagram and Facebook"),
            ("Analysis", "Analyze performance of my last campaign"),
            ("Email", "Write a newsletter for my clients"),
            ("WhatsApp", "Automate WhatsApp messages for my business"),
        ]

        for i, (title_text, prompt_text) in enumerate(suggestions):
            btn = QPushButton(title_text)
            btn.setToolTip(prompt_text)
            btn.clicked.connect(lambda _, text=prompt_text: self.prompt_input.setPlainText(text))
            suggestions_grid.addWidget(btn, i // 2, i % 2)

        suggestions_layout.addWidget(title)
        suggestions_layout.addLayout(suggestions_grid)
        return suggestions_layout

    def setup_connections(self):
        self.analyze_button.clicked.connect(self.start_analysis)

    def start_analysis(self):
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            return

        self.progress_bar.show()
        self.analyze_button.setEnabled(False)

        self.analysis_thread = AnalysisThread(prompt, self.db_path)
        self.analysis_thread.analysis_complete.connect(self.show_analysis_results)
        self.analysis_thread.error_occurred.connect(self.show_error_message)
        self.analysis_thread.progress_updated.connect(self.progress_bar.setValue)
        self.analysis_thread.start()

    def show_analysis_results(self, html_report, detected_items):
        self.progress_bar.hide()
        self.analyze_button.setEnabled(True)
        self.results_display.setHtml(html_report)
        self.results_display.show()

    def show_error_message(self, error_msg):
        self.progress_bar.hide()
        self.analyze_button.setEnabled(True)
        QMessageBox.critical(self, "Error", error_msg)

    def execute_action(self, action_data):
        # This will be expanded later to handle different actions
        QMessageBox.information(self, "Action Triggered", f"Action: {action_data}")

    def apply_styles(self):
        self.setStyleSheet(f"""
            QLabel#mainHeader {{ font-size: 24px; font-weight: bold; margin-bottom: 5px; }}
            QLabel#mainSubheader {{ color: {Constants.TEXT_SECONDARY}; margin-bottom: 15px; }}
            QTextEdit {{ border: 1px solid {Constants.CARD_BORDER}; border-radius: 8px; padding: 10px; }}
            QPushButton {{ background-color: {Constants.PRIMARY_COLOR}; color: white; border: none; border-radius: 8px; padding: 10px; }}
            QPushButton:hover {{ background-color: {Constants.PRIMARY_HOVER}; }}
        """)
