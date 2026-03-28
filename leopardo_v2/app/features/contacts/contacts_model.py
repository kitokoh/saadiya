import sqlite3
import pandas as pd
from ...core.database import get_db_path

class ContactsModel:
    def __init__(self):
        self.db_path = get_db_path()
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def get_contacts(self):
        conn = sqlite3.connect(self.db_path)
        query = "SELECT name, email, phone FROM contacts"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def add_contact(self, name, email, phone):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
        conn.commit()
        conn.close()

    def update_contact(self, index, name, email, phone):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # To update by index, we need a reliable way to identify the row.
        # Assuming 'index' corresponds to the rowid or a specific query result order.
        # A more robust way would be to use a unique ID.
        # For this example, we'll fetch the id based on the index.
        cursor.execute("SELECT id FROM contacts LIMIT 1 OFFSET ?", (index,))
        row = cursor.fetchone()
        if row:
            contact_id = row[0]
            cursor.execute("UPDATE contacts SET name=?, email=?, phone=? WHERE id=?", (name, email, phone, contact_id))
            conn.commit()
        conn.close()

    def delete_contact(self, index):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Similar to update, we need a reliable way to identify the row to delete.
        cursor.execute("SELECT id FROM contacts LIMIT 1 OFFSET ?", (index,))
        row = cursor.fetchone()
        if row:
            contact_id = row[0]
            cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
            conn.commit()
        conn.close()

