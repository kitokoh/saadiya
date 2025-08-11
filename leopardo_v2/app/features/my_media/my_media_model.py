import sqlite3
import pandas as pd
from ...core.database import get_db_path

class MyMediaModel:
    def __init__(self):
        self.db_path = get_db_path()
        self._create_table_if_not_exists()
        self._load_initial_data()

    def _create_table_if_not_exists(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS my_media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                type TEXT,
                path TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _load_initial_data(self):
        # No initial data for this model
        pass

    def get_media(self):
        conn = sqlite3.connect(self.db_path)
        query = "SELECT title, type, path FROM my_media"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def add_media(self, title, type, path):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO my_media (title, type, path) VALUES (?, ?, ?)", (title, type, path))
        conn.commit()
        conn.close()

    def update_media(self, index, title, type, path):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM my_media LIMIT 1 OFFSET ?", (index,))
        row = cursor.fetchone()
        if row:
            media_id = row[0]
            cursor.execute("UPDATE my_media SET title=?, type=?, path=? WHERE id=?", (title, type, path, media_id))
            conn.commit()
        conn.close()

    def delete_media(self, index):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM my_media LIMIT 1 OFFSET ?", (index,))
        row = cursor.fetchone()
        if row:
            media_id = row[0]
            cursor.execute("DELETE FROM my_media WHERE id=?", (media_id,))
            conn.commit()
        conn.close()
