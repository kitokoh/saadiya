import sys
import sqlite3
import csv
import json
from datetime import datetime
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
                            QListWidget, QListWidgetItem, QLabel, QLineEdit, QTextEdit,
                            QSpinBox, QComboBox, QPushButton, QFormLayout, QSplitter,
                            QMessageBox, QInputDialog, QFileDialog, QToolBar, QStatusBar,
                            QApplication, QDialog, QTableWidget, QTableWidgetItem,
                            QStyledItemDelegate, QHeaderView, QAction, QFileDialog, 
                            QGroupBox, QCheckBox, QScrollArea)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QTimer, QDate
from PyQt5.QtGui import QIcon, QColor, QFont, QPixmap, QPalette
from PyQt5.QtCore import QObject





class DatabaseManager(QObject):  # Hérite maintenant de QObject

    database_updated = pyqtSignal()

    def __init__(self, db_name="personas.db"):
        super().__init__()
        self.db_name = db_name
        self._init_db()
        self._add_initial_data()  # Ajout des données initiales

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
                industry TEXT,
                company_size TEXT,
                job_title TEXT,
                challenges TEXT,
                motivations TEXT,
                preferred_channels TEXT,
                decision_making TEXT,
                photo_path TEXT,
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
            
            # Table Journeys
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS journeys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    persona_id INTEGER,
                    stage TEXT,
                    actions TEXT,
                    touchpoints TEXT,
                    emotions TEXT,
                    opportunities TEXT,
                    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE
                )
            """)
            
            # Table Notes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    persona_id INTEGER,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE
                )
            """)
            





            # Ajouter après la création des tables dans DatabaseManager._init_db()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    color TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS persona_tags (
                    persona_id INTEGER,
                    tag_id INTEGER,
                    PRIMARY KEY (persona_id, tag_id),
                    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
                    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    data TEXT NOT NULL,  -- JSON data of the template
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)







            conn.commit()
    # Ajouter des données initiales
    def _add_initial_data(self):
        # Vérifier si des données existent déjà
        existing_personas = self.execute_query("SELECT COUNT(*) FROM personas", fetch_one=True)[0]
        if existing_personas == 0:
            # Ajouter des tags initiaux
            tags = [
                ("Client Premium", "#FF5733"),
                ("Nouveau Client", "#33FF57"),
                ("Fidèle", "#3357FF"),
                ("B2B", "#F033FF"),
                ("B2C", "#33FFF0")
            ]
            for name, color in tags:
                self.add_tag(name, color)

            # Ajouter des templates initiaux
            templates = [
                {
                    "name": "Entrepreneur Tech",
                    "description": "Propriétaire d'une startup technologique",
                    "data": {
                        "role": "Fondateur/CEO",
                        "industry": "Technologie",
                        "company_size": "Petite (10-49)",
                        "challenges": "Recrutement de talents, levée de fonds, scaling",
                        "motivations": "Croissance rapide, innovation, impact"
                    }
                },
                {
                    "name": "Mère de famille",
                    "description": "Mère active avec enfants",
                    "data": {
                        "gender": "Femme",
                        "age": 35,
                        "location": "Banlieue",
                        "challenges": "Manque de temps, budget serré",
                        "motivations": "Qualité de vie, éducation des enfants"
                    }
                }
            ]
            for template in templates:
                self.save_template(template["name"], template["description"], template["data"])

            # Ajouter des personas exemples
            example_personas = [
                {
                    "name": "Marie Dupont",
                    "role": "Directrice Marketing",
                    "age": 38,
                    "gender": "Femme",
                    "location": "Paris",
                    "education": "Master",
                    "income_level": "Élevé",
                    "industry": "Luxe",
                    "company_size": "Grande (250+)",
                    "job_title": "Directrice Marketing Digital",
                    "challenges": "Digitalisation du secteur, nouveaux canaux de communication",
                    "motivations": "Innovation, expérience client premium",
                    "preferred_channels": "LinkedIn, salons professionnels, emailing",
                    "decision_making": "Basé sur les données mais avec une approche créative"
                },
                {
                    "name": "Thomas Martin",
                    "role": "Entrepreneur",
                    "age": 32,
                    "gender": "Homme",
                    "location": "Lyon",
                    "education": "École de commerce",
                    "income_level": "Moyen",
                    "industry": "SaaS",
                    "company_size": "Petite (10-49)",
                    "job_title": "CEO & Co-fondateur",
                    "challenges": "Recrutement, acquisition clients, cashflow",
                    "motivations": "Croissance, impact, liberté",
                    "preferred_channels": "Twitter, événements networking, bouche-à-oreille",
                    "decision_making": "Rapide, basé sur l'intuition et les retours clients"
                }
            ]
            
            for persona_data in example_personas:
                persona_id = self.add_persona(persona_data)
                # Ajouter des tags aux personas exemples
                if persona_data["name"] == "Marie Dupont":
                    self.add_tag_to_persona(persona_id, 1)  # Client Premium
                    self.add_tag_to_persona(persona_id, 4)  # B2B
                elif persona_data["name"] == "Thomas Martin":
                    self.add_tag_to_persona(persona_id, 2)  # Nouveau Client
                    self.add_tag_to_persona(persona_id, 4)  # B2B

                # Ajouter des données complémentaires
                if persona_data["name"] == "Marie Dupont":
                    self.add_goal(persona_id, "Augmenter l'engagement digital de la marque", 1)
                    self.add_pain_point(persona_id, "Difficulté à mesurer le ROI des canaux digitaux", 3)
                    self.add_behavior(persona_id, "Participe à des conférences sur le luxe digital", "Mensuelle")
                    self.add_quote(persona_id, "Le digital doit servir l'expérience, pas la remplacer", 
                                "Lors d'une conférence sur l'avenir du luxe")
                    
                    # Customer journey
                    self.add_journey(
                        persona_id,
                        "Conscience",
                        "Recherche d'information sur les solutions digitales",
                        "Salons professionnels, recommandations collègues",
                        "Curiosité, besoin d'être rassurée",
                        "Présenter des études de cas pertinentes"
                    )
                    
                elif persona_data["name"] == "Thomas Martin":
                    self.add_goal(persona_id, "Atteindre le seuil de rentabilité", 1)
                    self.add_pain_point(persona_id, "Trouver les bons talents techniques", 4)
                    self.add_behavior(persona_id, "Teste constamment de nouveaux outils SaaS", "Hebdomadaire")
                    self.add_quote(persona_id, "Je préfère itérer rapidement qu'attendre la perfection", 
                                "Lors d'un podcast sur les startups")
                    
                    # Customer journey
                    self.add_journey(
                        persona_id,
                        "Décision",
                        "Comparaison des solutions, demande de démo",
                        "Site web, vidéos démo, avis en ligne",
                        "Prudent mais excité par les possibilités",
                        "Offrir un essai gratuit sans engagement"
                    )



    # Ajouter ces méthodes à la classe DatabaseManager
    def add_tag(self, name, color=None):
        self.execute_query(
            "INSERT INTO tags (name, color) VALUES (?, ?)",
            (name, color)
        )
        return self.execute_query("SELECT last_insert_rowid()", fetch_one=True)[0]

    def get_all_tags(self):
        return self.execute_query("SELECT id, name, color FROM tags ORDER BY name", fetch=True)

    def add_tag_to_persona(self, persona_id, tag_id):
        self.execute_query(
            "INSERT INTO persona_tags (persona_id, tag_id) VALUES (?, ?)",
            (persona_id, tag_id)
        )

    def remove_tag_from_persona(self, persona_id, tag_id):
        self.execute_query(
            "DELETE FROM persona_tags WHERE persona_id = ? AND tag_id = ?",
            (persona_id, tag_id)
        )

    def get_persona_tags(self, persona_id):
        return self.execute_query("""
            SELECT t.id, t.name, t.color 
            FROM tags t
            JOIN persona_tags pt ON t.id = pt.tag_id
            WHERE pt.persona_id = ?
        """, (persona_id,), fetch=True)

    def save_template(self, name, description, data):
        self.execute_query(
            "INSERT INTO templates (name, description, data) VALUES (?, ?, ?)",
            (name, description, json.dumps(data))
        )

    def get_all_templates(self):
        templates = self.execute_query("SELECT id, name, description, data FROM templates", fetch=True)
        return [(t[0], t[1], t[2], json.loads(t[3])) for t in templates]

    def delete_template(self, template_id):
        self.execute_query("DELETE FROM templates WHERE id = ?", (template_id,))


    def _get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def execute_query(self, query, params=(), fetch=False, fetch_one=False):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            elif fetch_one:
                return cursor.fetchone()
            conn.commit()
            self.database_updated.emit()

    def add_persona(self, persona_data):
        query = """
            INSERT INTO personas (
                name, role, age, gender, location, education, income_level,
                industry, company_size, job_title, challenges, motivations,
                preferred_channels, decision_making
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute_query(query, (
            persona_data['name'],
            persona_data.get('role', ''),
            persona_data.get('age', 0),
            persona_data.get('gender', ''),
            persona_data.get('location', ''),
            persona_data.get('education', ''),
            persona_data.get('income_level', ''),
            persona_data.get('industry', ''),
            persona_data.get('company_size', ''),
            persona_data.get('job_title', ''),
            persona_data.get('challenges', ''),
            persona_data.get('motivations', ''),
            persona_data.get('preferred_channels', ''),
            persona_data.get('decision_making', '')
        ))
        return self.execute_query("SELECT last_insert_rowid()", fetch_one=True)[0]

    def get_all_personas(self):
        query = "SELECT id, name, role, photo_path FROM personas ORDER BY name"
        return self.execute_query(query, fetch=True)

    def get_persona_details(self, persona_id):
        persona = self.execute_query("SELECT * FROM personas WHERE id = ?", (persona_id,), fetch_one=True)
        if persona:
            goals = self.execute_query("SELECT id, description, priority FROM goals WHERE persona_id = ?", (persona_id,), fetch=True)
            pain_points = self.execute_query("SELECT id, description, severity FROM pain_points WHERE persona_id = ?", (persona_id,), fetch=True)
            behaviors = self.execute_query("SELECT id, description, frequency FROM behaviors WHERE persona_id = ?", (persona_id,), fetch=True)
            quotes = self.execute_query("SELECT id, quote_text, context FROM quotes WHERE persona_id = ?", (persona_id,), fetch=True)
            scenarios = self.execute_query("SELECT id, title, description, steps FROM scenarios WHERE persona_id = ?", (persona_id,), fetch=True)
            journeys = self.execute_query("SELECT id, stage, actions, touchpoints, emotions, opportunities FROM journeys WHERE persona_id = ?", (persona_id,), fetch=True)
            notes = self.execute_query("SELECT id, content, created_at FROM notes WHERE persona_id = ? ORDER BY created_at DESC", (persona_id,), fetch=True)
            
            return {
                'persona': persona,
                'goals': goals,
                'pain_points': pain_points,
                'behaviors': behaviors,
                'quotes': quotes,
                'scenarios': scenarios,
                'journeys': journeys,
                'notes': notes
            }
        return None

    def update_persona(self, persona_id, updated_data):
        query = """
            UPDATE personas 
            SET name = ?, role = ?, age = ?, gender = ?, location = ?, 
                education = ?, income_level = ?, industry = ?, company_size = ?,
                job_title = ?, challenges = ?, motivations = ?, preferred_channels = ?,
                decision_making = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        self.execute_query(query, (
            updated_data['name'],
            updated_data.get('role', ''),
            updated_data.get('age', 0),
            updated_data.get('gender', ''),
            updated_data.get('location', ''),
            updated_data.get('education', ''),
            updated_data.get('income_level', ''),
            updated_data.get('industry', ''),
            updated_data.get('company_size', ''),
            updated_data.get('job_title', ''),
            updated_data.get('challenges', ''),
            updated_data.get('motivations', ''),
            updated_data.get('preferred_channels', ''),
            updated_data.get('decision_making', ''),
            persona_id
        ))

    def update_persona_photo(self, persona_id, photo_path):
        self.execute_query(
            "UPDATE personas SET photo_path = ? WHERE id = ?",
            (photo_path, persona_id)
        )

    def delete_persona(self, persona_id):
        self.execute_query("DELETE FROM personas WHERE id = ?", (persona_id,))

    def add_goal(self, persona_id, description, priority):
        self.execute_query(
            "INSERT INTO goals (persona_id, description, priority) VALUES (?, ?, ?)",
            (persona_id, description, priority)
        )

    def update_goal(self, goal_id, description, priority):
        self.execute_query(
            "UPDATE goals SET description = ?, priority = ? WHERE id = ?",
            (description, priority, goal_id)
        )

    def delete_goal(self, goal_id):
        self.execute_query("DELETE FROM goals WHERE id = ?", (goal_id,))

    def add_pain_point(self, persona_id, description, severity):
        self.execute_query(
            "INSERT INTO pain_points (persona_id, description, severity) VALUES (?, ?, ?)",
            (persona_id, description, severity)
        )

    def update_pain_point(self, pain_point_id, description, severity):
        self.execute_query(
            "UPDATE pain_points SET description = ?, severity = ? WHERE id = ?",
            (description, severity, pain_point_id)
        )

    def delete_pain_point(self, pain_point_id):
        self.execute_query("DELETE FROM pain_points WHERE id = ?", (pain_point_id,))

    def add_behavior(self, persona_id, description, frequency):
        self.execute_query(
            "INSERT INTO behaviors (persona_id, description, frequency) VALUES (?, ?, ?)",
            (persona_id, description, frequency)
        )

    def update_behavior(self, behavior_id, description, frequency):
        self.execute_query(
            "UPDATE behaviors SET description = ?, frequency = ? WHERE id = ?",
            (description, frequency, behavior_id)
        )

    def delete_behavior(self, behavior_id):
        self.execute_query("DELETE FROM behaviors WHERE id = ?", (behavior_id,))

    def add_quote(self, persona_id, quote_text, context):
        self.execute_query(
            "INSERT INTO quotes (persona_id, quote_text, context) VALUES (?, ?, ?)",
            (persona_id, quote_text, context)
        )

    def update_quote(self, quote_id, quote_text, context):
        self.execute_query(
            "UPDATE quotes SET quote_text = ?, context = ? WHERE id = ?",
            (quote_text, context, quote_id)
        )

    def delete_quote(self, quote_id):
        self.execute_query("DELETE FROM quotes WHERE id = ?", (quote_id,))

    def add_scenario(self, persona_id, title, description, steps):
        self.execute_query(
            "INSERT INTO scenarios (persona_id, title, description, steps) VALUES (?, ?, ?, ?)",
            (persona_id, title, description, steps)
        )

    def update_scenario(self, scenario_id, title, description, steps):
        self.execute_query(
            "UPDATE scenarios SET title = ?, description = ?, steps = ? WHERE id = ?",
            (title, description, steps, scenario_id)
        )

    def delete_scenario(self, scenario_id):
        self.execute_query("DELETE FROM scenarios WHERE id = ?", (scenario_id,))

    def add_journey(self, persona_id, stage, actions, touchpoints, emotions, opportunities):
        self.execute_query(
            """INSERT INTO journeys 
            (persona_id, stage, actions, touchpoints, emotions, opportunities) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (persona_id, stage, actions, touchpoints, emotions, opportunities)
        )

    def update_journey(self, journey_id, stage, actions, touchpoints, emotions, opportunities):
        self.execute_query(
            """UPDATE journeys SET 
            stage = ?, actions = ?, touchpoints = ?, emotions = ?, opportunities = ?
            WHERE id = ?""",
            (stage, actions, touchpoints, emotions, opportunities, journey_id)
        )

    def delete_journey(self, journey_id):
        self.execute_query("DELETE FROM journeys WHERE id = ?", (journey_id,))

    def add_note(self, persona_id, content):
        self.execute_query(
            "INSERT INTO notes (persona_id, content) VALUES (?, ?)",
            (persona_id, content)
        )

    def update_note(self, note_id, content):
        self.execute_query(
            "UPDATE notes SET content = ? WHERE id = ?",
            (content, note_id)
        )

    def delete_note(self, note_id):
        self.execute_query("DELETE FROM notes WHERE id = ?", (note_id,))

    def export_personas(self, file_path):
        personas = self.execute_query("SELECT * FROM personas", fetch=True)
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Role', 'Age', 'Gender', 'Location', 'Education', 
                           'Income Level', 'Industry', 'Company Size', 'Job Title', 'Challenges',
                           'Motivations', 'Preferred Channels', 'Decision Making', 'Photo Path',
                           'Created At', 'Updated At'])
            writer.writerows(personas)

    def import_personas(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                self.add_persona({
                    'name': row[1],
                    'role': row[2],
                    'age': int(row[3]) if row[3] else 0,
                    'gender': row[4],
                    'location': row[5],
                    'education': row[6],
                    'income_level': row[7],
                    'industry': row[8],
                    'company_size': row[9],
                    'job_title': row[10],
                    'challenges': row[11],
                    'motivations': row[12],
                    'preferred_channels': row[13],
                    'decision_making': row[14]
                })


class PersonaDesignerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Persona Designer Pro")
        self.setMinimumSize(1400, 900)
        self.current_persona_id = None
        self.dark_mode = False
        
        # Initialize database
        self.db = DatabaseManager()
        self.db.database_updated.connect(self._refresh_personas_list)
        
        # Setup UI
        self._setup_ui()
        self._refresh_personas_list()
        
        # Load last session
        self._load_settings()
        
    def _setup_ui(self):
        self._create_actions()
        self._create_menu()
        self._create_toolbar()
        self._create_main_layout()

        self._create_status_bar()
        self._apply_stylesheet()
        
    def _create_actions(self):
        # File Actions
        self.new_persona_action = QAction(QIcon("icons/add.png"), "Nouveau Persona", self)
        self.new_persona_action.setShortcut("Ctrl+N")
        self.new_persona_action.triggered.connect(self._create_persona)
        
        self.export_action = QAction(QIcon("icons/export.png"), "Exporter", self)
        self.export_action.setShortcut("Ctrl+E")
        self.export_action.triggered.connect(self._export_data)
        
        self.import_action = QAction(QIcon("icons/import.png"), "Importer", self)
        self.import_action.setShortcut("Ctrl+I")
        self.import_action.triggered.connect(self._import_data)
        
        self.exit_action = QAction("Quitter", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)
        
        # Edit Actions
        self.delete_action = QAction(QIcon("icons/delete.png"), "Supprimer", self)
        self.delete_action.setShortcut("Del")
        self.delete_action.triggered.connect(self._delete_persona)
        
        self.duplicate_action = QAction(QIcon("icons/duplicate.png"), "Dupliquer", self)
        self.duplicate_action.setShortcut("Ctrl+D")
        self.duplicate_action.triggered.connect(self._duplicate_persona)
        
        # View Actions
        self.dark_mode_action = QAction("Mode Sombre", self, checkable=True)
        self.dark_mode_action.triggered.connect(self._toggle_dark_mode)
        
        self.fullscreen_action = QAction("Plein écran", self, checkable=True)
        self.fullscreen_action.setShortcut("F11")
        self.fullscreen_action.triggered.connect(self._toggle_fullscreen)
        
        # Help Actions
        self.about_action = QAction("À propos", self)
        self.about_action.triggered.connect(self._show_about)
        
        self.help_action = QAction("Aide", self)
        self.help_action.setShortcut("F1")
        self.help_action.triggered.connect(self._show_help)



    # Implémentation des méthodes pour les templates
    def _create_from_template(self):
        templates = self.db.get_all_templates()
        if not templates:
            QMessageBox.information(self, "Information", "Aucun template disponible")
            return
        
        items = [f"{t[1]} - {t[2]}" for t in templates]
        item, ok = QInputDialog.getItem(
            self, 
            "Créer depuis Template",
            "Choisissez un template:",
            items,
            0, False
        )
        
        if ok and item:
            template_id = templates[items.index(item)][0]
            template_data = templates[items.index(item)][3]
            
            name, ok = QInputDialog.getText(
                self,
                "Nom du Persona",
                "Entrez le nom pour ce nouveau persona:",
                QLineEdit.Normal,
                f"Nouveau {template_data.get('name', 'Persona')}"
            )
            
            if ok and name:
                persona_data = {
                    'name': name,
                    'role': template_data.get('role', ''),
                    'age': template_data.get('age', 0),
                    'gender': template_data.get('gender', ''),
                    'location': template_data.get('location', ''),
                    'education': template_data.get('education', ''),
                    'income_level': template_data.get('income_level', ''),
                    'industry': template_data.get('industry', ''),
                    'company_size': template_data.get('company_size', ''),
                    'job_title': template_data.get('job_title', ''),
                    'challenges': template_data.get('challenges', ''),
                    'motivations': template_data.get('motivations', ''),
                    'preferred_channels': template_data.get('preferred_channels', ''),
                    'decision_making': template_data.get('decision_making', '')
                }
                
                persona_id = self.db.add_persona(persona_data)
                self._refresh_personas_list()
                
                # Sélectionner le nouveau persona
                for i in range(self.personas_list.count()):
                    item = self.personas_list.item(i)
                    if item.data(Qt.UserRole) == persona_id:
                        self.personas_list.setCurrentItem(item)
                        break

    def _manage_templates(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Gestion des Templates")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Liste des templates
        self.templates_table = QTableWidget()
        self.templates_table.setColumnCount(4)
        self.templates_table.setHorizontalHeaderLabels(["ID", "Nom", "Description", "Actions"])
        self.templates_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.templates_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.templates_table.verticalHeader().setVisible(False)
        self.templates_table.setColumnHidden(0, True)
        
        # Boutons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Nouveau Template")
        add_btn.setIcon(QIcon("icons/add.png"))
        add_btn.clicked.connect(self._add_new_template)
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(dialog.close)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        
        layout.addWidget(self.templates_table)
        layout.addLayout(btn_layout)
        
        # Charger les templates
        self._update_templates_table()
        
        dialog.exec_()

    def _update_templates_table(self):
        templates = self.db.get_all_templates()
        self.templates_table.setRowCount(len(templates))
        
        for row, template in enumerate(templates):
            # Ajouter les données
            self.templates_table.setItem(row, 0, QTableWidgetItem(str(template[0])))
            self.templates_table.setItem(row, 1, QTableWidgetItem(template[1]))
            self.templates_table.setItem(row, 2, QTableWidgetItem(template[2]))
            
            # Ajouter les boutons d'action
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_btn = QPushButton()
            edit_btn.setIcon(QIcon("icons/edit.png"))
            edit_btn.setFixedSize(24, 24)
            edit_btn.clicked.connect(lambda _, r=row: self._edit_template(r))
            
            del_btn = QPushButton()
            del_btn.setIcon(QIcon("icons/delete.png"))
            del_btn.setFixedSize(24, 24)
            del_btn.clicked.connect(lambda _, r=row: self._delete_template(r))
            
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(del_btn)
            
            self.templates_table.setCellWidget(row, 3, btn_widget)

    def _add_new_template(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nouveau Template")
        dialog.setMinimumWidth(500)
        
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        
        name_edit = QLineEdit()
        desc_edit = QLineEdit()
        data_edit = QTextEdit()
        data_edit.setPlaceholderText('''{
        "role": "",
        "age": 0,
        "gender": "",
        "industry": "",
        "challenges": "",
        "motivations": ""
    }''')
        
        form.addRow("Nom:", name_edit)
        form.addRow("Description:", desc_edit)
        form.addRow("Données (JSON):", data_edit)
        
        btn_box = QHBoxLayout()
        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(dialog.accept)
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(dialog.reject)
        
        btn_box.addWidget(save_btn)
        btn_box.addWidget(cancel_btn)
        
        layout.addLayout(form)
        layout.addLayout(btn_box)
        
        if dialog.exec_() == QDialog.Accepted:
            try:
                data = json.loads(data_edit.toPlainText())
                self.db.save_template(
                    name_edit.text(),
                    desc_edit.text(),
                    data
                )
                self._update_templates_table()
            except json.JSONDecodeError:
                QMessageBox.warning(self, "Erreur", "Le format JSON est invalide")

    # ... ajouter les méthodes _edit_template et _delete_template de manière similaire




    def _create_menu(self):


        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("Fichier")
        file_menu.addAction(self.new_persona_action)
        # file_menu.addAction(self.new_from_template_action)  # Ajouté
        file_menu.addAction(self.duplicate_action)
        file_menu.addSeparator()
        file_menu.addAction(self.export_action)
        file_menu.addAction(self.import_action)
        file_menu.addSeparator()
        # file_menu.addAction(self.manage_templates_action)  # Ajouté
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        
        # ... reste du cod
        

        # Edit Menu
        edit_menu = menubar.addMenu("Édition")
        edit_menu.addAction(self.delete_action)
        
        # View Menu
        view_menu = menubar.addMenu("Affichage")
        view_menu.addAction(self.dark_mode_action)
        view_menu.addAction(self.fullscreen_action)
        
        # Help Menu
        help_menu = menubar.addMenu("Aide")
        help_menu.addAction(self.help_action)
        help_menu.addAction(self.about_action)
    
    def _create_toolbar(self):
        toolbar = self.addToolBar("Outils")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        
        toolbar.addAction(self.new_persona_action)
        toolbar.addAction(self.duplicate_action)
        toolbar.addAction(self.delete_action)
        toolbar.addSeparator()
        toolbar.addAction(self.export_action)
        toolbar.addAction(self.import_action)
    
    def _create_status_bar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        self.last_update_label = QLabel()
        self.statusbar.addPermanentWidget(self.last_update_label)
        self._update_status_bar()
    
    def _create_main_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        splitter = QSplitter(Qt.Horizontal)
        
        # Personas List Section
        self.personas_list = QListWidget()
        self.personas_list.setFixedWidth(300)
        self.personas_list.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                border: none;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background: #3498db;
                color: white;
                border-radius: 4px;
            }
        """)
        self.personas_list.itemSelectionChanged.connect(self._load_persona_details)
        
        # Search Box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Rechercher des personas...")
        self.search_box.textChanged.connect(self._filter_personas_list)
        
        # Personas List Container
        personas_container = QWidget()
        personas_layout = QVBoxLayout(personas_container)
        personas_layout.setContentsMargins(0, 0, 0, 0)
        personas_layout.addWidget(QLabel("Personas"))
        personas_layout.addWidget(self.search_box)
        personas_layout.addWidget(self.personas_list)
        
        # Details Section
        self.details_widget = QTabWidget()
        self.details_widget.setTabPosition(QTabWidget.North)
        self._setup_details_tabs()
        
        splitter.addWidget(personas_container)
        splitter.addWidget(self.details_widget)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
    
    def _setup_details_tabs(self):
        # Profile Tab
        self.profile_tab = QWidget()
        self._setup_profile_tab()
        self.details_widget.addTab(self.profile_tab, QIcon("icons/profile.png"), "Profil")
        
        # Psychographics Tab
        self.psycho_tab = QWidget()
        self._setup_psycho_tab()
        self.details_widget.addTab(self.psycho_tab, QIcon("icons/brain.png"), "Psychographie")
        
        # Customer Journey Tab
        self.journey_tab = QWidget()
        self._setup_journey_tab()
        self.details_widget.addTab(self.journey_tab, QIcon("icons/journey.png"), "Parcours Client")
        
        # Scenarios Tab
        self.scenarios_tab = QWidget()
        self._setup_scenarios_tab()
        self.details_widget.addTab(self.scenarios_tab, QIcon("icons/scenario.png"), "Scénarios")
        
        # Notes Tab
        self.notes_tab = QWidget()
        self._setup_notes_tab()
        self.details_widget.addTab(self.notes_tab, QIcon("icons/notes.png"), "Notes")
    
    def _setup_profile_tab(self):
        layout = QVBoxLayout(self.profile_tab)
        
        # Top Section - Photo + Basic Info
        top_section = QHBoxLayout()
        
        # Photo Section
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(180, 180)
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                border-radius: 4px;
                background: white;
            }
        """)
        
        self.change_photo_btn = QPushButton("Changer la photo")
        self.change_photo_btn.setIcon(QIcon("icons/photo.png"))
        self.change_photo_btn.clicked.connect(self._change_photo)
        
        photo_layout = QVBoxLayout()
        photo_layout.addWidget(self.photo_label)
        photo_layout.addWidget(self.change_photo_btn, 0, Qt.AlignHCenter)
        photo_layout.setAlignment(Qt.AlignTop)
        top_section.addLayout(photo_layout)
        
        # Basic Info Section
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        self.name_edit = QLineEdit()
        self.role_edit = QLineEdit()
        self.age_spin = QSpinBox()
        self.age_spin.setRange(0, 120)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["", "Homme", "Femme", "Non-binaire", "Autre"])
        
        form_layout.addRow("Nom:", self.name_edit)
        form_layout.addRow("Rôle:", self.role_edit)
        form_layout.addRow("Âge:", self.age_spin)
        form_layout.addRow("Genre:", self.gender_combo)
        
        top_section.addLayout(form_layout)
        layout.addLayout(top_section)
        
        # Demographic Section
        demo_group = QGroupBox("Démographie")
        demo_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        
        demo_layout = QFormLayout(demo_group)
        self.location_edit = QLineEdit()
        self.education_combo = QComboBox()
        self.education_combo.addItems(["", "Primaire", "Secondaire", "Bac", "Licence", "Master", "Doctorat"])
        self.income_combo = QComboBox()
        self.income_combo.addItems(["", "Faible", "Moyen", "Élevé"])
        
        demo_layout.addRow("Localisation:", self.location_edit)
        demo_layout.addRow("Éducation:", self.education_combo)
        demo_layout.addRow("Revenu:", self.income_combo)
        
        # Professional Section
        prof_group = QGroupBox("Professionnel")
        prof_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        
        prof_layout = QFormLayout(prof_group)
        self.industry_edit = QLineEdit()
        self.company_size_combo = QComboBox()
        self.company_size_combo.addItems(["", "Micro (1-9)", "Petite (10-49)", "Moyenne (50-249)", "Grande (250+)", "Entreprise"])
        self.job_title_edit = QLineEdit()
        
        prof_layout.addRow("Industrie:", self.industry_edit)
        prof_layout.addRow("Taille entreprise:", self.company_size_combo)
        prof_layout.addRow("Poste:", self.job_title_edit)
        
        # Two columns layout
        cols_layout = QHBoxLayout()
        cols_layout.addWidget(demo_group)
        cols_layout.addWidget(prof_group)
        layout.addLayout(cols_layout)
        
        # Additional Info Section
        add_group = QGroupBox("Informations Complémentaires")
        add_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        
        add_layout = QFormLayout(add_group)
        self.challenges_edit = QTextEdit()
        self.challenges_edit.setMaximumHeight(80)
        self.motivations_edit = QTextEdit()
        self.motivations_edit.setMaximumHeight(80)
        self.channels_edit = QTextEdit()
        self.channels_edit.setMaximumHeight(80)
        self.decision_edit = QTextEdit()
        self.decision_edit.setMaximumHeight(80)
        
        add_layout.addRow("Défis:", self.challenges_edit)
        add_layout.addRow("Motivations:", self.motivations_edit)
        add_layout.addRow("Canaux préférés:", self.channels_edit)
        add_layout.addRow("Processus décisionnel:", self.decision_edit)
        
        layout.addWidget(add_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Enregistrer")
        self.save_btn.setIcon(QIcon("icons/save.png"))
        self.save_btn.setStyleSheet("background: #27ae60; color: white;")
        self.save_btn.clicked.connect(self._save_persona)
        
        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.setIcon(QIcon("icons/cancel.png"))
        self.cancel_btn.setStyleSheet("background: #e74c3c; color: white;")
        self.cancel_btn.clicked.connect(self._cancel_edits)
        
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)



        # Dans PersonaDesignerApp._setup_profile_tab(), ajouter après les autres champs
        # Section Tags
        tags_group = QGroupBox("Tags")
        tags_layout = QVBoxLayout(tags_group)

        self.tags_list = QListWidget()
        self.tags_list.setSelectionMode(QListWidget.MultiSelection)
        self.tags_list.setFixedHeight(100)

        self.add_tag_combo = QComboBox()
        self.add_tag_btn = QPushButton("Ajouter Tag")
        self.add_tag_btn.setIcon(QIcon("icons/add.png"))
        self.add_tag_btn.clicked.connect(self._add_tag_to_persona)

        tag_controls = QHBoxLayout()
        tag_controls.addWidget(self.add_tag_combo)
        tag_controls.addWidget(self.add_tag_btn)

        tags_layout.addWidget(QLabel("Tags associés:"))
        tags_layout.addWidget(self.tags_list)
        tags_layout.addLayout(tag_controls)

        layout.insertWidget(3, tags_group)  # Ajouter après les infos de base




    # Nouvelle méthode pour gérer les tags
    def _update_tags_display(self):
        if not self.current_persona_id:
            return
        
        # Mettre à jour la liste des tags disponibles
        all_tags = self.db.get_all_tags()
        self.add_tag_combo.clear()
        for tag in all_tags:
            self.add_tag_combo.addItem(tag[1], tag[0])
        
        # Mettre à jour les tags du persona
        persona_tags = self.db.get_persona_tags(self.current_persona_id)
        self.tags_list.clear()
        for tag in persona_tags:
            item = QListWidgetItem(tag[1])
            item.setData(Qt.UserRole, tag[0])
            if tag[2]:  # Si une couleur est définie
                item.setBackground(QColor(tag[2]))
            self.tags_list.addItem(item)

    def _add_tag_to_persona(self):
        if not self.current_persona_id:
            return
        
        tag_id = self.add_tag_combo.currentData()
        if tag_id:
            self.db.add_tag_to_persona(self.current_persona_id, tag_id)
            self._update_tags_display()







    def _setup_psycho_tab(self):
        layout = QVBoxLayout(self.psycho_tab)
        
        # Goals Section
        goals_group = QGroupBox("Objectifs")
        goals_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        goals_layout = QVBoxLayout(goals_group)
        
        self.goals_table = QTableWidget()
        self.goals_table.setColumnCount(4)
        self.goals_table.setHorizontalHeaderLabels(["ID", "Objectif", "Priorité", "Actions"])
        self.goals_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.goals_table.verticalHeader().setVisible(False)
        self.goals_table.setColumnHidden(0, True)
        
        add_goal_btn = QPushButton("Ajouter un objectif")
        add_goal_btn.setIcon(QIcon("icons/add.png"))
        add_goal_btn.clicked.connect(lambda: self._add_table_item("goal"))
        
        goals_layout.addWidget(self.goals_table)
        goals_layout.addWidget(add_goal_btn)
        
        # Pain Points Section
        pains_group = QGroupBox("Points de Douleur")
        pains_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        pains_layout = QVBoxLayout(pains_group)
        
        self.pains_table = QTableWidget()
        self.pains_table.setColumnCount(4)
        self.pains_table.setHorizontalHeaderLabels(["ID", "Point de douleur", "Sévérité", "Actions"])
        self.pains_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.pains_table.verticalHeader().setVisible(False)
        self.pains_table.setColumnHidden(0, True)
        
        add_pain_btn = QPushButton("Ajouter un point de douleur")
        add_pain_btn.setIcon(QIcon("icons/add.png"))
        add_pain_btn.clicked.connect(lambda: self._add_table_item("pain_point"))
        
        pains_layout.addWidget(self.pains_table)
        pains_layout.addWidget(add_pain_btn)
        
        # Behaviors Section
        behaviors_group = QGroupBox("Comportements")
        behaviors_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        behaviors_layout = QVBoxLayout(behaviors_group)
        
        self.behaviors_table = QTableWidget()
        self.behaviors_table.setColumnCount(4)
        self.behaviors_table.setHorizontalHeaderLabels(["ID", "Comportement", "Fréquence", "Actions"])
        self.behaviors_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.behaviors_table.verticalHeader().setVisible(False)
        self.behaviors_table.setColumnHidden(0, True)
        
        add_behavior_btn = QPushButton("Ajouter un comportement")
        add_behavior_btn.setIcon(QIcon("icons/add.png"))
        add_behavior_btn.clicked.connect(lambda: self._add_table_item("behavior"))
        
        behaviors_layout.addWidget(self.behaviors_table)
        behaviors_layout.addWidget(add_behavior_btn)
        
        # Quotes Section
        quotes_group = QGroupBox("Citations")
        quotes_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        quotes_layout = QVBoxLayout(quotes_group)
        
        self.quotes_table = QTableWidget()
        self.quotes_table.setColumnCount(4)
        self.quotes_table.setHorizontalHeaderLabels(["ID", "Citation", "Contexte", "Actions"])
        self.quotes_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.quotes_table.verticalHeader().setVisible(False)
        self.quotes_table.setColumnHidden(0, True)
        
        add_quote_btn = QPushButton("Ajouter une citation")
        add_quote_btn.setIcon(QIcon("icons/add.png"))
        add_quote_btn.clicked.connect(lambda: self._add_table_item("quote"))
        
        quotes_layout.addWidget(self.quotes_table)
        quotes_layout.addWidget(add_quote_btn)
        
        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.addWidget(goals_group)
        container_layout.addWidget(pains_group)
        container_layout.addWidget(behaviors_group)
        container_layout.addWidget(quotes_group)
        container_layout.addStretch()
        
        scroll.setWidget(container)
        layout.addWidget(scroll)
    
    def _setup_journey_tab(self):
        layout = QVBoxLayout(self.journey_tab)
        
        self.journey_table = QTableWidget()
        self.journey_table.setColumnCount(7)
        self.journey_table.setHorizontalHeaderLabels(["ID", "Étape", "Actions", "Points de Contact", "Émotions", "Opportunités", "Actions"])
        self.journey_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.journey_table.verticalHeader().setVisible(False)
        self.journey_table.setColumnHidden(0, True)
        
        add_journey_btn = QPushButton("Ajouter une étape")
        add_journey_btn.setIcon(QIcon("icons/add.png"))
        add_journey_btn.clicked.connect(lambda: self._add_table_item("journey"))
        
        layout.addWidget(self.journey_table)
        layout.addWidget(add_journey_btn)
    
    def _setup_scenarios_tab(self):
        layout = QVBoxLayout(self.scenarios_tab)
        
        self.scenarios_table = QTableWidget()
        self.scenarios_table.setColumnCount(5)
        self.scenarios_table.setHorizontalHeaderLabels(["ID", "Titre", "Description", "Étapes", "Actions"])
        self.scenarios_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.scenarios_table.verticalHeader().setVisible(False)
        self.scenarios_table.setColumnHidden(0, True)
        
        add_scenario_btn = QPushButton("Ajouter un scénario")
        add_scenario_btn.setIcon(QIcon("icons/add.png"))
        add_scenario_btn.clicked.connect(lambda: self._add_table_item("scenario"))
        
        layout.addWidget(self.scenarios_table)
        layout.addWidget(add_scenario_btn)
    
    def _setup_notes_tab(self):
        layout = QVBoxLayout(self.notes_tab)
        
        # Notes List
        self.notes_list = QListWidget()
        self.notes_list.setStyleSheet("QListWidget { border: none; }")
        
        # Note Editor
        self.note_edit = QTextEdit()
        self.note_edit.setPlaceholderText("Écrivez votre note ici...")
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.add_note_btn = QPushButton("Ajouter")
        self.add_note_btn.setIcon(QIcon("icons/add.png"))
        self.add_note_btn.clicked.connect(self._add_note)
        
        self.save_note_btn = QPushButton("Enregistrer")
        self.save_note_btn.setIcon(QIcon("icons/save.png"))
        self.save_note_btn.clicked.connect(self._save_note)
        
        self.delete_note_btn = QPushButton("Supprimer")
        self.delete_note_btn.setIcon(QIcon("icons/delete.png"))
        self.delete_note_btn.clicked.connect(self._delete_note)
        
        btn_layout.addWidget(self.add_note_btn)
        btn_layout.addWidget(self.save_note_btn)
        btn_layout.addWidget(self.delete_note_btn)
        
        # Splitter for list and editor
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.notes_list)
        splitter.addWidget(self.note_edit)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter)
        layout.addLayout(btn_layout)
        
        # Connect signals
        self.notes_list.currentItemChanged.connect(self._load_note_content)
    
    def _apply_stylesheet(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2c3e50;
                }
                QWidget {
                    background-color: #34495e;
                    color: #ecf0f1;
                    border: 1px solid #2c3e50;
                }
                QListWidget, QTableWidget, QTextEdit, QLineEdit, QSpinBox, QComboBox {
                    background-color: #2c3e50;
                    color: #ecf0f1;
                    border: 1px solid #7f8c8d;
                }
                QTabWidget::pane {
                    border: 1px solid #7f8c8d;
                    background: #34495e;
                }
                QTabBar::tab {
                    background: #2c3e50;
                    color: #ecf0f1;
                    padding: 8px;
                    border: 1px solid #7f8c8d;
                    border-bottom: none;
                }
                QTabBar::tab:selected {
                    background: #34495e;
                    border-bottom: 2px solid #3498db;
                }
                QPushButton {
                    background: #3498db;
                    color: white;
                    padding: 5px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background: #2980b9;
                }
                QGroupBox {
                    border: 1px solid #7f8c8d;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 15px;
                }
                QHeaderView::section {
                    background-color: #3498db;
                    color: white;
                    padding: 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f5f5f5;
                }
                QWidget {
                    background-color: white;
                    color: #333;
                }
                QListWidget, QTableWidget, QTextEdit, QLineEdit, QSpinBox, QComboBox {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
                QTabWidget::pane {
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    background: white;
                }
                QTabBar::tab {
                    background: #e0e0e0;
                    color: #333;
                    padding: 8px;
                    border: 1px solid #ddd;
                    border-bottom: none;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background: white;
                    border-bottom: 2px solid #3498db;
                }
                QPushButton {
                    background: #3498db;
                    color: white;
                    padding: 5px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background: #2980b9;
                }
                QGroupBox {
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 15px;
                }
                QHeaderView::section {
                    background-color: #3498db;
                    color: white;
                    padding: 5px;
                }
            """)
    
    def _refresh_personas_list(self):
        self.personas_list.clear()
        personas = self.db.get_all_personas()
        for persona in personas:
            item = QListWidgetItem(persona[1])
            item.setData(Qt.UserRole, persona[0])
            
            # Add icon if photo exists
            if persona[3]:  # photo_path
                item.setIcon(QIcon(persona[3]))
            
            self.personas_list.addItem(item)
        
        self._update_status_bar()
    
    def _filter_personas_list(self):
        search_text = self.search_box.text().lower()
        for i in range(self.personas_list.count()):
            item = self.personas_list.item(i)
            item.setHidden(search_text not in item.text().lower())
    
    def _load_persona_details(self):
        selected = self.personas_list.selectedItems()
        if not selected:
            self.current_persona_id = None
            self._clear_details()
            return
            
        persona_id = selected[0].data(Qt.UserRole)
        self.current_persona_id = persona_id
        
        # Load data from database
        persona_data = self.db.get_persona_details(persona_id)
        
        # Update UI
        if persona_data:
            persona = persona_data['persona']
            
            # Basic Info
            self.name_edit.setText(persona[1])
            self.role_edit.setText(persona[2])
            self.age_spin.setValue(persona[3] if persona[3] else 0)
            self.gender_combo.setCurrentText(persona[4])
            
            # Demographic Info
            self.location_edit.setText(persona[5])
            self.education_combo.setCurrentText(persona[6])
            self.income_combo.setCurrentText(persona[7])
            
            # Professional Info
            self.industry_edit.setText(persona[8])
            self.company_size_combo.setCurrentText(persona[9])
            self.job_title_edit.setText(persona[10])
            
            # Additional Info
            self.challenges_edit.setText(persona[11])
            self.motivations_edit.setText(persona[12])
            self.channels_edit.setText(persona[13])
            self.decision_edit.setText(persona[14])
            
            # Load photo if exists
            if persona[15]:  # photo_path
                self._load_photo(persona[15])
            else:
                self.photo_label.clear()
                self.photo_label.setText("Aucune photo")
            
            # Update tables
            self._update_table(self.goals_table, persona_data['goals'])
            self._update_table(self.pains_table, persona_data['pain_points'])
            self._update_table(self.behaviors_table, persona_data['behaviors'])
            self._update_table(self.quotes_table, persona_data['quotes'])
            self._update_table(self.scenarios_table, persona_data['scenarios'])
            self._update_table(self.journey_table, persona_data['journeys'])
            
            # Update notes
            self._update_notes_list(persona_data['notes'])
            
            self._update_tags_display()



    # Ajouter un menu pour gérer les templates
    def _create_template_actions(self):
        self.new_from_template_action = QAction(QIcon("icons/template.png"), "Nouveau depuis Template", self)
        self.new_from_template_action.triggered.connect(self._create_from_template)
        
        self.manage_templates_action = QAction("Gérer les Templates", self)
        self.manage_templates_action.triggered.connect(self._manage_templates)




    def _clear_details(self):
        # Clear all fields
        self.name_edit.clear()
        self.role_edit.clear()
        self.age_spin.setValue(0)
        self.gender_combo.setCurrentIndex(0)
        self.location_edit.clear()
        self.education_combo.setCurrentIndex(0)
        self.income_combo.setCurrentIndex(0)
        self.industry_edit.clear()
        self.company_size_combo.setCurrentIndex(0)
        self.job_title_edit.clear()
        self.challenges_edit.clear()
        self.motivations_edit.clear()
        self.channels_edit.clear()
        self.decision_edit.clear()
        
        # Clear photo
        self.photo_label.clear()
        self.photo_label.setText("Aucune photo")
        
        # Clear tables
        self.goals_table.setRowCount(0)
        self.pains_table.setRowCount(0)
        self.behaviors_table.setRowCount(0)
        self.quotes_table.setRowCount(0)
        self.scenarios_table.setRowCount(0)
        self.journey_table.setRowCount(0)
        
        # Clear notes
        self.notes_list.clear()
        self.note_edit.clear()
    
    def _update_table(self, table, data):
        table.setRowCount(len(data))
        
        for row, item in enumerate(data):
            # Add data to columns
            for col in range(len(item)):
                table.setItem(row, col, QTableWidgetItem(str(item[col])))
            
            # Add action buttons
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_btn = QPushButton()
            edit_btn.setIcon(QIcon("icons/edit.png"))
            edit_btn.setFixedSize(24, 24)
            edit_btn.clicked.connect(lambda _, r=row, t=table: self._edit_table_item(r, t))
            
            del_btn = QPushButton()
            del_btn.setIcon(QIcon("icons/delete.png"))
            del_btn.setFixedSize(24, 24)
            del_btn.clicked.connect(lambda _, r=row, t=table: self._delete_table_item(r, t))
            
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(del_btn)
            
            table.setCellWidget(row, table.columnCount()-1, btn_widget)
    
    def _update_notes_list(self, notes):
        self.notes_list.clear()
        for note in notes:
            item = QListWidgetItem(note[2][:20] + "...")  # Truncate date
            item.setData(Qt.UserRole, note[0])  # Store note ID
            self.notes_list.addItem(item)
        
        if self.notes_list.count() > 0:
            self.notes_list.setCurrentRow(0)
    
    def _load_note_content(self, current, previous):
        if not current:
            self.note_edit.clear()
            return
            
        note_id = current.data(Qt.UserRole)
        note = self.db.execute_query(
            "SELECT content FROM notes WHERE id = ?", 
            (note_id,), 
            fetch_one=True
        )
        
        if note:
            self.note_edit.setText(note[0])
    
    def _create_persona(self):
        name, ok = QInputDialog.getText(
            self, 
            "Nouveau Persona", 
            "Nom du persona:",
            QLineEdit.Normal,
            "Nouveau Persona"
        )
        
        if ok and name:
            persona_id = self.db.add_persona({
                'name': name,
                'role': '',
                'age': 0,
                'gender': '',
                'location': '',
                'education': '',
                'income_level': '',
                'industry': '',
                'company_size': '',
                'job_title': '',
                'challenges': '',
                'motivations': '',
                'preferred_channels': '',
                'decision_making': ''
            })
            
            self._refresh_personas_list()
            
            # Select the newly created persona
            for i in range(self.personas_list.count()):
                item = self.personas_list.item(i)
                if item.data(Qt.UserRole) == persona_id:
                    self.personas_list.setCurrentItem(item)
                    break
    
    def _duplicate_persona(self):
        selected = self.personas_list.selectedItems()
        if not selected:
            return
            
        persona_id = selected[0].data(Qt.UserRole)
        persona_data = self.db.get_persona_details(persona_id)
        
        if persona_data:
            # Ask for new name
            name, ok = QInputDialog.getText(
                self,
                "Dupliquer Persona",
                "Nom du nouveau persona:",
                QLineEdit.Normal,
                f"{persona_data['persona'][1]} (Copie)"
            )
            
            if ok and name:
                # Create new persona with same data but new name
                new_persona = {
                    'name': name,
                    'role': persona_data['persona'][2],
                    'age': persona_data['persona'][3],
                    'gender': persona_data['persona'][4],
                    'location': persona_data['persona'][5],
                    'education': persona_data['persona'][6],
                    'income_level': persona_data['persona'][7],
                    'industry': persona_data['persona'][8],
                    'company_size': persona_data['persona'][9],
                    'job_title': persona_data['persona'][10],
                    'challenges': persona_data['persona'][11],
                    'motivations': persona_data['persona'][12],
                    'preferred_channels': persona_data['persona'][13],
                    'decision_making': persona_data['persona'][14]
                }
                
                new_id = self.db.add_persona(new_persona)
                
                # Duplicate all related data
                for goal in persona_data['goals']:
                    self.db.add_goal(new_id, goal[1], goal[2])
                
                for pain in persona_data['pain_points']:
                    self.db.add_pain_point(new_id, pain[1], pain[2])
                
                for behavior in persona_data['behaviors']:
                    self.db.add_behavior(new_id, behavior[1], behavior[2])
                
                for quote in persona_data['quotes']:
                    self.db.add_quote(new_id, quote[1], quote[2])
                
                for scenario in persona_data['scenarios']:
                    self.db.add_scenario(new_id, scenario[1], scenario[2], scenario[3])
                
                for journey in persona_data['journeys']:
                    self.db.add_journey(new_id, journey[1], journey[2], journey[3], journey[4], journey[5])
                
                self._refresh_personas_list()
                
                # Select the new persona
                for i in range(self.personas_list.count()):
                    item = self.personas_list.item(i)
                    if item.data(Qt.UserRole) == new_id:
                        self.personas_list.setCurrentItem(item)
                        break
    
    def _save_persona(self):
        if not self.current_persona_id:
            return
            
        self.db.update_persona(self.current_persona_id, {
            'name': self.name_edit.text(),
            'role': self.role_edit.text(),
            'age': self.age_spin.value(),
            'gender': self.gender_combo.currentText(),
            'location': self.location_edit.text(),
            'education': self.education_combo.currentText(),
            'income_level': self.income_combo.currentText(),
            'industry': self.industry_edit.text(),
            'company_size': self.company_size_combo.currentText(),
            'job_title': self.job_title_edit.text(),
            'challenges': self.challenges_edit.toPlainText(),
            'motivations': self.motivations_edit.toPlainText(),
            'preferred_channels': self.channels_edit.toPlainText(),
            'decision_making': self.decision_edit.toPlainText()
        })
        
        self.statusbar.showMessage("Persona enregistré avec succès", 3000)
        self._refresh_personas_list()
    
    def _delete_persona(self):
        selected = self.personas_list.selectedItems()
        if not selected:
            return
            
        reply = QMessageBox.question(
            self, 
            'Confirmation',
            "Êtes-vous sûr de vouloir supprimer ce persona? Cette action est irréversible.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            persona_id = selected[0].data(Qt.UserRole)
            self.db.delete_persona(persona_id)
            self._refresh_personas_list()
            self._clear_details()
    
    def _change_photo(self):
        if not self.current_persona_id:
            return
            
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Choisir une image", 
            "", 
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_name:
            self._load_photo(file_name)
            self.db.update_persona_photo(self.current_persona_id, file_name)
            self._refresh_personas_list()
    
    def _load_photo(self, path):
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                self.photo_label.width(), 
                self.photo_label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.photo_label.setPixmap(pixmap)
    
    def _export_data(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter les données",
            "",
            "CSV Files (*.csv);;JSON Files (*.json)"
        )
        
        if file_name:
            if file_name.endswith('.csv'):
                self.db.export_personas(file_name)
                self.statusbar.showMessage("Données exportées en CSV avec succès", 3000)
            elif file_name.endswith('.json'):
                self._export_to_json(file_name)
                self.statusbar.showMessage("Données exportées en JSON avec succès", 3000)
    
    def _import_data(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Importer des données",
            "",
            "CSV Files (*.csv);;JSON Files (*.json)"
        )
        
        if file_name:
            if file_name.endswith('.csv'):
                self.db.import_personas(file_name)
                self.statusbar.showMessage("Données importées depuis CSV avec succès", 3000)
                self._refresh_personas_list()
            elif file_name.endswith('.json'):
                self._import_from_json(file_name)
                self.statusbar.showMessage("Données importées depuis JSON avec succès", 3000)
                self._refresh_personas_list()
    
    def _export_to_json(self, file_path):
        personas = self.db.execute_query("SELECT * FROM personas", fetch=True)
        data = []
        
        for persona in personas:
            persona_id = persona[0]
            persona_data = {
                'name': persona[1],
                'role': persona[2],
                'age': persona[3],
                'gender': persona[4],
                'location': persona[5],
                'education': persona[6],
                'income_level': persona[7],
                'industry': persona[8],
                'company_size': persona[9],
                'job_title': persona[10],
                'challenges': persona[11],
                'motivations': persona[12],
                'preferred_channels': persona[13],
                'decision_making': persona[14],
                'photo_path': persona[15],
                'goals': [],
                'pain_points': [],
                'behaviors': [],
                'quotes': [],
                'scenarios': [],
                'journeys': [],
                'notes': []
            }
            
            # Get related data
            goals = self.db.execute_query("SELECT description, priority FROM goals WHERE persona_id = ?", (persona_id,), fetch=True)
            for goal in goals:
                persona_data['goals'].append({'description': goal[0], 'priority': goal[1]})
            
            pains = self.db.execute_query("SELECT description, severity FROM pain_points WHERE persona_id = ?", (persona_id,), fetch=True)
            for pain in pains:
                persona_data['pain_points'].append({'description': pain[0], 'severity': pain[1]})
            
            behaviors = self.db.execute_query("SELECT description, frequency FROM behaviors WHERE persona_id = ?", (persona_id,), fetch=True)
            for behavior in behaviors:
                persona_data['behaviors'].append({'description': behavior[0], 'frequency': behavior[1]})
            
            quotes = self.db.execute_query("SELECT quote_text, context FROM quotes WHERE persona_id = ?", (persona_id,), fetch=True)
            for quote in quotes:
                persona_data['quotes'].append({'quote': quote[0], 'context': quote[1]})
            
            scenarios = self.db.execute_query("SELECT title, description, steps FROM scenarios WHERE persona_id = ?", (persona_id,), fetch=True)
            for scenario in scenarios:
                persona_data['scenarios'].append({'title': scenario[0], 'description': scenario[1], 'steps': scenario[2]})
            
            journeys = self.db.execute_query("SELECT stage, actions, touchpoints, emotions, opportunities FROM journeys WHERE persona_id = ?", (persona_id,), fetch=True)
            for journey in journeys:
                persona_data['journeys'].append({
                    'stage': journey[0],
                    'actions': journey[1],
                    'touchpoints': journey[2],
                    'emotions': journey[3],
                    'opportunities': journey[4]
                })
            
            notes = self.db.execute_query("SELECT content, created_at FROM notes WHERE persona_id = ?", (persona_id,), fetch=True)
            for note in notes:
                persona_data['notes'].append({'content': note[0], 'created_at': note[1]})
            
            data.append(persona_data)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def _import_from_json(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            for persona in data:
                # Create persona
                persona_id = self.db.add_persona({
                    'name': persona['name'],
                    'role': persona.get('role', ''),
                    'age': persona.get('age', 0),
                    'gender': persona.get('gender', ''),
                    'location': persona.get('location', ''),
                    'education': persona.get('education', ''),
                    'income_level': persona.get('income_level', ''),
                    'industry': persona.get('industry', ''),
                    'company_size': persona.get('company_size', ''),
                    'job_title': persona.get('job_title', ''),
                    'challenges': persona.get('challenges', ''),
                    'motivations': persona.get('motivations', ''),
                    'preferred_channels': persona.get('preferred_channels', ''),
                    'decision_making': persona.get('decision_making', '')
                })
                
                # Add photo path if exists
                if persona.get('photo_path'):
                    self.db.update_persona_photo(persona_id, persona['photo_path'])
                
                # Add related data
                for goal in persona.get('goals', []):
                    self.db.add_goal(persona_id, goal['description'], goal.get('priority', 1))
                
                for pain in persona.get('pain_points', []):
                    self.db.add_pain_point(persona_id, pain['description'], pain.get('severity', 1))
                
                for behavior in persona.get('behaviors', []):
                    self.db.add_behavior(persona_id, behavior['description'], behavior.get('frequency', ''))
                
                for quote in persona.get('quotes', []):
                    self.db.add_quote(persona_id, quote['quote'], quote.get('context', ''))
                
                for scenario in persona.get('scenarios', []):
                    self.db.add_scenario(persona_id, scenario['title'], scenario.get('description', ''), scenario.get('steps', ''))
                
                for journey in persona.get('journeys', []):
                    self.db.add_journey(
                        persona_id,
                        journey.get('stage', ''),
                        journey.get('actions', ''),
                        journey.get('touchpoints', ''),
                        journey.get('emotions', ''),
                        journey.get('opportunities', '')
                    )
                
                for note in persona.get('notes', []):
                    self.db.add_note(persona_id, note['content'])
    
    def _add_table_item(self, item_type):
        if not self.current_persona_id:
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Ajouter un {self._get_item_label(item_type)}")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        
        # Common fields
        desc_edit = QTextEdit()
        desc_edit.setMinimumHeight(100)
        form.addRow("Description:", desc_edit)
        
        # Type-specific fields
        if item_type in ["goal", "pain_point"]:
            priority_spin = QSpinBox()
            priority_spin.setRange(1, 5)
            form.addRow("Priorité:" if item_type == "goal" else "Sévérité:", priority_spin)
        elif item_type == "behavior":
            freq_edit = QLineEdit()
            form.addRow("Fréquence:", freq_edit)
        elif item_type == "quote":
            context_edit = QTextEdit()
            context_edit.setMinimumHeight(60)
            form.addRow("Contexte:", context_edit)
        elif item_type == "scenario":
            title_edit = QLineEdit()
            steps_edit = QTextEdit()
            steps_edit.setMinimumHeight(100)
            form.addRow("Titre:", title_edit)
            form.addRow("Étapes:", steps_edit)
        elif item_type == "journey":
            stage_combo = QComboBox()
            stage_combo.addItems(["Conscience", "Considération", "Décision", "Fidélité", "Advocacy"])
            actions_edit = QTextEdit()
            actions_edit.setMinimumHeight(60)
            touchpoints_edit = QTextEdit()
            touchpoints_edit.setMinimumHeight(60)
            emotions_edit = QTextEdit()
            emotions_edit.setMinimumHeight(60)
            opportunities_edit = QTextEdit()
            opportunities_edit.setMinimumHeight(60)
            
            form.addRow("Étape:", stage_combo)
            form.addRow("Actions:", actions_edit)
            form.addRow("Points de contact:", touchpoints_edit)
            form.addRow("Émotions:", emotions_edit)
            form.addRow("Opportunités:", opportunities_edit)
        
        layout.addLayout(form)
        
        btn_box = QHBoxLayout()
        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(dialog.accept)
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(dialog.reject)
        
        btn_box.addWidget(save_btn)
        btn_box.addWidget(cancel_btn)
        layout.addLayout(btn_box)
        
        if dialog.exec_() == QDialog.Accepted:
            if item_type == "goal":
                self.db.add_goal(
                    self.current_persona_id,
                    desc_edit.toPlainText(),
                    priority_spin.value()
                )
            elif item_type == "pain_point":
                self.db.add_pain_point(
                    self.current_persona_id,
                    desc_edit.toPlainText(),
                    priority_spin.value()
                )
            elif item_type == "behavior":
                self.db.add_behavior(
                    self.current_persona_id,
                    desc_edit.toPlainText(),
                    freq_edit.text()
                )
            elif item_type == "quote":
                self.db.add_quote(
                    self.current_persona_id,
                    desc_edit.toPlainText(),
                    context_edit.toPlainText()
                )
            elif item_type == "scenario":
                self.db.add_scenario(
                    self.current_persona_id,
                    title_edit.text(),
                    desc_edit.toPlainText(),
                    steps_edit.toPlainText()
                )
            elif item_type == "journey":
                self.db.add_journey(
                    self.current_persona_id,
                    stage_combo.currentText(),
                    actions_edit.toPlainText(),
                    touchpoints_edit.toPlainText(),
                    emotions_edit.toPlainText(),
                    opportunities_edit.toPlainText()
                )
            
            self._load_persona_details()
    
    def _edit_table_item(self, row, table):
        item_id = int(table.item(row, 0).text())
        item_type = self._get_item_type(table)
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Modifier {self._get_item_label(item_type)}")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        
        # Get current data
        if item_type == "goal":
            data = self.db.execute_query(
                "SELECT description, priority FROM goals WHERE id = ?",
                (item_id,),
                fetch_one=True
            )
        elif item_type == "pain_point":
            data = self.db.execute_query(
                "SELECT description, severity FROM pain_points WHERE id = ?",
                (item_id,),
                fetch_one=True
            )
        elif item_type == "behavior":
            data = self.db.execute_query(
                "SELECT description, frequency FROM behaviors WHERE id = ?",
                (item_id,),
                fetch_one=True
            )
        elif item_type == "quote":
            data = self.db.execute_query(
                "SELECT quote_text, context FROM quotes WHERE id = ?",
                (item_id,),
                fetch_one=True
            )
        elif item_type == "scenario":
            data = self.db.execute_query(
                "SELECT title, description, steps FROM scenarios WHERE id = ?",
                (item_id,),
                fetch_one=True
            )
        elif item_type == "journey":
            data = self.db.execute_query(
                "SELECT stage, actions, touchpoints, emotions, opportunities FROM journeys WHERE id = ?",
                (item_id,),
                fetch_one=True
            )
        
        # Common fields
        desc_edit = QTextEdit()
        desc_edit.setMinimumHeight(100)
        
        if item_type in ["goal", "pain_point", "behavior", "quote"]:
            desc_edit.setText(data[0])
            form.addRow("Description:", desc_edit)
        
        # Type-specific fields
        if item_type in ["goal", "pain_point"]:
            priority_spin = QSpinBox()
            priority_spin.setRange(1, 5)
            priority_spin.setValue(data[1])
            form.addRow("Priorité:" if item_type == "goal" else "Sévérité:", priority_spin)
        elif item_type == "behavior":
            freq_edit = QLineEdit()
            freq_edit.setText(data[1])
            form.addRow("Fréquence:", freq_edit)
        elif item_type == "quote":
            context_edit = QTextEdit()
            context_edit.setMinimumHeight(60)
            context_edit.setText(data[1])
            form.addRow("Contexte:", context_edit)
        elif item_type == "scenario":
            title_edit = QLineEdit()
            title_edit.setText(data[0])
            form.addRow("Titre:", title_edit)
            
            desc_edit.setText(data[1])
            form.addRow("Description:", desc_edit)
            
            steps_edit = QTextEdit()
            steps_edit.setMinimumHeight(100)
            steps_edit.setText(data[2])
            form.addRow("Étapes:", steps_edit)
        elif item_type == "journey":
            stage_combo = QComboBox()
            stage_combo.addItems(["Conscience", "Considération", "Décision", "Fidélité", "Advocacy"])
            stage_combo.setCurrentText(data[0])
            form.addRow("Étape:", stage_combo)
            
            actions_edit = QTextEdit()
            actions_edit.setMinimumHeight(60)
            actions_edit.setText(data[1])
            form.addRow("Actions:", actions_edit)
            
            touchpoints_edit = QTextEdit()
            touchpoints_edit.setMinimumHeight(60)
            touchpoints_edit.setText(data[2])
            form.addRow("Points de contact:", touchpoints_edit)
            
            emotions_edit = QTextEdit()
            emotions_edit.setMinimumHeight(60)
            emotions_edit.setText(data[3])
            form.addRow("Émotions:", emotions_edit)
            
            opportunities_edit = QTextEdit()
            opportunities_edit.setMinimumHeight(60)
            opportunities_edit.setText(data[4])
            form.addRow("Opportunités:", opportunities_edit)
        
        layout.addLayout(form)
        
        btn_box = QHBoxLayout()
        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(dialog.accept)
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(dialog.reject)
        
        btn_box.addWidget(save_btn)
        btn_box.addWidget(cancel_btn)
        layout.addLayout(btn_box)
        
        if dialog.exec_() == QDialog.Accepted:
            if item_type == "goal":
                self.db.update_goal(
                    item_id,
                    desc_edit.toPlainText(),
                    priority_spin.value()
                )
            elif item_type == "pain_point":
                self.db.update_pain_point(
                    item_id,
                    desc_edit.toPlainText(),
                    priority_spin.value()
                )
            elif item_type == "behavior":
                self.db.update_behavior(
                    item_id,
                    desc_edit.toPlainText(),
                    freq_edit.text()
                )
            elif item_type == "quote":
                self.db.update_quote(
                    item_id,
                    desc_edit.toPlainText(),
                    context_edit.toPlainText()
                )
            elif item_type == "scenario":
                self.db.update_scenario(
                    item_id,
                    title_edit.text(),
                    desc_edit.toPlainText(),
                    steps_edit.toPlainText()
                )
            elif item_type == "journey":
                self.db.update_journey(
                    item_id,
                    stage_combo.currentText(),
                    actions_edit.toPlainText(),
                    touchpoints_edit.toPlainText(),
                    emotions_edit.toPlainText(),
                    opportunities_edit.toPlainText()
                )
            
            self._load_persona_details()
    
    def _delete_table_item(self, row, table):
        item_id = int(table.item(row, 0).text())
        item_type = self._get_item_type(table)
        
        reply = QMessageBox.question(
            self, 
            'Confirmation',
            f"Êtes-vous sûr de vouloir supprimer cet élément?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if item_type == "goal":
                self.db.delete_goal(item_id)
            elif item_type == "pain_point":
                self.db.delete_pain_point(item_id)
            elif item_type == "behavior":
                self.db.delete_behavior(item_id)
            elif item_type == "quote":
                self.db.delete_quote(item_id)
            elif item_type == "scenario":
                self.db.delete_scenario(item_id)
            elif item_type == "journey":
                self.db.delete_journey(item_id)
            
            self._load_persona_details()
    
    def _add_note(self):
        if not self.current_persona_id:
            return
            
        self.note_edit.clear()
        self.notes_list.clearSelection()
    
    def _save_note(self):
        if not self.current_persona_id:
            return
            
        selected_note = self.notes_list.currentItem()
        content = self.note_edit.toPlainText()
        
        if not content:
            QMessageBox.warning(self, "Erreur", "La note ne peut pas être vide")
            return
            
        if selected_note:
            # Update existing note
            note_id = selected_note.data(Qt.UserRole)
            self.db.update_note(note_id, content)
        else:
            # Add new note
            self.db.add_note(self.current_persona_id, content)
        
        self._load_persona_details()
        self.statusbar.showMessage("Note enregistrée", 2000)
    
    def _delete_note(self):
        selected_note = self.notes_list.currentItem()
        if not selected_note:
            return
            
        reply = QMessageBox.question(
            self, 
            'Confirmation',
            "Êtes-vous sûr de vouloir supprimer cette note?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            note_id = selected_note.data(Qt.UserRole)
            self.db.delete_note(note_id)
            self._load_persona_details()
    
    def _get_item_type(self, table):
        if table == self.goals_table:
            return "goal"
        elif table == self.pains_table:
            return "pain_point"
        elif table == self.behaviors_table:
            return "behavior"
        elif table == self.quotes_table:
            return "quote"
        elif table == self.scenarios_table:
            return "scenario"
        elif table == self.journey_table:
            return "journey"
        return ""
    
    def _get_item_label(self, item_type):
        labels = {
            "goal": "objectif",
            "pain_point": "point de douleur",
            "behavior": "comportement",
            "quote": "citation",
            "scenario": "scénario",
            "journey": "étape du parcours"
        }
        return labels.get(item_type, "élément")
    
    def _cancel_edits(self):
        self._load_persona_details()
    
    def _toggle_dark_mode(self, checked):
        self.dark_mode = checked
        self._apply_stylesheet()
        self._save_settings()
    
    def _toggle_fullscreen(self, checked):
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()
    
    def _show_about(self):
        QMessageBox.about(
            self,
            "À propos de Persona Designer Pro",
            """<h2>Persona Designer Pro</h2>
            <p>Version 2.0</p>
            <p>Une application pour créer et gérer des personas marketing.</p>
            <p>Développé pour les entrepreneurs et marketeurs.</p>
            <p>© 2023 Tous droits réservés</p>"""
        )
    
    def _show_help(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Aide")
        help_dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(help_dialog)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml("""
            <h1>Aide de Persona Designer Pro</h1>
            <h2>Création de Personas</h2>
            <p>Pour créer un nouveau persona, cliquez sur le bouton <b>Nouveau Persona</b> ou utilisez le raccourci Ctrl+N.</p>
            
            <h2>Édition des Personas</h2>
            <p>Les personas peuvent être modifiés dans les différents onglets :</p>
            <ul>
                <li><b>Profil</b> : Informations de base et démographiques</li>
                <li><b>Psychographie</b> : Objectifs, points de douleur, comportements et citations</li>
                <li><b>Parcours Client</b> : Étapes du parcours d'achat</li>
                <li><b>Scénarios</b> : Situations d'utilisation</li>
                <li><b>Notes</b> : Observations supplémentaires</li>
            </ul>
            
            <h2>Export/Import</h2>
            <p>Les données peuvent être exportées au format CSV ou JSON pour être partagées ou sauvegardées.</p>
        """)
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(help_dialog.close)
        
        layout.addWidget(text_edit)
        layout.addWidget(close_btn, 0, Qt.AlignRight)
        
        help_dialog.exec_()
    
    def _update_status_bar(self):
        count = self.personas_list.count()
        self.last_update_label.setText(f"Personas: {count} | Dernière mise à jour: {datetime.now().strftime('%H:%M:%S')}")
    
    def _load_settings(self):
        settings = QApplication.instance().settings = {}
        try:
            with open('settings.json', 'r') as f:
                settings.update(json.load(f))
                
                # Apply dark mode if was enabled
                if settings.get('dark_mode', False):
                    self.dark_mode_action.setChecked(True)
                    self._toggle_dark_mode(True)
                
                # Restore window geometry
                if settings.get('window_geometry'):
                    self.restoreGeometry(settings['window_geometry'])
                
                # Restore window state
                if settings.get('window_state'):
                    self.restoreState(settings['window_state'])
                
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    
    def _save_settings(self):
        settings = {
            'dark_mode': self.dark_mode,
            'window_geometry': self.saveGeometry(),
            'window_state': self.saveState()
        }
        
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
    
    def closeEvent(self, event):
        self._save_settings()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icons/app.png"))
    app.setStyle("Fusion")
    
    # Set application font
    font = QFont()
    font.setFamily("Segoe UI")
    font.setPointSize(10)
    app.setFont(font)
    
    window = PersonaDesignerApp()
    window.show()
    
    sys.exit(app.exec_())