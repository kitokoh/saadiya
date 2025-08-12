import sqlite3
import string
import random
from leopardo_v2.app.core.database import get_db_path

class ShortLinksModel:
    def __init__(self):
        self.db_path = get_db_path()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _generate_short_code(self, length=6):
        chars = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choice(chars) for _ in range(length))
            if not self.get_link_by_short_code(short_code):
                return short_code

    def create_short_link(self, original_url):
        short_code = self._generate_short_code()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO short_links (original_url, short_code) VALUES (?, ?)",
                (original_url, short_code)
            )
            conn.commit()
            return self.get_link(cursor.lastrowid)

    def get_all_links(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, original_url, short_code, click_count, creation_date FROM short_links ORDER BY creation_date DESC")
            return cursor.fetchall()

    def get_link(self, link_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM short_links WHERE id = ?", (link_id,))
            return cursor.fetchone()

    def get_link_by_short_code(self, short_code):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM short_links WHERE short_code = ?", (short_code,))
            return cursor.fetchone()

    def increment_click_count(self, link_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE short_links SET click_count = click_count + 1 WHERE id = ?",
                (link_id,)
            )
            conn.commit()

    def delete_link(self, link_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM short_links WHERE id = ?", (link_id,))
            conn.commit()
