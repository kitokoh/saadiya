import sqlite3
import pandas as pd
from ...core.database import get_db_path

class CrmModel:
    def __init__(self):
        self.db_path = get_db_path()
        self._create_table_if_not_exists()
        self._load_initial_data()

    def _create_table_if_not_exists(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crm (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                status TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _load_initial_data(self):
        # Initial data for demonstration
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM crm")
        if cursor.fetchone()[0] == 0:
            data = [
                ('Customer A', 'customer.a@example.com', '111-222-3333', 'Lead'),
                ('Customer B', 'customer.b@example.com', '444-555-6666', 'Contacted')
            ]
            cursor.executemany("INSERT INTO crm (name, email, phone, status) VALUES (?, ?, ?, ?)", data)
            conn.commit()
        conn.close()


    def get_customers(self):
        conn = sqlite3.connect(self.db_path)
        query = "SELECT name, email, phone, status FROM crm"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def add_customer(self, name, email, phone, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO crm (name, email, phone, status) VALUES (?, ?, ?, ?)", (name, email, phone, status))
        conn.commit()
        conn.close()

    def update_customer(self, index, name, email, phone, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM crm LIMIT 1 OFFSET ?", (index,))
        row = cursor.fetchone()
        if row:
            customer_id = row[0]
            cursor.execute("UPDATE crm SET name=?, email=?, phone=?, status=? WHERE id=?", (name, email, phone, status, customer_id))
            conn.commit()
        conn.close()

    def delete_customer(self, index):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM crm LIMIT 1 OFFSET ?", (index,))
        row = cursor.fetchone()
        if row:
            customer_id = row[0]
            cursor.execute("DELETE FROM crm WHERE id=?", (customer_id,))
            conn.commit()
        conn.close()
