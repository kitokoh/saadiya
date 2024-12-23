from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QTimer


class RemoteControl(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark_theme = True  # Default to dark mode
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Nova360 AI - Remote Control")
        self.setWindowIcon(QIcon('../resources/icons/robot-icons-30504-Windows.ico'))  # Assurez-vous que le chemin de l'icône est correct

        self.setFixedSize(450, 700)  # Set fixed size for the window

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Digital screen with modern styling
        self.screen = QLabel("Ready to Control")
        self.screen.setFixedHeight(self.height() // 5)
        self.screen.setAlignment(Qt.AlignCenter)
        self.apply_shadow_effect(self.screen)
        self.screen.setStyleSheet(self.get_screen_stylesheet())
        main_layout.addWidget(self.screen)

        # Central area: circular buttons and small buttons
        central_layout = QHBoxLayout()

        # Small buttons on the left
        left_buttons = QVBoxLayout()
        for name, icon in [("Fb Robot", "icons/fb.png"), ("Multi Fb", "icons/multi_fb.png"), 
                           ("WA", "icons/wa.png"), ("Insta", "icons/insta.png")]:
            btn = self.create_small_button(name, icon)
            self.apply_shadow_effect(btn)
            left_buttons.addWidget(btn)

        # Circular buttons in the center
        circle_buttons_layout = QVBoxLayout()
        self.open_panel_btn = self.create_circular_button("Open Panel", "icons/panel.png")
        self.start_robots_btn = self.create_circular_button("Start Robots", "icons/robot.png")
        self.choice_module_btn = self.create_circular_button("Choice Module", "icons/module.png")
        
        for btn in [self.open_panel_btn, self.start_robots_btn, self.choice_module_btn]:
            self.apply_shadow_effect(btn)
            circle_buttons_layout.addWidget(btn)

        # Small buttons on the right
        right_buttons = QVBoxLayout()
        for name, icon in [("Pin", "icons/pin.png"), ("X", "icons/x.png"), 
                           ("In", "icons/linkedin.png"), ("YTB", "icons/ytb.png")]:
            btn = self.create_small_button(name, icon)
            self.apply_shadow_effect(btn)
            right_buttons.addWidget(btn)

        # Add layouts to the central layout
        central_layout.addLayout(left_buttons)
        central_layout.addLayout(circle_buttons_layout)
        central_layout.addLayout(right_buttons)

        main_layout.addLayout(central_layout)

        # Toggle theme button
        self.toggle_theme_btn = QPushButton("Toggle Theme")
        self.toggle_theme_btn.clicked.connect(self.toggle_theme)
        self.apply_shadow_effect(self.toggle_theme_btn)
        self.toggle_theme_btn.setStyleSheet(self.get_toggle_button_stylesheet())
        main_layout.addWidget(self.toggle_theme_btn)

        # Footer with sleek design
        footer = QLabel("© 2024 Nova360 AI - Remote Control")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            QLabel {
                color: #aaa;
                font-size: 12px;
                font-style: italic;
                margin-top: 10px;
            }
        """)
        self.apply_shadow_effect(footer)
        main_layout.addWidget(footer)

        # Apply the main layout
        self.setLayout(main_layout)

        # Connect main buttons for light effect
        self.open_panel_btn.clicked.connect(lambda: self.activate_light("Open Panel Activated"))
        self.start_robots_btn.clicked.connect(lambda: self.activate_light("Robots Started"))
        self.choice_module_btn.clicked.connect(lambda: self.activate_light("Module Chosen"))

    def create_circular_button(self, name, icon_path):
        """Create a circular button with an icon and sleek styling"""
        button = QPushButton(name)
        button.setFixedSize(100, 100)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(button.size() * 0.5)
        button.setStyleSheet(self.get_circular_button_stylesheet())
        return button

    def create_small_button(self, name, icon_path):
        """Create a small rectangular button with a polished design"""
        button = QPushButton(name)
        button.setFixedSize(90, 40)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(button.size() * 0.5)
        button.setStyleSheet(self.get_small_button_stylesheet())
        return button

    def activate_light(self, message):
        """Simulate a red light effect on the screen"""
        self.screen.setText(message)
        self.screen.setStyleSheet(self.get_light_stylesheet())
        QTimer.singleShot(1000, self.reset_light)

    def reset_light(self):
        """Reset the screen after the light effect"""
        self.screen.setText("Ready to Control")
        self.screen.setStyleSheet(self.get_screen_stylesheet())

    def toggle_theme(self):
        """Toggle between dark and light modes"""
        self.is_dark_theme = not self.is_dark_theme
        self.setStyleSheet(self.get_app_stylesheet())

    def apply_shadow_effect(self, widget):
        """Apply a shadow effect to a widget"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 4)
        shadow.setBlurRadius(10)
        widget.setGraphicsEffect(shadow)

    def get_screen_stylesheet(self):
        """Return the style for the screen"""
        return """
            QLabel {
                background-color: #2d2d3f;
                color: #00ff7f;
                font-size: 20px;
                font-weight: bold;
                border: 2px solid #00ff7f;
                border-radius: 15px;
                padding: 15px;
            }
        """

    def get_light_stylesheet(self):
        """Return the style for the screen when light is activated"""
        return """
            QLabel {
                background-color: #ff4500;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: 2px solid #8b0000;
                border-radius: 15px;
                padding: 15px;
            }
        """

    def get_circular_button_stylesheet(self):
        """Style for circular buttons"""
        return """
            QPushButton {
                border-radius: 50px;
                background-color: #0078d7;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border: 3px solid #005bb5;
            }
            QPushButton:hover {
                background-color: #005bb5;
                border-color: #003f91;
            }
            QPushButton:pressed {
                background-color: #003f91;
                border-color: #ff4500;
            }
        """

    def get_small_button_stylesheet(self):
        """Style for small buttons"""
        return """
            QPushButton {
                background-color: #3a3a4f;
                color: #ffffff;
                font-size: 12px;
                border-radius: 5px;
                border: 2px solid #444;
            }
            QPushButton:hover {
                background-color: #444;
                border-color: #555;
            }
            QPushButton:pressed {
                background-color: #555;
                border-color: #ff4500;
            }
        """

    def get_toggle_button_stylesheet(self):
        """Style for the toggle theme button"""
        return """
            QPushButton {
                background-color: #444;
                color: #fff;
                font-size: 14px;
                padding: 10px;
                border: 2px solid #666;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #555;
                border-color: #777;
            }
            QPushButton:pressed {
                background-color: #222;
                border-color: #ff4500;
            }
        """

    def get_app_stylesheet(self):
        """Return the style for the current theme"""
        if self.is_dark_theme:
            return """
                QWidget { background-color: #2d2d3f; color: #ffffff; }
            """
        return """
            QWidget { background-color: #ffffff; color: #000000; }
        """


# Test the application
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    remote = RemoteControl()
    remote.show()
    sys.exit(app.exec_())
