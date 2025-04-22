import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QGraphicsDropShadowEffect
)

from Home.chromeFox import SecureBrowserConnect
from Home.telecommande import RemoteControl

# Fonts & Styles
LABEL_FONT = QFont("Arial", 14, QFont.Bold)
CONTENT_FONT = QFont("Arial", 16)
SECTION_BACKGROUND = "background-color: #ffffff; color: #2c3e50;"
FRAME_BACKGROUND = "background-color: #f0f3f5; border: 1px solid #dfe6e9;"
BUTTON_STYLE = """
QPushButton {
    background-color: {bg_color}; 
    color: white; 
    border: none;
    border-radius: 10px; 
    padding: 12px 20px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: {hover_color};
}
"""

def styled_label(text, font=LABEL_FONT, align=Qt.AlignCenter, style=SECTION_BACKGROUND):
    label = QLabel(text)
    label.setFont(font)
    label.setAlignment(align)
    label.setStyleSheet(style)
    return label

def add_shadow(widget):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(20)
    shadow.setXOffset(0)
    shadow.setYOffset(4)
    shadow.setColor(Qt.gray)
    widget.setGraphicsEffect(shadow)

# Display components
class Class1Display(QWidget):
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
        button.setCursor(Qt.PointingHandCursor)
        layout.addWidget(button)
        layout.addStretch()


class Class2Display(QWidget):
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
        button.setCursor(Qt.PointingHandCursor)
        layout.addWidget(button)
        layout.addStretch()

# Split Screen Layout
class SplitScreenView(QWidget):
    def __init__(self, main_app=None):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("Split Screen - Modern UI")
        self.setGeometry(100, 100, 1000, 730)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Left Section
        left_section = QVBoxLayout()
        left_section.addWidget(styled_label("Connected Account"))

        left_frame = QFrame()
        left_frame.setStyleSheet(FRAME_BACKGROUND)
        add_shadow(left_frame)
        left_frame_layout = QVBoxLayout(left_frame)
        left_frame_layout.addWidget(SecureBrowserConnect())
        left_frame_layout.addStretch()
        left_section.addWidget(left_frame)

        # Center Band (Logo/Image)
        middle_band = QLabel()
        image_path = "resources/images/barre.webp"
        if os.path.exists(image_path):
            middle_band.setPixmap(
                QPixmap(image_path).scaled(80, 730, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            middle_band.setText("LOGO")
            middle_band.setFont(CONTENT_FONT)
            middle_band.setAlignment(Qt.AlignCenter)
        middle_band.setStyleSheet("background-color: #ecf0f1; border-radius: 10px;")
        middle_band.setFixedWidth(80)

        # Right Section
        right_section = QVBoxLayout()
        right_section.addWidget(styled_label("Remote Control"))

        right_frame = QFrame()
        right_frame.setStyleSheet(FRAME_BACKGROUND)
        add_shadow(right_frame)
        right_frame_layout = QVBoxLayout(right_frame)
        right_frame_layout.addWidget(RemoteControl())
        right_frame_layout.addStretch()
        right_section.addWidget(right_frame)

        # Assemble all sections
        main_layout.addLayout(left_section)
        main_layout.addWidget(middle_band)
        main_layout.addLayout(right_section)

# Main block
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = SplitScreenView()
    window.show()
    sys.exit(app.exec_())
