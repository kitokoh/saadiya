import sqlite3
import csv
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
                             QHeaderView, QAbstractItemView, QLineEdit, QHBoxLayout, QCheckBox,
                             QMenu, QAction, QDialog, QFormLayout, QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import Qt  
from group_manager import GroupTable
# Import du header, footer et menu secondaire
from ui.header import HeaderSection  
from ui.footer import FooterSection  
from ui.secondry_menu import SecondaryMenu  
import subprocess  # Pour exécuter le script externe

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
        self.visible_columns = ['Select', 'Nom Instance', 'Description', 'User', 'Expire Date', 'Actions']

        layout = QVBoxLayout(self)

        # Ajouter le header
        header = HeaderSection(self)
        layout.addWidget(header)

        # Menu secondaire
        self.secondary_menu = SecondaryMenu(self)
        self.secondary_menu.menu_selected.connect(self.change_content)
        layout.addWidget(self.secondary_menu)

        # Disposition en haut pour le titre, la barre de recherche et les boutons
        top_layout = QHBoxLayout()
        instance_label = QLabel(self.tr("Liste des Instances:"), self)
        instance_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_layout.addWidget(instance_label)

        # Barre de recherche
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText(self.tr("Rechercher dans les instances..."))
        self.search_field.textChanged.connect(self.filter_table)
        self.search_field.setStyleSheet("padding: 5px; font-size: 14px;")
        top_layout.addWidget(self.search_field)

        # Boutons Ajouter Instance et Exporter CSV
        self.add_instance_button = self.create_button(self.tr('Ajouter Instance'), '#28a745', self.add_new_instance)
        self.export_button = self.create_button(self.tr('Exporter CSV'), '#17a2b8', self.export_to_csv)

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
        self.table.setStyleSheet(self.get_table_styles())
        layout.addWidget(self.table)

        # Charger les données dans le tableau
        self.populate_table()  

        # Ajouter le footer
        footer = FooterSection(self)
        layout.addWidget(footer)

    def create_button(self, text, color, handler):
        button = QPushButton(text, self)
        button.setStyleSheet(f"background-color: {color}; color: white; padding: 5px 10px;")
        button.clicked.connect(handler)
        return button

    def get_table_styles(self):
        return """
            QTableWidget { 
                font-size: 14px; 
            } 
            QHeaderView::section { 
                background-color: #007BFF; 
                color: white; 
                padding: 10px; 
            } 
        """

    def load_instances(self):
        try:
            conn = sqlite3.connect('resources/data/nova360.db')  # Remplacez par le chemin de votre base de données
            cursor = conn.cursor()
            cursor.execute(""" 
                    SELECT i.name, i.description, u.facebook_name, i.created_at
                    FROM instances i 
                    JOIN facebook_users u ON i.facebook_user_id = u.id 
                """)  # Modifiez selon votre table
            instances = cursor.fetchall()
            # Créer une liste de dictionnaires
            return [{"name": name, "description": description, "user": user, "expire_date": expire_date}
                    for name, description, user, expire_date in instances]
        except sqlite3.Error as e:
            QMessageBox.warning(self, self.tr("Erreur"), f"{self.tr('Erreur lors du chargement des instances :')} {e}")
            return []

    def populate_table(self):
        self.table.setRowCount(len(self.instance_list))  
        for row, instance in enumerate(self.instance_list):
            if isinstance(instance, dict):  
                # Case à cocher pour la sélection
                checkbox = QCheckBox()
                self.table.setCellWidget(row, 0, checkbox)

                # Remplir les colonnes
                self.fill_table_row(row, instance)

                # Bouton d'actions
                self.add_action_buttons(row)

    def fill_table_row(self, row, instance):
        self.table.setItem(row, 1, QTableWidgetItem(instance.get('name', '')))
        self.table.setItem(row, 2, QTableWidgetItem(instance.get('description', '')))
        self.table.setItem(row, 3, QTableWidgetItem(instance.get('user', '')))
        self.table.setItem(row, 4, QTableWidgetItem(instance.get('expire_date', '')))

    def add_action_buttons(self, row):
        action_button = QPushButton(self.tr('Actions'))
        action_menu = QMenu(self)

        update_license_action = QAction(self.tr('Mettre à jour la licence'), self)
        edit_action = QAction(self.tr('Éditer'), self)

        action_menu.addAction(update_license_action)
        action_menu.addAction(edit_action)
        action_button.setMenu(action_menu)
        self.table.setCellWidget(row, 5, action_button)

        # Connexion des actions
        update_license_action.triggered.connect(self.update_license)
        edit_action.triggered.connect(self.edit_instance)

    def filter_table(self):
        filter_text = self.search_field.text().lower()
        self.table.setRowCount(len(self.instance_list))  # Réinitialiser le tableau
        filtered_instances = [instance for instance in self.instance_list if filter_text in instance.get('name', '').lower()]

        for row, instance in enumerate(filtered_instances):
            self.fill_table_row(row, instance)

    def add_new_instance(self):
        # Exécuter le script fb_robot_install.py
        subprocess.Popen(['python', 'fb_robot_install.py'])  # Remplacez par le chemin correct
        QMessageBox.information(self, self.tr("Information"), self.tr("Le script d'ajout d'instance a été lancé."))

    def export_to_csv(self):
        try:
            with open('data/instances.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.tr('Nom'), self.tr('Description'), self.tr('User'), self.tr('Expire Date')])  # Écrire l'en-tête
                for instance in self.instance_list:
                    writer.writerow([instance['name'], instance['description'], instance['user'], instance['expire_date']])
            QMessageBox.information(self, self.tr("Succès"), self.tr("Les données ont été exportées avec succès au format CSV."))
        except Exception as e:
            QMessageBox.critical(self, self.tr("Erreur"), f"{self.tr('Erreur lors de lexportation :')} {e}")

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
