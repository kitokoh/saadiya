import sqlite3
from leopardo_v2.app.core.database import get_db_path

class SavModel:
    def __init__(self):
        self.db_path = get_db_path()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_ticket(self, customer_name, issue_description):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sav (customer_name, issue_description) VALUES (?, ?)",
                (customer_name, issue_description)
            )
            conn.commit()
            return cursor.lastrowid

    def get_all_tickets(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, customer_name, issue_description, status, creation_date FROM sav ORDER BY creation_date DESC")
            return cursor.fetchall()

    def get_ticket(self, ticket_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, customer_name, issue_description, status, creation_date FROM sav WHERE id = ?", (ticket_id,))
            return cursor.fetchone()

    def update_ticket_status(self, ticket_id, status):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE sav SET status = ? WHERE id = ?",
                (status, ticket_id)
            )
            conn.commit()

    def delete_ticket(self, ticket_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sav WHERE id = ?", (ticket_id,))
            conn.commit()
