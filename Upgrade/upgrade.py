import sys
import webbrowser
import sqlite3
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QRadioButton, QButtonGroup, QPushButton, QMessageBox, QFrame, 
    QLineEdit, QStackedWidget, QSizePolicy, QSpacerItem
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor, QPainter, QBrush, QLinearGradient
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QPropertyAnimation, QEasingCurve

class AnimatedButton(QPushButton):
    """Custom animated button with hover effects"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.OutQuad)
        
    def enterEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(self.geometry().adjusted(-2, -2, 2, 2))
        self._animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(self.geometry().adjusted(2, 2, -2, -2))
        self._animation.start()
        super().leaveEvent(event)

class ContactDialog(QWidget):
    contact_method_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contact Leopardo AI")
        self.setMinimumSize(800, 700)
        self.setWindowIcon(QIcon(self.resource_path("icons/logo.png")))
        
        # Setup database
        self.setup_database()
        
        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Header with logo and title
        self.setup_header()
        
        # Stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        # Setup pages
        self.setup_main_page()
        self.setup_license_page()
        self.setup_email_page()
        
        self.setLayout(self.main_layout)
        self.setStyleSheet(self.get_stylesheet())
        
    def resource_path(self, relative_path):
        """Get absolute path to resource for PyInstaller"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def setup_database(self):
        """Setup SQLite database for license requests"""
        user_home = os.path.expanduser("~")
        db_path = os.path.join(user_home, "AppData", "Roaming", "LeopardoAI", "contacts.db")
        
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS license_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT NOT NULL,
                module TEXT NOT NULL,
                duration TEXT NOT NULL,
                request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'Pending'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT NOT NULL,
                method TEXT NOT NULL,
                message TEXT,
                contact_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def setup_header(self):
        """Create the header section with logo and title"""
        header = QWidget()
        header.setObjectName("header")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(30, 15, 30, 15)
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(self.resource_path("icons/logo.png")).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        header_layout.addWidget(logo_label)
        
        # Title and subtitle
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        
        title = QLabel("Leopardo AI")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        
        subtitle = QLabel("Contact & Support")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #7f8c8d;")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        header_layout.addLayout(title_layout)
        
        # Spacer
        header_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        header.setLayout(header_layout)
        self.main_layout.addWidget(header)
        
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("background-color: #e0e0e0; margin: 0 30px;")
        self.main_layout.addWidget(divider)
    
    def setup_main_page(self):
        """Create the main selection page with direct contact options"""
        main_page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(25)
        
        # Title
        title = QLabel("How would you like to contact us?")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Choose your preferred contact method")
        desc.setFont(QFont("Segoe UI", 10))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)
        
        # Contact options grid
        options_grid = QHBoxLayout()
        options_grid.setSpacing(20)
        
        # Left column (direct contact methods)
        left_column = QVBoxLayout()
        left_column.setSpacing(15)
        
        # WhatsApp button
        whatsapp_btn = self.create_contact_button(
            "WhatsApp", 
            "icons/whatsapp.png", 
            "Chat with us instantly", 
            "#25D366"
        )
        whatsapp_btn.clicked.connect(lambda: self.open_whatsapp())
        left_column.addWidget(whatsapp_btn)
        
        # Telegram button
        telegram_btn = self.create_contact_button(
            "Telegram", 
            "icons/telegram.png", 
            "Message us on Telegram", 
            "#0088cc"
        )
        telegram_btn.clicked.connect(lambda: self.open_telegram())
        left_column.addWidget(telegram_btn)
        
        options_grid.addLayout(left_column)
        
        # Right column (other methods)
        right_column = QVBoxLayout()
        right_column.setSpacing(15)
        
        # Email button
        email_btn = self.create_contact_button(
            "Email", 
            "icons/email.png", 
            "Send us an email", 
            "#EA4335"
        )
        email_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        right_column.addWidget(email_btn)
        
        # License button
        license_btn = self.create_contact_button(
            "License Request", 
            "icons/license.png", 
            "Get a software license", 
            "#673AB7"
        )
        license_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        right_column.addWidget(license_btn)
        
        options_grid.addLayout(right_column)
        layout.addLayout(options_grid)
        
        # Add spacer to center the options
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Footer
        footer = QLabel("We typically respond within 24 hours")
        footer.setFont(QFont("Segoe UI", 9))
        footer.setStyleSheet("color: #95a5a6; margin-top: 30px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
        
        main_page.setLayout(layout)
        self.stacked_widget.addWidget(main_page)
    
    def create_contact_button(self, title, icon_path, description, color):
        """Create a styled contact button"""
        btn = AnimatedButton()
        btn.setObjectName(f"contact_{title.lower().replace(' ', '_')}")
        btn.setFixedHeight(90)
        
        # Main layout
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(20, 10, 20, 10)
        btn_layout.setSpacing(15)
        
        # Icon
        icon_label = QLabel()
        icon_pixmap = QPixmap(self.resource_path(icon_path)).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        btn_layout.addWidget(icon_label)
        
        # Text
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title_label.setStyleSheet(f"color: {color};")
        
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Segoe UI", 9))
        desc_label.setStyleSheet("color: #666;")
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)
        btn_layout.addLayout(text_layout)
        
        # Arrow
        arrow_label = QLabel("→")
        arrow_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        arrow_label.setStyleSheet(f"color: {color};")
        btn_layout.addWidget(arrow_label)
        
        btn.setLayout(btn_layout)
        
        # Style
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.adjust_color(color, 90)}, 
                    stop:1 {self.adjust_color(color, 70)}
                );
                border-radius: 8px;
                text-align: left;
                border: none;
            }}
            QPushButton:hover {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.adjust_color(color, 80)}, 
                    stop:1 {self.adjust_color(color, 60)}
                );
            }}
        """)
        
        return btn
    
    def adjust_color(self, hex_color, lightness):
        """Adjust color lightness while maintaining hue"""
        color = QColor(hex_color)
        h, s, l, a = color.getHslF()
        new_l = lightness / 100.0
        color.setHslF(h, s, new_l, a)
        return color.name()
    
    def setup_license_page(self):
        """Create the license request page"""
        license_page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 30)
        layout.setSpacing(20)
        
        # Back button
        back_btn = QPushButton("← Back to Options")
        back_btn.setObjectName("backButton")
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setFont(QFont("Segoe UI", 10))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn, alignment=Qt.AlignLeft)
        
        # Title
        title = QLabel("License Request")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Fill out the form to request a software license")
        desc.setFont(QFont("Segoe UI", 10))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 30px;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)
        
        # Form container with card style
        form_container = QWidget()
        form_container.setObjectName("formContainer")
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(30, 20, 30, 20)
        form_layout.setSpacing(20)
        
        # Name field
        name_label = QLabel("Your Name:")
        name_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.setStyleSheet("padding: 12px;")
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)
        
        # Email field
        email_label = QLabel("Email Address:")
        email_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setStyleSheet("padding: 12px;")
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        
        # Module selection
        module_label = QLabel("Select Module:")
        module_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.module_combo = QComboBox()
        self.module_combo.addItems(["WA CRM", "FB Robot Pro", "XBot", "Complete Suite"])
        self.module_combo.setStyleSheet("padding: 10px; height: 40px;")
        form_layout.addWidget(module_label)
        form_layout.addWidget(self.module_combo)
        
        # Duration selection
        duration_label = QLabel("License Duration:")
        duration_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        
        duration_layout = QHBoxLayout()
        duration_layout.setSpacing(15)
        self.duration_group = QButtonGroup()
        durations = [
            {"text": "Monthly ($49)", "color": "#4CAF50"},
            {"text": "Annual ($399)", "color": "#2196F3"},
            {"text": "Lifetime ($999)", "color": "#9C27B0"}
        ]
        
        for i, duration in enumerate(durations):
            radio = QRadioButton(duration["text"])
            radio.setFont(QFont("Segoe UI", 10))
            radio.setStyleSheet(f"""
                QRadioButton {{
                    padding: 10px 15px;
                    border-radius: 6px;
                    background-color: {self.adjust_color(duration['color'], 95)};
                }}
                QRadioButton::indicator {{
                    width: 18px;
                    height: 18px;
                }}
                QRadioButton::indicator::checked {{
                    background-color: {duration['color']};
                    border: 2px solid {duration['color']};
                }}
            """)
            self.duration_group.addButton(radio, i)
            duration_layout.addWidget(radio)
        
        form_layout.addWidget(duration_label)
        form_layout.addLayout(duration_layout)
        form_container.setLayout(form_layout)
        layout.addWidget(form_container)
        
        # Submit button
        submit_btn = AnimatedButton("Request License")
        submit_btn.setObjectName("submitButton")
        submit_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        submit_btn.setFixedHeight(50)
        submit_btn.clicked.connect(self.submit_license_request)
        layout.addWidget(submit_btn, alignment=Qt.AlignCenter)
        
        # Add spacer to push everything up
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        license_page.setLayout(layout)
        self.stacked_widget.addWidget(license_page)
    
    def setup_email_page(self):
        """Create the email contact page"""
        email_page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 30)
        layout.setSpacing(20)
        
        # Back button
        back_btn = QPushButton("← Back to Options")
        back_btn.setObjectName("backButton")
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setFont(QFont("Segoe UI", 10))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn, alignment=Qt.AlignLeft)
        
        # Title
        title = QLabel("Email Support")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Send us a message and we'll get back to you soon")
        desc.setFont(QFont("Segoe UI", 10))
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 30px;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)
        
        # Form container with card style
        form_container = QWidget()
        form_container.setObjectName("formContainer")
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(30, 20, 30, 20)
        form_layout.setSpacing(20)
        
        # Name field
        name_label = QLabel("Your Name:")
        name_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.contact_name_input = QLineEdit()
        self.contact_name_input.setPlaceholderText("Enter your name")
        self.contact_name_input.setStyleSheet("padding: 12px;")
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.contact_name_input)
        
        # Email field
        email_label = QLabel("Email Address:")
        email_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.contact_email_input = QLineEdit()
        self.contact_email_input.setPlaceholderText("Enter your email")
        self.contact_email_input.setStyleSheet("padding: 12px;")
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.contact_email_input)
        
        # Message field
        message_label = QLabel("Your Message:")
        message_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Enter your message")
        self.message_input.setStyleSheet("padding: 12px;")
        form_layout.addWidget(message_label)
        form_layout.addWidget(self.message_input)
        
        form_container.setLayout(form_layout)
        layout.addWidget(form_container)
        
        # Submit button
        submit_btn = AnimatedButton("Send Email")
        submit_btn.setObjectName("submitButton")
        submit_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        submit_btn.setFixedHeight(50)
        submit_btn.clicked.connect(self.submit_email)
        layout.addWidget(submit_btn, alignment=Qt.AlignCenter)
        
        # Add spacer to push everything up
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        email_page.setLayout(layout)
        self.stacked_widget.addWidget(email_page)
    
    def open_whatsapp(self):
        """Open WhatsApp with predefined message"""
        phone_number = "+1234567890"  # Replace with your actual number
        message = "Hello Leopardo AI team, I need assistance with..."
        url = f"https://wa.me/{phone_number}?text={message}"
        webbrowser.open(url)
        
        # Save to database
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO contact_requests (method, contact_date) VALUES (?, CURRENT_TIMESTAMP)",
            ("whatsapp",)
        )
        self.conn.commit()
    
    def open_telegram(self):
        """Open Telegram with predefined message"""
        username = "leopardo_ai_support"  # Replace with your actual username
        message = "Hello Leopardo AI team, I need assistance with..."
        url = f"https://t.me/{username}?start={message}"
        webbrowser.open(url)
        
        # Save to database
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO contact_requests (method, contact_date) VALUES (?, CURRENT_TIMESTAMP)",
            ("telegram",)
        )
        self.conn.commit()
    
    def submit_license_request(self):
        """Handle license request submission"""
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        module = self.module_combo.currentText()
        duration_btn = self.duration_group.checkedButton()
        
        # Validation
        if not email or "@" not in email:
            self.shake(self.email_input)
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return
            
        if not duration_btn:
            QMessageBox.warning(self, "Missing Duration", "Please select a license duration.")
            return
            
        duration = duration_btn.text()
        
        # Save to database
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO license_requests (name, email, module, duration) VALUES (?, ?, ?, ?)",
            (name, email, module, duration)
        )
        self.conn.commit()
        
        # Open payment link
        webbrowser.open("https://leopardo-ai.com/payment")
        
        # Show confirmation with animation
        msg = QMessageBox(self)
        msg.setWindowTitle("Request Submitted")
        msg.setText("""
            <h3>Your license request has been received!</h3>
            <p>After payment processing, you'll receive your license key via email within 24 hours.</p>
        """)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        
        # Clear form
        self.name_input.clear()
        self.email_input.clear()
        self.duration_group.setExclusive(False)
        for btn in self.duration_group.buttons():
            btn.setChecked(False)
        self.duration_group.setExclusive(True)
        
        # Return to main page
        self.stacked_widget.setCurrentIndex(0)
    
    def submit_email(self):
        """Handle email submission"""
        name = self.contact_name_input.text().strip()
        email = self.contact_email_input.text().strip()
        message = self.message_input.text().strip()
        
        # Validation
        if not email or "@" not in email:
            self.shake(self.contact_email_input)
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return
            
        if not message:
            self.shake(self.message_input)
            QMessageBox.warning(self, "Missing Message", "Please enter your message.")
            return
        
        # Save to database
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO contact_requests (name, email, method, message) VALUES (?, ?, ?, ?)",
            (name, email, "email", message)
        )
        self.conn.commit()
        
        # Open email client
        webbrowser.open(f"mailto:support@leopardo-ai.com?subject=Contact from {name}&body={message}")
        
        # Show confirmation
        msg = QMessageBox(self)
        msg.setWindowTitle("Email Ready")
        msg.setText("""
            <h3>Your email is ready to send!</h3>
            <p>We've opened your email client with a pre-filled message. Just hit send to contact our support team.</p>
        """)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        
        # Clear form
        self.contact_name_input.clear()
        self.contact_email_input.clear()
        self.message_input.clear()
        
        # Return to main page
        self.stacked_widget.setCurrentIndex(0)
    
    def shake(self, widget):
        """Shake animation for invalid fields"""
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(100)
        animation.setLoopCount(2)
        animation.setKeyValueAt(0, widget.pos())
        animation.setKeyValueAt(0.2, widget.pos() + QPoint(-5, 0))
        animation.setKeyValueAt(0.4, widget.pos() + QPoint(5, 0))
        animation.setKeyValueAt(0.6, widget.pos() + QPoint(-5, 0))
        animation.setKeyValueAt(0.8, widget.pos() + QPoint(5, 0))
        animation.setKeyValueAt(1, widget.pos())
        animation.start(QPropertyAnimation.DeleteWhenStopped)
    
    def get_stylesheet(self):
        """Return the stylesheet for the application"""
        return """
            QWidget {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            #header {
                background-color: #ffffff;
                border-bottom: 1px solid #e0e0e0;
            }
            
            #formContainer {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
            }
            
            QPushButton {
                border-radius: 8px;
                border: none;
                font-weight: bold;
                padding: 12px 24px;
            }
            
            #backButton {
                background-color: transparent;
                color: #3498db;
                text-align: left;
                padding: 5px 10px;
            }
            
            #backButton:hover {
                text-decoration: underline;
            }
            
            #submitButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, 
                    stop:1 #2980b9
                );
                color: white;
                min-width: 200px;
                font-size: 14px;
            }
            
            #submitButton:hover {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2980b9, 
                    stop:1 #3498db
                );
            }
            
            QLineEdit, QComboBox {
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-size: 13px;
            }
            
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #3498db;
                outline: none;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox QAbstractItemView {
                border: 1px solid #ddd;
                selection-background-color: #3498db;
                selection-color: white;
                padding: 8px;
            }
        """
    
    def closeEvent(self, event):
        """Clean up when closing the application"""
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show the dialog
    dialog = ContactDialog()
    dialog.show()
    
    sys.exit(app.exec_())
    