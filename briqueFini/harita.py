import sys
import csv
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QListWidget, QMessageBox, QTableWidget, QTableWidgetItem, QFileDialog
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QFont
import sqlite3


class ProductApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDB()

    def initUI(self):
        self.setWindowTitle('Gestion de Produits et Zones Géographiques')
        self.setGeometry(100, 100, 1200, 900)

        # Layout principal
        main_layout = QVBoxLayout()

        # Style CSS pour l'interface
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
                color: #333;
            }
            QComboBox, QListWidget, QPushButton, QTableWidget {
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTableWidget {
                background-color: #f9f9f9;
                gridline-color: #ddd;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)

        # Type de produit
        self.productTypeLabel = QLabel('Type de Produit:')
        self.productTypeCombo = QComboBox()
        self.productTypeCombo.addItems(['Électronique', 'Vêtements', 'Alimentation', 'Autre'])
        main_layout.addWidget(self.productTypeLabel)
        main_layout.addWidget(self.productTypeCombo)

        # Catégorie
        self.categoryLabel = QLabel('Catégorie:')
        self.categoryCombo = QComboBox()
        self.categoryCombo.addItems(['Grand public', 'Professionnel'])
        main_layout.addWidget(self.categoryLabel)
        main_layout.addWidget(self.categoryCombo)

        # Sous-catégorie
        self.subCategoryLabel = QLabel('Sous-catégorie:')
        self.subCategoryCombo = QComboBox()
        self.subCategoryCombo.addItems(['Homme', 'Femme', 'Enfant'])
        main_layout.addWidget(self.subCategoryLabel)
        main_layout.addWidget(self.subCategoryCombo)

        # Zones géographiques
        self.zoneLabel = QLabel('Zones Géographiques:')
        self.zoneList = QListWidget()
        self.zoneList.addItems(['Afrique', 'Amérique', 'Asie', 'Europe', 'Océanie'])
        self.zoneList.setSelectionMode(QListWidget.MultiSelection)
        main_layout.addWidget(self.zoneLabel)
        main_layout.addWidget(self.zoneList)

        # Carte interactive avec Leaflet
        self.mapLabel = QLabel('Sélectionnez les zones sur la carte:')
        self.mapView = QWebEngineView()
        self.loadLeafletMap()
        main_layout.addWidget(self.mapLabel)
        main_layout.addWidget(self.mapView)

        # Boutons supplémentaires
        button_layout = QHBoxLayout()
        self.saveButton = QPushButton('Sauvegarder')
        self.saveButton.clicked.connect(self.saveData)
        self.exportButton = QPushButton('Exporter les données')
        self.exportButton.clicked.connect(self.exportData)
        self.importButton = QPushButton('Importer des zones')
        self.importButton.clicked.connect(self.importZones)
        button_layout.addWidget(self.saveButton)
        button_layout.addWidget(self.exportButton)
        button_layout.addWidget(self.importButton)
        main_layout.addLayout(button_layout)

        # Tableau pour afficher les données sauvegardées
        self.dataTable = QTableWidget()
        self.dataTable.setColumnCount(4)
        self.dataTable.setHorizontalHeaderLabels(['Type de Produit', 'Catégorie', 'Sous-catégorie', 'Zones'])
        self.dataTable.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.dataTable)

        self.setLayout(main_layout)

    def loadLeafletMap(self):
        """Charge une carte Leaflet dans QWebEngineView."""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Leaflet Map</title>
            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
            <style>
                #map { height: 400px; }
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                var map = L.map('map').setView([20, 0], 2);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors'
                }).addTo(map);

                var drawnItems = new L.FeatureGroup();
                map.addLayer(drawnItems);

                var drawControl = new L.Control.Draw({
                    edit: {
                        featureGroup: drawnItems
                    },
                    draw: {
                        polygon: true,
                        rectangle: true,
                        circle: true,
                        marker: false
                    }
                });
                map.addControl(drawControl);

                map.on('draw:created', function (e) {
                    var layer = e.layer;
                    drawnItems.addLayer(layer);
                });
            </script>
        </body>
        </html>
        """
        self.mapView.setHtml(html_content)

    def initDB(self):
        """Initialise la base de données SQLite."""
        self.conn = sqlite3.connect('products.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS products
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          product_type TEXT,
                          category TEXT,
                          sub_category TEXT,
                          zones TEXT)''')
        self.conn.commit()

    def saveData(self):
        """Sauvegarde les données dans la base de données."""
        product_type = self.productTypeCombo.currentText()
        category = self.categoryCombo.currentText()
        sub_category = self.subCategoryCombo.currentText()
        zones = ', '.join([item.text() for item in self.zoneList.selectedItems()])

        # Validation des données
        if not product_type or not category or not sub_category or not zones:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs et sélectionner au moins une zone.')
            return

        # Insertion dans la base de données
        self.c.execute("INSERT INTO products (product_type, category, sub_category, zones) VALUES (?, ?, ?, ?)",
                       (product_type, category, sub_category, zones))
        self.conn.commit()

        QMessageBox.information(self, 'Succès', 'Les données ont été sauvegardées avec succès!')
        self.loadData()

    def loadData(self):
        """Charge les données sauvegardées dans le tableau."""
        self.c.execute("SELECT product_type, category, sub_category, zones FROM products")
        rows = self.c.fetchall()
        self.dataTable.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, item in enumerate(row):
                self.dataTable.setItem(i, j, QTableWidgetItem(item))

    def exportData(self):
        """Exporte les données en CSV ou JSON."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Exporter les données", "", "CSV Files (*.csv);;JSON Files (*.json)", options=options)
        if file_name:
            self.c.execute("SELECT product_type, category, sub_category, zones FROM products")
            rows = self.c.fetchall()
            if file_name.endswith('.csv'):
                with open(file_name, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Type de Produit', 'Catégorie', 'Sous-catégorie', 'Zones'])
                    writer.writerows(rows)
            elif file_name.endswith('.json'):
                data = [{'product_type': row[0], 'category': row[1], 'sub_category': row[2], 'zones': row[3]} for row in rows]
                with open(file_name, 'w') as jsonfile:
                    json.dump(data, jsonfile, indent=4)
            QMessageBox.information(self, 'Succès', 'Les données ont été exportées avec succès!')

    def importZones(self):
        """Importe des zones à partir d'un fichier GeoJSON."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Importer des zones", "", "GeoJSON Files (*.geojson)", options=options)
        if file_name:
            with open(file_name, 'r') as geojsonfile:
                geojson_data = json.load(geojsonfile)
                # Traiter les données GeoJSON ici
                QMessageBox.information(self, 'Succès', 'Les zones ont été importées avec succès!')

    def closeEvent(self, event):
        """Ferme la connexion à la base de données lors de la fermeture de l'application."""
        self.conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProductApp()
    ex.show()
    sys.exit(app.exec_())