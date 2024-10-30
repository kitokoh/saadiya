import json
import os
import csv
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, 
                             QHeaderView, QAbstractItemView, QLineEdit, QHBoxLayout, QCheckBox, 
                             QMenu, QAction, QComboBox, QScrollBar, QFrame, QDialog, QFormLayout)
from PyQt5.QtCore import Qt, QSize, pyqtSignal  # Ajout de pyqtSignal ici
from ui.header import HeaderSection  # Import du header
from ui.footer import FooterSection  # Import du footer
from ui.secondry_menu import SecondaryMenu  # Assurez-vous d'importer votre nouvelle classe
from PyQt5.QtWidgets import QFileDialog
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *
class AddGroupDialog(QDialog):
    def __init__(self, parent=None):
                        # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

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
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load("resources/lang/en_US/modules/main_fb_robot_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/modules/main_fb_robot_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/modules/main_fb_robot_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/modules/main_fb_robot_translated.qm")

        # Installer le traducteur pour appliquer la nouvelle langue
        QApplication.instance().installTranslator(self.translator)
        
            # Sauvegarder le choix de l'utilisateur
        self.save_language_choice(language)


        # Réappliquer la traduction sur tous les éléments visibles de l'interface
        self.retranslateUi()

    def save_language_choice(self, language):
        """Sauvegarde le choix de langue de l'utilisateur dans un fichier JSON."""
        preferences = {'language': language}
        with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'w') as f:
            json.dump(preferences, f)
    def retranslateUi(self):
        """Recharge les textes traduits dans l'interface."""
        pass
        #self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # Par exemple, pour les actions du menu :
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.language_menu.setTitle(self.tr('Langue'))

    def init_language(self):
        """Initialise la langue par défaut à celle du système ou à celle choisie par l'utilisateur."""
        # Vérifiez si le fichier de préférences existe
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')  # Par défaut à l'anglais si non trouvé
        else:
            # Obtenir le code de langue du système
            system_locale = QLocale.system().name()[:2]  # Par exemple: 'fr', 'en', 'tr', etc.

            # Dictionnaire pour mapper les codes de langue aux traductions
            language_map = {
                'en': 'en',
                'fr': 'fr',
                'tr': 'tr',
                'ar': 'ar',
            }

            # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)

    def add_group(self):
        new_group = {
            'name': self.name_input.text(),
            'link': self.link_input.text(),
            'remarks': self.remarks_input.text(),
            'category': self.category_input.text(),
            'description': self.description_input.text()
        }
        self.accept()  # Ferme la boîte de dialogue et renvoie True

        return new_group  # Retourne le nouveau groupe

class GroupTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
                # Initialiser et charger les traductions
        #self.translator_manager = TranslatorManager()
        #self.translator_manager.load_translations()
                # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions


        self.group_list = self.load_groups()  # Charger les groupes
        self.visible_columns = [self.tr('Select'), self.tr('Name'), self.tr('Link'), self.tr('Remarks'), 
                                self.tr('Category'), self.tr('Description'), self.tr('Actions')]
        self.items_per_page = 5
        self.current_page = 1

        layout = QVBoxLayout(self)

        # Ajouter le header
        header = HeaderSection(self, title="FBK GRUP MANAGEMENT", app_name="Nova360 AI", slogan="AI Marketing & Management Auto")
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
        self.add_group_button.clicked.connect(self.open_add_group_dialog)
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
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load("resources/lang/en_US/modules/group_manager_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/modules/group_manager_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/modules/group_manager_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/modules/group_manager_translated.qm")

        # Installer le traducteur pour appliquer la nouvelle langue
        QApplication.instance().installTranslator(self.translator)
        
            # Sauvegarder le choix de l'utilisateur
        self.save_language_choice(language)


        # Réappliquer la traduction sur tous les éléments visibles de l'interface
        self.retranslateUi()

    def save_language_choice(self, language):
        """Sauvegarde le choix de langue de l'utilisateur dans un fichier JSON."""
        preferences = {'language': language}
        with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'w') as f:
            json.dump(preferences, f)
    def retranslateUi(self):
        """Recharge les textes traduits dans l'interface."""
        self.setWindowTitle(self.tr('AI PIN ROBOT Pro'))
        # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # Par exemple, pour les actions du menu :
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.language_menu.setTitle(self.tr('Langue'))

    def init_language(self):
        """Initialise la langue par défaut à celle du système ou à celle choisie par l'utilisateur."""
        # Vérifiez si le fichier de préférences existe
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')  # Par défaut à l'anglais si non trouvé
        else:
            # Obtenir le code de langue du système
            system_locale = QLocale.system().name()[:2]  # Par exemple: 'fr', 'en', 'tr', etc.

            # Dictionnaire pour mapper les codes de langue aux traductions
            language_map = {
                'en': 'en',
                'fr': 'fr',
                'tr': 'tr',
                'ar': 'ar',
            }

            # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)

    def load_groups(self):
        try:
            filedirect= os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-PIN-Robot', 'text','text1' , 'groups.json')
            with open(filedirect, 'r') as f:
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
                edit_action.triggered.connect(lambda _, r=row: self.edit_group(r))
                delete_action.triggered.connect(lambda _, r=row: self.delete_group(r))
                action_menu.addAction(edit_action)
                action_menu.addAction(delete_action)
                action_button.setMenu(action_menu)
                self.table.setCellWidget(row, 6, action_button)
            else:
                print(f"Warning: The group at row {row} is not a dictionary. Skipping...")

        # Mettre à jour l'affichage de la pagination
        self.pagination_label.setText(f"{self.tr('Page')} {self.current_page}")

    def import_groups(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Importer des groupes", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.group_list.append(row)
                    self.save_groups()  # Enregistrer les groupes après importation
                    self.populate_table()  # Mettre à jour le tableau
            except FileNotFoundError:
                print("Le fichier d'importation n'a pas été trouvé.")
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
            new_group = dialog.add_group()  # Récupérer le groupe ajouté
            self.group_list.append(new_group)  # Ajouter le groupe à la liste
            self.save_groups()  # Enregistrer les groupes après ajout
            self.populate_table()  # Mettre à jour le tableau

    def edit_group(self, row):
        group = self.group_list[row]  # Obtenir le groupe à éditer
        dialog = AddGroupDialog(self)
        dialog.name_input.setText(group.get('name', ''))
        dialog.link_input.setText(group.get('link', ''))
        dialog.remarks_input.setText(group.get('remarks', ''))
        dialog.category_input.setText(group.get('category', ''))
        dialog.description_input.setText(group.get('description', ''))

        if dialog.exec_() == QDialog.Accepted:
            # Mettre à jour le groupe dans la liste
            updated_group = dialog.add_group()
            self.group_list[row] = updated_group
            self.save_groups()  # Enregistrer les groupes après modification
            self.populate_table()  # Mettre à jour le tableau

    def delete_group(self, row):
        del self.group_list[row]  # Supprimer le groupe de la liste
        self.save_groups()  # Enregistrer les groupes après suppression
        self.populate_table()  # Mettre à jour le tableau

    def filter_table(self):
        search_text = self.search_field.text().lower()
        filtered_groups = [group for group in self.group_list if search_text in group.get('name', '').lower()]
        self.group_list = filtered_groups
        self.populate_table()  # Mettre à jour le tableau avec les groupes filtrés



    def next_page(self):
        if (self.current_page * self.items_per_page) < len(self.group_list):  # Vérifier si la page suivante existe
            self.current_page += 1
            self.populate_table()  # Mettre à jour le tableau

    def previous_page(self):
        if self.current_page > 1:  # Vérifier si la page précédente existe
            self.current_page -= 1
            self.populate_table()  # Mettre à jour le tableau

    def save_groups(self):
        filedirect= os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-PIN-Robot', 'text','text1' , 'groups.json')

        with open(filedirect, 'w') as f:
            json.dump({"groups": self.group_list}, f, indent=4)

    def change_content(self, content):
        # Logique pour changer le contenu selon le menu secondaire
        # À implémenter selon vos besoins
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


# N'oubliez pas d'importer QApplication et d'initialiser votre application
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = GroupTable()
    window.show()
    sys.exit(app.exec_())
