import sqlite3
import pandas as pd
from ...core.database import get_db_path

class DmsModel:
    def __init__(self):
        self.db_path = get_db_path()
        self._create_table_if_not_exists()
        self._load_initial_data()

    def _create_table_if_not_exists(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                type TEXT,
                path TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _load_initial_data(self):
        # Initial data for demonstration
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM dms")
        if cursor.fetchone()[0] == 0:
            data = [
                ('Quote 1', 'Quote', '/path/to/quote1.pdf'),
                ('Contract A', 'Contract', '/path/to/contract_a.pdf')
            ]
            cursor.executemany("INSERT INTO dms (title, type, path) VALUES (?, ?, ?)", data)
            conn.commit()
        conn.close()

    def get_documents(self):
        conn = sqlite3.connect(self.db_path)
        query = "SELECT title, type, path FROM dms"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def add_document(self, title, type, path):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dms (title, type, path) VALUES (?, ?, ?)", (title, type, path))
        conn.commit()
        conn.close()

    def update_document(self, index, title, type, path):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM dms LIMIT 1 OFFSET ?", (index,))
        row = cursor.fetchone()
        if row:
            document_id = row[0]
            cursor.execute("UPDATE dms SET title=?, type=?, path=? WHERE id=?", (title, type, path, document_id))
            conn.commit()
        conn.close()

    def delete_document(self, index):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM dms LIMIT 1 OFFSET ?", (index,))
        row = cursor.fetchone()
        if row:
            document_id = row[0]
            cursor.execute("DELETE FROM dms WHERE id=?", (document_id,))
            conn.commit()
        conn.close()
