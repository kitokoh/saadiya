import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QVBoxLayout, 
                            QLabel, QPushButton, QCheckBox, QLineEdit, 
                            QMessageBox, QWidget)
from PyQt5.QtCore import Qt
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Callable
from demarrage.terms_manager import TermsDialog
from ui.register import RegisterModule
from Mining.miningcoiy import MainWindow
from demarrage.feedback import FeedbackApp
from demarrage.tuto import TutorialDialog
from demarrage.evaluemarketing  import MarketingEvaluationDialog
from demarrage.baseDialog import BaseDialog

from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QScrollArea, QTextBrowser
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import QPropertyAnimation


from demarrage.feedback import FeedbackDialog
from demarrage.modules import ModuleSelectionDialog
from imports import DB_PATH_demarrage
class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH_demarrage)
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                session_type TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                accepted_terms BOOLEAN DEFAULT 0,
                selected_modules TEXT,
                preferences TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT UNIQUE,
                metric_value TEXT
            )
        ''')
        self.conn.commit()
    
    def record_session_start(self, session_type: str = "normal") -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO app_sessions (start_time, session_type)
            VALUES (?, ?)
        ''', (datetime.now().isoformat(), session_type))
        self.conn.commit()
        return cursor.lastrowid
    
    def record_session_end(self, session_id: int):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE app_sessions 
            SET end_time = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), session_id))
        self.conn.commit()
    
    def get_session_count(self) -> int:
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM app_sessions')
        return cursor.fetchone()[0]
    
    def get_previous_session_type(self) -> Optional[str]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT session_type FROM app_sessions 
            ORDER BY id DESC LIMIT 1 OFFSET 1
        ''')
        result = cursor.fetchone()
        return result[0] if result else None
    
    def save_user_settings(self, settings: Dict):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO user_settings 
            (username, accepted_terms, selected_modules, preferences)
            VALUES (?, ?, ?, ?)
        ''', (
            settings.get('username'),
            settings.get('accepted_terms', False),
            ','.join(settings.get('selected_modules', [])),
            str(settings.get('preferences', {}))
        ))
        self.conn.commit()
    
    def get_user_settings(self) -> Dict:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM user_settings ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'username': result[1],
                'accepted_terms': bool(result[2]),
                'selected_modules': result[3].split(',') if result[3] else [],
                'preferences': eval(result[4]) if result[4] else {}
            }
        return {}
    
    def set_metric(self, name: str, value: str):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO app_metrics (metric_name, metric_value)
            VALUES (?, ?)
        ''', (name, value))
        self.conn.commit()
    
    def get_metric(self, name: str, default: str = None) -> str:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT metric_value FROM app_metrics WHERE metric_name = ?
        ''', (name,))
        result = cursor.fetchone()
        return result[0] if result else default
    
    def close(self):
        self.conn.close()




class FlowManager:
    FLOWS = {
        1: {  # Premier démarrage
            'name': 'initial_setup',
            'description': 'Configuration initiale',
            'dialogs': [
                (TermsDialog, "Conditions d'utilisation"),


                (ModuleSelectionDialog, "Sélection des modules")

            ],
            'session_type': 'initial'
        },
        2: {  # Deuxième démarrage
            'name': 'tutorial',
            'description': 'Tutoriel de prise en main',
            'dialogs': [

                (TutorialDialog, "Guide d'utilisation")



            ],
            'session_type': 'tutorial'
        },
        3: {  # Troisième démarrage
            'name': 'evalue',
            'description': "Demande d'évaluation",
            'dialogs': [

                    (MarketingEvaluationDialog, "Création de compte")

            ],
            'session_type': 'evalue'
        },

                4: {  # Troisième démarrage
            'name': 'user',
            'description': "Demande d'évaluation",
            'dialogs': [
                    # (UserCreationDialog, "Sélection des modules"),
                # (FelicitationDialog, "Sélection des modules")

            ],
            'session_type': 'user'
        },
                        5: {  # Troisième démarrage
            'name': 'feedback',
            'description': "Demande d'évaluation",
            'dialogs': [
                (FeedbackDialog, "Sélection des modules"),


            ],
            'session_type': 'feedback'
        },
        # Ajoutez d'autres flux au besoin
    }
    
    DEFAULT_FLOW = {
        'name': 'normal',
        'description': 'Utilisation normale',
        'dialogs': [],
        'session_type': 'normal'
    }
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.session_id = None
        self.current_flow = None
    

    def execute_flow(self):
        if not self.current_flow:
            return False
        
        results = {}
        
        for dialog_class, title in self.current_flow['dialogs']:
            dialog = dialog_class(title)
            if dialog.exec_() != QDialog.Accepted:
                return False
            
            results.update(dialog.get_results())
        
        # Sauvegarder les résultats si nécessaire
        if self.current_flow['name'] == 'initial_setup':
            self.db.save_user_settings(results)
        
        return True
    
    def end_session(self):
        if self.session_id:
            self.db.record_session_end(self.session_id)

    def get_dynamic_flow(self, session_number: int) -> Optional[Dict]:
        # Exemple : exécuter FeedbackDialog tous les 5 démarrages
        if session_number % 5 == 0:
            return {
                'name': 'feedback_every_5',
                'description': f"Feedback demandé au {session_number}e démarrage",
                'dialogs': [
                    # (FeedbackDialog, "Que pensez-vous de l'application ?")
                ],
                'session_type': 'feedback_periodic'
            }

        # Exemple : exécuter ModuleSelectionDialog à chaque démarrage pair
        if session_number % 2 == 0:
            return {
                'name': 'pair_module_review',
                'description': f"Révision des modules au {session_number}e démarrage pair",
                'dialogs': [
                    # (ModuleSelectionDialog, "Modules à activer")
                ],
                'session_type': 'module_review'
            }

        # Exemple : lancer un tuto spécial au 13e démarrage
        if session_number == 13:
            return {
                'name': 'tuto_13',
                'description': "Tuto surprise au 13e démarrage",
                'dialogs': [
                    # (TutorialDialog, "Tuto avancé")
                ],
                'session_type': 'special_13'
            }

        return None

    def start_session(self):
        session_count = self.db.get_session_count()
        session_number = session_count + 1

        # Priorité : Flux prédéfinis (1, 2, 3…)
        flow = self.FLOWS.get(session_number)

        # Sinon, tester les règles dynamiques
        if not flow:
            flow = self.get_dynamic_flow(session_number)

        # Sinon, on reste sur le flow normal
        if not flow:
            flow = self.DEFAULT_FLOW

        self.current_flow = flow

        self.session_id = self.db.record_session_start(
            self.current_flow['session_type']
        )

        return self.current_flow

