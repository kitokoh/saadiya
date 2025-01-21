import sqlite3
import os
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QAbstractItemView, QLineEdit, QHBoxLayout, QCheckBox, QMenu, QAction, QComboBox, QScrollBar, QFrame, QDialog, QFormLayout
import csv
import json
import os
from PyQt5.QtCore import Qt, QSize, pyqtSignal  # Ajout de pyqtSignal ici
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
                             QHeaderView, QAbstractItemView, QLineEdit, QHBoxLayout, QCheckBox,
                             QMenu, QAction, QComboBox, QScrollBar, QFrame, QDialog, QFormLayout)

from ui.footer import FooterSection  # Import du footer
from ui.header import HeaderSection  # Import du header
from ui.secondry_menu import SecondaryMenu  # Assurez-vous d'importer votre nouvelle classe
class GroupModel:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                link TEXT NOT NULL,
                remarks TEXT,
                category TEXT,
                description TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def load_groups(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM groups')
        groups = cursor.fetchall()
        conn.close()
        return [dict(zip(['id', 'name', 'link', 'remarks', 'category', 'description'], group)) for group in groups]

    def save_group(self, group):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO groups (name, link, remarks, category, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (group['name'], group['link'], group['remarks'], group['category'], group['description']))
        conn.commit()
        conn.close()

    def update_group(self, group):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE groups
            SET name = ?, link = ?, remarks = ?, category = ?, description = ?
            WHERE id = ?
        ''', (group['name'], group['link'], group['remarks'], group['category'], group['description'], group['id']))
        conn.commit()
        conn.close()

    def delete_group(self, group_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM groups WHERE id = ?', (group_id,))
        conn.commit()
        conn.close()
# Chemin vers la base de données SQLite
DB_PATH = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'groups.db')


class AddGroupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un groupe")
        self.setFixedSize(300, 200)
        
        layout = QFormLayout(self)
        
        self.name_input = QLineEdit(self)
        self.link_input = QLineEdit(self)
        self.remarks_input = QLineEdit(self)
        self.category_input = QLineEdit(self)
        self.description_input = QLineEdit(self)
        
        layout.addRow("Nom:", self.name_input)
        layout.addRow("Lien:", self.link_input)
        layout.addRow("Remarques:", self.remarks_input)
        layout.addRow("Catégorie:", self.category_input)
        layout.addRow("Description:", self.description_input)

        self.submit_button = QPushButton("Soumettre", self)
        self.submit_button.clicked.connect(self.add_group)
        layout.addWidget(self.submit_button)

    def add_group(self):
        new_group = {
            'name': self.name_input.text(),
            'link': self.link_input.text(),
            'remarks': self.remarks_input.text(),
            'category': self.category_input.text(),
            'description': self.description_input.text()
        }
        save_group(new_group)
        self.accept()

class GroupTable(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.group_list = self.model.load_groups()
        self.visible_columns = ['Select', 'Name', 'Link', 'Remarks', 'Category', 'Description', 'Actions']
        self.items_per_page = 25
        self.current_page = 1

        layout = QVBoxLayout(self)

        # Ajouter le header
        header = HeaderSection(self, title="FBK GRUP MANAGEMENT", app_name="Nova360 AI", slogan="AI Marketing Automation Solution")
        layout.addWidget(header)

        # Disposition en haut pour le titre, la barre de recherche et les boutons
        top_layout = QHBoxLayout()

        # Menu secondaire
        self.secondary_menu = SecondaryMenu(self)
        self.secondary_menu.menu_selected.connect(self.change_content)
        layout.addWidget(self.secondary_menu)

        # Titre
        group_label = QLabel("Liste des groupes:", self)
        group_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_layout.addWidget(group_label)

        # Barre de recherche
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Rechercher dans les groupes...")
        self.search_field.textChanged.connect(self.filter_table)
        self.search_field.setStyleSheet("padding: 5px; font-size: 14px;")
        top_layout.addWidget(self.search_field)

        # Boutons Import, Export, Ajouter Group
        self.import_button = QPushButton('Import Group', self)
        self.import_button.setStyleSheet("background-color: #6c757d; color: white; padding: 5px 10px;")
        self.import_button.clicked.connect(self.import_groups)
        top_layout.addWidget(self.import_button)

        self.export_button = QPushButton('Export', self)
        self.export_button.setStyleSheet("background-color: #007bff; color: white; padding: 5px 10px;")
        self.export_button.clicked.connect(self.export_groups)
        top_layout.addWidget(self.export_button)

        self.add_group_button = QPushButton('+ 1 Group', self)
        self.add_group_button.setStyleSheet("background-color: #28a745; color: white; padding: 5px 10px;")
        self.add_group_button.clicked.connect(self.open_add_group_dialog)
        top_layout.addWidget(self.add_group_button)

        layout.addLayout(top_layout)

        # Tableau de groupes
        self.table = QTableWidget(self)
        self.table.setColumnCount(len(self.visible_columns))
        self.table.setHorizontalHeaderLabels(self.visible_columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setStyleSheet(""" 
            QTableWidget { 
                font-size: 14px; 
            } 
            QHeaderView::section { 
                background-color: #007BFF; 
                color: white; 
                padding: 10px; 
            } 
        """)
        layout.addWidget(self.table)

        # Cases à cocher pour masquer/afficher les colonnes
        self.checkboxes_layout = QHBoxLayout()
        for index, col_name in enumerate(self.visible_columns):
            checkbox = QCheckBox(col_name)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self.update_visible_columns)
            self.checkboxes_layout.addWidget(checkbox)
        layout.addLayout(self.checkboxes_layout)

        # Pagination
        self.pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Précédent")
        self.prev_button.clicked.connect(self.previous_page)
        self.next_button = QPushButton("Suivant")
        self.next_button.clicked.connect(self.next_page)

        self.pagination_label = QLabel(f"Page {self.current_page}")
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.pagination_label)
        self.pagination_layout.addWidget(self.next_button)
        layout.addLayout(self.pagination_layout)

        # Charger les données dans le tableau
        self.populate_table()
        # Ajouter le footer
        footer = FooterSection(self)
        layout.addWidget(footer)

    def populate_table(self):
        self.table.setRowCount(len(self.group_list))
        self.update_table()

    def update_table(self):
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        visible_groups = self.group_list[start_index:end_index]

        self.table.setRowCount(len(visible_groups))

        for row, group in enumerate(visible_groups):
            checkbox = QCheckBox()
            self.table.setCellWidget(row, 0, checkbox)

            self.table.setItem(row, 1, QTableWidgetItem(group.get('name', '')))
            self.table.setItem(row, 2, QTableWidgetItem(group.get('link', '')))
            self.table.setItem(row, 3, QTableWidgetItem(group.get('remarks', '')))
            self.table.setItem(row, 4, QTableWidgetItem(group.get('category', '')))
            self.table.setItem(row, 5, QTableWidgetItem(group.get('description', '')))

            action_button = QPushButton('Actions')
            action_menu = QMenu(self)
            edit_action = QAction('Edit', self)
            delete_action = QAction('Delete', self)
            edit_action.triggered.connect(lambda _, r=row: self.edit_group(r))
            delete_action.triggered.connect(lambda _, r=row: self.delete_group(r))
            action_menu.addAction(edit_action)
            action_menu.addAction(delete_action)
            action_button.setMenu(action_menu)
            self.table.setCellWidget(row, 6, action_button)

        self.pagination_label.setText(f"Page {self.current_page}")

    def import_groups(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Importer des groupes", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.model.save_group(row)
                    self.group_list = self.model.load_groups()
                    self.populate_table()
            except Exception as e:
                print(f"Erreur lors de l'importation: {e}")

    def export_groups(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Exporter des groupes", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.group_list[0].keys())
                    writer.writeheader()
                    writer.writerows(self.group_list)
                    print("Exportation réussie.")
            except Exception as e:
                print(f"Erreur lors de l'exportation: {e}")

    def open_add_group_dialog(self):
        dialog = AddGroupDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.group_list = self.model.load_groups()
            self.populate_table()

    def edit_group(self, row):
        group = self.group_list[row]
        dialog = AddGroupDialog(self)
        dialog.name_input.setText(group.get('name', ''))
        dialog.link_input.setText(group.get('link', ''))
        dialog.remarks_input.setText(group.get('remarks', ''))
        dialog.category_input.setText(group.get('category', ''))
        dialog.description_input.setText(group.get('description', ''))

        if dialog.exec_() == QDialog.Accepted:
            updated_group = {
                'id': group['id'],
                'name': dialog.name_input.text(),
                'link': dialog.link_input.text(),
                'remarks': dialog.remarks_input.text(),
                'category': dialog.category_input.text(),
                'description': dialog.description_input.text()
            }
            self.model.update_group(updated_group)
            self.group_list = self.model.load_groups()
            self.populate_table()

    def delete_group(self, row):
        group = self.group_list[row]
        self.model.delete_group(group['id'])
        self.group_list = self.model.load_groups()
        self.populate_table()

    def filter_table(self):
        search_text = self.search_field.text().lower()
        filtered_groups = [group for group in self.group_list if search_text in group.get('name', '').lower()]
        self.group_list = filtered_groups
        self.populate_table()

    def next_page(self):
        if (self.current_page * self.items_per_page) < len(self.group_list):
            self.current_page += 1
            self.populate_table()

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_table()

    def update_visible_columns(self):
        checkboxes = self.checkboxes_layout.children()
        for i, checkbox in enumerate(checkboxes):
            self.table.setColumnHidden(i, not checkbox.isChecked())
        for i in range(self.table.columnCount()):
            self.table.horizontalHeader().setVisible(True)

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    DB_PATH = os.path.join(os.getenv('APPDATA'), 'saadiya', 'resources', 'groups.db')
    model = GroupModel(DB_PATH)
    app = QApplication(sys.argv)
    window = GroupTable(model)
    window.show()
    sys.exit(app.exec_())