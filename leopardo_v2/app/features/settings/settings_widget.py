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
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QDialog, QMenu
)

from app.components.dialogs.edit_instance_dialog import EditInstanceDialog

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
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.role_input = QComboBox()
        self.role_input.addItems(["Admin", "User", "Guest"])

        user_form.addRow("Name:", self.name_input)
        user_form.addRow("Email:", self.email_input)
        user_form.addRow("Role:", self.role_input)
        self.settings_layout.addLayout(user_form)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        self.platforms_layout = QVBoxLayout()
        content_widget.setLayout(self.platforms_layout)
        scroll_area.setWidget(content_widget)
        self.settings_layout.addWidget(scroll_area)

        finalize_button = QPushButton("\U0001F680 Finalize Configuration")
        finalize_button.setFont(QFont("Arial", 16, QFont.Bold))
        finalize_button.setStyleSheet(
            "padding: 20px; background-color: #28a745; color: white; border-radius: 10px;"
            "hover { background-color: #218838; }"
        )
        self.settings_layout.addWidget(finalize_button)

    def setup_instances_ui(self):
        # This code is adapted from the InstanceTable class
        self.visible_columns = ['Select', 'Nam Instance', 'Description', 'User', 'Expire Date', 'Actions']

        top_layout = QHBoxLayout()
        instance_label = QLabel("Liste des Instances :", self)
        top_layout.addWidget(instance_label)

        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Rechercher dans les instances...")
        top_layout.addWidget(self.search_field)

        self.add_instance_button = QPushButton('Ajouter Instance')
        self.add_instance_button.setStyleSheet("background-color: #28a745; color: white; padding: 5px 10px;")
        top_layout.addWidget(self.add_instance_button)

        self.export_button = QPushButton('Exporter CSV')
        self.export_button.setStyleSheet("background-color: #17a2b8; color: white; padding: 5px 10px;")
        top_layout.addWidget(self.export_button)

        self.instances_layout.addLayout(top_layout)

        self.table = QTableWidget(self)
        self.table.setColumnCount(len(self.visible_columns))
        self.table.setHorizontalHeaderLabels(self.visible_columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.instances_layout.addWidget(self.table)

    def display_platforms(self, platforms):
        for platform in platforms:
            button = QPushButton(f"\u25B6 {platform}")
            button.setFont(QFont("Arial", 14))
            button.setStyleSheet(
                "padding: 15px; margin: 10px; background-color: #f0f0f0; border: 2px solid #007bff; border-radius: 10px;"
            )
            self.platforms_layout.addWidget(button)

    def display_instances(self, instances):
        self.table.setRowCount(len(instances))
        for row, instance in enumerate(instances):
            checkbox = QCheckBox()
            self.table.setCellWidget(row, 0, checkbox)
            self.table.setItem(row, 1, QTableWidgetItem(instance.get('name', '')))
            self.table.setItem(row, 2, QTableWidgetItem(instance.get('description', '')))
            self.table.setItem(row, 3, QTableWidgetItem(instance.get('user', '')))
            self.table.setItem(row, 4, QTableWidgetItem(instance.get('expire_date', '')))

            action_button = QPushButton("Actions")
            self.table.setCellWidget(row, 5, action_button)

    def show_edit_instance_dialog(self, instance):
        dialog = EditInstanceDialog(instance, self)
        if dialog.exec_() == QDialog.Accepted:
            return dialog.get_instance_data()
        return None
