import sqlite3
import os

class DatabaseService:
    def __init__(self, db_name="leopardo.db"):
        # Create a data directory if it doesn't exist
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        os.makedirs(data_dir, exist_ok=True)

        self.db_path = os.path.join(data_dir, db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Instances table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS instances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT,
            type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

    # --- Instance CRUD Methods ---
    def add_instance(self, name, status, type):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO instances (name, status, type) VALUES (?, ?, ?)", (name, status, type))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_instances(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, status, type FROM instances")
        return cursor.fetchall()

    def update_instance(self, instance_id, name, status, type):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE instances SET name = ?, status = ?, type = ? WHERE id = ?", (name, status, type, instance_id))
        self.conn.commit()

    def delete_instance(self, instance_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM instances WHERE id = ?", (instance_id,))
        self.conn.commit()

    def __del__(self):
        if self.conn:
            self.conn.close()

# Singleton instance of the database service
db_service = DatabaseService()
