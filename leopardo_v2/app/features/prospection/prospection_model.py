import sqlite3
from leopardo_v2.app.core.database import get_db_path
from datetime import date

class ProspectionModel:
    def __init__(self):
        self.db_path = get_db_path()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def add_prospect(self, name, contact_info, notes=""):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO prospection (prospect_name, contact_info, notes, last_follow_up) VALUES (?, ?, ?, ?)",
                (name, contact_info, notes, date.today())
            )
            conn.commit()
            return cursor.lastrowid

    def get_all_prospects(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, prospect_name, contact_info, status, last_follow_up, notes FROM prospection ORDER BY last_follow_up DESC")
            return cursor.fetchall()

    def get_prospect(self, prospect_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM prospection WHERE id = ?", (prospect_id,))
            return cursor.fetchone()

    def update_prospect(self, prospect_id, name, contact_info, status, notes):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE prospection SET prospect_name = ?, contact_info = ?, status = ?, notes = ?, last_follow_up = ? WHERE id = ?",
                (name, contact_info, status, notes, date.today(), prospect_id)
            )
            conn.commit()

    def update_follow_up_date(self, prospect_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE prospection SET last_follow_up = ? WHERE id = ?",
                (date.today(), prospect_id)
            )
            conn.commit()

    def delete_prospect(self, prospect_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM prospection WHERE id = ?", (prospect_id,))
            conn.commit()
