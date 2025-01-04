import json
import os
from PyQt5.QtCore import Qt, QPoint, QRect, QPropertyAnimation
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog, QPushButton, QHBoxLayout, QWidget, QMessageBox


class FirstTimeGuide(QDialog):
    SETTINGS_PATH = (
        os.path.expanduser("~/AppData/Roaming/saadiya/resources/settings.json")
        if os.name == "nt"
        else os.path.expanduser("~/.saadiya/resources/settings.json")
    )

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Nova360 AI - First Time Guide")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(parent.size())

        self.settings = self.load_settings()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.init_ui()
        self.setLayout(self.layout)

        self.steps = self.get_steps()
        self.current_step = 0

        self.highlight_overlay = QLabel(self)
        self.init_highlight_overlay()

        self.show_step()

    def init_ui(self):
        self.overlay_label = QLabel()
        self.overlay_label.setAlignment(Qt.AlignCenter)
        self.overlay_label.setStyleSheet(self.get_label_stylesheet())
        self.layout.addWidget(self.overlay_label)

        nav_layout = QHBoxLayout()
        self.next_button = self.create_button("Next", "#3498db", "#2980b9", self.next_step)
        nav_layout.addWidget(self.next_button)

        self.close_button = self.create_button("Skip", "#e74c3c", "#c0392b", self.skip_guide)
        nav_layout.addWidget(self.close_button)

        self.layout.addLayout(nav_layout)

    def create_button(self, text, bg_color, hover_color, callback):
        button = QPushButton(text)
        button.setStyleSheet(self.get_button_stylesheet(bg_color, hover_color))
        button.clicked.connect(callback)
        return button

    def init_highlight_overlay(self):
        self.highlight_overlay.setStyleSheet(self.get_highlight_stylesheet())
        self.highlight_overlay.hide()

    def load_settings(self):
        try:
            if os.path.exists(self.SETTINGS_PATH):
                with open(self.SETTINGS_PATH, "r") as file:
                    return json.load(file)
            return {"remotefirst": "False"}
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Error", "Invalid settings file. Recreating default settings.")
            return {"remotefirst": "False"}

    def save_settings(self):
        os.makedirs(os.path.dirname(self.SETTINGS_PATH), exist_ok=True)
        with open(self.SETTINGS_PATH, "w") as file:
            json.dump(self.settings, file)

    def get_steps(self):
        return [
            {
                "text": "Cliquez sur le bouton circulaire au centre pour accéder au panneau de contrôle.",
                "target": self.parent.open_panel_btn,
            },
            {
                "text": "Cliquez sur le bouton rectangulaire à gauche pour démarrer le robot FB.",
                "target": self.parent.button_tabs.widget(0) if self.parent.button_tabs.count() > 0 else None,
            },
        ]

    def show_step(self):
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self.overlay_label.setText(step["text"])
            self.highlight_widget(step["target"])
        else:
            QMessageBox.information(self, "Guide Complete", "Vous avez terminé le guide initial.")
            self.close()

    def highlight_widget(self, widget):
        if not widget or not widget.isVisible():
            return

        rect = widget.geometry()
        offset = widget.mapToGlobal(QPoint(0, 0))
        self.highlight_overlay.setGeometry(QRect(offset.x(), offset.y(), rect.width(), rect.height()))

        animation = QPropertyAnimation(self.highlight_overlay, b"geometry")
        animation.setDuration(500)
        animation.setStartValue(QRect(offset.x(), offset.y(), 0, 0))
        animation.setEndValue(QRect(offset.x(), offset.y(), rect.width(), rect.height()))
        animation.start()

        self.highlight_overlay.show()

    def next_step(self):
        self.highlight_overlay.hide()
        self.current_step += 1
        self.show_step()

    def skip_guide(self):
        self.settings["remotefirst"] = "True"
        self.save_settings()
        self.close()

    @staticmethod
    def get_label_stylesheet():
        return (
            "QLabel {"
            "    color: white;"
            "    font-size: 18px;"
            "    font-weight: bold;"
            "    background-color: rgba(0, 0, 0, 0.7);"
            "    border-radius: 10px;"
            "    padding: 15px;"
            "    font-family: Arial, sans-serif;"
            "}"
        )

    @staticmethod
    def get_button_stylesheet(bg_color, hover_color):
        return (
            f"QPushButton {{"
            f"    background-color: {bg_color};"
            f"    color: white;"
            f"    font-size: 14px;"
            f"    border-radius: 10px;"
            f"    padding: 10px 20px;"
            f"    font-family: Arial, sans-serif;"
            f"}}"
            f"QPushButton:hover {{"
            f"    background-color: {hover_color};"
            f"}}"
        )

    @staticmethod
    def get_highlight_stylesheet():
        return (
            "QLabel {"
            "    border: 3px solid #f39c12;"
            "    background-color: rgba(0, 0, 0, 0.5);"
            "}"
        )
