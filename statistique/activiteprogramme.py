from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QTableWidgetItem
import subprocess

class Activite(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("Gestionnaire d'Activités Programmées"))
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                background-color: #f4f4f4;
            }
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #333;
            }
            QLineEdit {
                border: 1px solid #888;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border-radius: 5px;
                border: none;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
            }
            QHeaderView::section {
                background-color: #ddd;
                font-weight: bold;
                padding: 4px;
            }
        """)
        self.resize(1000, 700)

        # Titre principal
        title_label = QtWidgets.QLabel(self.tr("Activités Programmées"))
        title_label.setAlignment(QtCore.Qt.AlignCenter)

        # Barre de recherche et boutons
        self.search_entry = QtWidgets.QLineEdit()
        self.search_entry.setPlaceholderText(self.tr("Rechercher une activité..."))
        
        search_button = QtWidgets.QPushButton(self.tr("Rechercher"))
        search_button.clicked.connect(self.search_activities)

        add_button = QtWidgets.QPushButton(self.tr("Programmer une Activité"))
        add_button.clicked.connect(self.add_activity)

        pause_button = QtWidgets.QPushButton(self.tr("Mettre en Pause"))
        pause_button.clicked.connect(self.pause_activity)

        refresh_button = QtWidgets.QPushButton(self.tr("Charger les Activités"))
        refresh_button.clicked.connect(self.load_activities)

        # Layout pour la barre de recherche et les boutons
        top_bar_layout = QtWidgets.QHBoxLayout()
        top_bar_layout.addWidget(self.search_entry)
        top_bar_layout.addWidget(search_button)
        top_bar_layout.addWidget(add_button)
        top_bar_layout.addWidget(pause_button)
        top_bar_layout.addWidget(refresh_button)

        # Tableau des activités
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            self.tr("Numéro"), self.tr("Nom"), self.tr("Description"), 
            self.tr("Date Début"), self.tr("Date Prochaine")
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(True)

        # Disposition principale
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addLayout(top_bar_layout)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

        # Charger les activités programmées au démarrage
        QtCore.QTimer.singleShot(100, self.load_activities)

    def load_activities(self):
        self.table.setRowCount(0)
        try:
            result = subprocess.check_output("schtasks /query /fo csv /nh", shell=True, text=True)
            lines = result.strip().splitlines()
            for i, line in enumerate(lines):
                parts = [p.strip('"') for p in line.split(",")]
                row_data = [str(i + 1), parts[0], parts[1], parts[2], parts[3]]
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                for j, data in enumerate(row_data):
                    self.table.setItem(row_position, j, QTableWidgetItem(data))
        except Exception:
           # QMessageBox.warning(self, self.tr("Erreur"), self.tr("Impossible de charger les activités."))
           pass

    def add_activity(self):
        name, ok = QInputDialog.getText(self, self.tr("Nom de l'Activité"), self.tr("Entrez le nom de l'activité :"))
        if not ok or not name:
            return
        description, ok = QInputDialog.getText(self, self.tr("Description"), self.tr("Entrez une description :"))
        if not ok or not description:
            return
        date_debut, ok = QInputDialog.getText(self, self.tr("Date de Début"), self.tr("Entrez la date de début (JJ/MM/AAAA) :"))
        if not ok or not date_debut:
            return
        date_prochaine, ok = QInputDialog.getText(self, self.tr("Date Prochaine"), self.tr("Entrez la date de prochaine exécution (JJ/MM/AAAA) :"))
        if not ok or not date_prochaine:
            return

        try:
            QMessageBox.information(self, self.tr("Succès"), self.tr("Activité ajoutée avec succès!"))
            self.load_activities()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Erreur"), self.tr(f"Erreur lors de l'ajout de l'activité : {e}"))

    def pause_activity(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, self.tr("Avertissement"), self.tr("Veuillez sélectionner une activité à mettre en pause."))
            return

        activity_name = self.table.item(selected_row, 1).text()
        try:
            subprocess.run(f'schtasks /change /tn "{activity_name}" /disable', shell=True)
            QMessageBox.information(self, self.tr("Succès"), self.tr("Activité mise en pause avec succès!"))
            self.load_activities()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Erreur"), self.tr(f"Erreur lors de la mise en pause de l'activité : {e}"))

    def search_activities(self):
        search_term = self.search_entry.text().strip().lower()
        if not search_term:
            self.load_activities()
            return

        self.table.setRowCount(0)
        try:
            result = subprocess.check_output("schtasks /query /fo csv /nh", shell=True, text=True)
            lines = result.strip().splitlines()
            for i, line in enumerate(lines):
                parts = [p.strip('"') for p in line.split(",")]
                if search_term in parts[0].lower():
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)
                    for j, data in enumerate([str(i + 1), parts[0], parts[1], parts[2], parts[3]]):
                        self.table.setItem(row_position, j, QTableWidgetItem(data))
        except Exception:
           # QMessageBox.warning(self, self.tr("Erreur"), self.tr("Impossible de charger les activités."))
           pass

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     window = Activite()
#     window.show()
#     sys.exit(app.exec_())
