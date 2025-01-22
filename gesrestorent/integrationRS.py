import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QTextEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('cafe_restaurant.db')
cursor = conn.cursor()

# Création des tables si elles n'existent pas
cursor.execute('''
CREATE TABLE IF NOT EXISTS avis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_client TEXT NOT NULL,
    commentaire TEXT NOT NULL,
    note INTEGER NOT NULL
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
    QLineEdit, QTextEdit {
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

# Classe pour l'intégration avec les réseaux sociaux
class IntegrationReseauxSociaux(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Boutons de partage sur les réseaux sociaux
        self.partage_facebook_btn = QPushButton('Partager sur Facebook', self)
        self.partage_twitter_btn = QPushButton('Partager sur Twitter', self)

        # Section pour les avis et commentaires
        self.nom_client = QLineEdit(self)
        self.commentaire_client = QTextEdit(self)
        self.note_client = QComboBox(self)
        self.note_client.addItems(['1', '2', '3', '4', '5'])
        self.poster_avis_btn = QPushButton('Poster un Avis', self)
        self.table_avis = QTableWidget(self)
        self.table_avis.setColumnCount(3)
        self.table_avis.setHorizontalHeaderLabels(['Nom', 'Commentaire', 'Note'])

        layout.addWidget(QLabel('Partage sur les Réseaux Sociaux:'))
        layout.addWidget(self.partage_facebook_btn)
        layout.addWidget(self.partage_twitter_btn)
        layout.addWidget(QLabel('Nom du Client:'))
        layout.addWidget(self.nom_client)
        layout.addWidget(QLabel('Commentaire:'))
        layout.addWidget(self.commentaire_client)
        layout.addWidget(QLabel('Note:'))
        layout.addWidget(self.note_client)
        layout.addWidget(self.poster_avis_btn)
        layout.addWidget(self.table_avis)

        self.setLayout(layout)

        self.partage_facebook_btn.clicked.connect(self.partager_facebook)
        self.partage_twitter_btn.clicked.connect(self.partager_twitter)
        self.poster_avis_btn.clicked.connect(self.poster_avis)
        self.charger_avis()

    def partager_facebook(self):
        url = "https://www.facebook.com/sharer/sharer.php?u=https://votre-restaurant.com"
        self.ouvrir_navigateur(url)

    def partager_twitter(self):
        url = "https://twitter.com/intent/tweet?text=Découvrez%20notre%20restaurant%20incroyable%20!&url=https://votre-restaurant.com"
        self.ouvrir_navigateur(url)

    def ouvrir_navigateur(self, url):
        self.navigateur = QWebEngineView()
        self.navigateur.setUrl(QUrl(url))
        self.navigateur.show()

    def poster_avis(self):
        nom = self.nom_client.text()
        commentaire = self.commentaire_client.toPlainText()
        note = self.note_client.currentText()

        if nom and commentaire and note:
            cursor.execute('INSERT INTO avis (nom_client, commentaire, note) VALUES (?, ?, ?)', (nom, commentaire, int(note)))
            conn.commit()
            self.charger_avis()
            self.nom_client.clear()
            self.commentaire_client.clear()
            QMessageBox.information(self, 'Succès', 'Avis posté avec succès.')
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs.')

    def charger_avis(self):
        self.table_avis.setRowCount(0)
        cursor.execute('SELECT nom_client, commentaire, note FROM avis')
        avis = cursor.fetchall()
        for row_number, avi in enumerate(avis):
            self.table_avis.insertRow(row_number)
            self.table_avis.setItem(row_number, 0, QTableWidgetItem(avi[0]))
            self.table_avis.setItem(row_number, 1, QTableWidgetItem(avi[1]))
            self.table_avis.setItem(row_number, 2, QTableWidgetItem(str(avi[2])))

# Classe principale
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gestion de Café/Restaurant')
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet(STYLESHEET)

        # Tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(IntegrationReseauxSociaux(), 'Réseaux Sociaux')

        self.setCentralWidget(self.tab_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())