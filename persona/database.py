import sqlite3
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

class DatabaseManager(QObject):
    database_updated = pyqtSignal()

    def __init__(self, db_name="personas.db"):
        super().__init__()
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Table Personas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS personas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    role TEXT,
                    age INTEGER,
                    gender TEXT,
                    location TEXT,
                    education TEXT,
                    income_level TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table Goals
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    persona_id INTEGER,
                    description TEXT,
                    priority INTEGER,
                    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE
                )
            """)
            
            # Table PainPoints
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pain_points (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    persona_id INTEGER,
                    description TEXT,
                    severity INTEGER,
                    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE
                )
            """)
            
            # Table Behaviors
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS behaviors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    persona_id INTEGER,
                    description TEXT,
                    frequency TEXT,
                    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE
                )
            """)
            
            # Table Quotes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quotes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    persona_id INTEGER,
                    quote_text TEXT,
                    context TEXT,
                    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE
                )
            """)
            
            # Table Scenarios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scenarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    persona_id INTEGER,
                    title TEXT,
                    description TEXT,
                    steps TEXT,
                    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE
                )
            """)
            
            conn.commit()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def execute_query(self, query, params=(), fetch=False):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            conn.commit()
            self.database_updated.emit()

    def add_persona(self, persona_data):
        query = """
            INSERT INTO personas (name, role, age, gender, location, education, income_level)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.execute_query(query, (
            persona_data['name'],
            persona_data['role'],
            persona_data['age'],
            persona_data['gender'],
            persona_data['location'],
            persona_data['education'],
            persona_data['income_level']
        ))

    def get_all_personas(self):
        query = "SELECT * FROM personas ORDER BY name"
        return self.execute_query(query, fetch=True)

    def get_persona_details(self, persona_id):
        persona = self.execute_query("SELECT * FROM personas WHERE id = ?", (persona_id,), fetch=True)
        if persona:
            goals = self.execute_query("SELECT * FROM goals WHERE persona_id = ?", (persona_id,), fetch=True)
            pain_points = self.execute_query("SELECT * FROM pain_points WHERE persona_id = ?", (persona_id,), fetch=True)
            behaviors = self.execute_query("SELECT * FROM behaviors WHERE persona_id = ?", (persona_id,), fetch=True)
            quotes = self.execute_query("SELECT * FROM quotes WHERE persona_id = ?", (persona_id,), fetch=True)
            scenarios = self.execute_query("SELECT * FROM scenarios WHERE persona_id = ?", (persona_id,), fetch=True)
            
            return {
                'persona': persona[0],
                'goals': goals,
                'pain_points': pain_points,
                'behaviors': behaviors,
                'quotes': quotes,
                'scenarios': scenarios
            }
        return None

    def update_persona(self, persona_id, updated_data):
        query = """
            UPDATE personas 
            SET name = ?, role = ?, age = ?, gender = ?, location = ?, education = ?, income_level = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        self.execute_query(query, (
            updated_data['name'],
            updated_data['role'],
            updated_data['age'],
            updated_data['gender'],
            updated_data['location'],
            updated_data['education'],
            updated_data['income_level'],
            persona_id
        ))

    def delete_persona(self, persona_id):
        self.execute_query("DELETE FROM personas WHERE id = ?", (persona_id,))

    def add_goal(self, persona_id, description, priority):
        self.execute_query(
            "INSERT INTO goals (persona_id, description, priority) VALUES (?, ?, ?)",
            (persona_id, description, priority)
        )

    def add_pain_point(self, persona_id, description, severity):
        self.execute_query(
            "INSERT INTO pain_points (persona_id, description, severity) VALUES (?, ?, ?)",
            (persona_id, description, severity)
        )

    def add_behavior(self, persona_id, description, frequency):
        self.execute_query(
            "INSERT INTO behaviors (persona_id, description, frequency) VALUES (?, ?, ?)",
            (persona_id, description, frequency)
        )

    def add_quote(self, persona_id, quote_text, context):
        self.execute_query(
            "INSERT INTO quotes (persona_id, quote_text, context) VALUES (?, ?, ?)",
            (persona_id, quote_text, context)
        )

    def add_scenario(self, persona_id, title, description, steps):
        self.execute_query(
            "INSERT INTO scenarios (persona_id, title, description, steps) VALUES (?, ?, ?, ?)",
            (persona_id, title, description, steps)
        )
        