# Imports
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton
)

from Home.chromeFox import SecureBrowserConnect
from Home.telecommande import RemoteControl

# Constants for Styling
LABEL_FONT = QFont("Arial", 14)
CONTENT_FONT = QFont("Arial", 16)
SECTION_BACKGROUND = "background-color: #ecf0f1; color: #34495e;"
FRAME_BACKGROUND = "background-color: #f7f7f7; border: 1px solid #bdc3c7;"
BUTTON_STYLE = """
    QPushButton {
        background-color: {bg_color}; color: white; border-radius: 8px; padding: 10px;
    }
    QPushButton:hover {
        background-color: {hover_color};
    }
"""

# Class Definitions

class Class1Display(QWidget):
    """Simulation of Class 1 displayed in the left section."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Content of Class 1")
        label.setFont(CONTENT_FONT)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(label)

        button = QPushButton("Class 1 Action")
        button.setStyleSheet(BUTTON_STYLE.format(bg_color="#3498db", hover_color="#2980b9"))
        layout.addWidget(button)


class Class2Display(QWidget):
    """Simulation of Class 2 displayed in the right section."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Content of Class 2")
        label.setFont(CONTENT_FONT)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(label)

        button = QPushButton("Class 2 Action")
        button.setStyleSheet(BUTTON_STYLE.format(bg_color="#e74c3c", hover_color="#c0392b"))
        layout.addWidget(button)


class SplitScreenView(QWidget):
    def __init__(self, main_app=None):
        super().__init__()
        self.main_app = main_app  # Store the main app object if provided

        self.setWindowTitle("Split Screen Example")
        self.setGeometry(100, 100, 1000, 730)  # Adjust total height to match 730 pixels
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left section (Class 1 display)
        left_section = QVBoxLayout()
        left_label = QLabel("Connected Account")
        left_label.setFont(LABEL_FONT)
        left_label.setAlignment(Qt.AlignCenter)
        left_label.setStyleSheet(SECTION_BACKGROUND)
        left_section.addWidget(left_label)

        left_frame = QFrame()
        left_frame.setStyleSheet(FRAME_BACKGROUND)
        left_frame_layout = QVBoxLayout(left_frame)
        left_frame_layout.addWidget(SecureBrowserConnect())
        left_section.addWidget(left_frame)

        # Middle band (decorative image or logo)
        middle_band = QLabel()
        image_path = "resources/images/barre.webp"
        if os.path.exists(image_path):
            middle_band.setPixmap(
                QPixmap(image_path).scaled(80, 730, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            middle_band.setText("Logo")
            middle_band.setAlignment(Qt.AlignCenter)
            middle_band.setFont(CONTENT_FONT)
        middle_band.setStyleSheet("background-color: #e0e0e0;")
        middle_band.setFixedWidth(80)

        # Right section (Class 2 display)
        right_section = QVBoxLayout()
        right_label = QLabel("Remote Control")
        right_label.setFont(LABEL_FONT)
        right_label.setAlignment(Qt.AlignCenter)
        right_label.setStyleSheet(SECTION_BACKGROUND)
        right_section.addWidget(right_label)

        right_frame = QFrame()
        right_frame.setStyleSheet(FRAME_BACKGROUND)
        right_frame_layout = QVBoxLayout(right_frame)
        right_frame_layout.addWidget(RemoteControl())
        right_section.addWidget(right_frame)

        # Add sections to main layout
        main_layout.addLayout(left_section)
        main_layout.addWidget(middle_band)
        main_layout.addLayout(right_section)


# Main Execution Block
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = SplitScreenView()
    window.show()
    sys.exit(app.exec_())
