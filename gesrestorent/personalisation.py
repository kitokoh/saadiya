import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QSpinBox, QDateEdit, QDialog, QFormLayout, QFileDialog, QColorDialog
)
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import QDate, Qt, QPropertyAnimation, QEasingCurve
import sqlite3
import json

# Connexion à la base de données SQLite
conn = sqlite3.connect('cafe_restaurant.db')
cursor = conn.cursor()

# Création des tables si elles n'existent pas
cursor.execute('''
CREATE TABLE IF NOT EXISTS plats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prix REAL NOT NULL,
    description TEXT,
    image TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    logo TEXT,
    couleur_principale TEXT,
    langue TEXT DEFAULT 'fr',
    devise TEXT DEFAULT 'EUR'
)
''')

conn.commit()

# Styles CSS pour l'interface
STYLESHEET = """
    QMainWindow {
        background-color: #f0f0f0;
    }
    QWidget {
        font-size: 14px;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QTableWidget {
        background-color: white;
        border: 1px solid #ddd;
    }
    QLineEdit, QComboBox, QSpinBox, QDateEdit {
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 3px;
    }
    QLabel {
        font-weight: bold;
    }
    QDialog {
        background-color: #f9f9f9;
    }
"""

# Classe pour la personnalisation de l'interface
class PersonnalisationUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Personnalisation de l\'Interface')
        self.setGeometry(200, 200, 400, 300)

        layout = QFormLayout()

        self.logo_label = QLabel('Logo:', self)
        self.logo_button = QPushButton('Choisir un Logo', self)
        self.logo_button.clicked.connect(self.choisir_logo)

        self.couleur_label = QLabel('Couleur Principale:', self)
        self.couleur_button = QPushButton('Choisir une Couleur', self)
        self.couleur_button.clicked.connect(self.choisir_couleur)

        self.langue_label = QLabel('Langue:', self)
        self.langue_combo = QComboBox(self)
        self.langue_combo.addItems(['Français', 'Anglais', 'Espagnol'])

        self.devise_label = QLabel('Devise:', self)
        self.devise_combo = QComboBox(self)
        self.devise_combo.addItems(['EUR', 'USD', 'GBP'])

        self.enregistrer_button = QPushButton('Enregistrer', self)
        self.enregistrer_button.clicked.connect(self.enregistrer_preferences)

        layout.addRow(self.logo_label, self.logo_button)
        layout.addRow(self.couleur_label, self.couleur_button)
        layout.addRow(self.langue_label, self.langue_combo)
        layout.addRow(self.devise_label, self.devise_combo)
        layout.addRow(self.enregistrer_button)

        self.setLayout(layout)

    def choisir_logo(self):
        fichier, _ = QFileDialog.getOpenFileName(self, 'Choisir un Logo', '', 'Images (*.png *.jpg *.jpeg)')
        if fichier:
            self.logo_path = fichier
            self.logo_button.setText('Logo sélectionné')

    def choisir_couleur(self):
        couleur = QColorDialog.getColor()
        if couleur.isValid():
            self.couleur_principale = couleur.name()
            self.couleur_button.setText('Couleur sélectionnée')

    def enregistrer_preferences(self):
        logo = getattr(self, 'logo_path', '')
        couleur = getattr(self, 'couleur_principale', '#4CAF50')
        langue = self.langue_combo.currentText()
        devise = self.devise_combo.currentText()

        cursor.execute('INSERT OR REPLACE INTO preferences (id, logo, couleur_principale, langue, devise) VALUES (1, ?, ?, ?, ?)', (logo, couleur, langue, devise))
        conn.commit()
        QMessageBox.information(self, 'Succès', 'Préférences enregistrées avec succès.')
        self.parent().appliquer_preferences()

# Classe principale
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gestion de Café/Restaurant')
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet(STYLESHEET)

        # Charger les préférences
        self.charger_preferences()

        # Menu principal
        self.menu_bar = self.menuBar()
        self.menu_personnalisation = self.menu_bar.addMenu('Personnalisation')
        self.action_personnalisation = self.menu_personnalisation.addAction('Personnaliser l\'Interface')
        self.action_personnalisation.triggered.connect(self.personnaliser_interface)

        # Tabs
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

    def charger_preferences(self):
        cursor.execute('SELECT logo, couleur_principale, langue, devise FROM preferences WHERE id = 1')
        preferences = cursor.fetchone()
        if preferences:
            self.logo, self.couleur_principale, self.langue, self.devise = preferences
            self.appliquer_preferences()
        else:
            self.logo, self.couleur_principale, self.langue, self.devise = '', '#4CAF50', 'Français', 'EUR'

    def appliquer_preferences(self):
        # Appliquer le logo
        if self.logo:
            pixmap = QPixmap(self.logo)
            self.setWindowIcon(pixmap)

        # Appliquer la couleur principale
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #f0f0f0;
            }}
            QPushButton {{
                background-color: {self.couleur_principale};
                color: white;
                padding: 10px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {QColor(self.couleur_principale).darker(110).name()};
            }}
        """)

    def personnaliser_interface(self):
        dialog = PersonnalisationUI(self)
        dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())