import os
import base64
import json
import csv
import sqlite3
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
                             QHeaderView, QAbstractItemView, QLineEdit, QHBoxLayout, QCheckBox,
                             QMenu, QAction, QMessageBox, QComboBox, QScrollBar, QFrame, QDialog, QFormLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QFileDialog
from translation import TranslatorManager
from PyQt5.QtGui import QFont, QIcon
from ui.header import HeaderSection  
from ui.footer import FooterSection 
from PyQt5.QtWidgets import QPushButton, QMenu, QAction, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt
import re
from datetime import datetime
import logging
logging.basicConfig(level=logging.ERROR)

import sqlite3
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QUrlQuery, QObject, pyqtSlot
SCOPES = ['https://www.googleapis.com/auth/drive.readonly',
          'https://www.googleapis.com/auth/contacts.readonly']

from PyQt5.QtCore import QUrl, QUrlQuery
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import pandas as pd
import sqlite3
import platform

def get_output_folder():
    """
    Returns the path to the 'Wabon/Robot1' folder located at the root of the system.
    """
    if platform.system() == "Windows":
        # On Windows: C:\Wabon\Robot1
        return os.path.join("C:\\", "Wabon", "robot1")
    elif platform.system() in ["Darwin", "Linux"]:  # macOS and Linux
        # On macOS/Linux: /Wabon/Robot1
        return os.path.join("/", "Wabon", "robot1")
    else:
        raise OSError("Unsupported operating system.")

# Base64 encoded client_secret.json
CLIENT_SECRET_BASE64 = "eyJpbnN0YWxsZWQiOnsiY2xpZW50X2lkIjoiMjU4MDE1NDY5NTc3LWRpdDhxNzdxNWNsZzQ0cmpscjcxNDFwdWIyMnJkZHNiLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwicHJvamVjdF9pZCI6InRlYWstbWFudGlzLTQzMzIxMy1hNCIsImF1dGhfdXJpIjoiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tL28vb2F1dGgyL2F1dGgiLCJ0b2tlbl91cmkiOiJodHRwczovL29hdXRoMi5nb29nbGVhcGlzLmNvbS90b2tlbiIsImF1dGhfcHJvdmlkZXJfeDUwOV9jZXJ0X3VybCI6Imh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL29hdXRoMi92MS9jZXJ0cyIsImNsaWVudF9zZWNyZXQiOiJHT0NTUFgtUDhoZXYteEE4aGFxbzdqRjZ1ZlVQdkdFeGJ4MiIsInJlZGlyZWN0X3VyaXMiOlsiaHR0cDovL2xvY2FsaG9zdCJdfX0="

# Decode the client_secret.json from base64
client_secret_json_str = base64.b64decode(CLIENT_SECRET_BASE64).decode('utf-8')
client_secret_dict = json.loads(client_secret_json_str)

class OAuthDialog(QDialog):
    def __init__(self, client_secret_dict, scopes, redirect_uri, parent=None):
        super().__init__(parent)
        self.client_secret_dict = client_secret_dict
        self.scopes = scopes
        self.redirect_uri = redirect_uri
        self.web_view = QWebEngineView()
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        self.setLayout(layout)
        self.web_view.urlChanged.connect(self.handle_url_changed)
        self.flow = Flow.from_client_config(
            client_config=client_secret_dict,
            scopes=scopes,
            redirect_uri=redirect_uri
        )
        self.auth_url, _ = self.flow.authorization_url(prompt='consent')

    def showEvent(self, event):
        super().showEvent(event)
        self.web_view.load(QUrl(self.auth_url))

    def handle_url_changed(self, url):
        url_str = url.toString()
        if self.redirect_uri in url_str:
            query = QUrlQuery(url)
            code = query.queryItemValue('code')
            if code:
                self.flow.fetch_token(code=code)
                self.credentials = self.flow.credentials
                self.accept()
            else:
                QMessageBox.warning(self, self.tr("Error"), self.tr("No code found in the redirect URL."))
                self.reject()

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection to database successful.")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_table(conn):
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone_number TEXT,
                email TEXT,
                category TEXT,
                description TEXT,
                note TEXT
            );
        ''')
        print("Table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

class ContactDialog(QDialog):
    def __init__(self, mode="add", contact=None, conn=None, parent=None):
        super().__init__(parent)
        self.mode = mode
        self.contact = contact
        self.conn = conn

        # Set the title and size of the window
        self.setWindowTitle(self.tr("Add Contact") if mode == "add" else self.tr("Edit Contact"))
        self.setFixedSize(700, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                border-radius: 12px;
                border: 1px solid #dcdcdc;
            }
        """)

        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Frame for the image
        image_frame = QFrame(self)
        image_frame.setFixedSize(200, 360)
        image_frame.setStyleSheet("""
            QFrame {
                border: 2px solid #dcdcdc;
                border-radius: 10px;
                background-color: #ffffff;
            }
        """)

        # Add an image in the frame
        image_label = QLabel(image_frame)
        image_label.setPixmap(QPixmap("resources/images/5.jpg").scaled(180, 340, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(image_frame)

        # Form section
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Title
        title_label = QLabel(self.tr("Add New Contact") if mode == "add" else self.tr("Edit Contact"))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        form_layout.addWidget(title_label)

        # Form with validations and advanced styles
        form_inputs_layout = QFormLayout()
        form_inputs_layout.setSpacing(15)

        self.name_input = self._create_styled_line_edit(self.tr("Enter full name"))
        self.phone_input = self._create_styled_line_edit(self.tr("Enter phone number"), validation="phone")
        self.email_input = self._create_styled_line_edit(self.tr("Enter email address"), validation="email")
        self.category_combo = self._create_styled_combo_box([self.tr("Client"), self.tr("Prospect"), self.tr("Partner"), self.tr("Other")])
        self.description_input = self._create_styled_line_edit(self.tr("Enter a description (optional)"))
        self.note_input = self._create_styled_line_edit(self.tr("Add a note (optional)"))

        form_inputs_layout.addRow(self._create_styled_label(self.tr("Name:")), self.name_input)
        form_inputs_layout.addRow(self._create_styled_label(self.tr("Phone:")), self.phone_input)
        form_inputs_layout.addRow(self._create_styled_label(self.tr("Email:")), self.email_input)
        form_inputs_layout.addRow(self._create_styled_label(self.tr("Category:")), self.category_combo)
        form_inputs_layout.addRow(self._create_styled_label(self.tr("Description:")), self.description_input)
        form_inputs_layout.addRow(self._create_styled_label(self.tr("Note:")), self.note_input)

        form_layout.addLayout(form_inputs_layout)

        # Buttons at the bottom
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.submit_button = QPushButton(self.tr("Submit"))
        self.submit_button.setIcon(QIcon("icons/checkmark.png"))  # Add an icon if available
        self.submit_button.setStyleSheet(self._button_style("#27ae60"))
        self.submit_button.clicked.connect(self.handle_submit)

        self.cancel_button = QPushButton(self.tr("Cancel"))
        self.cancel_button.setStyleSheet(self._button_style("#e74c3c"))
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.cancel_button)

        form_layout.addSpacing(20)
        form_layout.addLayout(button_layout)

        main_layout.addLayout(form_layout)

        # Pre-fill fields in edit mode
        if mode == "edit" and contact:
            self.name_input.setText(contact.get("name", ""))
            self.phone_input.setText(contact.get("phone_number", ""))
            self.email_input.setText(contact.get("email", ""))
            self.category_combo.setCurrentText(contact.get("category", ""))
            self.description_input.setText(contact.get("description", ""))
            self.note_input.setText(contact.get("note", ""))

    def _create_styled_line_edit(self, placeholder, validation=None, font_size=14, border_color="#d0d0d0", focus_color="#3498db", bg_color="#f7f7f7", text_color="#2c3e50"):
        """
        Creates a styled text field with full customization options.

        Args:
            placeholder (str): Placeholder text.
            validation (str, optional): Type of validation ("phone", "email"). Default is None.
            font_size (int, optional): Font size. Default is 14.
            border_color (str, optional): Normal border color. Default is "#d0d0d0".
            focus_color (str, optional): Focus border color. Default is "#3498db".
            bg_color (str, optional): Background color. Default is "#f7f7f7".
            text_color (str, optional): Text color. Default is "#2c3e50".

        Returns:
            QLineEdit: A styled text field.
        """
        line_edit = QLineEdit(self)
        line_edit.setPlaceholderText(placeholder)
        line_edit.setStyleSheet(f"""
            QLineEdit {{
                font-size: {font_size}px;
                padding: 2px;
                border: 2px solid {border_color};
                border-radius: 1px;
                background-color: {bg_color};
                color: {text_color};
            }}
            QLineEdit:focus {{
                border-color: {focus_color};
                background-color: #ffffff;
                color: {text_color};
            }}
        """)
        if validation == "phone":
            line_edit.textChanged.connect(self.validate_phone)
        elif validation == "email":
            line_edit.textChanged.connect(self.validate_email)
        return line_edit

    def _create_styled_combo_box(self, items, font_size=14, border_color="#d0d0d0", focus_color="#3498db", bg_color="#f7f7f7", text_color="#2c3e50", selection_color="#ecf0f1"):
        """
        Creates a styled combo box with customization options.

        Args:
            items (list): List of items.
            font_size (int, optional): Font size. Default is 14.
            border_color (str, optional): Border color. Default is "#d0d0d0".
            focus_color (str, optional): Focus border color. Default is "#3498db".
            bg_color (str, optional): Background color. Default is "#f7f7f7".
            text_color (str, optional): Text color. Default is "#2c3e50".
            selection_color (str, optional): Selected item background color. Default is "#ecf0f1".

        Returns:
            QComboBox: A styled combo box.
        """
        combo_box = QComboBox(self)
        combo_box.addItems(items)
        combo_box.setStyleSheet(f"""
            QComboBox {{
                font-size: {font_size}px;
                padding: 2px;
                border: 2px solid {border_color};
                border-radius: 2px;
                background-color: {bg_color};
                color: {text_color};
            }}
            QComboBox:focus {{
                border-color: {focus_color};
            }}
            QComboBox QAbstractItemView {{
                selection-background-color: {focus_color};
                background-color: {selection_color};
                color: {text_color};
            }}
        """)
        return combo_box

    def _create_styled_label(self, text, font="Arial", font_size=12, text_color="#34495e", alignment=Qt.AlignLeft):
        """
        Creates a modern and customized label.

        Args:
            text (str): Text to display.
            font (str, optional): Font of the text. Default is "Arial".
            font_size (int, optional): Font size. Default is 12.
            text_color (str, optional): Text color. Default is "#34495e".
            alignment (Qt.Alignment, optional): Text alignment. Default is Qt.AlignLeft.

        Returns:
            QLabel: A styled label.
        """
        label = QLabel(text, self)
        label.setFont(QFont(font, font_size))
        label.setStyleSheet(f"color: {text_color};")
        label.setAlignment(alignment)
        return label

    def _button_style(self, color):
        """Create a style for buttons."""
        return f"""
            QPushButton {{
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
                background-color: {color};
                color: white;
            }}
            QPushButton:hover {{
                background-color: {self._darken_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(color, 30)};
            }}
        """

    def _darken_color(self, color, factor=10):
        """Darken a hexadecimal color."""
        color = color.lstrip("#")
        r = max(0, int(color[:2], 16) - factor)
        g = max(0, int(color[2:4], 16) - factor)
        b = max(0, int(color[4:], 16) - factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    def validate_phone(self, text):
        """Validate that the field contains only numbers."""
        if not re.fullmatch(r"\+?[0-9]*", text):
            self.phone_input.setStyleSheet("border: 2px solid #e74c3c; background-color: #fdecea;")
        else:
            self.phone_input.setStyleSheet("border: 2px solid #27ae60; background-color: #f9f9f9;")

    def validate_email(self, text):
        """Validate that the field contains a valid email address."""
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", text):
            self.email_input.setStyleSheet("border: 2px solid #e74c3c; background-color: #fdecea;")
        else:
            self.email_input.setStyleSheet("border: 2px solid #27ae60; background-color: #f9f9f9;")

    def handle_submit(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        category = self.category_combo.currentText()
        description = self.description_input.text()
        note = self.note_input.text()
        
        if self.conn:
            cursor = self.conn.cursor()
            if self.mode == 'add':
                cursor.execute('''
                    INSERT INTO contacts (name, phone_number, email, category, description, note)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, phone, email, category, description, note))
            elif self.mode == 'edit':
                cursor.execute('''
                    UPDATE contacts SET
                    name = ?,
                    phone_number = ?,
                    email = ?,
                    category = ?,
                    description = ?,
                    note = ?
                    WHERE id = ?
                ''', (name, phone, email, category, description, note, self.contact['id']))
            self.conn.commit()
        self.accept()

db_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-WA-Robot', 'contacts.db')

# Create database connection and table
conn = create_connection(db_path)
create_table(conn)

class ContactTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        db_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-WA-Robot', 'contacts.db')

        self.conn = create_connection(db_path)
        create_table(self.conn)
        layout = QVBoxLayout(self)
        # Add the header
        header = HeaderSection(self, title=self.tr("Contact Management"), app_name=self.tr("Nova360 AI"), slogan=self.tr("AI Marketing & Management Auto"))
        layout.addWidget(header)
        self.contacts = self.load_contacts()
        self.items_per_page = 10
        self.current_page = 1

        # Search bar and buttons layout (single row)
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 0, 10, 20)  # Add margins for better spacing
        top_layout.setSpacing(15)  # Spacing between elements

        # Search bar
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText(self.tr("Search contacts..."))
        self.search_field.textChanged.connect(self.filter_table)
        self.search_field.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 2px solid #dcdcdc;
                border-radius: 8px;
                background-color: #ffffff;
                min-width: 300px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                outline: none;
                background-color: #f5f5f5;
            }
        """)
        top_layout.addWidget(self.search_field)

        # Import menu
        import_button = QPushButton(self.tr("📥 Import"), self)
        import_button.setStyleSheet(self.get_button_style())
        import_menu = QMenu(self.tr("Import"), self)
        import_from_device_action = QAction(self.tr("From Device"), self)
        import_from_drive_action = QAction(self.tr("From Google Drive"), self)
        import_from_contacts_action = QAction(self.tr("From Google Contacts"), self)
        import_menu.addAction(import_from_device_action)
        import_menu.addAction(import_from_drive_action)
        import_menu.addAction(import_from_contacts_action)
        import_button.setMenu(import_menu)

        # Connect actions
        import_from_device_action.triggered.connect(self.import_contacts)
        import_from_drive_action.triggered.connect(self.import_contacts)
        import_from_contacts_action.triggered.connect(self.import_contacts)

        top_layout.addWidget(import_button)

        # Export button
        export_button = QPushButton(self.tr("📤 Export"), self)
        export_button.setStyleSheet(self.get_button_style())
        export_button.clicked.connect(self.export_contacts)
        top_layout.addWidget(export_button)

        # Add contact button
        add_contact_button = QPushButton(self.tr("➕ Add Contact"), self)
        add_contact_button.setStyleSheet(self.get_button_style(highlight=True))
        add_contact_button.clicked.connect(self.open_add_contact_dialog)
        top_layout.addWidget(add_contact_button)

        db_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-WA-Robot', 'contacts.db')
        output_folder = get_output_folder()

        add_send_button = QPushButton(self.tr("🚀 Send to Robot"), self)
        add_send_button.setStyleSheet("""
            QPushButton {
                background-color: #1F1B24; /* Dark background */
                color: #00D4FF; /* Neon text color */
                border: 2px solid #00D4FF; /* Bright border */
                border-radius: 20px; /* Rounded corners */
                font-size: 16px;
                padding: 10px 20px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #00D4FF; /* Hover color */
                color: #1F1B24; /* Inverted text */
                border: 2px solid #1F1B24; /* Dark border */
            }
            QPushButton:pressed {
                background-color: #008DBE; /* Click color */
                border: 2px solid #006B93;
            }
        """)

        # Add a glowing shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 212, 255))  # Neon blue
        shadow.setOffset(0, 5)
        add_send_button.setGraphicsEffect(shadow)

        # Elegant and modern font
        font = QFont("Segoe UI", 14, QFont.Bold)
        add_send_button.setFont(font)

        # Create context menu
        send_menu = QMenu(self.tr("Send"), self)
        send_selected = QAction(self.tr("📋 Send Selected"), self)
        send_all = QAction(self.tr("📁 Send All Contacts"), self)
        send_menu.addAction(send_all)
        send_menu.addAction(send_selected)
        add_send_button.setMenu(send_menu)

        # Connect actions
        send_selected.triggered.connect(self.export_selected_contacts_to_json)
        send_all.triggered.connect(lambda: self.export_contacts_to_json(self.db_path, self.output_folder))

        top_layout.addWidget(add_send_button)

        # Add the top layout to the main layout
        layout.addLayout(top_layout)
        # Contact table
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)

        self.table.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                alternate-background-color: #f0f0f0;
            }
            QHeaderView::section {
                background-color: #007BFF;
                color: white;
                padding: 10px;
            }
        """)

        self.table.setHorizontalHeaderLabels([self.tr("Select"), self.tr("Name"), self.tr("Phone"), self.tr("Email"), self.tr("Category"), self.tr("Actions")])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Pagination
        self.pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton(self.tr("Previous"))
        self.prev_button.clicked.connect(self.previous_page)
        self.next_button = QPushButton(self.tr("Next"))
        self.next_button.clicked.connect(self.next_page)

        self.pagination_label = QLabel(self.tr(f"Page {self.current_page}"))
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.pagination_label)
        self.pagination_layout.addWidget(self.next_button)
        layout.addLayout(self.pagination_layout)

        self.prev_button.setStyleSheet("background-color: #6c757d; color: white; padding: 5px 10px;")
        self.next_button.setStyleSheet("background-color: #007bff; color: white; padding: 5px 10px;")
        self.pagination_label.setStyleSheet("font-size: 14px;")

        self.populate_table()
        # Add the footer
        footer = FooterSection(self)
        layout.addWidget(footer)

    def get_button_style(self, highlight=False):
        """
        Returns a consistent style for buttons, with optional highlight for primary buttons.
        """
        base_style = """
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                background-color: #7f8c8d;
                border: none;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
                transition: background-color 0.3s ease, transform 0.2s ease;
            }
            QPushButton:hover {
                background-color: #95a5a6;
                transform: scale(1.05);
            }
        """
        highlight_style = """
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                background-color: #3498db;
                border: none;
                box-shadow: 2px 2px 8px rgba(52, 152, 219, 0.4);
                transition: background-color 0.3s ease, transform 0.2s ease;
            }
            QPushButton:hover {
                background-color: #2980b9;
                transform: scale(1.05);
            }
        """
        return highlight_style if highlight else base_style

    def load_contacts(self):
        contacts = []
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM contacts")
            rows = cursor.fetchall()
            for row in rows:
                note = row[6] if row[6] is not None else ''
                contact = {
                    'id': row[0],
                    'name': row[1],
                    'phone_number': row[2],
                    'email': row[3],
                    'category': row[4],
                    'description': row[5],
                    'note': note
                }
                contacts.append(contact)
        except sqlite3.Error as e:
            print(f"Error loading contacts: {e}")
        return contacts

    def populate_table(self):
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        visible_contacts = self.contacts[start_index:end_index]

        self.table.setRowCount(len(visible_contacts))
        for row, contact in enumerate(visible_contacts):
            checkbox = QCheckBox()
            self.table.setCellWidget(row, 0, checkbox)

            self.table.setItem(row, 1, QTableWidgetItem(contact['name']))
            self.table.setItem(row, 2, QTableWidgetItem(contact['phone_number']))
            self.table.setItem(row, 3, QTableWidgetItem(contact['email']))
            self.table.setItem(row, 4, QTableWidgetItem(contact['category']))

            action_button = QPushButton(self.tr("Actions"))
            action_menu = QMenu(self)
            edit_action = QAction(self.tr("Edit"), self)
            delete_action = QAction(self.tr("Delete"), self)
            show_action = QAction(self.tr("Show"), self)
            edit_action.triggered.connect(lambda _, r=contact['id']: self.edit_contact(r))
            delete_action.triggered.connect(lambda _, r=contact['id']: self.delete_contact(r))
            show_action.triggered.connect(lambda _, r=contact['id']: self.show_contact(r))
            action_menu.addAction(edit_action)
            action_menu.addAction(delete_action)
            action_menu.addAction(show_action)
            action_button.setMenu(action_menu)
            self.table.setCellWidget(row, 5, action_button)

        self.pagination_label.setText(self.tr(f"Page {self.current_page}"))

    def show_contact(self, contact_id):
        contact = self.get_contact_by_id(contact_id)
        if contact:
            dialog = ShowContactDialog(contact, self)
            dialog.exec_()

    def get_contact_by_id(self, contact_id):
        for contact in self.contacts:
            if contact['id'] == contact_id:
                return contact
        return None

    def detect_columns(self, headers):
        """
        Detects columns corresponding to expected fields using multilingual keywords.
        :param headers: List of column headers from the file.
        :return: A dictionary mapping fields to column indices.
        """
        # Keywords for each field in different languages
        keywords = {
            'name': ['name', 'nom', 'isim', 'اسم', 'full name', 'fullname', 'contact name'],
            'phone_number': ['phone', 'telephone', 'téléphone', 'numara', 'رقم الهاتف', 'mobile', 'phone number'],
            'email': ['email', 'e-mail', 'mail', 'courriel', 'e-posta', 'بريد إلكتروني'],
            'category': ['category', 'catégorie', 'kategori', 'فئة', 'type', 'group'],
            'description': ['description', 'وصف', 'açıklama', 'info', 'notes'],
            'note': ['note', 'comment', 'commentaire', 'yorum', 'ملاحظة']
        }

        column_mapping = {}
        for i, header in enumerate(headers):
            header_lower = header.lower().strip()  # Normalize the header
            for field, keys in keywords.items():
                if any(key in header_lower for key in keys):
                    column_mapping[field] = i
                    break  # Stop as soon as a match is found

        return column_mapping

    def import_contacts(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            self.tr("Import Contacts"), 
            "", 
            self.tr("CSV Files (*.csv);;Excel Files (*.xlsx *.xls)")
        )
        if file_name:
            if file_name.endswith('.csv'):
                self.import_from_csv(file_name)
            elif file_name.endswith(('.xlsx', '.xls')):
                self.import_from_excel(file_name)
            else:
                QMessageBox.warning(self, self.tr("Unsupported Format"), self.tr("The selected file format is not supported."))

    def import_from_excel(self, file_name):
        try:
            if file_name.endswith('.xlsx'):
                df = pd.read_excel(file_name, engine='openpyxl')
            elif file_name.endswith('.xls'):
                df = pd.read_excel(file_name, engine='xlrd')
            else:
                raise ValueError(self.tr("Unsupported Excel file format."))

            # Convert headers to lowercase for easier detection
            df.columns = [header.lower() for header in df.columns]
            column_mapping = self.detect_columns(df.columns)

            # Check that minimal columns are detected
            if 'name' not in column_mapping or 'phone_number' not in column_mapping:
                QMessageBox.warning(self, self.tr("Error"), self.tr("The 'name' and 'phone_number' columns are required."))
                return

            for _, row in df.iterrows():
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO contacts (name, phone_number, email, category, description, note)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    row[column_mapping.get('name', '')],
                    row[column_mapping.get('phone_number', '')],
                    row[column_mapping.get('email', '')],
                    row[column_mapping.get('category', '')],
                    row[column_mapping.get('description', '')],
                    row[column_mapping.get('note', '')]
                ))
                self.conn.commit()
            self.contacts = self.load_contacts()
            self.populate_table()
        except Exception as e:
            QMessageBox.warning(self, self.tr("Import Error"), self.tr(f"An error occurred during import: {e}"))

    def import_from_csv(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as f:  # Handle UTF-8 encoding
                reader = csv.reader(f)
                headers = next(reader)  # Read headers
                column_mapping = self.detect_columns(headers)

                # Check that minimal columns are detected
                if 'name' not in column_mapping or 'phone_number' not in column_mapping:
                    QMessageBox.warning(self, self.tr("Error"), self.tr("The 'name' and 'phone_number' columns are required."))
                    return

                for row in reader:
                    cursor = self.conn.cursor()
                    cursor.execute('''
                        INSERT INTO contacts (name, phone_number, email, category, description, note)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        row[column_mapping.get('name', '')],
                        row[column_mapping.get('phone_number', '')],
                        row[column_mapping.get('email', '')],
                        row[column_mapping.get('category', '')],
                        row[column_mapping.get('description', '')],
                        row[column_mapping.get('note', '')]
                    ))
                    self.conn.commit()
            self.contacts = self.load_contacts()
            self.populate_table()
        except Exception as e:
            QMessageBox.warning(self, self.tr("Import Error"), self.tr(f"An error occurred during import: {e}"))

    def export_contacts_to_json(self, db_path, output_folder):
        """
        Exports contacts from the database to a JSON file.

        Args:
            db_path (str): The path to the SQLite database.
            output_folder (str): The folder where the JSON file will be saved.

        Returns:
            str: The full path of the generated JSON file.
        """
        # Check if the database file exists
        if not os.path.exists(db_path):
            raise FileNotFoundError(self.tr(f"The database is not found."))

        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Retrieve contacts
        cursor.execute("SELECT name, phone_number FROM contacts")
        contacts = cursor.fetchall()

        # Format contacts as a list of dictionaries
        formatted_contacts = [{"name": name, "phone": phone} for name, phone in contacts]

        # JSON file name
        output_file = os.path.join(output_folder, "wacontact.json")

        # Handle name conflicts (if a file with the same name already exists)
        if os.path.exists(output_file):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_file_name = f"wacontact_{timestamp}.json"
            renamed_file = os.path.join(output_folder, new_file_name)

            # Check if the renamed file already exists to avoid any conflict
            while os.path.exists(renamed_file):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_file_name = f"wacontact_{timestamp}.json"
                renamed_file = os.path.join(output_folder, new_file_name)

            os.rename(output_file, renamed_file)

        # Save data in JSON format
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(formatted_contacts, json_file, ensure_ascii=False, indent=4)

        # Close the database connection
        conn.close()
        self.notify_robot_updated(output_file)
        # Return the path of the generated file
        return output_file

    def notify_robot_updated(self, output_file):
        """
        Displays a confirmation message to inform that the robot has been updated.

        Args:
            output_file (str): The path of the generated JSON file.
        """
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setWindowTitle(self.tr("Update Complete"))
        message.setText(self.tr("The robot has been successfully updated!"))
        message.setInformativeText(self.tr(f"File generated the robot is happy"))
        message.setStandardButtons(QMessageBox.Ok)
        message.exec_()

    def get_selected_contacts(self):
        """
        Retrieves the selected contacts in the table (checked boxes).

        Returns:
            list: A list of dictionaries representing the selected contacts.
        """
        selected_contacts = []

        # Iterate through the table rows
        for row in range(self.table.rowCount()):
            # Check if the checkbox is checked
            checkbox = self.table.cellWidget(row, 0)
            if checkbox is not None and checkbox.isChecked():
                # Retrieve the data from the selected row
                contact = {
                    'name': self.table.item(row, 1).text(),
                    'phone': self.table.item(row, 2).text(),
                    'email': self.table.item(row, 3).text(),
                    'category': self.table.item(row, 4).text(),
                }
                selected_contacts.append(contact)

        return selected_contacts

    def export_selected_contacts_to_json(self):
        """
        Exports the selected contacts in the table to a JSON file.
        If wacontact.json already exists, it is renamed for archiving before creating a new wacontact.json.
        """
        selected_contacts = self.get_selected_contacts()

        if not selected_contacts:
            QMessageBox.information(self, self.tr("No Contacts"), self.tr("No contacts selected."))
            return

        # Path to save the file
        output_folder = get_output_folder()
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, "wacontact.json")

        # If the file exists, rename it for archiving
        if os.path.exists(output_file):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archived_file = os.path.join(output_folder, f"wacontact_{timestamp}.json")
            os.rename(output_file, archived_file)

        # Save selected contacts to a JSON file
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(selected_contacts, json_file, ensure_ascii=False, indent=4)

        # Display a confirmation message
        QMessageBox.information(
            self,
            self.tr("Export Successful"),
            self.tr(f"The selected contacts have been successfully exported to:\n the robot\n"
            f"The old file has been archived if necessary."),
        )

    def export_contacts(self):
        file_name, _ = QFileDialog.getSaveFileName(self, self.tr("Export Contacts"), "", self.tr("CSV Files (*.csv)"))
        if file_name:
            try:
                fieldnames = ['name', 'phone_number', 'email', 'category', 'description', 'note']
                with open(file_name, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows({k: contact[k] for k in fieldnames} for contact in self.contacts)
            except Exception as e:
                print(f"Error exporting contacts: {e}")

    def open_add_contact_dialog(self):
        dialog = ContactDialog(mode='add', conn=self.conn, parent=self)
        dialog.exec_()
        self.contacts = self.load_contacts()
        self.populate_table()

    def edit_contact(self, contact_id):
        contact = self.get_contact_by_id(contact_id)
        if contact:
            dialog = ContactDialog(mode='edit', contact=contact, conn=self.conn, parent=self)
            if dialog.exec_():
                self.contacts = self.load_contacts()
                self.populate_table()

    def delete_contact(self, contact_id):
        reply = QMessageBox.question(self, self.tr('Confirmation'), self.tr('Do you want to delete this contact?'), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
                self.conn.commit()
                self.contacts = self.load_contacts()
                self.populate_table()
            except sqlite3.Error as e:
                print(f"Error deleting contact: {e}")

    def filter_table(self):
        search_text = self.search_field.text().lower()
        filtered_contacts = [contact for contact in self.contacts if search_text in contact['name'].lower()]
        self.contacts = filtered_contacts
        self.current_page = 1
        self.populate_table()

    def next_page(self):
        total_pages = (len(self.contacts) + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.populate_table()

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_table()

    def import_from_google_contacts(self):
        scopes = ['https://www.googleapis.com/auth/contacts.readonly']
        redirect_uri = 'http://localhost:5000/callback'
        # Load client_secret_dict from 'a.json' or wherever it's stored
        # client_secret_dict = ... 
        oauth_dialog = OAuthDialog(client_secret_dict, scopes, redirect_uri, self)
        if oauth_dialog.exec_() == QDialog.Accepted:
            credentials = oauth_dialog.credentials
            service_people = build('people', 'v1', credentials=credentials)
            
            # Fetch contacts from Google Contacts
            connections = service_people.people().connections().list(
                resourceName='people/me',
                personFields='names,emailAddresses,phoneNumbers'
            ).execute()
            contacts = connections.get('connections', [])
            
            # Prepare data for CSV
            data = []
            for contact in contacts:
                name = contact.get('names', [{}])[0].get('displayName', '') if contact.get('names') else ''
                emails = [e['value'] for e in contact.get('emailAddresses', [])]
                phones = [p['value'] for p in contact.get('phoneNumbers', [])]
                data.append({
                    'name': name,
                    'email': ', '.join(emails),
                    'phone_number': ', '.join(phones)
                })
            
            # Save to CSV
            df = pd.DataFrame(data)
            csv_file = 'google_contacts.csv'
            df.to_csv(csv_file, index=False)
            
            # Import CSV into the database
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cursor = self.conn.cursor()
                    cursor.execute('''
                        INSERT INTO contacts (name, phone_number, email, category, description, note)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        row.get('name', ''),
                        row.get('phone_number', ''),
                        row.get('email', ''),
                        'Imported from Google Contacts',
                        '',
                        ''
                    ))
                    self.conn.commit()
            
            # Remove the temporary CSV file
            os.remove(csv_file)
            
            # Reload contacts and repopulate the table
            self.contacts = self.load_contacts()
            self.populate_table()

    def import_from_google_drive(self):
        scopes = ['https://www.googleapis.com/auth/drive.readonly']
        redirect_uri = 'http://localhost:5000/callback'
        # Load client_secret_dict from 'a.json' or wherever it's stored
        # client_secret_dict = ... 
        oauth_dialog = OAuthDialog(client_secret_dict, scopes, redirect_uri, self)
        if oauth_dialog.exec_() == QDialog.Accepted:
            credentials = oauth_dialog.credentials
            service_drive = build('drive', 'v3', credentials=credentials)
            
            # List and import files from Google Drive
            results = service_drive.files().list(
                q="mimeType='text/csv' or mimeType='application/vnd.ms-excel' or mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'",
                fields="files(id, name)").execute()
            items = results.get('files', [])
            if not items:
                print("No CSV or Excel files found.")
            else:
                print("Available files:")
                for i, item in enumerate(items):
                    print(f"{i+1}. {item['name']} (ID: {item['id']})")
                selection = int(input(self.tr("Select a file by its number: "))) - 1
                if 0 <= selection < len(items):
                    file_id = items[selection]['id']
                    file_name = items[selection]['name']
                    request = service_drive.files().get_media(fileId=file_id)
                    with open(file_name, 'wb') as f:
                        f.write(request.execute())
                    if file_name.endswith(('.xlsx', '.xls', '.csv')):
                        self.import_from_excel(file_name)
                    else:
                        print("Unsupported file format.")
                else:
                    print("Invalid selection.")

class ShowContactDialog(QDialog):
    def __init__(self, contact, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Contact Details"))
        layout = QFormLayout(self)
        
        layout.addRow(self.tr("Name:"), QLabel(contact['name']))
        layout.addRow(self.tr("Phone:"), QLabel(contact['phone_number']))
        layout.addRow(self.tr("Email:"), QLabel(contact['email']))
        layout.addRow(self.tr("Category:"), QLabel(contact['category']))
        layout.addRow(self.tr("Description:"), QLabel(contact['description']))
        layout.addRow(self.tr("Note:"), QLabel(contact['note']))

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Database path
    db_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-WA-Robot', 'contacts.db')

    # Create database connection and table
    conn = create_connection(db_path)
    create_table(conn)

    # Initialize the contact table widget
    contact_table = ContactTable()
    contact_table.show()

    sys.exit(app.exec_())