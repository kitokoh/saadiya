import sqlite3
import pandas as pd
from ...core.database import get_db_path

class EmailSmsModel:
    def __init__(self):
        self.db_path = get_db_path()
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_sms_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                content TEXT,
                status TEXT
            )
        ''')
        # Add some initial data for demonstration if the table is empty
        cursor.execute("SELECT COUNT(*) FROM email_sms_campaigns")
        if cursor.fetchone()[0] == 0:
            data = [
                ('Welcome Email', 'Email', 'Welcome to our service!', 'Draft'),
                ('SMS Promo', 'SMS', 'Get 20% off this week!', 'Sent')
            ]
            cursor.executemany("INSERT INTO email_sms_campaigns (name, type, content, status) VALUES (?, ?, ?, ?)", data)
        conn.commit()
        conn.close()

    def get_campaigns(self):
        conn = sqlite3.connect(self.db_path)
        query = "SELECT id, name, type, content, status FROM email_sms_campaigns"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def add_campaign(self, name, type, content, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO email_sms_campaigns (name, type, content, status) VALUES (?, ?, ?, ?)", (name, type, content, status))
        conn.commit()
        conn.close()

    def update_campaign(self, campaign_id, name, type, content, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE email_sms_campaigns SET name=?, type=?, content=?, status=? WHERE id=?", (name, type, content, status, campaign_id))
        conn.commit()
        conn.close()

    def delete_campaign(self, campaign_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM email_sms_campaigns WHERE id=?", (campaign_id,))
        conn.commit()
        conn.close()
