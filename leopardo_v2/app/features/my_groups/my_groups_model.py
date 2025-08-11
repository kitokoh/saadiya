import sqlite3
import pandas as pd
from ...core.database import get_db_path

class MyGroupsModel:
    def __init__(self):
        self.db_path = get_db_path()
        self._create_table_if_not_exists()
        self._load_initial_data()

    def _create_table_if_not_exists(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS my_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _load_initial_data(self):
        # No initial data for this model
        pass

    def get_groups(self):
        conn = sqlite3.connect(self.db_path)
        query = "SELECT name, description FROM my_groups"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def add_group(self, name, description):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO my_groups (name, description) VALUES (?, ?)", (name, description))
        conn.commit()
        conn.close()

    def update_group(self, index, name, description):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM my_groups LIMIT 1 OFFSET ?", (index,))
        row = cursor.fetchone()
        if row:
            group_id = row[0]
            cursor.execute("UPDATE my_groups SET name=?, description=? WHERE id=?", (name, description, group_id))
            conn.commit()
        conn.close()

    def delete_group(self, index):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM my_groups LIMIT 1 OFFSET ?", (index,))
        row = cursor.fetchone()
        if row:
            group_id = row[0]
            cursor.execute("DELETE FROM my_groups WHERE id=?", (group_id,))
            conn.commit()
        conn.close()
