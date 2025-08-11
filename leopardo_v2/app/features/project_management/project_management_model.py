import sqlite3
import pandas as pd
from ...core.database import get_db_path

class ProjectManagementModel:
    def __init__(self):
        self.db_path = get_db_path()
        self._create_table_if_not_exists()
        self._load_initial_data()

    def _create_table_if_not_exists(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_management (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _load_initial_data(self):
        # Initial data for demonstration
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM project_management")
        if cursor.fetchone()[0] == 0:
            data = [
                ('Project Alpha', 'The first project', 'In Progress'),
                ('Project Beta', 'The second project', 'Completed')
            ]
            cursor.executemany("INSERT INTO project_management (name, description, status) VALUES (?, ?, ?)", data)
            conn.commit()
        conn.close()

    def get_projects(self):
        conn = sqlite3.connect(self.db_path)
        query = "SELECT name, description, status FROM project_management"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def add_project(self, name, description, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO project_management (name, description, status) VALUES (?, ?, ?)", (name, description, status))
        conn.commit()
        conn.close()

    def update_project(self, index, name, description, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM project_management LIMIT 1 OFFSET ?", (index,))
        row = cursor.fetchone()
        if row:
            project_id = row[0]
            cursor.execute("UPDATE project_management SET name=?, description=?, status=? WHERE id=?", (name, description, status, project_id))
            conn.commit()
        conn.close()

    def delete_project(self, index):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM project_management LIMIT 1 OFFSET ?", (index,))
        row = cursor.fetchone()
        if row:
            project_id = row[0]
            cursor.execute("DELETE FROM project_management WHERE id=?", (project_id,))
            conn.commit()
        conn.close()
