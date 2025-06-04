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
from ui.footer import FooterSection
from ui.header import HeaderSection
from ui.secondry_menu import SecondaryMenu

import sqlite3
import subprocess  # Pour exécuter le script externe
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
                             QHeaderView, QAbstractItemView, QLineEdit, QHBoxLayout, QCheckBox,
                             QMenu, QAction, QDialog, QFormLayout, QDialogButtonBox, QMessageBox)

from ModulesUI.tiktok.group_manager import GroupTable
from ui.footer import FooterSection
# Import du header, footer et menu secondaire
from ui.header import HeaderSection
from ui.secondry_menu import SecondaryMenu
import os

class EditInstanceDialog(QDialog):
    def __init__(self, instance, parent=None):
        super().__init__(parent)
        self.instance = instance
        self.setWindowTitle(self.tr("Éditer Instance"))
        self.layout = QFormLayout(self)

        # Champs d'édition
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


class InstanceTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.instance_list = self.load_instances()  # Charger les instances depuis SQLite
        self.visible_columns = ['Select', 'Nam Instance', 'Description', 'User', 'Expire Date', 'Actions']

        # Configuration générale de l'interface
        layout = QVBoxLayout(self)

        # Ajouter le header
        header = HeaderSection(self)
        layout.addWidget(header)

        # Menu secondaire
        self.secondary_menu = SecondaryMenu(self)
        layout.addWidget(self.secondary_menu)

        # Barre de recherche et boutons en haut
        top_layout = QHBoxLayout()
        instance_label = QLabel("Liste des Instances :", self)
        top_layout.addWidget(instance_label)

        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Rechercher dans les instances...")
        self.search_field.textChanged.connect(self.filter_table)
        top_layout.addWidget(self.search_field)

        # Boutons "Ajouter" et "Exporter CSV"
        self.add_instance_button = self.create_button(' Instance', '#28a745', self.add_new_instance)
        self.export_button = self.create_button('Exporter CSV', '#17a2b8', self.export_to_csv)
        top_layout.addWidget(self.add_instance_button)
        top_layout.addWidget(self.export_button)
        layout.addLayout(top_layout)

        # Tableau d'instances
        self.table = QTableWidget(self)
        self.table.setColumnCount(len(self.visible_columns))
        self.table.setHorizontalHeaderLabels(self.visible_columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.table)

        # Ajouter le footer
        footer = FooterSection(self)
        layout.addWidget(footer)

        self.populate_table()

    def create_button(self, text, color, handler):
        button = QPushButton(text, self)
        button.setStyleSheet(f"background-color: {color}; color: white; padding: 5px 10px;")
        button.clicked.connect(handler)
        return button

    def load_instances(self):
        """Charge les données des instances depuis SQLite, ou crée la base de données si elle est introuvable."""
        instances = []
        roaming_path = os.path.expandvars(r'%APPDATA%')
        from imports import DB_PATH_instances
        # db_path = os.path.join(roaming_path, 'saadiya', 'resources', 'data', 'nova360.db')
        db_path = DB_PATH_instances
        # Vérifie si le dossier et le fichier de la base de données existent
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Connecte ou crée la base de données
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Crée les tables si elles n'existent pas
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

            # Charge les données des instances
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
        """Remplit le tableau avec les données des instances."""
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
        """Exporte les instances vers un fichier CSV."""
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
        """Filtre les lignes du tableau en fonction de la recherche."""
        filter_text = self.search_field.text().lower()
        filtered_instances = [inst for inst in self.instance_list if filter_text in inst['name'].lower()]
        self.table.setRowCount(len(filtered_instances))
        for row, instance in enumerate(filtered_instances):
            self.populate_table_row(row, instance)

    def populate_table_row(self, row, instance):
        """Remplit une ligne du tableau avec les données d'une instance."""
        checkbox = QCheckBox()
        self.table.setCellWidget(row, 0, checkbox)
        self.table.setItem(row, 1, QTableWidgetItem(instance.get('name', '')))
        self.table.setItem(row, 2, QTableWidgetItem(instance.get('description', '')))
        self.table.setItem(row, 3, QTableWidgetItem(instance.get('user', '')))
        self.table.setItem(row, 4, QTableWidgetItem(instance.get('expire_date', '')))

    def add_new_instance(self):
        """Ajoute une nouvelle instance (via un script externe)."""
        subprocess.Popen(['python', 'fb_robot_install.py'])
        QMessageBox.information(self, "Info", "Script d'ajout d'instance lancé.")



    def update_license(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, self.tr("Avertissement"), self.tr("Veuillez sélectionner une instance à mettre à jour."))
            return

        # On suppose que vous ne voulez mettre à jour qu'une seule instance à la fois
        row = selected_rows[0].row()  # Récupérer l'index de la première ligne sélectionnée
        instance = self.instance_list[row]
        dialog = EditInstanceDialog(instance, self)
        
        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_instance_data()
            self.instance_list[row] = updated_data  # Mettre à jour l'instance dans la liste
            self.populate_table()  # Recharger le tableau

    def edit_instance(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, self.tr("Avertissement"), self.tr("Veuillez sélectionner une instance à éditer."))
            return

        row = selected_rows[0].row()  # Récupérer l'index de la première ligne sélectionnée
        instance = self.instance_list[row]
        dialog = EditInstanceDialog(instance, self)

        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_instance_data()
            self.instance_list[row] = updated_data  # Mettre à jour l'instance dans la liste
            self.populate_table()  # Recharger le tableau

    def change_content(self, selected_menu):
        # Logique pour changer le contenu en fonction du menu sélectionné
        pass


    def save_instances(self):
        # Ne pas nécessaire car les données viennent de la base de données
        pass







    def contact_support(self):
        # Implémenter une fonction pour contacter le support
        print("Contacter le support...")


    def display_media(self):
        # Code pour afficher la liste des médias
        print("Affichage de la liste des médias...")

    def display_groups(self):
        # Code pour afficher la liste des groupes
        #self.setCentralWidget(GroupTable(self))  # Affiche la table des groupes

        print("Affichage de la liste des groupes...")

# N'oubliez pas d'importer QApplication et d'initialiser votre application
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = InstanceTable()
    window.show()
    sys.exit(app.exec_())
