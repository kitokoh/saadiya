import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QDateEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import numpy as np
from sklearn.linear_model import LinearRegression

# Connexion à la base de données SQLite
conn = sqlite3.connect('cafe_restaurant.db')
cursor = conn.cursor()

# Création des tables si elles n'existent pas
cursor.execute('''
CREATE TABLE IF NOT EXISTS ventes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    plat_id INTEGER NOT NULL,
    quantite INTEGER NOT NULL,
    montant REAL NOT NULL,
    FOREIGN KEY (plat_id) REFERENCES plats(id)
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
    QLineEdit, QComboBox, QDateEdit {
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

# Classe pour le tableau de bord interactif
class TableauDeBord(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.date_debut = QDateEdit(self)
        self.date_debut.setDate(QDate.currentDate().addDays(-7))
        self.date_fin = QDateEdit(self)
        self.date_fin.setDate(QDate.currentDate())
        self.generer_rapport_btn = QPushButton('Générer Rapport', self)
        self.exporter_pdf_btn = QPushButton('Exporter en PDF', self)

        layout.addWidget(QLabel('Date de Début:'))
        layout.addWidget(self.date_debut)
        layout.addWidget(QLabel('Date de Fin:'))
        layout.addWidget(self.date_fin)
        layout.addWidget(self.generer_rapport_btn)
        layout.addWidget(self.exporter_pdf_btn)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        self.generer_rapport_btn.clicked.connect(self.generer_rapport)
        self.exporter_pdf_btn.clicked.connect(self.exporter_pdf)

    def generer_rapport(self):
        date_debut = self.date_debut.date().toString('yyyy-MM-dd')
        date_fin = self.date_fin.date().toString('yyyy-MM-dd')

        # Chiffre d'affaires
        cursor.execute('SELECT SUM(montant) FROM ventes WHERE date BETWEEN ? AND ?', (date_debut, date_fin))
        chiffre_affaires = cursor.fetchone()[0] or 0

        # Plats populaires
        cursor.execute('''
        SELECT plats.nom, SUM(ventes.quantite) as total_quantite
        FROM ventes
        JOIN plats ON ventes.plat_id = plats.id
        WHERE ventes.date BETWEEN ? AND ?
        GROUP BY plats.nom
        ORDER BY total_quantite DESC
        LIMIT 5
        ''', (date_debut, date_fin))
        plats_populaires = cursor.fetchall()

        # Prédiction des ventes
        cursor.execute('SELECT date, SUM(montant) FROM ventes GROUP BY date ORDER BY date')
        donnees_historiques = cursor.fetchall()
        dates = [QDate.fromString(row[0], 'yyyy-MM-dd').toJulianDay() for row in donnees_historiques]
        ventes = [row[1] for row in donnees_historiques]

        if len(dates) > 1:
            model = LinearRegression()
            model.fit(np.array(dates).reshape(-1, 1), np.array(ventes))
            prediction = model.predict(np.array([QDate.currentDate().addDays(7).toJulianDay()]).reshape(-1, 1))[0]
        else:
            prediction = 0

        # Affichage des données
        self.ax.clear()
        self.ax.bar(['Chiffre d\'Affaires'], [chiffre_affaires], color='blue')
        self.ax.set_ylabel('Montant (€)')
        self.ax.set_title(f'Chiffre d\'Affaires du {date_debut} au {date_fin}')
        self.canvas.draw()

        # Affichage des plats populaires
        plats = [plat[0] for plat in plats_populaires]
        quantites = [plat[1] for plat in plats_populaires]

        self.ax.clear()
        self.ax.bar(plats, quantites, color='green')
        self.ax.set_ylabel('Quantité Vendue')
        self.ax.set_title('Plats les Plus Populaires')
        self.canvas.draw()

        # Affichage de la prédiction
        QMessageBox.information(self, 'Prédiction', f'Prédiction des ventes pour la semaine prochaine : {prediction:.2f} €')

    def exporter_pdf(self):
        date_debut = self.date_debut.date().toString('yyyy-MM-dd')
        date_fin = self.date_fin.date().toString('yyyy-MM-dd')

        fichier_pdf, _ = QFileDialog.getSaveFileName(self, 'Exporter en PDF', '', 'PDF Files (*.pdf)')
        if fichier_pdf:
            c = canvas.Canvas(fichier_pdf, pagesize=letter)
            c.drawString(100, 750, f'Rapport du {date_debut} au {date_fin}')

            # Chiffre d'affaires
            cursor.execute('SELECT SUM(montant) FROM ventes WHERE date BETWEEN ? AND ?', (date_debut, date_fin))
            chiffre_affaires = cursor.fetchone()[0] or 0
            c.drawString(100, 730, f'Chiffre d\'Affaires: {chiffre_affaires:.2f} €')

            # Plats populaires
            c.drawString(100, 710, 'Plats les Plus Populaires:')
            cursor.execute('''
            SELECT plats.nom, SUM(ventes.quantite) as total_quantite
            FROM ventes
            JOIN plats ON ventes.plat_id = plats.id
            WHERE ventes.date BETWEEN ? AND ?
            GROUP BY plats.nom
            ORDER BY total_quantite DESC
            LIMIT 5
            ''', (date_debut, date_fin))
            plats_populaires = cursor.fetchall()
            y = 690
            for plat in plats_populaires:
                c.drawString(120, y, f'{plat[0]}: {plat[1]} unités')
                y -= 20

            c.save()

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
        self.tab_widget.addTab(TableauDeBord(), 'Tableau de Bord')

        self.setCentralWidget(self.tab_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())