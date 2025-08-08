import os
import csv
import sqlite3
import subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView, QAbstractItemView, QLineEdit, QHBoxLayout, QCheckBox,
    QMenu, QAction, QDialog, QFormLayout, QDialogButtonBox, QMessageBox
)

class EditInstanceDialog(QDialog):
    def __init__(self, instance, parent=None):
        super().__init__(parent)
        self.instance = instance
        self.setWindowTitle(self.tr("Éditer Instance"))
        self.layout = QFormLayout(self)

        self.name_field = QLineEdit(instance['name'])
        self.description_field = QLineEdit(instance['description'])
        self.user_field = QLineEdit(instance['user'])
        self.expire_date_field = QLineEdit(instance['expire_date'])

        self.layout.addRow(self.tr("Nom :"), self.name_field)
        self.layout.addRow(self.tr("Description :"), self.description_field)
        self.layout.addRow(self.tr("Utilisateur :"), self.user_field)
        self.layout.addRow(self.tr("Date d'expiration :"), self.expire_date_field)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def get_instance_data(self):
        return {
            "name": self.name_field.text(),
            "description": self.description_field.text(),
            "user": self.user_field.text(),
            "expire_date": self.expire_date_field.text()
        }


class InstancesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.instance_list = self.load_instances()
        self.visible_columns = ['Select', 'Nam Instance', 'Description', 'User', 'Expire Date', 'Actions']

        layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        instance_label = QLabel("Liste des Instances :", self)
        top_layout.addWidget(instance_label)

        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Rechercher dans les instances...")
        self.search_field.textChanged.connect(self.filter_table)
        top_layout.addWidget(self.search_field)

        self.add_instance_button = self.create_button(' Instance', '#28a745', self.add_new_instance)
        self.export_button = self.create_button('Exporter CSV', '#17a2b8', self.export_to_csv)
        top_layout.addWidget(self.add_instance_button)
        top_layout.addWidget(self.export_button)
        layout.addLayout(top_layout)

        self.table = QTableWidget(self)
        self.table.setColumnCount(len(self.visible_columns))
        self.table.setHorizontalHeaderLabels(self.visible_columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.table)

        self.populate_table()

    def create_button(self, text, color, handler):
        button = QPushButton(text, self)
        button.setStyleSheet(f"background-color: {color}; color: white; padding: 5px 10px;")
        button.clicked.connect(handler)
        return button

    def load_instances(self):
        instances = []
        db_path = 'nova360.db'
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS facebook_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    facebook_name TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS instances (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    facebook_user_id INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (facebook_user_id) REFERENCES facebook_users(id)
                )
            """)

            cursor.execute("""
                SELECT i.name, i.description, u.facebook_name, i.created_at
                FROM instances i
                LEFT JOIN facebook_users u ON i.facebook_user_id = u.id
            """)
            rows = cursor.fetchall()
            instances = [{"name": row[0], "description": row[1], "user": row[2], "expire_date": row[3]} for row in rows]

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur SQLite", f"Impossible de charger les instances ou de créer la base de données : {e}")
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
            self.table.setCellWidget(row, 5, action_button)

    def export_to_csv(self):
        try:
            output_path = os.path.join(os.getcwd(), 'instances.csv')
            with open(output_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Nom', 'Description', 'User', 'Expire Date'])
                for instance in self.instance_list:
                    writer.writerow([instance['name'], instance['description'], instance['user'], instance['expire_date']])
            QMessageBox.information(self, "Succès", f"Instances exportées avec succès dans : {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur CSV", f"Erreur lors de l'exportation : {e}")

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

    def add_new_instance(self):
        subprocess.Popen(['python', 'fb_robot_install.py'])
        QMessageBox.information(self, "Info", "Script d'ajout d'instance lancé.")

    def update_license(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, self.tr("Avertissement"), self.tr("Veuillez sélectionner une instance à mettre à jour."))
            return

        row = selected_rows[0].row()
        instance = self.instance_list[row]
        dialog = EditInstanceDialog(instance, self)

        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_instance_data()
            self.instance_list[row] = updated_data
            self.populate_table()

    def edit_instance(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, self.tr("Avertissement"), self.tr("Veuillez sélectionner une instance à éditer."))
            return

        row = selected_rows[0].row()
        instance = self.instance_list[row]
        dialog = EditInstanceDialog(instance, self)

        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_instance_data()
            self.instance_list[row] = updated_data
            self.populate_table()
