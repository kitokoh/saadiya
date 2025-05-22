import sys
import webbrowser
import sqlite3
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QRadioButton, QButtonGroup, QPushButton, QMessageBox, QFrame, 
    QLineEdit, QStackedWidget, QSizePolicy, QSpacerItem
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor
from PyQt5.QtCore import Qt, QSize, pyqtSignal

class ContactDialog(QWidget):
    contact_method_selected = pyqtSignal(str)  # Signal for contact method selection
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contact Leopardo AI")
        self.setMinimumSize(700, 600)
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
        self.setup_contact_page()
        
        self.setLayout(self.main_layout)
        self.setStyleSheet(self.get_stylesheet())
        
    def resource_path(self, relative_path):
        """ Get absolute path to resource for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def setup_database(self):
        """ Setup SQLite database for license requests """
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
        """ Create the header section with logo and title """
        header = QWidget()
        header.setObjectName("header")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(self.resource_path("icons/logo.png")).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        header_layout.addWidget(logo_label)
        
        # Title
        title = QLabel("Leopardo AI")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title)
        header_layout.setAlignment(title, Qt.AlignLeft)
        
        # Spacer
        header_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        header.setLayout(header_layout)
        self.main_layout.addWidget(header)
        
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("background-color: #e0e0e0; margin: 0 20px;")
        self.main_layout.addWidget(divider)
    
    def setup_main_page(self):
        """ Create the main selection page """
        main_page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(25)
        
        # Title
        title = QLabel("How would you like to contact us?")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Contact options
        options = [
            {"name": "Email", "icon": "icons/email.png", "description": "Send us an email directly"},
            {"name": "Telegram", "icon": "icons/telegram.png", "description": "Message us on Telegram"},
            {"name": "WhatsApp", "icon": "icons/whatsapp.png", "description": "Chat with us on WhatsApp"},
            {"name": "License Request", "icon": "icons/license.png", "description": "Request a software license"}
        ]
        
        for option in options:
            btn = QPushButton()
            btn.setObjectName(f"option_{option['name'].lower()}")
            btn.setCursor(Qt.PointingHandCursor)
            
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(15, 10, 15, 10)
            btn_layout.setSpacing(15)
            
            # Icon
            icon_label = QLabel()
            icon_pixmap = QPixmap(self.resource_path(option['icon'])).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(icon_pixmap)
            btn_layout.addWidget(icon_label)
            
            # Text
            text_layout = QVBoxLayout()
            text_layout.setSpacing(5)
            
            name_label = QLabel(option['name'])
            name_label.setFont(QFont("Arial", 12, QFont.Bold))
            name_label.setStyleSheet("color: #2c3e50;")
            
            desc_label = QLabel(option['description'])
            desc_label.setFont(QFont("Arial", 10))
            desc_label.setStyleSheet("color: #666;")
            
            text_layout.addWidget(name_label)
            text_layout.addWidget(desc_label)
            btn_layout.addLayout(text_layout)
            
            # Arrow
            arrow_label = QLabel("→")
            arrow_label.setFont(QFont("Arial", 14, QFont.Bold))
            arrow_label.setStyleSheet("color: #888;")
            btn_layout.addWidget(arrow_label)
            
            btn.setLayout(btn_layout)
            btn.setFixedHeight(70)
            btn.clicked.connect(lambda _, x=option['name'].lower(): self.handle_option_selection(x))
            layout.addWidget(btn)
        
        # Footer
        footer = QLabel("We typically respond within 24 hours")
        footer.setFont(QFont("Arial", 10))
        footer.setStyleSheet("color: #888; margin-top: 20px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
        
        main_page.setLayout(layout)
        self.stacked_widget.addWidget(main_page)
    
    def setup_license_page(self):
        """ Create the license request page """
        license_page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 30)
        layout.setSpacing(20)
        
        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setObjectName("backButton")
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setFont(QFont("Arial", 10))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn, alignment=Qt.AlignLeft)
        
        # Title
        title = QLabel("License Request")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Name field
        name_label = QLabel("Your Name:")
        name_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)
        
        # Email field
        email_label = QLabel("Email Address:")
        email_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        
        # Module selection
        module_label = QLabel("Select Module:")
        module_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.module_combo = QComboBox()
        self.module_combo.addItems(["WA CRM", "FB Robot Pro", "XBot", "Complete Suite"])
        form_layout.addWidget(module_label)
        form_layout.addWidget(self.module_combo)
        
        # Duration selection
        duration_label = QLabel("License Duration:")
        duration_label.setFont(QFont("Arial", 10, QFont.Bold))
        
        duration_layout = QHBoxLayout()
        self.duration_group = QButtonGroup()
        durations = ["Monthly ($49)", "Annual ($399)", "Lifetime ($999)"]
        
        for i, duration in enumerate(durations):
            radio = QRadioButton(duration)
            radio.setFont(QFont("Arial", 10))
            self.duration_group.addButton(radio, i)
            duration_layout.addWidget(radio)
        
        form_layout.addWidget(duration_label)
        form_layout.addLayout(duration_layout)
        
        layout.addLayout(form_layout)
        
        # Submit button
        submit_btn = QPushButton("Request License")
        submit_btn.setObjectName("submitButton")
        submit_btn.setCursor(Qt.PointingHandCursor)
        submit_btn.setFont(QFont("Arial", 12, QFont.Bold))
        submit_btn.clicked.connect(self.submit_license_request)
        layout.addWidget(submit_btn, alignment=Qt.AlignCenter)
        
        # Add spacer to push everything up
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        license_page.setLayout(layout)
        self.stacked_widget.addWidget(license_page)
    
    def setup_contact_page(self):
        """ Create the contact form page """
        contact_page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 30)
        layout.setSpacing(20)
        
        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setObjectName("backButton")
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setFont(QFont("Arial", 10))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn, alignment=Qt.AlignLeft)
        
        # Title
        self.contact_title = QLabel()
        self.contact_title.setFont(QFont("Arial", 16, QFont.Bold))
        self.contact_title.setStyleSheet("color: #2c3e50;")
        self.contact_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.contact_title)
        
        # Contact method indicator
        self.contact_method = QLabel()
        self.contact_method.setFont(QFont("Arial", 10))
        self.contact_method.setStyleSheet("color: #666;")
        self.contact_method.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.contact_method)
        
        # Form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Name field
        name_label = QLabel("Your Name:")
        name_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.contact_name_input = QLineEdit()
        self.contact_name_input.setPlaceholderText("Enter your name")
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.contact_name_input)
        
        # Email field
        email_label = QLabel("Email Address:")
        email_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.contact_email_input = QLineEdit()
        self.contact_email_input.setPlaceholderText("Enter your email")
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.contact_email_input)
        
        # Message field (only for email)
        self.message_label = QLabel("Your Message:")
        self.message_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Enter your message")
        self.message_input.setVisible(False)  # Hidden by default
        
        form_layout.addWidget(self.message_label)
        form_layout.addWidget(self.message_input)
        
        layout.addLayout(form_layout)
        
        # Submit button
        self.contact_submit_btn = QPushButton()
        self.contact_submit_btn.setObjectName("submitButton")
        self.contact_submit_btn.setCursor(Qt.PointingHandCursor)
        self.contact_submit_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.contact_submit_btn.clicked.connect(self.handle_contact_submit)
        layout.addWidget(self.contact_submit_btn, alignment=Qt.AlignCenter)
        
        # Add spacer to push everything up
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        contact_page.setLayout(layout)
        self.stacked_widget.addWidget(contact_page)
    
    def handle_option_selection(self, option):
        """ Handle selection of a contact option """
        if option == "license request":
            self.stacked_widget.setCurrentIndex(1)  # License page
        else:
            self.current_contact_method = option
            self.contact_title.setText(f"Contact via {option.capitalize()}")
            self.contact_method.setText(f"Using {option.capitalize()}")
            
            # Update UI based on contact method
            if option == "email":
                self.message_label.setVisible(True)
                self.message_input.setVisible(True)
                self.message_input.setPlaceholderText("Enter your message")
                self.contact_submit_btn.setText("Send Email")
            elif option in ["telegram", "whatsapp"]:
                self.message_label.setVisible(True)
                self.message_input.setVisible(True)
                self.message_input.setPlaceholderText("Optional message (you can add it later)")
                self.contact_submit_btn.setText(f"Open {option.capitalize()}")
            else:
                self.message_label.setVisible(False)
                self.message_input.setVisible(False)
                self.contact_submit_btn.setText("Continue")
            
            self.stacked_widget.setCurrentIndex(2)  # Contact page
    
    def submit_license_request(self):
        """ Handle license request submission """
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        module = self.module_combo.currentText()
        duration_btn = self.duration_group.checkedButton()
        
        # Validation
        if not email or "@" not in email:
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
        
        # Show confirmation
        QMessageBox.information(
            self,
            "Request Submitted",
            "Your license request has been received. After payment processing, "
            "you'll receive your license key via email within 24 hours."
        )
        
        # Clear form
        self.name_input.clear()
        self.email_input.clear()
        self.duration_group.setExclusive(False)
        for btn in self.duration_group.buttons():
            btn.setChecked(False)
        self.duration_group.setExclusive(True)
        
        # Return to main page
        self.stacked_widget.setCurrentIndex(0)
    
    def handle_contact_submit(self):
        """ Handle contact form submission """
        name = self.contact_name_input.text().strip()
        email = self.contact_email_input.text().strip()
        message = self.message_input.text().strip() if self.message_input.isVisible() else ""
        method = self.current_contact_method
        
        # Validation
        if not email or "@" not in email:
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return
            
        if method == "email" and not message:
            QMessageBox.warning(self, "Missing Message", "Please enter your message.")
            return
        
        # Save to database
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO contact_requests (name, email, method, message) VALUES (?, ?, ?, ?)",
            (name, email, method, message)
        )
        self.conn.commit()
        
        # Handle different contact methods
        if method == "email":
            webbrowser.open(f"mailto:support@leopardo-ai.com?subject=Contact%20from%20{name}&body={message}")
            QMessageBox.information(
                self,
                "Email Ready",
                "Your email client should open with a pre-filled message. "
                "Just hit send to contact our support team."
            )
        elif method == "telegram":
            webbrowser.open("https://t.me/leopardo_ai_support")
            QMessageBox.information(
                self,
                "Telegram Ready",
                "We've opened Telegram. Please send your message to @leopardo_ai_support"
            )
        elif method == "whatsapp":
            webbrowser.open("https://wa.me/1234567890")  # Replace with actual number
            QMessageBox.information(
                self,
                "WhatsApp Ready",
                "We've opened WhatsApp. Please send your message to our support number."
            )
        
        # Clear form
        self.contact_name_input.clear()
        self.contact_email_input.clear()
        self.message_input.clear()
        
        # Return to main page
        self.stacked_widget.setCurrentIndex(0)
    
    def get_stylesheet(self):
        """ Return the stylesheet for the application """
        return """
            QWidget {
                background-color: #ffffff;
            }
            
            #header {
                background-color: #ffffff;
                border-bottom: 1px solid #e0e0e0;
            }
            
            QPushButton {
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
                font-weight: bold;
            }
            
            QPushButton:hover {
                opacity: 0.9;
            }
            
            #backButton {
                background-color: transparent;
                color: #0078d4;
                text-align: left;
                padding: 5px 10px;
            }
            
            #backButton:hover {
                text-decoration: underline;
            }
            
            #submitButton {
                background-color: #0078d4;
                color: white;
                min-width: 200px;
                padding: 12px 24px;
            }
            
            #submitButton:hover {
                background-color: #005a9e;
            }
            
            QLineEdit, QComboBox {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 12px;
            }
            
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #0078d4;
                outline: none;
            }
            
            QRadioButton {
                spacing: 8px;
                font-size: 12px;
            }
            
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            
            QRadioButton::indicator::unchecked {
                border: 2px solid #aaa;
                border-radius: 9px;
            }
            
            QRadioButton::indicator::checked {
                border: 2px solid #0078d4;
                border-radius: 9px;
                background-color: #0078d4;
            }
            
            QPushButton[objectName^="option_"] {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                text-align: left;
            }
            
            QPushButton[objectName^="option_"]:hover {
                background-color: #e9ecef;
                border-color: #d4d4d4;
            }
        """
    
    def closeEvent(self, event):
        """ Clean up when closing the application """
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