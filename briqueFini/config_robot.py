import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
import sqlite3

class RobotConfigApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDB()

    def initUI(self):
        self.setWindowTitle('Configuration Robot')
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        layout = QVBoxLayout()

        # Champs de saisie
        self.reseau_input = QLineEdit(self)
        self.robot_input = QLineEdit(self)
        self.json1_input = QLineEdit(self)
        self.json2_input = QLineEdit(self)
        self.json3_input = QLineEdit(self)
        self.json4_input = QLineEdit(self)
        self.time_sleep_input = QLineEdit(self)

        # Ajout des champs de saisie au layout
        layout.addWidget(QLabel('Réseau:'))
        layout.addWidget(self.reseau_input)
        layout.addWidget(QLabel('Robot:'))
        layout.addWidget(self.robot_input)
        layout.addWidget(QLabel('JSON1:'))
        layout.addWidget(self.json1_input)
        layout.addWidget(QLabel('JSON2:'))
        layout.addWidget(self.json2_input)
        layout.addWidget(QLabel('JSON3:'))
        layout.addWidget(self.json3_input)
        layout.addWidget(QLabel('JSON4:'))
        layout.addWidget(self.json4_input)
        layout.addWidget(QLabel('Time Sleep:'))
        layout.addWidget(self.time_sleep_input)

        # Boutons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton('Sauvegarder', self)
        self.load_btn = QPushButton('Charger', self)
        self.clear_btn = QPushButton('Effacer', self)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.load_btn)
        btn_layout.addWidget(self.clear_btn)
        layout.addLayout(btn_layout)

        # Tableau pour afficher les configurations
        self.table = QTableWidget(self)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['ID', 'Réseau', 'Robot', 'JSON1', 'JSON2', 'JSON3', 'JSON4', 'Time Sleep'])
        layout.addWidget(self.table)

        # Connexion des boutons aux fonctions
        self.save_btn.clicked.connect(self.save_config)
        self.load_btn.clicked.connect(self.load_config)
        self.clear_btn.clicked.connect(self.clear_fields)

        self.setLayout(layout)

    def initDB(self):
        self.conn = sqlite3.connect('robot_config.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuration_robot (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reseau TEXT,
                robot TEXT,
                json1 TEXT,
                json2 TEXT,
                json3 TEXT,
                json4 TEXT,
                time_sleep TEXT
            )
        ''')
        self.conn.commit()

    def save_config(self):
        reseau = self.reseau_input.text()
        robot = self.robot_input.text()
        json1 = self.json1_input.text()
        json2 = self.json2_input.text()
        json3 = self.json3_input.text()
        json4 = self.json4_input.text()
        time_sleep = self.time_sleep_input.text()

        if reseau and robot and json1 and json2 and json3 and json4 and time_sleep:
            self.cursor.execute('''
                INSERT INTO configuration_robot (reseau, robot, json1, json2, json3, json4, time_sleep)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (reseau, robot, json1, json2, json3, json4, time_sleep))
            self.conn.commit()
            self.clear_fields()
            self.load_config()
        else:
            QMessageBox.warning(self, 'Erreur', 'Tous les champs doivent être remplis.')

    def load_config(self):
        self.cursor.execute('SELECT * FROM configuration_robot')
        rows = self.cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def clear_fields(self):
        self.reseau_input.clear()
        self.robot_input.clear()
        self.json1_input.clear()
        self.json2_input.clear()
        self.json3_input.clear()
        self.json4_input.clear()
        self.time_sleep_input.clear()

    def closeEvent(self, event):
        self.conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RobotConfigApp()
    ex.show()
    sys.exit(app.exec_())