import sqlite3
import pandas as pd
from ...core.database import get_db_path

class AdsManagerModel:
    def __init__(self):
        self.db_path = get_db_path()
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads_manager (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                platform TEXT NOT NULL,
                budget REAL,
                status TEXT
            )
        ''')
        # Add some initial data for demonstration if the table is empty
        cursor.execute("SELECT COUNT(*) FROM ads_manager")
        if cursor.fetchone()[0] == 0:
            data = [
                ('Summer Sale', 'Facebook', 500.00, 'Active'),
                ('New Product Launch', 'Instagram', 1000.00, 'Paused')
            ]
            cursor.executemany("INSERT INTO ads_manager (name, platform, budget, status) VALUES (?, ?, ?, ?)", data)
        conn.commit()
        conn.close()

    def get_campaigns(self):
        conn = sqlite3.connect(self.db_path)
        query = "SELECT id, name, platform, budget, status FROM ads_manager"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def add_campaign(self, name, platform, budget, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ads_manager (name, platform, budget, status) VALUES (?, ?, ?, ?)", (name, platform, budget, status))
        conn.commit()
        conn.close()

    def update_campaign_status(self, campaign_id, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE ads_manager SET status=? WHERE id=?", (status, campaign_id))
        conn.commit()
        conn.close()

    def update_campaign(self, campaign_id, name, platform, budget, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE ads_manager SET name=?, platform=?, budget=?, status=? WHERE id=?", (name, platform, budget, status, campaign_id))
        conn.commit()
        conn.close()

    def delete_campaign(self, campaign_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ads_manager WHERE id=?", (campaign_id,))
        conn.commit()
        conn.close()
