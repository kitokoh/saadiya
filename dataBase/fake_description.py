from imports import DB_PATH_multilingual_text1
import os
import sqlite3
import os
import sqlite3
from datetime import datetime, timedelta
import random

class DatabaseManager:
    def __init__(self, db_name=DB_PATH_multilingual_text1):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        self.insert_sample_data()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS languages_text1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                code TEXT UNIQUE NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS descriptions_text1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(language_id) REFERENCES languages_text1(id)
            )
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_desc_timestamp_text1
            AFTER UPDATE ON descriptions_text1
            FOR EACH ROW
            BEGIN
                UPDATE descriptions_text1 SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
            END;
        """)

        self.conn.commit()

    def insert_sample_data(self):
        cursor = self.conn.cursor()

        languages = [
            ("Français", "fr"),
            ("Anglais", "en"),
            ("Arabe", "ar"),
            ("Turc", "tr")
        ]

        for name, code in languages:
            try:
                cursor.execute(
                    "INSERT INTO languages_text1 (name, code) VALUES (?, ?)",
                    (name, code)
                )
            except sqlite3.IntegrityError:
                pass

        cursor.execute("SELECT COUNT(*) FROM descriptions_text1")
        if cursor.fetchone()[0] == 0:
            self.insert_fake_descriptions()

        self.conn.commit()

    def insert_fake_descriptions(self):
        cursor = self.conn.cursor()

        fake_data = {
            "Français": [
                "Promotion exceptionnelle cette semaine seulement!\nProfitez-en vite!",
                "Nouvelle collection disponible dès maintenant\nDécouvrez nos nouveautés",
                "Livraison gratuite sur toutes les commandes\nValable jusqu'au 31 décembre",
                "Réduction de 50% sur une sélection d'articles\nDans la limite des stocks disponibles",
                "Abonnez-vous à notre newsletter pour des offres exclusives\nEt recevez un cadeau de bienvenue"
            ],
            "Anglais": [
                "Special promotion this week only!\nHurry up while stocks last!",
                "New collection available now\nDiscover our latest trends",
                "Free shipping on all orders\nValid until December 31st",
                "50% off on selected items\nWhile supplies last",
                "Subscribe to our newsletter for exclusive offers\nAnd get a welcome gift"
            ],
            "Arabe": [
                "ترقية استثنائية هذا الأسبوع فقط!\nاستفد منها بسرعة!",
                "مجموعة جديدة متاحة الآن\nاكتشف أحدث الاتجاهات لدينا",
                "شحن مجاني على جميع الطلبات\nصالحة حتى 31 ديسمبر",
                "خصم 50٪ على مجموعة مختارة من العناصر\nفي حدود الكميات المتوفرة",
                "اشترك في نشرتنا الإخبارية للحصول على عروض حصرية\nواحصل على هدية ترحيبية"
            ],
            "Turc": [
                "Xop lép kép xon fon qix!\nNox jox kox!",
                "Nox kolix zop fon pix!\nLix mix jop qox!",
                "Lix mix jop qox zix!\nPox rox dox!",
                "50% kox nox jix!\nZox qox lox!",
                "Sox rox nox dox lox!\nMox pox kox!"
            ]
        }

        for lang, descriptions in fake_data.items():
            cursor.execute("SELECT id FROM languages_text1 WHERE name = ?", (lang,))
            lang_id = cursor.fetchone()[0]

            for desc in descriptions:
                cursor.execute("""
                    INSERT INTO descriptions_text1 (language_id, content)
                    VALUES (?, ?)
                """, (lang_id, desc))

    def get_languages(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, code FROM languages_text1 ORDER BY name")
        return cursor.fetchall()

    def get_descriptions(self, language):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT d.id, d.content, d.created_at, d.updated_at
            FROM descriptions_text1 d
            JOIN languages_text1 l ON d.language_id = l.id
            WHERE l.name = ?
            ORDER BY d.created_at DESC
        """, (language,))
        return cursor.fetchall()

    def add_description(self, language, content):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM languages_text1 WHERE name = ?", (language,))
        lang_id = cursor.fetchone()[0]
        cursor.execute("""
            INSERT INTO descriptions_text1 (language_id, content)
            VALUES (?, ?)
        """, (lang_id, content))
        self.conn.commit()
        return cursor.lastrowid

    def update_description(self, desc_id, new_content):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE descriptions_text1
            SET content = ?
            WHERE id = ?
        """, (new_content, desc_id))
        self.conn.commit()

    def delete_description(self, desc_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM descriptions_text1 WHERE id = ?", (desc_id,))
        self.conn.commit()

    def search_descriptions(self, language, query):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT d.id, d.content
            FROM descriptions_text1 d
            JOIN languages_text1 l ON d.language_id = l.id
            WHERE l.name = ? AND d.content LIKE ?
            ORDER BY d.updated_at DESC
        """, (language, f"%{query}%"))
        return cursor.fetchall()

    def __del__(self):
        self.conn.close()
