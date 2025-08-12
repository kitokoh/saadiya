import sqlite3
from leopardo_v2.app.core.database import get_db_path

class SalesTemplatesModel:
    def __init__(self):
        self.db_path = get_db_path()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def add_template(self, title, content):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sales_templates (title, content) VALUES (?, ?)",
                (title, content)
            )
            conn.commit()
            return cursor.lastrowid

    def get_all_templates(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, content FROM sales_templates ORDER BY title")
            return cursor.fetchall()

    def get_template(self, template_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, content FROM sales_templates WHERE id = ?", (template_id,))
            return cursor.fetchone()

    def update_template(self, template_id, title, content):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE sales_templates SET title = ?, content = ? WHERE id = ?",
                (title, content, template_id)
            )
            conn.commit()

    def delete_template(self, template_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sales_templates WHERE id = ?", (template_id,))
            conn.commit()
