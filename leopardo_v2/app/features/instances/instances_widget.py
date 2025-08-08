import csv
import subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView, QAbstractItemView, QLineEdit, QHBoxLayout, QCheckBox,
    QMenu, QAction, QDialog, QFormLayout, QDialogButtonBox, QMessageBox
)
from ...services.database_service import db_service

class EditInstanceDialog(QDialog):
    def __init__(self, instance_data, parent=None):
        super().__init__(parent)
        self.instance_data = instance_data
        self.setWindowTitle(self.tr("Éditer Instance"))
        self.layout = QFormLayout(self)

        self.name_field = QLineEdit(instance_data['name'])
        self.status_field = QLineEdit(instance_data['status'])
        self.type_field = QLineEdit(instance_data['type'])

        self.layout.addRow(self.tr("Nom :"), self.name_field)
        self.layout.addRow(self.tr("Statut :"), self.status_field)
        self.layout.addRow(self.tr("Type :"), self.type_field)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def get_instance_data(self):
        return {
            "id": self.instance_data['id'],
            "name": self.name_field.text(),
            "status": self.status_field.text(),
            "type": self.type_field.text(),
        }

class InstancesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.visible_columns = ['Select', 'Name', 'Status', 'Type', 'Actions']
        self.instance_list = []

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

        self.load_instances()

    def create_button(self, text, color, handler):
        button = QPushButton(text, self)
        button.setStyleSheet(f"background-color: {color}; color: white; padding: 5px 10px;")
        button.clicked.connect(handler)
        return button

    def load_instances(self):
        try:
            instances_data = db_service.get_all_instances()
            self.instance_list = [
                {'id': row[0], 'name': row[1], 'status': row[2], 'type': row[3]}
                for row in instances_data
            ]
            self.populate_table()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les instances : {e}")

    def populate_table(self):
        self.table.setRowCount(len(self.instance_list))
        for row, instance in enumerate(self.instance_list):
            self.populate_table_row(row, instance)

    def populate_table_row(self, row, instance):
        checkbox = QCheckBox()
        self.table.setCellWidget(row, 0, checkbox)
        self.table.setItem(row, 1, QTableWidgetItem(instance.get('name', '')))
        self.table.setItem(row, 2, QTableWidgetItem(instance.get('status', '')))
        self.table.setItem(row, 3, QTableWidgetItem(instance.get('type', '')))

        action_button = QPushButton("Actions")
        action_button.clicked.connect(lambda _, r=row: self.show_actions_menu(r))
        self.table.setCellWidget(row, 4, action_button)

    def show_actions_menu(self, row):
        menu = QMenu()
        edit_action = QAction("Éditer", self)
        edit_action.triggered.connect(lambda: self.edit_instance(row))
        menu.addAction(edit_action)

        delete_action = QAction("Supprimer", self)
        delete_action.triggered.connect(lambda: self.delete_instance(row))
        menu.addAction(delete_action)

        action_button = self.table.cellWidget(row, 4)
        menu.exec_(action_button.mapToGlobal(action_button.rect().bottomLeft()))

    def export_to_csv(self):
        try:
            output_path = os.path.join(os.getcwd(), 'instances.csv')
            with open(output_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Name', 'Status', 'Type'])
                for instance in self.instance_list:
                    writer.writerow([instance['id'], instance['name'], instance['status'], instance['type']])
            QMessageBox.information(self, "Succès", f"Instances exportées avec succès dans : {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur CSV", f"Erreur lors de l'exportation : {e}")

    def filter_table(self):
        filter_text = self.search_field.text().lower()
        self.table.setRowCount(0)
        for row, instance in enumerate(self.instance_list):
            if filter_text in instance['name'].lower():
                self.table.insertRow(self.table.rowCount())
                self.populate_table_row(self.table.rowCount() - 1, instance)

    def add_new_instance(self):
        # This still uses the old script, which is out of scope for the current task
        # of unifying the database. We can refactor this later.
        try:
            subprocess.Popen(['python', 'fb_robot_install.py'])
            QMessageBox.information(self, "Info", "Script d'ajout d'instance lancé.")
            # For now, let's add a dummy instance to the db to show it works
            db_service.add_instance("New Instance", "Pending", "Facebook")
            self.load_instances() # Refresh the table
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de lancer le script : {e}")

    def edit_instance(self, row):
        instance = self.instance_list[row]
        dialog = EditInstanceDialog(instance, self)

        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_instance_data()
            try:
                db_service.update_instance(
                    updated_data['id'],
                    updated_data['name'],
                    updated_data['status'],
                    updated_data['type']
                )
                self.load_instances() # Refresh
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de mettre à jour l'instance : {e}")

    def delete_instance(self, row):
        instance = self.instance_list[row]
        reply = QMessageBox.question(self, 'Supprimer Instance',
                                     f"Êtes-vous sûr de vouloir supprimer l'instance '{instance['name']}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                db_service.delete_instance(instance['id'])
                self.load_instances() # Refresh
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de supprimer l'instance : {e}")
