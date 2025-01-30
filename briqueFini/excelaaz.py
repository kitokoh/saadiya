import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import Qt
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Excel-like Table with SQLite")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        self.add_column_button = QPushButton("Add Column", self)
        self.add_column_button.clicked.connect(self.add_column)
        self.layout.addWidget(self.add_column_button)

        self.import_button = QPushButton("Import Excel", self)
        self.import_button.clicked.connect(self.import_excel)
        self.layout.addWidget(self.import_button)

        self.db_connection = sqlite3.connect('data.db')
        self.create_tables()

        self.load_data()

    def create_tables(self):
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
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM main_data")
        rows = cursor.fetchall()

        if rows:
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(len(rows[0]) - 1)  # Exclude the ID column

            for i, row in enumerate(rows):
                for j, value in enumerate(row[1:]):  # Skip the ID column
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))

        self.update_headers()

    def update_headers(self):
        headers = [chr(65 + i) for i in range(self.table.columnCount())]
        self.table.setHorizontalHeaderLabels(headers)

    def add_column(self):
        current_column_count = self.table.columnCount()
        if current_column_count < 26:  # Only up to Z
            self.table.setColumnCount(current_column_count + 1)
            self.update_headers()

    def import_excel(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_name:
            df = pd.read_excel(file_name)
            self.table.setRowCount(df.shape[0])
            self.table.setColumnCount(df.shape[1])

            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    self.table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

            self.update_headers()

    def save_data(self):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM main_data")  # Clear existing data

        for i in range(self.table.rowCount()):
            row_data = [self.table.item(i, j).text() if self.table.item(i, j) else '' for j in range(self.table.columnCount())]
            cursor.execute(f"INSERT INTO main_data ({', '.join([chr(65 + j) for j in range(self.table.columnCount())])}) VALUES ({', '.join(['?'] * self.table.columnCount())})", row_data)

        self.db_connection.commit()

    def closeEvent(self, event):
        self.save_data()
        self.db_connection.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())