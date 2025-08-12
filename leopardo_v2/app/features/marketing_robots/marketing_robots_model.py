import pandas as pd
import sqlite3
from ...core.database import get_db_path

class MarketingRobotsModel:
    def __init__(self):
        self.db_path = get_db_path()
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS marketing_robots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                platform TEXT NOT NULL,
                status TEXT
            )
        ''')
        # Add some initial data for demonstration if the table is empty
        cursor.execute("SELECT COUNT(*) FROM marketing_robots")
        if cursor.fetchone()[0] == 0:
            data = [
                ('Facebook Group Poster', 'Facebook', 'Stopped'),
                ('Instagram Follower', 'Instagram', 'Running')
            ]
            cursor.executemany("INSERT INTO marketing_robots (name, platform, status) VALUES (?, ?, ?)", data)
        conn.commit()
        conn.close()

    def get_robots(self):
        conn = sqlite3.connect(self.db_path)
        query = "SELECT id, name, platform, status FROM marketing_robots"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def add_robot(self, name, platform, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO marketing_robots (name, platform, status) VALUES (?, ?, ?)", (name, platform, status))
        conn.commit()
        conn.close()

    def update_robot_status(self, robot_id, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE marketing_robots SET status=? WHERE id=?", (status, robot_id))
        conn.commit()
        conn.close()

    def delete_robot(self, robot_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM marketing_robots WHERE id=?", (robot_id,))
        conn.commit()
        conn.close()
