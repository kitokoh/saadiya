import sqlite3
import pandas as pd
from ...core.database import get_db_path

class CampaignSchedulerModel:
    def __init__(self):
        self.db_path = get_db_path()
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaign_scheduler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                platform TEXT NOT NULL,
                schedule TEXT,
                status TEXT
            )
        ''')
        # Add some initial data for demonstration if the table is empty
        cursor.execute("SELECT COUNT(*) FROM campaign_scheduler")
        if cursor.fetchone()[0] == 0:
            data = [
                ('Weekly Newsletter', 'Email', 'Every Friday at 9am', 'Active'),
                ('Daily Posts', 'Facebook', 'Every day at 12pm', 'Active')
            ]
            cursor.executemany("INSERT INTO campaign_scheduler (name, platform, schedule, status) VALUES (?, ?, ?, ?)", data)
        conn.commit()
        conn.close()

    def get_campaigns(self):
        conn = sqlite3.connect(self.db_path)
        query = "SELECT id, name, platform, schedule, status FROM campaign_scheduler"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def add_campaign(self, name, platform, schedule, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO campaign_scheduler (name, platform, schedule, status) VALUES (?, ?, ?, ?)", (name, platform, schedule, status))
        conn.commit()
        conn.close()

    def update_campaign(self, campaign_id, name, platform, schedule, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE campaign_scheduler SET name=?, platform=?, schedule=?, status=? WHERE id=?", (name, platform, schedule, status, campaign_id))
        conn.commit()
        conn.close()

    def delete_campaign(self, campaign_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM campaign_scheduler WHERE id=?", (campaign_id,))
        conn.commit()
        conn.close()
