import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLineEdit, QTextEdit,
    QDateEdit, QLabel, QMessageBox, QFormLayout, QTabWidget, QInputDialog, QListWidgetItem, QComboBox, QDialog, QDialogButtonBox
)
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QIcon
import sqlite3

class ContactManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire de Contacts Complexes")
        self.setGeometry(100, 100, 1000, 800)

        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        self.init_db()
        self.init_ui()

    def init_db(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                modified_at TEXT,
                deleted_at TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS relatives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER,
                name TEXT NOT NULL,
                title TEXT NOT NULL,
                FOREIGN KEY(contact_id) REFERENCES contacts(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER,
                note TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(contact_id) REFERENCES contacts(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS discussions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER,
                last_discussed TEXT,
                next_discussion TEXT,
                FOREIGN KEY(contact_id) REFERENCES contacts(id)
            )
        ''')
        self.conn.commit()

    def init_ui(self):
        self.contact_tab = QWidget()
        self.contact_layout = QVBoxLayout()

        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher un contact...")
        self.search_input.textChanged.connect(self.search_contacts)
        self.search_layout.addWidget(self.search_input)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Tous", "Actifs", "Supprimés"])
        self.filter_combo.currentIndexChanged.connect(self.load_contacts)
        self.search_layout.addWidget(self.filter_combo)

        self.contact_layout.addLayout(self.search_layout)

        self.contact_form = QFormLayout()
        self.contact_name_input = QLineEdit()
        self.contact_form.addRow("Nom du Contact:", self.contact_name_input)

        self.add_contact_button = QPushButton("Ajouter Contact")
        self.add_contact_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_contact_button.clicked.connect(self.add_contact)
        self.contact_layout.addLayout(self.contact_form)
        self.contact_layout.addWidget(self.add_contact_button)

        self.contact_list_widget = QListWidget()
        self.contact_list_widget.itemClicked.connect(self.load_contact_details)
        self.contact_layout.addWidget(self.contact_list_widget)

        self.contact_tab.setLayout(self.contact_layout)
        self.central_widget.addTab(self.contact_tab, "Contacts")

        self.load_contacts()

    def load_contacts(self):
        self.contact_list_widget.clear()
        filter_text = self.filter_combo.currentText()
        query = "SELECT id, name FROM contacts WHERE deleted_at IS NULL"
        if filter_text == "Supprimés":
            query = "SELECT id, name FROM contacts WHERE deleted_at IS NOT NULL"
        elif filter_text == "Actifs":
            query = "SELECT id, name FROM contacts WHERE deleted_at IS NULL"

        self.cursor.execute(query)
        contacts = self.cursor.fetchall()
        for contact in contacts:
            item = QListWidgetItem(f"{contact[0]}: {contact[1]}")
            item.setData(Qt.UserRole, contact[0])
            self.contact_list_widget.addItem(item)

    def search_contacts(self):
        search_text = self.search_input.text()
        self.cursor.execute("SELECT id, name FROM contacts WHERE name LIKE ? AND deleted_at IS NULL", (f"%{search_text}%",))
        contacts = self.cursor.fetchall()
        self.contact_list_widget.clear()
        for contact in contacts:
            self.contact_list_widget.addItem(f"{contact[0]}: {contact[1]}")

    def add_contact(self):
        name = self.contact_name_input.text()
        if name:
            created_at = QDateTime.currentDateTime().toString(Qt.ISODate)
            self.cursor.execute("INSERT INTO contacts (name, created_at) VALUES (?, ?)", (name, created_at))
            self.conn.commit()
            self.load_contacts()
            self.contact_name_input.clear()
        else:
            QMessageBox.warning(self, "Erreur", "Le nom du contact ne peut pas être vide.")

    def load_contact_details(self, item):
        contact_id = item.data(Qt.UserRole)
        self.cursor.execute("SELECT name, created_at, modified_at FROM contacts WHERE id = ?", (contact_id,))
        contact_details = self.cursor.fetchone()

        self.details_tab = QWidget()
        self.details_layout = QVBoxLayout()

        self.details_form = QFormLayout()
        self.details_name_input = QLineEdit(contact_details[0])
        self.details_form.addRow("Nom du Contact:", self.details_name_input)

        self.details_created_at_label = QLabel(f"Créé le: {contact_details[1]}")
        self.details_form.addRow(self.details_created_at_label)

        if contact_details[2]:
            self.details_modified_at_label = QLabel(f"Modifié le: {contact_details[2]}")
            self.details_form.addRow(self.details_modified_at_label)

        self.update_contact_button = QPushButton("Mettre à jour")
        self.update_contact_button.setIcon(QIcon.fromTheme("document-save"))
        self.update_contact_button.clicked.connect(lambda: self.update_contact(contact_id))
        self.details_layout.addLayout(self.details_form)
        self.details_layout.addWidget(self.update_contact_button)

        self.add_relative_button = QPushButton("Ajouter un Proche")
        self.add_relative_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_relative_button.clicked.connect(lambda: self.add_relative(contact_id))
        self.details_layout.addWidget(self.add_relative_button)

        self.relatives_list_widget = QListWidget()
        self.load_relatives(contact_id)
        self.details_layout.addWidget(self.relatives_list_widget)

        self.add_note_button = QPushButton("Ajouter une Note")
        self.add_note_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_note_button.clicked.connect(lambda: self.add_note(contact_id))
        self.details_layout.addWidget(self.add_note_button)

        self.notes_list_widget = QListWidget()
        self.load_notes(contact_id)
        self.details_layout.addWidget(self.notes_list_widget)

        self.discussion_button = QPushButton("Planifier une Discussion")
        self.discussion_button.setIcon(QIcon.fromTheme("appointment-new"))
        self.discussion_button.clicked.connect(lambda: self.schedule_discussion(contact_id))
        self.details_layout.addWidget(self.discussion_button)

        self.details_tab.setLayout(self.details_layout)
        self.central_widget.addTab(self.details_tab, "Détails du Contact")

    def update_contact(self, contact_id):
        name = self.details_name_input.text()
        if name:
            modified_at = QDateTime.currentDateTime().toString(Qt.ISODate)
            self.cursor.execute("UPDATE contacts SET name = ?, modified_at = ? WHERE id = ?", (name, modified_at, contact_id))
            self.conn.commit()
            self.load_contacts()
            QMessageBox.information(self, "Succès", "Contact mis à jour avec succès.")
        else:
            QMessageBox.warning(self, "Erreur", "Le nom du contact ne peut pas être vide.")

    def add_relative(self, contact_id):
        name, ok = QInputDialog.getText(self, "Ajouter un Proche", "Nom du proche:")
        if ok and name:
            title, ok = QInputDialog.getText(self, "Ajouter un Proche", "Titre du proche:")
            if ok and title:
                self.cursor.execute("INSERT INTO relatives (contact_id, name, title) VALUES (?, ?, ?)", (contact_id, name, title))
                self.conn.commit()
                self.load_relatives(contact_id)

    def load_relatives(self, contact_id):
        self.relatives_list_widget.clear()
        self.cursor.execute("SELECT name, title FROM relatives WHERE contact_id = ?", (contact_id,))
        relatives = self.cursor.fetchall()
        for relative in relatives:
            self.relatives_list_widget.addItem(f"{relative[0]} ({relative[1]})")

    def add_note(self, contact_id):
        note, ok = QInputDialog.getText(self, "Ajouter une Note", "Note:")
        if ok and note:
            created_at = QDateTime.currentDateTime().toString(Qt.ISODate)
            self.cursor.execute("INSERT INTO notes (contact_id, note, created_at) VALUES (?, ?, ?)", (contact_id, note, created_at))
            self.conn.commit()
            self.load_notes(contact_id)

    def load_notes(self, contact_id):
        self.notes_list_widget.clear()
        self.cursor.execute("SELECT note, created_at FROM notes WHERE contact_id = ?", (contact_id,))
        notes = self.cursor.fetchall()
        for note in notes:
            self.notes_list_widget.addItem(f"{note[1]}: {note[0]}")

    def schedule_discussion(self, contact_id):
        dialog = QDialog(self)
        dialog.setWindowTitle("Planifier une Discussion")
        layout = QVBoxLayout()

        last_discussed_label = QLabel("Dernière discussion:")
        self.last_discussed_input = QDateEdit()
        layout.addWidget(last_discussed_label)
        layout.addWidget(self.last_discussed_input)

        next_discussion_label = QLabel("Prochaine discussion:")
        self.next_discussion_input = QDateEdit()
        layout.addWidget(next_discussion_label)
        layout.addWidget(self.next_discussion_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            last_discussed = self.last_discussed_input.date().toString(Qt.ISODate)
            next_discussion = self.next_discussion_input.date().toString(Qt.ISODate)
            self.cursor.execute("INSERT INTO discussions (contact_id, last_discussed, next_discussion) VALUES (?, ?, ?)", (contact_id, last_discussed, next_discussion))
            self.conn.commit()

    def delete_contact(self, contact_id):
        deleted_at = QDateTime.currentDateTime().toString(Qt.ISODate)
        self.cursor.execute("UPDATE contacts SET deleted_at = ? WHERE id = ?", (deleted_at, contact_id))
        self.conn.commit()
        self.load_contacts()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactManager()
    window.show()
    sys.exit(app.exec_())