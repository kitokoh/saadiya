import json
import csv
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, 
                             QHeaderView, QAbstractItemView, QLineEdit, QHBoxLayout, QCheckBox, 
                             QMenu, QAction, QComboBox, QScrollBar, QFrame)
from PyQt5.QtCore import Qt, QSize, pyqtSignal  # Ajout de pyqtSignal ici
from ui.header import HeaderSection  # Import du header
from ui.footer import FooterSection  # Import du footer
from ui.secondry_menu import SecondaryMenu  # Assurez-vous d'importer votre nouvelle classe

class GroupTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.group_list = self.load_groups()  # Charger les groupes
        self.visible_columns = [self.tr('Select'), self.tr('Name'), self.tr('Link'), self.tr('Remarks'), 
                                self.tr('Category'), self.tr('Description'), self.tr('Actions')]
        self.items_per_page = 5
        self.current_page = 1

        layout = QVBoxLayout(self)

        # Ajouter le header
        header = HeaderSection(self)
        layout.addWidget(header)

        # Disposition en haut pour le titre, la barre de recherche et les boutons
        top_layout = QHBoxLayout()

        # Menu secondaire
        self.secondary_menu = SecondaryMenu(self)
        self.secondary_menu.menu_selected.connect(self.change_content)
        layout.addWidget(self.secondary_menu)

        # Titre
        group_label = QLabel(self.tr("Liste des groupes:"), self)
        group_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_layout.addWidget(group_label)

        # Barre de recherche
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText(self.tr("Rechercher dans les groupes..."))
        self.search_field.textChanged.connect(self.filter_table)
        self.search_field.setStyleSheet("padding: 5px; font-size: 14px;")
        top_layout.addWidget(self.search_field)

        # Boutons Import, Export, Ajouter Group
        self.import_button = QPushButton(self.tr('Import Group'), self)
        self.import_button.setStyleSheet("background-color: #6c757d; color: white; padding: 5px 10px;")
        self.import_button.clicked.connect(self.import_groups)
        top_layout.addWidget(self.import_button)

        self.export_button = QPushButton(self.tr('Export'), self)
        self.export_button.setStyleSheet("background-color: #007bff; color: white; padding: 5px 10px;")
        self.export_button.clicked.connect(self.export_groups)
        top_layout.addWidget(self.export_button)

        self.add_group_button = QPushButton(self.tr('+ 1 Group'), self)
        self.add_group_button.setStyleSheet("background-color: #28a745; color: white; padding: 5px 10px;")
        self.add_group_button.clicked.connect(self.add_new_group)
        top_layout.addWidget(self.add_group_button)

        layout.addLayout(top_layout)

        # Tableau de groupes
        self.table = QTableWidget(self)
        self.table.setColumnCount(len(self.visible_columns))  # Nombre de colonnes basé sur les colonnes visibles
        self.table.setHorizontalHeaderLabels(self.visible_columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Réduire la taille de "Select"
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
            checkbox.setChecked(True)  # Par défaut, toutes les colonnes sont visibles
            checkbox.stateChanged.connect(self.update_visible_columns)
            self.checkboxes_layout.addWidget(checkbox)
        layout.addLayout(self.checkboxes_layout)

        # Pagination
        self.pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton(self.tr("Précédent"))
        self.prev_button.clicked.connect(self.previous_page)
        self.next_button = QPushButton(self.tr("Suivant"))
        self.next_button.clicked.connect(self.next_page)

        self.pagination_label = QLabel(f"{self.tr('Page')} {self.current_page}")
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.pagination_label)
        self.pagination_layout.addWidget(self.next_button)
        layout.addLayout(self.pagination_layout)

        # Charger les données dans le tableau
        self.populate_table()  # Appel à la méthode pour remplir le tableau
        # Ajouter le footer
        footer = FooterSection(self)
        layout.addWidget(footer)

    def load_groups(self):
        try:
            with open('resources/data/groups.json', 'r') as f:
                data = json.load(f)
                return data.get("groups", [])  # Retourne la liste des groupes
        except (FileNotFoundError, json.JSONDecodeError):
            print("Erreur lors du chargement du fichier 'groups.json'.")
            return []

    def populate_table(self):
        self.table.setRowCount(len(self.group_list))  # Fixer le nombre de lignes
        self.update_table()

    def update_table(self):
        # Calculer l'index de début et de fin pour la pagination
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        visible_groups = self.group_list[start_index:end_index]

        self.table.setRowCount(len(visible_groups))  # Fixer le nombre de lignes affichées

        for row, group in enumerate(visible_groups):
            if isinstance(group, dict):  # Vérifier que c'est bien un dictionnaire
                # Case à cocher pour la sélection
                checkbox = QCheckBox()
                self.table.setCellWidget(row, 0, checkbox)

                # Remplir les colonnes
                self.table.setItem(row, 1, QTableWidgetItem(group.get('name', '')))
                self.table.setItem(row, 2, QTableWidgetItem(group.get('link', '')))
                self.table.setItem(row, 3, QTableWidgetItem(group.get('remarks', '')))
                self.table.setItem(row, 4, QTableWidgetItem(group.get('category', '')))
                self.table.setItem(row, 5, QTableWidgetItem(group.get('description', '')))

                # Bouton d'actions (Éditer/Supprimer)
                action_button = QPushButton(self.tr('Actions'))
                action_menu = QMenu(self)
                edit_action = QAction(self.tr('Edit'), self)
                delete_action = QAction(self.tr('Delete'), self)
                action_menu.addAction(edit_action)
                action_menu.addAction(delete_action)
                action_button.setMenu(action_menu)
                self.table.setCellWidget(row, 6, action_button)
            else:
                print(f"Warning: The group at row {row} is not a dictionary. Skipping...")

        # Mettre à jour l'affichage de la pagination
        self.pagination_label.setText(f"{self.tr('Page')} {self.current_page}")
    def import_groups(self):
        try:
            with open('resources/data/groups.json', 'r') as f:
                data = json.load(f)
                self.group_list = data.get("groups", [])  # Charger la liste des groupes
                self.populate_table()  # Actualiser la table
        except FileNotFoundError:
            print(self.tr("Le fichier groupes.json est introuvable."))

    def export_groups(self):
        try:
            with open('data/exported_groups.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([self.tr('Name'), self.tr('Link'), self.tr('Remarks'), self.tr('Category'), self.tr('Description')])

                for row in range(self.table.rowCount()):
                    name = self.table.item(row, 1).text()
                    link = self.table.item(row, 2).text()
                    remarks = self.table.item(row, 3).text()
                    category = self.table.item(row, 4).text()
                    description = self.table.item(row, 5).text()
                    writer.writerow([name, link, remarks, category, description])

            print(self.tr("Groupes exportés avec succès."))
        except Exception as e:
            print(self.tr(f"Erreur lors de l'exportation des groupes: {e}"))

    def change_content(self, menu_name):
        if menu_name == "media":
            self.populate_table()  # Affiche la table des médias
        elif menu_name == "groups":
            # Ajoutez le code pour afficher les groupes
            pass
        elif menu_name == "instances":
            # Ajoutez le code pour afficher les instances
            pass

    def add_new_group(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        checkbox = QCheckBox()
        self.table.setCellWidget(row_position, 0, checkbox)

        for col in range(1, 6):
            self.table.setItem(row_position, col, QTableWidgetItem(""))

        action_button = QPushButton(self.tr('Actions'))
        action_menu = QMenu(self)
        edit_action = QAction(self.tr('Edit'), self)
        delete_action = QAction(self.tr('Delete'), self)
        action_menu.addAction(edit_action)
        action_menu.addAction(delete_action)
        action_button.setMenu(action_menu)
        self.table.setCellWidget(row_position, 6, action_button)

    def filter_table(self):
        filter_text = self.search_field.text().lower()
        filtered_groups = [group for group in self.group_list if filter_text in group.get('name', '').lower()]
        self.table.setRowCount(len(filtered_groups))  # Fixer le nombre de lignes
        for row, group in enumerate(filtered_groups):
            self.table.setItem(row, 1, QTableWidgetItem(group.get('name', '')))
            self.table.setItem(row, 2, QTableWidgetItem(group.get('link', '')))
            self.table.setItem(row, 3, QTableWidgetItem(group.get('remarks', '')))
            self.table.setItem(row, 4, QTableWidgetItem(group.get('category', '')))
            self.table.setItem(row, 5, QTableWidgetItem(group.get('description', '')))

    def import_dynamic_groups(self):
        try:
            with open('f.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    name, link, remarks, category, description = line.strip().split(',')
                    new_group = {
                        'name': name,
                        'link': link,
                        'remarks': remarks,
                        'category': category,
                        'description': description
                    }
                    self.group_list.append(new_group)
                self.populate_table()
        except Exception as e:
            print(self.tr(f"Erreur lors de l'importation dynamique des groupes: {e}"))

    def update_visible_columns(self):
        checkboxes = self.checkboxes_layout.children()
        for i, checkbox in enumerate(checkboxes):
            # Masquer ou afficher la colonne selon l'état de la case à cocher
            self.table.setColumnHidden(i, not checkbox.isChecked())
            
        # Mettre à jour l'affichage des en-têtes
        for i in range(self.table.columnCount()):
            self.table.horizontalHeader().setVisible(True)  # Toujours afficher les en-têtes    

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_table()

    def next_page(self):
        if self.current_page * self.items_per_page < len(self.group_list):
            self.current_page += 1
            self.update_table()

class HeaderSection1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.label = QLabel(self.tr("Header Section"), self)
        layout.addWidget(self.label)

class FooterSection1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.label = QLabel(self.tr("Footer Section"), self)
        layout.addWidget(self.label)

class SecondaryMenu1(QWidget):
    menu_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.media_button = QPushButton(self.tr("Media"), self)
        self.media_button.clicked.connect(lambda: self.menu_selected.emit("media"))
        layout.addWidget(self.media_button)

        self.groups_button = QPushButton(self.tr("Groups"), self)
        self.groups_button.clicked.connect(lambda: self.menu_selected.emit("groups"))
        layout.addWidget(self.groups_button)

        self.instances_button = QPushButton(self.tr("Instances"), self)
        self.instances_button.clicked.connect(lambda: self.menu_selected.emit("instances"))
        layout.addWidget(self.instances_button)

# N'oubliez pas d'importer QApplication et d'initialiser votre application
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = GroupTable()
    window.show()
    sys.exit(app.exec_())
