import sys
import sqlite3
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QFileDialog,
    QDialog, QFormLayout, QLineEdit, QMessageBox, QHBoxLayout, QStatusBar, QMenu, QAction, QToolBar, QStyleFactory
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPalette
import pandas as pd


# Styles CSS pour l'application
STYLESHEET = """
    QMainWindow {
        background-color: #2E3440;
    }
    QTableWidget {
        background-color: #3B4252;
        color: #ECEFF4;
        gridline-color: #4C566A;
        font-size: 14px;
    }
    QHeaderView::section {
        background-color: #4C566A;
        color: #ECEFF4;
        padding: 5px;
        font-size: 14px;
    }
    QPushButton {
        background-color: #5E81AC;
        color: #ECEFF4;
        padding: 8px;
        border-radius: 5px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #81A1C1;
    }
    QPushButton:pressed {
        background-color: #4C566A;
    }
    QStatusBar {
        background-color: #4C566A;
        color: #ECEFF4;
        font-size: 14px;
    }
    QMenu {
        background-color: #3B4252;
        color: #ECEFF4;
        border: 1px solid #4C566A;
    }
    QMenu::item:selected {
        background-color: #5E81AC;
    }
    QLineEdit {
        background-color: #4C566A;
        color: #ECEFF4;
        border: 1px solid #5E81AC;
        padding: 5px;
        border-radius: 5px;
    }
"""


class ContactDialog(QDialog):
    """Fenêtre modale pour gérer les contacts."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestion des contacts")
        self.setModal(True)
        self.setStyleSheet(STYLESHEET)
        self.layout = QFormLayout(self)

        # Champs de saisie
        self.contact_name_input = QLineEdit(self)
        self.contact_phone_input = QLineEdit(self)
        self.layout.addRow("Nom du contact:", self.contact_name_input)
        self.layout.addRow("Numéro de téléphone:", self.contact_phone_input)

        # Boutons
        self.save_button = QPushButton("Enregistrer", self)
        self.save_button.clicked.connect(self.validate_and_save)
        self.cancel_button = QPushButton("Annuler", self)
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addRow(self.save_button, self.cancel_button)

    def validate_and_save(self):
        """Valide les entrées et ferme la fenêtre si tout est correct."""
        name = self.contact_name_input.text().strip()
        phone = self.contact_phone_input.text().strip()

        # Validation du nom
        if not name:
            QMessageBox.warning(self, "Erreur", "Le nom du contact ne peut pas être vide.")
            return

        # Validation du numéro de téléphone
        if not re.match(r"^\+?[0-9\s-]{10,}$", phone):
            QMessageBox.warning(self, "Erreur", "Le numéro de téléphone est invalide.")
            return

        self.accept()

    def get_contact_data(self):
        """Retourne les données du contact."""
        return {
            "name": self.contact_name_input.text().strip(),
            "phone": self.contact_phone_input.text().strip(),
        }


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel-like Table with SQLite")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(STYLESHEET)

        # Thème sombre par défaut
        self.dark_theme = True
        self.apply_theme()

        # Widget central et layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Barre d'outils
        self.toolbar = QToolBar("Barre d'outils")
        self.addToolBar(self.toolbar)

        # Boutons de la barre d'outils
        self.add_column_action = QAction("Ajouter une colonne", self)
        self.add_column_action.triggered.connect(self.add_column)
        self.toolbar.addAction(self.add_column_action)

        self.remove_column_action = QAction("Supprimer une colonne", self)
        self.remove_column_action.triggered.connect(self.remove_column)
        self.toolbar.addAction(self.remove_column_action)

        self.clear_data_action = QAction("Effacer toutes les données", self)
        self.clear_data_action.triggered.connect(self.clear_data)
        self.toolbar.addAction(self.clear_data_action)

        self.import_action = QAction("Importer Excel", self)
        self.import_action.triggered.connect(self.import_excel)
        self.toolbar.addAction(self.import_action)

        self.export_action = QAction("Exporter vers Excel", self)
        self.export_action.triggered.connect(self.export_excel)
        self.toolbar.addAction(self.export_action)

        self.toggle_theme_action = QAction("Basculer le thème", self)
        self.toggle_theme_action.triggered.connect(self.toggle_theme)
        self.toolbar.addAction(self.toggle_theme_action)

        # Tableau pour afficher les données
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)  # Colonnes initiales : A, B, C
        self.update_headers()
        self.layout.addWidget(self.table)

        # Barre de statut
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt")

        # Connexion à la base de données
        self.db_connection = sqlite3.connect('data.db')
        self.create_tables()
        self.load_data()

        # Menu contextuel
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

    def create_tables(self):
        """Crée les tables dans la base de données."""
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS main_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                A TEXT, B TEXT, C TEXT, D TEXT, E TEXT, F TEXT, G TEXT, H TEXT, I TEXT, J TEXT,
                K TEXT, L TEXT, M TEXT, N TEXT, O TEXT, P TEXT, Q TEXT, R TEXT, S TEXT, T TEXT,
                U TEXT, V TEXT, W TEXT, X TEXT, Y TEXT, Z TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                main_data_id INTEGER,
                contact_name TEXT,
                contact_phone_number TEXT,
                FOREIGN KEY(main_data_id) REFERENCES main_data(id)
            )
        ''')
        self.db_connection.commit()

    def load_data(self):
        """Charge les données depuis la base de données."""
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM main_data")
        rows = cursor.fetchall()

        if rows:
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(len(rows[0]) - 1)  # Exclure la colonne ID

            for i, row in enumerate(rows):
                for j, value in enumerate(row[1:]):  # Ignorer la colonne ID
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))

        self.update_headers()

    def update_headers(self):
        """Met à jour les en-têtes de colonnes."""
        headers = [chr(65 + i) for i in range(self.table.columnCount())]
        self.table.setHorizontalHeaderLabels(headers)

    def add_column(self):
        """Ajoute une colonne au tableau."""
        current_column_count = self.table.columnCount()
        if current_column_count < 26:  # Limite à Z
            self.table.setColumnCount(current_column_count + 1)
            self.update_headers()
            self.status_bar.showMessage(f"Colonne {chr(65 + current_column_count)} ajoutée.")
        else:
            self.status_bar.showMessage("Nombre maximal de colonnes atteint (Z).")

    def remove_column(self):
        """Supprime la dernière colonne du tableau."""
        current_column_count = self.table.columnCount()
        if current_column_count > 1:  # Garder au moins une colonne
            self.table.setColumnCount(current_column_count - 1)
            self.update_headers()
            self.status_bar.showMessage(f"Colonne {chr(64 + current_column_count)} supprimée.")
        else:
            self.status_bar.showMessage("Impossible de supprimer la dernière colonne.")

    def clear_data(self):
        """Efface toutes les données du tableau et de la base de données."""
        reply = QMessageBox.question(
            self, "Confirmation", "Êtes-vous sûr de vouloir effacer toutes les données ?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.table.setRowCount(0)
            cursor = self.db_connection.cursor()
            cursor.execute("DELETE FROM main_data")
            cursor.execute("DELETE FROM contacts")
            self.db_connection.commit()
            self.status_bar.showMessage("Toutes les données ont été effacées.")

    def import_excel(self):
        """Importe les données depuis un fichier Excel."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier Excel", "", "Fichiers Excel (*.xlsx *.xls)")
        if file_name:
            df = pd.read_excel(file_name)
            self.table.setRowCount(df.shape[0])
            self.table.setColumnCount(df.shape[1])

            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    self.table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

            self.update_headers()
            self.status_bar.showMessage(f"Fichier Excel importé : {file_name}")

    def export_excel(self):
        """Exporte les données vers un fichier Excel."""
        file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer sous", "", "Fichiers Excel (*.xlsx)")
        if file_name:
            data = []
            for i in range(self.table.rowCount()):
                row = []
                for j in range(self.table.columnCount()):
                    item = self.table.item(i, j)
                    row.append(item.text() if item else "")
                data.append(row)

            df = pd.DataFrame(data, columns=[chr(65 + i) for i in range(self.table.columnCount())])
            df.to_excel(file_name, index=False)
            self.status_bar.showMessage(f"Fichier Excel enregistré : {file_name}")

    def show_context_menu(self, position):
        """Affiche un menu contextuel pour gérer les lignes et les colonnes."""
        menu = QMenu(self)
        add_contact_action = menu.addAction("Ajouter un contact")
        add_contact_action.triggered.connect(self.add_contact)
        menu.exec_(self.table.viewport().mapToGlobal(position))

    def add_contact(self):
        """Ouvre la fenêtre modale pour ajouter un contact."""
        dialog = ContactDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            contact_data = dialog.get_contact_data()
            self.status_bar.showMessage(f"Contact ajouté : {contact_data['name']} - {contact_data['phone']}")

    def toggle_theme(self):
        """Bascule entre le thème sombre et le thème clair."""
        self.dark_theme = not self.dark_theme
        self.apply_theme()

    def apply_theme(self):
        """Applique le thème sélectionné."""
        if self.dark_theme:
            self.setStyleSheet(STYLESHEET)
        else:
            self.setStyleSheet("")  # Réinitialise le style au thème par défaut de Qt

    def closeEvent(self, event):
        """Sauvegarde les données avant de fermer l'application."""
        self.save_data()
        self.db_connection.close()
        event.accept()

    def save_data(self):
        """Sauvegarde les données dans la base de données."""
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM main_data")  # Efface les données existantes

        for i in range(self.table.rowCount()):
            row_data = [self.table.item(i, j).text() if self.table.item(i, j) else '' for j in range(self.table.columnCount())]
            cursor.execute(
                f"INSERT INTO main_data ({', '.join([chr(65 + j) for j in range(self.table.columnCount())])}) VALUES ({', '.join(['?'] * self.table.columnCount())})",
                row_data
            )

        self.db_connection.commit()
        self.status_bar.showMessage("Données sauvegardées.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())