from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton
)


class Class1Display(QWidget):
    """Simulation de la classe 1 affichée dans la section gauche."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Contenu de la Classe 1")
        label.setFont(QFont("Arial", 16))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(label)

        button = QPushButton("Action Classe 1")
        button.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; border-radius: 8px; padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(button)


class Class2Display(QWidget):
    """Simulation de la classe 2 affichée dans la section droite."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Contenu de la Classe 2")
        label.setFont(QFont("Arial", 16))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(label)

        button = QPushButton("Action Classe 2")
        button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; color: white; border-radius: 8px; padding: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        layout.addWidget(button)


class SplitScreenView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Split Screen Example")
        self.setGeometry(100, 100, 1000, 600)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left section (Class 1 display)
        left_section = QVBoxLayout()
        left_label = QLabel("Classe 1")
        left_label.setFont(QFont("Arial", 18))
        left_label.setAlignment(Qt.AlignCenter)
        left_label.setStyleSheet("background-color: #ecf0f1; color: #34495e;")
        left_section.addWidget(left_label)

        left_frame = QFrame()
        left_frame.setStyleSheet("background-color: #f7f7f7; border: 1px solid #bdc3c7;")
        left_frame_layout = QVBoxLayout(left_frame)
        left_frame_layout.addWidget(Class1Display())
        left_section.addWidget(left_frame)

        # Middle band (decorative image or logo)
        middle_band = QLabel()
        middle_band.setPixmap(
            QPixmap("path/to/your/image.png").scaled(80, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        middle_band.setAlignment(Qt.AlignCenter)
        middle_band.setStyleSheet("background-color: #e0e0e0;")
        middle_band.setFixedWidth(80)

        # Right section (Class 2 display)
        right_section = QVBoxLayout()
        right_label = QLabel("Classe 2")
        right_label.setFont(QFont("Arial", 18))
        right_label.setAlignment(Qt.AlignCenter)
        right_label.setStyleSheet("background-color: #ecf0f1; color: #34495e;")
        right_section.addWidget(right_label)

        right_frame = QFrame()
        right_frame.setStyleSheet("background-color: #f7f7f7; border: 1px solid #bdc3c7;")
        right_frame_layout = QVBoxLayout(right_frame)
        right_frame_layout.addWidget(Class2Display())
        right_section.addWidget(right_frame)

        # Add sections to main layout
        main_layout.addLayout(left_section)
        main_layout.addWidget(middle_band)
        main_layout.addLayout(right_section)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = SplitScreenView()
    window.show()
    sys.exit(app.exec_())
