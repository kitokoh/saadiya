import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QVBoxLayout, 
                            QLabel, QPushButton, QCheckBox, QLineEdit, 
                            QMessageBox, QWidget)
from PyQt5.QtCore import Qt
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Callable
# from demarrage.terms_manager import TermsDialog
# from Installsweb.installmodules import InstallerDialog
# from ui.register import RegisterModule
# from Mining.miningcoiy import MainWindow
# from demarrage.feedback import FeedbackApp
class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('app_state.db')
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

class BaseDialog(QDialog):
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)
        self.setModal(True)
        self.init_ui()
        
    def init_ui(self):
        raise NotImplementedError("Subclasses must implement init_ui")
    
    def get_results(self) -> Dict:
        return {}
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QScrollArea, QTextBrowser
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import QPropertyAnimation


class TermsDialog(BaseDialog):
    def init_ui(self):
        # Layout principal avec espacement et marges modernes
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 20)
        layout.setSpacing(25)
        
        # En-tête stylisé
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel("Conditions d'utilisation de l'application")
        self.label.setObjectName("titleLabel")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        
        version_label = QLabel(f"Version 2.3.1 • {QDate.currentDate().toString('dd MMMM yyyy')}")
        version_label.setObjectName("versionLabel")
        version_label.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(self.label)
        header_layout.addWidget(version_label)
        header_layout.addSpacing(10)
        
        # Zone de texte avec barre de défilement moderne
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        self.terms_text = QTextBrowser()
        self.terms_text.setOpenExternalLinks(True)
        self.terms_text.setObjectName("termsText")
        self.load_terms_content()
        
        scroll_area.setWidget(self.terms_text)
        
        # Case à cocher avec style moderne
        self.accept_checkbox = QCheckBox("J'accepte les conditions d'utilisation")
        self.accept_checkbox.setObjectName("acceptCheckbox")
        self.accept_checkbox.setCursor(Qt.PointingHandCursor)
        
        # Boutons avec disposition moderne
        button_container = QFrame()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(15)
        
        self.continue_btn = QPushButton("Continuer")
        self.continue_btn.setObjectName("primaryButton")
        self.continue_btn.setEnabled(False)
        self.continue_btn.setCursor(Qt.PointingHandCursor)
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setObjectName("secondaryButton")
        cancel_btn.setCursor(Qt.PointingHandCursor)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(self.continue_btn)
        
        # Ajout des widgets au layout principal
        layout.addWidget(header_frame)
        layout.addWidget(scroll_area)
        layout.addWidget(self.accept_checkbox)
        layout.addWidget(button_container)
        
        # Connexions des signaux
        self.accept_checkbox.stateChanged.connect(self.toggle_continue_button)
        self.continue_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        # Appliquer le style
        self.setStyleSheet("""
            #headerFrame {
                background-color: #f8f9fa;
                border-radius: 12px;
                padding: 20px;
            }
            
            #titleLabel {
                font-size: 18px;
                font-weight: 600;
                color: #2d3748;
            }
            
            #versionLabel {
                font-size: 12px;
                color: #718096;
            }
            
            #termsText {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 20px;
                font-size: 13px;
                color: #4a5568;
            }
            
            #acceptCheckbox {
                font-size: 14px;
                color: #4a5568;
                spacing: 10px;
            }
            
            #acceptCheckbox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #cbd5e0;
                border-radius: 4px;
            }
            
            #acceptCheckbox::indicator:checked {
                background-color: #4299e1;
                border-color: #4299e1;
                image: url(:/icons/checkmark.svg);
            }
            
            #primaryButton {
                background-color: #4299e1;
                color: white;
                border-radius: 6px;
                padding: 10px 24px;
                font-weight: 500;
                min-width: 120px;
            }
            
            #primaryButton:hover {
                background-color: #3182ce;
            }
            
            #primaryButton:disabled {
                background-color: #bee3f8;
            }
            
            #secondaryButton {
                background-color: white;
                color: #4a5568;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 10px 24px;
                font-weight: 500;
                min-width: 120px;
            }
            
            #secondaryButton:hover {
                background-color: #f7fafc;
                border-color: #cbd5e0;
            }
        """)
        
        self.setLayout(layout)
    
    def load_terms_content(self):
        """Charge un contenu HTML stylisé dans le QTextBrowser"""
        terms_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    font-family: 'Segoe UI', system-ui, sans-serif;
                    line-height: 1.6;
                    color: #2d3748;
                }
                h2 {
                    color: #2b6cb0;
                    margin-top: 1.5em;
                    font-size: 1.2em;
                }
                h3 {
                    color: #4a5568;
                    margin-top: 1em;
                }
                ul {
                    padding-left: 1.5em;
                }
                li {
                    margin-bottom: 0.5em;
                }
                strong {
                    color: #2d3748;
                }
                .highlight {
                    background-color: #ebf8ff;
                    padding: 0.2em 0.4em;
                    border-radius: 0.2em;
                }
            </style>
        </head>
        <body>
            <h2>1. Acceptation des conditions</h2>
            <p>En utilisant cette application, vous acceptez les conditions suivantes. Veuillez les lire attentivement.</p>
            
            <h2>2. Utilisation du service</h2>
            <p>Cette application vous permet de :</p>
            <ul>
                <li>Gérer vos publications sur les réseaux sociaux</li>
                <li>Organiser votre contenu marketing</li>
                <li>Collaborer avec votre équipe</li>
            </ul>
            
            <h2>3. Protection des données</h2>
            <p>Nous nous engageons à protéger vos données :</p>
            <ul>
                <li>Vos données sont stockées <span class="highlight">localement</span> sur votre appareil</li>
                <li>Chiffrement des informations sensibles</li>
                <li>Respect des réglementations en vigueur</li>
            </ul>
            
            <h2>4. Responsabilités</h2>
            <p>Vous vous engagez à :</p>
            <ul>
                <li>Utiliser l'application conformément à la loi</li>
                <li>Maintenir la confidentialité de vos identifiants</li>
                <li>Ne pas contourner les mesures de sécurité</li>
            </ul>
        </body>
        </html>
        """
        self.terms_text.setHtml(terms_html)
    
    def toggle_continue_button(self, state):
        """Active/désactive le bouton Continuer avec animation"""
        self.continue_btn.setEnabled(state == Qt.Checked)
        
        # Petite animation lors de l'activation
        if state == Qt.Checked:
            animation = QPropertyAnimation(self.continue_btn, b"geometry")
            animation.setDuration(150)
            animation.setStartValue(self.continue_btn.geometry())
            end_geo = self.continue_btn.geometry()
            end_geo.setWidth(end_geo.width() + 10)
            animation.setEndValue(end_geo)
            animation.start()
    
    def get_results(self) -> Dict:
        return {'accepted_terms': self.accept_checkbox.isChecked()}
class ModuleSelectionDialog(BaseDialog):
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Sélectionnez les modules à activer:")
        layout.addWidget(self.label)
        
        self.modules = {
            'module1': QCheckBox("Module Analyse de données"),
            'module2': QCheckBox("Module Reporting"),
            'module3': QCheckBox("Module Administration"),
            'module4': QCheckBox("Module Statistiques")
        }
        
        for module in self.modules.values():
            layout.addWidget(module)
        
        self.submit_btn = QPushButton("Valider")
        self.submit_btn.clicked.connect(self.accept)
        layout.addWidget(self.submit_btn)
        
        self.setLayout(layout)
    
    def get_results(self) -> Dict:
        return {
            'selected_modules': [
                name for name, checkbox in self.modules.items() 
                if checkbox.isChecked()
            ]
        }

class UserCreationDialog(BaseDialog):
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirmer le mot de passe")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        
        self.create_btn = QPushButton("Créer le compte")
        self.create_btn.clicked.connect(self.validate_and_accept)
        
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_input)
        layout.addWidget(self.create_btn)
        
        self.setLayout(layout)
    
    def validate_and_accept(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        if not username:
            QMessageBox.warning(self, "Erreur", "Le nom d'utilisateur est requis")
            return
        
        if not password or len(password) < 6:
            QMessageBox.warning(self, "Erreur", "Le mot de passe doit contenir au moins 6 caractères")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Erreur", "Les mots de passe ne correspondent pas")
            return
            
        self.accept()
    
    def get_results(self) -> Dict:
        return {
            'username': self.username_input.text().strip(),
            'password': self.password_input.text()  # Note: En production, il faudrait hasher
        }

class TutorialDialog(BaseDialog):
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Bienvenue dans le tutoriel d'utilisation!")
        self.label.setWordWrap(True)
        layout.addWidget(self.label)
        
        self.content = QLabel(
            "Ceci est un guide rapide pour utiliser l'application...\n\n"
            "1. Fonctionnalité A\n2. Fonctionnalité B\n3. Fonctionnalité C"
        )
        layout.addWidget(self.content)
        
        self.continue_btn = QPushButton("Compris!")
        self.continue_btn.clicked.connect(self.accept)
        layout.addWidget(self.continue_btn)
        
        self.setLayout(layout)

class FeedbackDialog(BaseDialog):
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Comment évaluez-vous votre expérience jusqu'à présent?")
        layout.addWidget(self.label)
        
        self.rating = 0
        self.rating_btns = []
        for i in range(1, 6):
            btn = QPushButton(str(i))
            btn.clicked.connect(lambda _, r=i: self.set_rating(r))
            self.rating_btns.append(btn)
            layout.addWidget(btn)
        
        self.feedback_input = QLineEdit()
        self.feedback_input.setPlaceholderText("Vos commentaires (optionnel)")
        layout.addWidget(self.feedback_input)
        
        self.submit_btn = QPushButton("Envoyer")
        self.submit_btn.clicked.connect(self.accept)
        layout.addWidget(self.submit_btn)
        
        self.setLayout(layout)
    
    def set_rating(self, rating: int):
        self.rating = rating
        for i, btn in enumerate(self.rating_btns):
            btn.setStyleSheet(
                "background-color: #4CAF50" if i < rating else ""
            )
    
    def get_results(self) -> Dict:
        return {
            'rating': self.rating,
            'feedback': self.feedback_input.text().strip()
        }
import sys
import sqlite3
import os
from datetime import datetime
from pathlib import Path
from typing import Dict
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, QStandardPaths
from PyQt5.QtGui import QIcon
from Installsweb.installmodules import ModuleSelectionDialog
class BaseDialogg(QWidget):
    """Classe de base pour les dialogues personnalisés"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.init_ui()
    
    def init_ui(self):
        """Initialiser l'interface utilisateur (à implémenter dans les classes enfants)"""
        raise NotImplementedError
    
    def get_results(self) -> Dict:
        """Récupérer les résultats du dialogue (à implémenter dans les classes enfants)"""
        raise NotImplementedError

class FeedbackDialog(BaseDialog):
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Titre
        self.label = QLabel("Comment évaluez-vous votre expérience jusqu'à présent?")
        layout.addWidget(self.label)
        
        # Boutons de notation
        self.rating = 0
        self.rating_btns = []
        btn_layout = QHBoxLayout()
        
        for i in range(1, 6):
            btn = QPushButton(str(i))
            btn.setFixedSize(40, 40)
            btn.clicked.connect(lambda _, r=i: self.set_rating(r))
            self.rating_btns.append(btn)
            btn_layout.addWidget(btn)
        
        layout.addLayout(btn_layout)
        
        # Champ de commentaire
        self.feedback_input = QLineEdit()
        self.feedback_input.setPlaceholderText("Vos commentaires (optionnel)")
        layout.addWidget(self.feedback_input)
        
        # Bouton d'envoi
        self.submit_btn = QPushButton("Envoyer")
        self.submit_btn.clicked.connect(self.accept)
        layout.addWidget(self.submit_btn)
        
        self.setLayout(layout)
    
    def set_rating(self, rating: int):
        """Définir la note et mettre à jour l'apparence des boutons"""
        self.rating = rating
        for i, btn in enumerate(self.rating_btns):
            btn.setStyleSheet(
                "background-color: #4CAF50; color: white;" if i < rating else ""
            )
    
    def get_results(self) -> Dict:
        """Récupérer les résultats sous forme de dictionnaire"""
        return {
            'rating': self.rating,
            'feedback': self.feedback_input.text().strip()
        }

class FeedbackDatabase:
    def __init__(self):
        db_path = self.get_db_path()
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def get_db_path(self):
        data_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        return os.path.join(data_dir, 'feedback.db')

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating INTEGER,
            comment TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.conn.commit()

    def save_feedback(self, rating: int, comment: str):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO feedback (rating, comment)
        VALUES (?, ?)
        ''', (rating, comment))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_feedback(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM feedback ORDER BY timestamp DESC')
        return cursor.fetchall()

    def __del__(self):
        self.conn.close()

class FeedbackApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Collecteur de Feedback")
        self.setMinimumSize(400, 300)
        
        self.db = FeedbackDatabase()
        self.setup_ui()
        self.show_feedback_stats()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Bouton pour ouvrir le dialogue de feedback
        self.feedback_btn = QPushButton("Donner votre feedback")
        self.feedback_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.feedback_btn.clicked.connect(self.open_feedback_dialog)
        layout.addWidget(self.feedback_btn, 0, Qt.AlignCenter)
        
        # Statistiques
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.stats_label)
        
        # Bouton pour rafraîchir
        refresh_btn = QPushButton("Rafraîchir les statistiques")
        refresh_btn.clicked.connect(self.show_feedback_stats)
        layout.addWidget(refresh_btn)
    
    def open_feedback_dialog(self):
        dialog = FeedbackDialog(self)
        if dialog.exec_() == QWidget.Accepted:
            results = dialog.get_results()
            try:
                self.db.save_feedback(results['rating'], results['feedback'])
                QMessageBox.information(self, "Merci!", "Votre feedback a été enregistré.")
                self.show_feedback_stats()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible d'enregistrer: {str(e)}")
    
    def show_feedback_stats(self):
        feedbacks = self.db.get_all_feedback()
        
        if not feedbacks:
            self.stats_label.setText("Aucun feedback enregistré pour le moment.")
            return
        
        total = len(feedbacks)
        avg_rating = sum(f[1] for f in feedbacks) / total
        
        self.stats_label.setText(
            f"Statistiques: {total} feedbacks | Moyenne: {avg_rating:.1f}/5"
        )


class MainWindow(QMainWindow):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.setWindowTitle("Application Principale")
        self.setGeometry(100, 100, 800, 600)
        
        self.user_settings = self.db.get_user_settings()
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel(f"Bienvenue {self.user_settings.get('username', 'Utilisateur')}!")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        modules = QLabel(
            "Modules activés: " + 
            ', '.join(self.user_settings.get('selected_modules', ['Aucun']))
        )
        layout.addWidget(modules)
        
        stats = QLabel(
            f"Sessions complètes: {self.db.get_session_count()}\n"
            f"Dernière session: {self.db.get_previous_session_type() or 'N/A'}"
        )
        layout.addWidget(stats)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
class FlowManager:
    FLOWS = {
        1: {  # Premier démarrage
            'name': 'initial_setup',
            'description': 'Configuration initiale',
            'dialogs': [
                (TermsDialog, "Conditions d'utilisation"),
                (ModuleSelectionDialog, "Sélection des modules"),
                # (ModuleSelectionDialog, "Sélection des modules"),

                # (RegisterModule, "Création de compte")
            ],
            'session_type': 'initial'
        },
        2: {  # Deuxième démarrage
            'name': 'tutorial',
            'description': 'Tutoriel de prise en main',
            'dialogs': [
                (TutorialDialog, "Guide d'utilisation"),
                #  (MainWindow, "Guide d'utilisation")

            ],
            'session_type': 'tutorial'
        },
        3: {  # Troisième démarrage
            'name': 'feedback',
            'description': "Demande d'évaluation",
            'dialogs': [
                (TutorialDialog, "Votre avis compte!")
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
    
    def start_session(self):
        session_count = self.db.get_session_count()
        self.current_flow = self.FLOWS.get(session_count + 1, self.DEFAULT_FLOW)
        
        self.session_id = self.db.record_session_start(
            self.current_flow['session_type']
        )
        
        return self.current_flow
    
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

class ApplicationController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.db = DatabaseManager()
        self.flow_manager = FlowManager(self.db)
    
    def run(self):
        try:
            # Démarrer la session et déterminer le flux
            flow = self.flow_manager.start_session()
            print(f"Exécution du flux: {flow['description']}")
            
            # Exécuter les dialogues du flux
            if not self.flow_manager.execute_flow():
                return 1
            
            # Si tout s'est bien passé, afficher la fenêtre principale
            main_window = MainWindow(self.db)
            main_window.show()
            
            return self.app.exec_()
        finally:
            self.flow_manager.end_session()
            self.db.close()

if __name__ == "__main__":
    controller = ApplicationController()
    sys.exit(controller.run())