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
from fb_robot_install import FbRobot
import subprocess  # Pour exécuter le script externe
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *

class LicenseDialog(QDialog):
    def __init__(self, parent=None):

                # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        super().__init__(parent)
        self.setWindowTitle(self.tr("Ajouter Licence"))
        self.layout = QFormLayout(self)

        self.license_field = QLineEdit(self)
        self.layout.addRow(self.tr("Nouvelle Licence :"), self.license_field)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','instances_table_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','instances_table_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','instances_table_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','instances_table_translated.qm'))

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
        self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # Par exemple, pour les actions du menu :
        self.instance_action.setText(self.tr('Instance'))
        self.media_action.setText(self.tr('Médias'))
        self.group_action.setText(self.tr('Groupes'))
        self.about_action.setText(self.tr('About'))
        self.certificate_action.setText(self.tr('Certif'))
        self.language_menu.setTitle(self.tr('Langue'))

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

    def get_license(self):
        return self.license_field.text()


class InstanceTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.instance_list = self.load_instances()  # Charger les instances depuis SQLite
        self.visible_columns = ['Select', 'Nom Instance', 'Description', 'User', 'Expire Date', 'Actions']

        # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()

        layout = QVBoxLayout(self)

        # Ajouter le header
        header = HeaderSection(self, title="AI FBK Marketing Instances", app_name="Nova360 AI", slogan="AI Marketing & Management Auto")
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
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','modules','instances_table_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','modules','instances_table_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','modules','instances_table_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','modules','instances_table_translated.qm'))

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
        self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # Par exemple, pour les actions du menu :
        self.instance_action.setText(self.tr('Instance'))
        self.media_action.setText(self.tr('Médias'))
        self.group_action.setText(self.tr('Groupes'))
        self.about_action.setText(self.tr('About'))
        self.certificate_action.setText(self.tr('Certif'))
        self.language_menu.setTitle(self.tr('Langue'))

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
               SELECT 
                i.name AS instance_name, 
                i.type AS instance_type, 
                f.name AS facebook_user_name, 
                l.request_date
            FROM 
                instances i
            JOIN 
                facebook_users f ON f.instance_id = i.id
            JOIN 
                licences l ON l.instance_id = i.id;
                """)
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
        details_action = QAction(self.tr('Détails'), self)

        action_menu.addAction(update_license_action)
        action_menu.addAction(edit_action)
        action_menu.addAction(details_action)
        action_button.setMenu(action_menu)
        self.table.setCellWidget(row, 5, action_button)

        # Connexion des actions
        update_license_action.triggered.connect(self.update_license)
        edit_action.triggered.connect(self.edit_instance)
        details_action.triggered.connect(self.show_details)

    def show_details(self):
        # Logique pour afficher un modal avec les détails de l'instance
        QMessageBox.information(self, self.tr("Détails de l'instance"), self.tr("Voici les détails de l'instance."))

    def filter_table(self):
        filter_text = self.search_field.text().lower()
        self.table.setRowCount(len(self.instance_list))  # Réinitialiser le tableau
        filtered_instances = [instance for instance in self.instance_list if filter_text in instance.get('name', '').lower()]

        for row, instance in enumerate(filtered_instances):
            self.fill_table_row(row, instance)

    def add_new_instance(self):
        # Exécuter le script fb_robot_install.py
        self.face_main = FbRobot()  # Remplacez ceci par votre classe de page d'accueil
        self.face_main.show()
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
        if selected_rows:
            dialog = LicenseDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                new_license = dialog.get_license()
                # Logique pour mettre à jour la licence dans la base de données
                QMessageBox.information(self, self.tr("Licence mise à jour"), self.tr("La licence a été mise à jour avec succès."))
        else:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Veuillez sélectionner une instance."))

    def edit_instance(self):
        # Logique pour éditer l'instance
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            QMessageBox.information(self, self.tr("Édition"), self.tr("Vous pouvez maintenant éditer l'instance sélectionnée."))
        else:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Veuillez sélectionner une instance."))

    def change_content(self, menu_item):
        print(f"Changement de contenu pour : {menu_item}")


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
