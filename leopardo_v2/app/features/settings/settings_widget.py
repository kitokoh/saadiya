import sys
import json
import os
import sqlite3
import subprocess
import csv
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QMovie, QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QWidget, QScrollArea, QMessageBox, QLineEdit, QFormLayout, QComboBox,
    QGraphicsOpacityEffect, QCheckBox, QListWidget, QListWidgetItem, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QDialog
)

from .helpers import EditInstanceDialog

class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Create Tab Widget
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        # Settings Tab
        self.settings_tab = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_tab)
        self.tab_widget.addTab(self.settings_tab, "Settings")
        self.setup_settings_ui()

        # Instances Tab
        self.instances_tab = QWidget()
        self.instances_layout = QVBoxLayout(self.instances_tab)
        self.tab_widget.addTab(self.instances_tab, "Instances")
        self.setup_instances_ui()

    def setup_settings_ui(self):
        # This code is adapted from the Nova360Ultimate class
        self.user_data = {
            "bots": {},
            "modules": {},
            "info": {
                "name": "",
                "email": "",
                "role": ""
            }
        }

        self.platforms = {
            "Facebook": ["Group Share", "Auto Comment", "Page Management"],
            "Twitter": ["Auto Tweet", "Hashtag Tracker", "Analytics"],
            "Instagram": ["Auto Post", "Story Scheduler", "Hashtag Analyzer"],
        }

        self.db_path = self.get_database_path('settings.db')
        self.conn_settings = sqlite3.connect(self.db_path)
        self.cursor_settings = self.conn_settings.cursor()
        self.create_settings_tables()
        self.load_user_preferences()

        self.title_label = QLabel("\u2728 Welcome to Leopardo Settings \u2728")
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #007bff;")
        self.settings_layout.addWidget(self.title_label)

        description = QLabel("\"Configure your marketing automation experience!\"")
        description.setFont(QFont("Arial", 16))
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("color: #6c757d;")
        self.settings_layout.addWidget(description)

        user_form = QFormLayout()
        self.name_input = QLineEdit(self.user_data["info"]["name"])
        self.email_input = QLineEdit(self.user_data["info"]["email"])
        self.role_input = QComboBox()
        self.role_input.addItems(["Admin", "User", "Guest"])
        self.role_input.setCurrentText(self.user_data["info"]["role"])

        user_form.addRow("Name:", self.name_input)
        user_form.addRow("Email:", self.email_input)
        user_form.addRow("Role:", self.role_input)
        self.settings_layout.addLayout(user_form)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout()

        for platform in self.platforms.keys():
            if platform not in self.user_data["bots"]:
                button = QPushButton(f"\u25B6 {platform}")
                button.setFont(QFont("Arial", 14))
                button.setStyleSheet(
                    "padding: 15px; margin: 10px; background-color: #f0f0f0; border: 2px solid #007bff; border-radius: 10px;"
                )
                button.clicked.connect(lambda _, p=platform: self.show_modules(p))
                content_layout.addWidget(button)

        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        self.settings_layout.addWidget(scroll_area)

        finalize_button = QPushButton("\U0001F680 Finalize Configuration")
        finalize_button.setFont(QFont("Arial", 16, QFont.Bold))
        finalize_button.setStyleSheet(
            "padding: 20px; background-color: #28a745; color: white; border-radius: 10px;"
            "hover { background-color: #218838; }"
        )
        finalize_button.clicked.connect(self.finalize_setup)
        self.settings_layout.addWidget(finalize_button)

    def setup_instances_ui(self):
        # This code is adapted from the InstanceTable class
        self.instance_list = self.load_instances()
        self.visible_columns = ['Select', 'Nam Instance', 'Description', 'User', 'Expire Date', 'Actions']

        top_layout = QHBoxLayout()
        instance_label = QLabel("Liste des Instances :", self)
        top_layout.addWidget(instance_label)

        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Rechercher dans les instances...")
        self.search_field.textChanged.connect(self.filter_table)
        top_layout.addWidget(self.search_field)

        self.add_instance_button = QPushButton('Ajouter Instance')
        self.add_instance_button.setStyleSheet("background-color: #28a745; color: white; padding: 5px 10px;")
        self.add_instance_button.clicked.connect(self.add_new_instance)
        top_layout.addWidget(self.add_instance_button)

        self.export_button = QPushButton('Exporter CSV')
        self.export_button.setStyleSheet("background-color: #17a2b8; color: white; padding: 5px 10px;")
        self.export_button.clicked.connect(self.export_to_csv)
        top_layout.addWidget(self.export_button)

        self.instances_layout.addLayout(top_layout)

        self.table = QTableWidget(self)
        self.table.setColumnCount(len(self.visible_columns))
        self.table.setHorizontalHeaderLabels(self.visible_columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.instances_layout.addWidget(self.table)

        self.populate_table()

    def get_database_path(self, db_name):
        roaming_path = os.path.join(os.getenv('APPDATA'), "saadiya", "resources")
        os.makedirs(roaming_path, exist_ok=True)
        return os.path.join(roaming_path, db_name)

    def create_settings_tables(self):
        try:
            self.cursor_settings.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    role TEXT,
                    bots TEXT,
                    modules TEXT
                )
            ''')
            self.conn_settings.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {e}")

    def load_user_preferences(self):
        try:
            self.cursor_settings.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
            result = self.cursor_settings.fetchone()
            if result:
                self.user_data["info"]["name"] = result[1]
                self.user_data["info"]["email"] = result[2]
                self.user_data["info"]["role"] = result[3]
                self.user_data["bots"] = json.loads(result[4])
                self.user_data["modules"] = json.loads(result[5])
        except (sqlite3.Error, json.JSONDecodeError) as e:
            QMessageBox.warning(self, "Warning", f"Failed to load user preferences: {e}")

    def show_modules(self, platform):
        self.current_platform = platform
        self.user_data["bots"].setdefault(platform, [])

        self.clear_layout(self.settings_layout)

        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel(f"\u2728 Available Modules for {platform} \u2728")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.module_list = QListWidget()
        for module in self.platforms[platform]:
            item = QListWidgetItem(module)
            item.setCheckState(Qt.Unchecked)
            if module in self.user_data["bots"][platform]:
                item.setCheckState(Qt.Checked)
            self.module_list.addItem(item)
        layout.addWidget(self.module_list)

        confirm_button = QPushButton("\U0001F44D Confirm Selection")
        confirm_button.setFont(QFont("Arial", 14))
        confirm_button.setStyleSheet(
            "padding: 15px; background-color: #007bff; color: white; border-radius: 5px;"
        )
        confirm_button.clicked.connect(self.save_modules)
        layout.addWidget(confirm_button)

        back_button = QPushButton("\u2B05 Back")
        back_button.setFont(QFont("Arial", 14))
        back_button.setStyleSheet(
            "padding: 15px; background-color: #d9534f; color: white; border-radius: 5px;"
        )
        back_button.clicked.connect(self.reset_settings_ui)
        layout.addWidget(back_button)

        widget.setLayout(layout)
        self.settings_layout.addWidget(widget)

    def save_modules(self):
        selected_modules = []
        for index in range(self.module_list.count()):
            item = self.module_list.item(index)
            if item.checkState() == Qt.Checked:
                selected_modules.append(item.text())

        self.user_data["bots"][self.current_platform] = selected_modules
        self.show_summary()

    def show_summary(self):
        self.clear_layout(self.settings_layout)

        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("\u2728 Your Selections \u2728")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        summary_label = QLabel()
        summary_text = ""
        for platform, modules in self.user_data["bots"].items():
            summary_text += f"<b>{platform}:</b><br>"
            for module in modules:
                summary_text += f" - {module}<br>"
            summary_text += "<br>"
        summary_label.setText(summary_text)
        summary_label.setFont(QFont("Arial", 14))
        layout.addWidget(summary_label)

        finish_button = QPushButton("\U0001F680 Finish")
        finish_button.setFont(QFont("Arial", 16, QFont.Bold))
        finish_button.setStyleSheet(
            "padding: 20px; background-color: #28a745; color: white; border-radius: 10px;"
        )
        finish_button.clicked.connect(self.reset_settings_ui)
        layout.addWidget(finish_button)

        widget.setLayout(layout)
        self.settings_layout.addWidget(widget)

    def finalize_setup(self):
        try:
            self.user_data["info"]["name"] = self.name_input.text()
            self.user_data["info"]["email"] = self.email_input.text()
            self.user_data["info"]["role"] = self.role_input.currentText()

            bots_json = json.dumps(self.user_data["bots"])
            modules_json = json.dumps(self.user_data["modules"])

            self.cursor_settings.execute('''
                INSERT INTO users (name, email, role, bots, modules)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                self.user_data["info"]["name"],
                self.user_data["info"]["email"],
                self.user_data["info"]["role"],
                bots_json,
                modules_json
            ))
            self.conn_settings.commit()
            QMessageBox.information(self, "Success", "\U0001F389 Settings saved successfully!\U0001F389")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {e}")

    def load_instances(self):
        instances = []
        db_path = self.get_database_path('instances.db')

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS instances (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    user TEXT,
                    expire_date TEXT
                )
            """)

            cursor.execute("SELECT name, description, user, expire_date FROM instances")
            rows = cursor.fetchall()
            instances = [{"name": row[0], "description": row[1], "user": row[2], "expire_date": row[3]} for row in rows]

        except sqlite3.Error as e:
            QMessageBox.critical(self, "SQLite Error", f"Could not load instances: {e}")
        finally:
            if conn:
                conn.close()

        return instances

    def populate_table(self):
        self.table.setRowCount(len(self.instance_list))
        for row, instance in enumerate(self.instance_list):
            checkbox = QCheckBox()
            self.table.setCellWidget(row, 0, checkbox)
            self.table.setItem(row, 1, QTableWidgetItem(instance.get('name', '')))
            self.table.setItem(row, 2, QTableWidgetItem(instance.get('description', '')))
            self.table.setItem(row, 3, QTableWidgetItem(instance.get('user', '')))
            self.table.setItem(row, 4, QTableWidgetItem(instance.get('expire_date', '')))

            action_button = QPushButton("Actions")
            action_button.clicked.connect(lambda _, r=row: self.show_actions_menu(r))
            self.table.setCellWidget(row, 5, action_button)

    def show_actions_menu(self, row):
        menu = QMenu()
        edit_action = menu.addAction("Edit")
        delete_action = menu.addAction("Delete")

        action = menu.exec_(self.table.cellWidget(row, 5).mapToGlobal(self.table.cellWidget(row,5).rect().bottomLeft()))

        if action == edit_action:
            self.edit_instance(row)
        elif action == delete_action:
            self.delete_instance(row)

    def edit_instance(self, row):
        instance = self.instance_list[row]
        dialog = EditInstanceDialog(instance, self)

        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_instance_data()
            self.instance_list[row] = updated_data
            self.save_instances_to_db()
            self.populate_table()

    def delete_instance(self, row):
        instance_name = self.instance_list[row]['name']
        reply = QMessageBox.question(self, 'Delete Instance', f"Are you sure you want to delete the instance '{instance_name}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            del self.instance_list[row]
            self.save_instances_to_db()
            self.populate_table()

    def filter_table(self):
        filter_text = self.search_field.text().lower()
        filtered_instances = [inst for inst in self.instance_list if filter_text in inst['name'].lower()]
        self.table.setRowCount(len(filtered_instances))
        for row, instance in enumerate(filtered_instances):
            self.populate_table_row(row, instance)

    def populate_table_row(self, row, instance):
        checkbox = QCheckBox()
        self.table.setCellWidget(row, 0, checkbox)
        self.table.setItem(row, 1, QTableWidgetItem(instance.get('name', '')))
        self.table.setItem(row, 2, QTableWidgetItem(instance.get('description', '')))
        self.table.setItem(row, 3, QTableWidgetItem(instance.get('user', '')))
        self.table.setItem(row, 4, QTableWidgetItem(instance.get('expire_date', '')))

        action_button = QPushButton("Actions")
        action_button.clicked.connect(lambda _, r=row: self.show_actions_menu(r))
        self.table.setCellWidget(row, 5, action_button)

    def add_new_instance(self):
        # This is a placeholder for the external script execution
        QMessageBox.information(self, "Info", "Functionality to add a new instance via external script is not implemented in this refactored version.")

    def export_to_csv(self):
        try:
            output_path = os.path.join(os.getcwd(), 'instances.csv')
            with open(output_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Nom', 'Description', 'User', 'Expire Date'])
                for instance in self.instance_list:
                    writer.writerow([instance['name'], instance['description'], instance['user'], instance['expire_date']])
            QMessageBox.information(self, "Success", f"Instances exported to: {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "CSV Error", f"Error during export: {e}")

    def save_instances_to_db(self):
        db_path = self.get_database_path('instances.db')
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM instances") # Clear the table
            for instance in self.instance_list:
                cursor.execute("""
                    INSERT INTO instances (name, description, user, expire_date)
                    VALUES (?, ?, ?, ?)
                """, (instance['name'], instance['description'], instance['user'], instance['expire_date']))
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "SQLite Error", f"Could not save instances: {e}")
        finally:
            if conn:
                conn.close()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def reset_settings_ui(self):
        self.clear_layout(self.settings_layout)
        self.setup_settings_ui()
