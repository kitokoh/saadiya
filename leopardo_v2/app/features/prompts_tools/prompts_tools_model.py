import sqlite3
from leopardo_v2.app.core.database import get_db_path

class PromptsToolsModel:
    def __init__(self):
        self.db_path = get_db_path()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def add_prompt(self, title, prompt, category="General"):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO prompts_tools (title, prompt, category) VALUES (?, ?, ?)",
                (title, prompt, category)
            )
            conn.commit()
            return cursor.lastrowid

    def get_all_prompts(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, prompt, category FROM prompts_tools ORDER BY category, title")
            return cursor.fetchall()

    def get_prompts_by_category(self, category):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, prompt, category FROM prompts_tools WHERE category = ? ORDER BY title", (category,))
            return cursor.fetchall()

    def get_categories(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM prompts_tools ORDER BY category")
            return [row[0] for row in cursor.fetchall()]

    def update_prompt(self, prompt_id, title, prompt, category):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE prompts_tools SET title = ?, prompt = ?, category = ? WHERE id = ?",
                (title, prompt, category, prompt_id)
            )
            conn.commit()

    def delete_prompt(self, prompt_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM prompts_tools WHERE id = ?", (prompt_id,))
            conn.commit()
