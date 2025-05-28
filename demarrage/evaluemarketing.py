import sys
import sqlite3
import webbrowser
from typing import Dict, List, Optional
from PyQt5.QtCore import (Qt, pyqtSignal, pyqtProperty, QPointF, QPropertyAnimation, 
                         QSequentialAnimationGroup, QEasingCurve, QTimer)
from PyQt5.QtGui import (QPainter, QPainterPath, QLinearGradient, QRadialGradient, 
                        QColor, QBrush, QPen, QIcon, QPixmap)
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QStackedWidget, QProgressBar, QMessageBox,
                            QGraphicsDropShadowEffect, QSizePolicy)

from demarrage.modules import GlassButton, ParticleSystem

class MarketingPresenceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Évaluation de Présence Marketing")
        self.setWindowIcon(QIcon(":/icons/app_icon.png"))
        self.setMinimumSize(800, 600)
        
        # Initialisation de la base de données
        self.init_db()
        
        # Style de l'application
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #ffffff;
                font-family: 'Segoe UI';
            }
            QLabel {
                font-size: 16px;
            }
            QProgressBar {
                height: 20px;
                border-radius: 10px;
                background-color: #2d2d3d;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #6c5ce7;
                border-radius: 10px;
            }
        """)
        
        # Création de l'interface
        self.init_ui()
        
        # Charger les réponses existantes
        self.load_existing_responses()
        
        # Démarrer avec la première question non répondue
        self.show_next_question()

    def init_db(self):
        """Initialise la base de données SQLite"""
        self.conn = sqlite3.connect('marketing_presence.db')
        self.cursor = self.conn.cursor()
        
        # Création de la table si elle n'existe pas
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            response BOOLEAN NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        self.main_layout.addWidget(self.progress_bar)
        
        # Widget empilé pour les questions
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget, 1)
        
        # Widget de score
        self.score_widget = ScoreWidget()
        self.main_layout.addWidget(self.score_widget)
        
        # Liste des questions
        self.questions = [
            {
                'id': 1,
                'text': "Avez-vous une page Google My Business pour votre entreprise?",
                'weight': 8,
                'action_text': "Créer une page Google My Business",
                'action_url': "https://www.google.com/business/"
            },
            {
                'id': 2,
                'text': "Avez-vous un site web professionnel pour votre entreprise?",
                'weight': 10,
                'action_text': "Créer un site web",
                'action_url': "https://sites.google.com/"
            },
            {
                'id': 3,
                'text': "Avez-vous une boutique en ligne (e-commerce)?",
                'weight': 7,
                'action_text': "Créer une boutique en ligne",
                'action_url': "https://www.shopify.com/"
            },
            {
                'id': 4,
                'text': "Avez-vous une page Facebook pour votre entreprise?",
                'weight': 6,
                'action_text': "Créer une page Facebook",
                'action_url': "https://www.facebook.com/pages/create/"
            },
            {
                'id': 5,
                'text': "Avez-vous un compte Instagram professionnel?",
                'weight': 6,
                'action_text': "Créer un compte Instagram",
                'action_url': "https://www.instagram.com/"
            },
            {
                'id': 6,
                'text': "Avez-vous un profil LinkedIn pour votre entreprise?",
                'weight': 5,
                'action_text': "Créer un profil LinkedIn",
                'action_url': "https://www.linkedin.com/company/setup/new/"
            },
            {
                'id': 7,
                'text': "Avez-vous un numéro WhatsApp Business?",
                'weight': 4,
                'action_text': "Configurer WhatsApp Business",
                'action_url': "https://www.whatsapp.com/business/"
            },
            {
                'id': 8,
                'text': "Publiez-vous régulièrement du contenu sur vos réseaux sociaux?",
                'weight': 5,
                'action_text': "Voir des conseils de contenu",
                'action_url': "https://blog.hootsuite.com/fr/contenu-reseaux-sociaux/"
            },
            {
                'id': 9,
                'text': "Utilisez-vous des publicités en ligne (Google Ads, Facebook Ads)?",
                'weight': 7,
                'action_text': "Découvrir les publicités en ligne",
                'action_url': "https://ads.google.com/"
            },
            {
                'id': 10,
                'text': "Avez-vous une stratégie de référencement (SEO) pour votre site?",
                'weight': 8,
                'action_text': "Apprendre le SEO",
                'action_url': "https://developers.google.com/search/docs/fundamentals/seo-starter-guide"
            },
            {
                'id': 11,
                'text': "Collectez-vous les avis clients en ligne?",
                'weight': 6,
                'action_text': "Découvrir des outils d'avis",
                'action_url': "https://www.trustpilot.com/"
            },
            {
                'id': 12,
                'text': "Avez-vous une newsletter ou un système d'email marketing?",
                'weight': 5,
                'action_text': "Essayer Mailchimp",
                'action_url': "https://mailchimp.com/"
            },
            {
                'id': 13,
                'text': "Participez-vous à des événements professionnels ou salons?",
                'weight': 4,
                'action_text': "Trouver des événements",
                'action_url': "https://www.eventbrite.com/"
            },
            {
                'id': 14,
                'text': "Avez-vous des partenariats avec d'autres entreprises?",
                'weight': 4,
                'action_text': None,
                'action_url': None
            },
            {
                'id': 15,
                'text': "Avez-vous une stratégie de contenu (blog, vidéos, etc.)?",
                'weight': 6,
                'action_text': "Voir des exemples de stratégie",
                'action_url': "https://coschedule.com/content-marketing-strategy"
            },
            {
                'id': 16,
                'text': "Utilisez-vous des outils d'analyse (Google Analytics, etc.)?",
                'weight': 5,
                'action_text': "Découvrir Google Analytics",
                'action_url': "https://analytics.google.com/"
            },
            {
                'id': 17,
                'text': "Avez-vous une identité visuelle cohérente (logo, couleurs)?",
                'weight': 7,
                'action_text': "Créer un logo",
                'action_url': "https://www.canva.com/fr_fr/creer/logos/"
            },
            {
                'id': 18,
                'text': "Avez-vous des témoignages ou études de cas clients?",
                'weight': 5,
                'action_text': None,
                'action_url': None
            },
            {
                'id': 19,
                'text': "Proposez-vous des promotions ou offres spéciales?",
                'weight': 4,
                'action_text': None,
                'action_url': None
            },
            {
                'id': 20,
                'text': "Avez-vous une stratégie pour les influenceurs ou ambassadeurs?",
                'weight': 5,
                'action_text': "Découvrir le marketing d'influence",
                'action_url': "https://influencermarketinghub.com/"
            }
        ]
        
        # Créer les widgets de question
        self.question_widgets = []
        for question in self.questions:
            widget = QuestionWidget(question)
            widget.response_submitted.connect(self.handle_response)
            self.stacked_widget.addWidget(widget)
            self.question_widgets.append(widget)

    def load_existing_responses(self):
        """Charge les réponses existantes depuis la base de données"""
        self.cursor.execute("SELECT question_id, response FROM responses")
        self.existing_responses = {row[0]: row[1] for row in self.cursor.fetchall()}
        
        # Calculer le score initial
        self.calculate_score()

    def show_next_question(self):
        """Affiche la prochaine question non répondue"""
        for i, question in enumerate(self.questions):
            if question['id'] not in self.existing_responses:
                self.stacked_widget.setCurrentIndex(i)
                return
        
        # Toutes les questions ont été répondues
        self.show_completion_message()

    def handle_response(self, question_id: int, response: bool):
        """Enregistre la réponse et passe à la question suivante"""
        # Enregistrer dans la base de données
        self.cursor.execute(
            "INSERT INTO responses (question_id, response) VALUES (?, ?)",
            (question_id, response)
        )
        self.conn.commit()
        
        # Mettre à jour les réponses existantes
        self.existing_responses[question_id] = response
        
        # Calculer le nouveau score
        self.calculate_score()
        
        # Passer à la question suivante
        self.show_next_question()

    def calculate_score(self):
        """Calcule le score actuel"""
        total_possible = sum(q['weight'] for q in self.questions)
        current_score = 0
        
        for question in self.questions:
            if question['id'] in self.existing_responses and self.existing_responses[question['id']]:
                current_score += question['weight']
        
        self.current_score = int((current_score / total_possible) * 100) if total_possible > 0 else 0
        self.progress_bar.setValue(self.current_score)
        self.score_widget.update_score(self.current_score)

    def show_completion_message(self):
        """Affiche un message lorsque toutes les questions sont répondues"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Évaluation terminée")
        msg.setText("Vous avez répondu à toutes les questions !")
        msg.setInformativeText(f"Votre score final est de {self.current_score}%.\n\nConsultez vos résultats pour des recommandations personnalisées.")
        msg.exec_()

    def closeEvent(self, event):
        """Ferme proprement la connexion à la base de données"""
        self.conn.close()
        event.accept()

class QuestionWidget(QWidget):
    response_submitted = pyqtSignal(int, bool)
    
    def __init__(self, question_data: Dict):
        super().__init__()
        self.question_data = question_data
        self.init_ui()
        
        # Effet de particules en arrière-plan
        self.particles = ParticleSystem(self)
        self.particles.lower()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        self.setLayout(layout)
        
        # Label de question
        self.question_label = QLabel(self.question_data['text'])
        self.question_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 40px;
            }
        """)
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.question_label, 0, Qt.AlignCenter)
        
        # Boutons de réponse
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(30)
        
        self.yes_btn = GlassButton("Oui", ":/icons/check.png")
        self.yes_btn.clicked.connect(lambda: self.submit_response(True))
        
        self.no_btn = GlassButton("Non", ":/icons/close.png")
        self.no_btn.clicked.connect(lambda: self.submit_response(False))
        
        btn_layout.addWidget(self.yes_btn)
        btn_layout.addWidget(self.no_btn)
        
        layout.addLayout(btn_layout)
        
        # Bouton d'action (si applicable)
        if self.question_data['action_text']:
            self.action_btn = GlassButton(self.question_data['action_text'], ":/icons/link.png")
            self.action_btn.clicked.connect(self.open_action_url)
            
            self.ignore_btn = GlassButton("Ignorer pour l'instant", ":/icons/skip.png")
            self.ignore_btn.clicked.connect(lambda: self.submit_response(False))
            
            action_layout = QHBoxLayout()
            action_layout.addWidget(self.action_btn)
            action_layout.addWidget(self.ignore_btn)
            
            layout.addLayout(action_layout)

    def submit_response(self, response: bool):
        """Émet le signal avec la réponse"""
        self.response_submitted.emit(self.question_data['id'], response)

    def open_action_url(self):
        """Ouvre l'URL d'action dans le navigateur"""
        if self.question_data['action_url']:
            webbrowser.open(self.question_data['action_url'])
            self.submit_response(True)  # Considérer que l'utilisateur a pris des mesures

    def resizeEvent(self, event):
        """Redimensionne le système de particules"""
        self.particles.resize(self.size())
        super().resizeEvent(event)

class ScoreWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.score = 0
        
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 20)
        self.setLayout(layout)
        
        # Label de score
        self.score_label = QLabel("Score: 0%")
        self.score_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #6c5ce7;
            }
        """)
        layout.addWidget(self.score_label)
        
        # Bouton de recommandations
        self.recommend_btn = GlassButton("Voir les recommandations", ":/icons/recommend.png")
        layout.addWidget(self.recommend_btn)
        
    def update_score(self, score: int):
        """Met à jour l'affichage du score"""
        self.score = score
        self.score_label.setText(f"Score: {score}%")
        
        # Changer la couleur en fonction du score
        if score < 40:
            color = "#ff4757"  # Rouge
        elif score < 70:
            color = "#ffa502"  # Orange
        else:
            color = "#2ed573"  # Vert
            
        self.score_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {color};
            }}
        """)

# Classes pour les effets visuels (ParticleSystem et GlassButton comme fournies dans votre exemple)
# ... (Insérez ici les classes ParticleSystem et GlassButton que vous avez fournies)





import sys
import sqlite3
import webbrowser
from typing import Dict, Optional
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QMessageBox, 
                            QCheckBox, QHBoxLayout, QLabel, QProgressBar)

from demarrage.baseDialog import BaseDialog
class MarketingEvaluationDialog(BaseDialog):
    evaluation_complete = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.questions = []  # Initialiser la liste des questions
        self.current_question_index = 0
        self.responses = {}
        self.init_db()  # Cette méthode doit charger les questions dans self.questions
        self.init_ui()
        self.load_progress()  # Maintenant self.questions est disponible
        self.show_question()

    def init_db(self):
        """Initialise la base de données et charge les questions"""
        self.conn = sqlite3.connect('marketing_evaluation.db')
        self.cursor = self.conn.cursor()

        # Création des tables si elles n'existent pas
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            text TEXT NOT NULL,
            weight INTEGER NOT NULL,
            action_url TEXT,
            category TEXT
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            response BOOLEAN NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(question_id) REFERENCES questions(id)
        )
        """)

        # Charger les questions dans self.questions
        self.cursor.execute("SELECT id, text, weight, action_url, category FROM questions ORDER BY id")
        self.questions = self.cursor.fetchall()

        # Si pas de questions, insérer les valeurs par défaut
        if not self.questions:
            self.insert_default_questions()
            self.cursor.execute("SELECT id, text, weight, action_url, category FROM questions ORDER BY id")
            self.questions = self.cursor.fetchall()

        # Insertion des questions si la table est vide
        self.cursor.execute("SELECT COUNT(*) FROM questions")
        if self.cursor.fetchone()[0] == 0:
            self.insert_default_questions()

        self.conn.commit()

    def insert_default_questions(self):
        """Insère les questions par défaut dans la base de données"""
        questions = [
            (1, "Avez-vous une page Google My Business pour votre entreprise?", 8,
             "https://www.google.com/business/", "online_presence"),
            (2, "Avez-vous un site web professionnel pour votre entreprise?", 10,
             "https://sites.google.com/", "online_presence"),
            (3, "Avez-vous une boutique en ligne (e-commerce)?", 7,
             "https://www.shopify.com/", "ecommerce"),
            # ... (ajouter les autres questions de la même manière)
            (20, "Avez-vous une stratégie pour les influenceurs ou ambassadeurs?", 5,
             "https://influencermarketinghub.com/", "social_media")
        ]
        self.cursor.executemany(
            "INSERT INTO questions (id, text, weight, action_url, category) VALUES (?, ?, ?, ?, ?)",
            questions
        )

    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("Évaluation de Présence Marketing")
        self.setWindowIcon(QIcon(":/icons/chart.png"))
        self.setMinimumSize(600, 400)

        # Style premium
        self.setStyleSheet("""
            MarketingEvaluationDialog {
                background-color: #2a2a3a;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-family: 'Segoe UI';
            }
            QCheckBox {
                color: #cccccc;
                font-size: 14px;
                spacing: 10px;
            }
            QProgressBar {
                height: 12px;
                border-radius: 6px;
                background-color: #3a3a4a;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #6c5ce7;
                border-radius: 6px;
            }
        """)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.main_layout.addWidget(self.progress_bar)

        # Conteneur de question
        self.question_container = QVBoxLayout()
        self.question_container.setSpacing(15)

        # Label de question
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-size: 18px; font-weight: 600;")
        self.question_container.addWidget(self.question_label)

        # Options de réponse
        self.response_layout = QVBoxLayout()

        # Case à cocher pour "Oui"
        self.yes_checkbox = QCheckBox("Oui, c'est déjà mis en place")
        self.yes_checkbox.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px; }")

        # Case à cocher pour action
        self.action_checkbox = QCheckBox()
        self.action_checkbox.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px; }")

        self.response_layout.addWidget(self.yes_checkbox)
        self.response_layout.addWidget(self.action_checkbox)
        self.question_container.addLayout(self.response_layout)

        # Boutons de navigation
        self.button_layout = QHBoxLayout()

        self.skip_button = QPushButton("Passer")
        self.skip_button.setStyleSheet(self.get_button_style("#4a4a5a"))
        self.skip_button.clicked.connect(self.skip_question)

        self.next_button = QPushButton("Suivant")
        self.next_button.setStyleSheet(self.get_button_style("#6c5ce7"))
        self.next_button.clicked.connect(self.next_question)

        self.button_layout.addWidget(self.skip_button)
        self.button_layout.addWidget(self.next_button)

        self.main_layout.addLayout(self.question_container)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

    def get_button_style(self, color: str) -> str:
        """Retourne le style CSS pour un bouton"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {self.adjust_color(color, 20)};
            }}
            QPushButton:pressed {{
                background-color: {self.adjust_color(color, -20)};
            }}
        """

    def adjust_color(self, color: str, amount: int) -> str:
        """Ajuste la luminosité d'une couleur hexadécimale (ex: #RRGGBB)"""
        r = max(0, min(255, int(color[1:3], 16) + amount))
        g = max(0, min(255, int(color[3:5], 16) + amount))
        b = max(0, min(255, int(color[5:7], 16) + amount))
        return f"#{r:02x}{g:02x}{b:02x}"

    def load_progress(self):
        """Charge les réponses existantes depuis la base de données"""
        # Maintenant self.questions est bien initialisé
        self.cursor.execute("SELECT question_id, response FROM responses")
        self.responses = {row[0]: bool(row[1]) for row in self.cursor.fetchall()}
        self.calculate_score()

    def show_question(self):
        """Affiche la question actuelle"""
        if self.current_question_index >= len(self.questions):
            self.evaluation_complete.emit(self.get_results())
            self.accept()
            return

        q_id, text, weight, action_url, category = self.questions[self.current_question_index]

        # Mise à jour de l'interface
        self.question_label.setText(text)
        self.yes_checkbox.setChecked(False)
        self.action_checkbox.setVisible(bool(action_url))

        if action_url:
            self.action_checkbox.setText(f"Créer/maintenir via {action_url.split('//')[1].split('/')[0]}")
            self.action_checkbox.setChecked(False)

        # Mise à jour de la progression
        progress = int((self.current_question_index / len(self.questions)) * 100)
        self.progress_bar.setValue(progress)

    def next_question(self):
        """Passe à la question suivante après validation"""
        q_id = self.questions[self.current_question_index][0]

        # Enregistrement de la réponse
        response = self.yes_checkbox.isChecked()
        action_taken = self.action_checkbox.isChecked() if self.action_checkbox.isVisible() else False

        # Si l'utilisateur a pris une action, considérer comme une réponse positive
        final_response = response or action_taken

        self.cursor.execute(
            "INSERT OR REPLACE INTO responses (question_id, response) VALUES (?, ?)",
            (q_id, final_response)
        )
        self.conn.commit()

        # Mise à jour des réponses en mémoire
        self.responses[q_id] = final_response

        # Si une action est demandée, ouvrir le lien
        if action_taken and self.questions[self.current_question_index][3]:
            webbrowser.open(self.questions[self.current_question_index][3])

        # Passer à la question suivante
        self.current_question_index += 1
        self.show_question()

        # Recalculer le score
        self.calculate_score()

    def skip_question(self):
        """Passe à la question suivante sans enregistrer de réponse"""
        self.current_question_index += 1
        self.show_question()

    def calculate_score(self):
        """Calcule le score actuel"""
        if not hasattr(self, 'questions') or not self.questions:
            self.current_score = 0
            return

        total_weight = sum(q[2] for q in self.questions)
        current_score = 0

        for q_id, response in self.responses.items():
            if response:
                # Trouver le poids de cette question
                for q in self.questions:
                    if q[0] == q_id:
                        current_score += q[2]
                        break

        self.current_score = int((current_score / total_weight) * 100) if total_weight > 0 else 0

    def get_results(self) -> Dict:
        """Retourne les résultats de l'évaluation"""
        return {
            'score': self.current_score,
            'responses': self.responses,
            'recommendations': self.generate_recommendations()
        }

    def generate_recommendations(self) -> List[str]:
        """Génère des recommandations basées sur les réponses"""
        recommendations = []

        # Analyse par catégorie
        categories = {}
        self.cursor.execute("SELECT category, SUM(weight) as total, SUM(weight * response) as score FROM questions LEFT JOIN responses ON questions.id = responses.question_id GROUP BY category")

        for category, total, score in self.cursor.fetchall():
            if score / total < 0.5:  # Moins de 50% dans cette catégorie
                recommendations.append(f"Améliorer votre présence dans la catégorie {category.replace('_', ' ')}")

        # Recommandations spécifiques
        self.cursor.execute("SELECT id, text FROM questions WHERE id NOT IN (SELECT question_id FROM responses WHERE response = 1)")
        for q_id, text in self.cursor.fetchall():
            recommendations.append(f"Envisagez de mettre en place: {text}")

        return recommendations

    def closeEvent(self, event):
        """Ferme proprement la connexion à la base de données"""
        self.conn.close()
        event.accept()
import sys
import sqlite3
import webbrowser
from typing import Dict, List
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QCheckBox, 
                            QHBoxLayout, QPushButton, QProgressBar)

from demarrage.baseDialog import BaseDialog

class MarketingEvaluationDialog(BaseDialog):
    evaluation_complete = pyqtSignal(dict)

    def __init__(self, title: str = "Évaluation Marketing"):
        # Initialisation des attributs avant super().__init__()
        self.questions = []
        self.responses = {}
        self.current_question_index = 0
        self.current_score = 0
        self.conn = None
        self.cursor = None
        
        super().__init__(title)
        
        # Initialisation séquentielle
        self.setup_database()
        self.load_questions()
        self.load_responses()
        
        # Configuration UI
        self.setMinimumSize(650, 350)
        self.setWindowIcon(QIcon(":/icons/chart.png"))

    def init_ui(self):
        """Initialise l'interface utilisateur"""
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)
        
        # Question
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.question_label)
        
        # Réponses
        self.yes_checkbox = QCheckBox("Oui, déjà implémenté")
        self.action_checkbox = QCheckBox()
        layout.addWidget(self.yes_checkbox)
        layout.addWidget(self.action_checkbox)
        
        # Boutons
        button_layout = QHBoxLayout()
        self.skip_button = QPushButton("Passer")
        self.next_button = QPushButton("Suivant")
        button_layout.addWidget(self.skip_button)
        button_layout.addWidget(self.next_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Connexions
        self.skip_button.clicked.connect(self.next_question)
        self.next_button.clicked.connect(self.process_response)
        
        # Afficher la première question
        self.show_question()

    def setup_database(self):
        """Configure la base de données"""
        self.conn = sqlite3.connect('marketing_eval.db')
        self.cursor = self.conn.cursor()
        
        # Création des tables
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            text TEXT NOT NULL,
            weight INTEGER NOT NULL,
            action_url TEXT,
            category TEXT
        )""")
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            question_id INTEGER PRIMARY KEY,
            response BOOLEAN NOT NULL,
            FOREIGN KEY(question_id) REFERENCES questions(id)
        )""")
        
        # Peuplement initial
        if not self.cursor.execute("SELECT 1 FROM questions LIMIT 1").fetchone():
            self.populate_questions()

    def populate_questions(self):
        """Insère les questions par défaut"""
        questions = [
            (1, "Avez-vous une page Google My Business?", 8, 
             "https://www.google.com/business/", "online_presence"),
            (2, "Avez-vous un site web professionnel?", 10,
             "https://sites.google.com/", "online_presence"),
            # ... (ajoutez les autres questions ici)
            (20, "Utilisez-vous des outils d'analyse?", 5,
             "https://analytics.google.com/", "analytics")
        ]
        
        self.cursor.executemany(
            "INSERT INTO questions VALUES (?, ?, ?, ?, ?)",
            questions
        )
        self.conn.commit()

    def load_questions(self):
        """Charge les questions depuis la base"""
        self.cursor.execute("SELECT id, text, weight, action_url FROM questions ORDER BY id")
        self.questions = self.cursor.fetchall()
        
        if not self.questions:
            raise ValueError("Aucune question trouvée dans la base de données")

    def load_responses(self):
        """Charge les réponses existantes"""
        self.cursor.execute("SELECT question_id, response FROM responses")
        self.responses = dict(self.cursor.fetchall())

    def show_question(self):
        """Affiche la question actuelle"""
        if self.current_question_index >= len(self.questions):
            self.finalize_evaluation()
            return
            
        q_id, text, weight, action_url = self.questions[self.current_question_index]
        self.question_label.setText(text)
        
        # Configure l'action checkbox
        if action_url:
            domain = action_url.split('//')[1].split('/')[0]
            self.action_checkbox.setText(f"Créer sur {domain}")
            self.action_checkbox.setVisible(True)
        else:
            self.action_checkbox.setVisible(False)
        
        # Réinitialise les cases
        self.yes_checkbox.setChecked(False)
        self.action_checkbox.setChecked(False)
        
        # Met à jour la progression
        progress = int((self.current_question_index / len(self.questions)) * 100)
        self.progress_bar.setValue(progress)

    def process_response(self):
        """Traite la réponse et passe à la suivante"""
        q_id, _, _, action_url = self.questions[self.current_question_index]
        response = self.yes_checkbox.isChecked()
        action_taken = self.action_checkbox.isChecked() if action_url else False
        
        # Enregistrement
        self.cursor.execute(
            "INSERT OR REPLACE INTO responses VALUES (?, ?)",
            (q_id, response or action_taken)
        )
        self.conn.commit()
        
        # Ouvre l'URL si nécessaire
        if action_taken and action_url:
            webbrowser.open(action_url)
        
        self.next_question()

    def next_question(self):
        """Passe à la question suivante"""
        self.current_question_index += 1
        self.show_question()
        self.update_score()

    def update_score(self):
        """Calcule le score actuel"""
        total = sum(q[2] for q in self.questions)
        score = sum(q[2] for q in self.questions 
                  if self.responses.get(q[0], False))
        
        self.current_score = int((score / total) * 100) if total > 0 else 0

    def finalize_evaluation(self):
        """Termine l'évaluation et émet les résultats"""
        results = {
            'score': self.current_score,
            'recommendations': self.generate_recommendations()
        }
        self.evaluation_complete.emit(results)
        self.accept()

    def generate_recommendations(self):
        """Génère des recommandations personnalisées"""
        recommendations = []
        
        # Questions sans réponse positive
        answered = [qid for qid, resp in self.responses.items() if resp]
        missing = [q for q in self.questions if q[0] not in answered]
        
        for q in missing:
            rec = f"Mettre en place: {q[1]}"
            if q[3]:  # Si URL disponible
                rec += f" ({q[3]})"
            recommendations.append(rec)
        
        return recommendations

    def get_results(self) -> Dict:
        """Retourne les résultats pour BaseDialog"""
        return {
            'score': self.current_score,
            'questions_answered': len(self.responses),
            'total_questions': len(self.questions)
        }

    def closeEvent(self, event):
        """Nettoyage à la fermeture"""
        if self.conn:
            self.conn.close()
        super().closeEvent(event)







import sys
import sqlite3
import webbrowser
from typing import Dict, List, Tuple
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QCheckBox, QHBoxLayout, 
                            QPushButton, QProgressBar, QScrollArea, QWidget, 
                            QFrame, QSpacerItem, QSizePolicy)

from demarrage.baseDialog import BaseDialog
from demarrage.modules import GlassButton, ParticleSystem

class MarketingEvaluationDialog(BaseDialog):
    evaluation_complete = pyqtSignal(dict)

    def __init__(self, title: str = "Évaluation Marketing"):
        # Initialisation des attributs
        self.questions: List[Dict] = []
        self.responses: Dict[int, bool] = {}
        self.current_question_index: int = 0
        self.current_score: int = 0
        self.conn = None
        self.cursor = None
        
        super().__init__(title)
        
        # Configuration initiale
        self.setMinimumSize(800, 500)
        self.setWindowIcon(QIcon(":/icons/chart.png"))
        
        # Initialisation séquentielle
        self.setup_database()
        self.load_questions()
        self.load_responses()
        
        # # Effet de particules
        # self.particles = ParticleSystem(self)
        # self.particles.lower()
        # Background with particle system

    def init_ui(self):
        """Initialise l'interface avec un design premium"""
        self.bg = ParticleSystem(self)
        # self.bg.setGeometry(0, 0, self.width(), self.height())
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # Barre de progression stylisée
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                height: 12px;
                border-radius: 6px;
                background: #3a3a4a;
            }
            QProgressBar::chunk {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, 
                    stop:0 #6c5ce7, stop:1 #a29bfe
                );
                border-radius: 6px;
            }
        """)
        main_layout.addWidget(self.progress_bar)
        
        # Conteneur de question
        self.question_container = QVBoxLayout()
        self.question_container.setSpacing(25)
        
        # Label de question avec style
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: 600;
                color: #ffffff;
                padding: 15px;
            }
        """)
        self.question_container.addWidget(self.question_label)
        
        # Options de réponse
        self.response_container = QVBoxLayout()
        self.response_container.setSpacing(15)
        
        # Bouton Oui (GlassButton)
        self.yes_button = GlassButton("Oui, c'est fait", ":/icons/check.png")
        self.yes_button.clicked.connect(lambda: self.process_response(True))
        
        # Bouton Plus Tard (GlassButton)
        self.later_button = GlassButton("Plus tard", ":/icons/clock.png")
        self.later_button.clicked.connect(lambda: self.process_response(False))
        
        # Bouton Action (GlassButton)
        self.action_button = GlassButton("Faire maintenant", ":/icons/rocket.png")
        self.action_button.clicked.connect(self.handle_action)
        self.action_button.setVisible(False)
        
        self.response_container.addWidget(self.yes_button)
        self.response_container.addWidget(self.later_button)
        self.response_container.addWidget(self.action_button)
        
        self.question_container.addLayout(self.response_container)
        main_layout.addLayout(self.question_container)
        
        # Espacement
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)
        
        self.setLayout(main_layout)
        
        # Afficher la première question non répondue
        self.show_next_unanswered_question()


    def setup_database(self):
        """Configure la base de données SQLite"""
        self.conn = sqlite3.connect('marketing_evaluation.db')
        self.cursor = self.conn.cursor()
        
        # Création des tables
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            text TEXT NOT NULL,
            weight INTEGER NOT NULL,
            action_url TEXT,
            category TEXT
        )""")
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            question_id INTEGER PRIMARY KEY,
            response BOOLEAN NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(question_id) REFERENCES questions(id)
        )""")
        
        # Peuplement initial
        if not self.cursor.execute("SELECT 1 FROM questions LIMIT 1").fetchone():
            self.populate_default_questions()

    def populate_default_questions(self):
        """Insère les questions marketing par défaut"""
        questions = [
            (1, "Avez-vous une page Google My Business pour votre entreprise?", 8,
             "https://www.google.com/business/", "online_presence"),
            (2, "Avez-vous un site web professionnel pour votre entreprise?", 10,
             "https://sites.google.com/", "online_presence"),
            # ... (autres questions)
            (20, "Avez-vous une stratégie pour les influenceurs?", 5,
             "https://influencermarketinghub.com/", "social_media")
        ]
        
        self.cursor.executemany(
            "INSERT INTO questions VALUES (?, ?, ?, ?, ?)",
            questions
        )
        self.conn.commit()

    def load_questions(self):
        """Charge toutes les questions depuis la base"""
        self.cursor.execute("SELECT id, text, weight, action_url FROM questions ORDER BY id")
        self.questions = [
            {
                'id': row[0],
                'text': row[1],
                'weight': row[2],
                'action_url': row[3]
            } for row in self.cursor.fetchall()
        ]

    def load_responses(self):
        """Charge les réponses existantes"""
        self.cursor.execute("SELECT question_id, response FROM responses")
        self.responses = dict(self.cursor.fetchall())

    def show_next_unanswered_question(self):
        """Affiche la prochaine question non répondue"""
        for i, question in enumerate(self.questions):
            if question['id'] not in self.responses:
                self.current_question_index = i
                self.display_question(question)
                return
        
        # Toutes les questions ont été répondues
        self.show_summary()

    def display_question(self, question: Dict):
        """Affiche une question spécifique"""
        self.question_label.setText(question['text'])
        
        # Configure le bouton d'action si applicable
        if question['action_url']:
            domain = question['action_url'].split('//')[1].split('/')[0]
            self.action_button.setText(f"Ouvrir {domain}")
            self.action_button.setVisible(True)
        else:
            self.action_button.setVisible(False)
        
        # Met à jour la progression
        progress = int((self.current_question_index / len(self.questions)) * 100)
        self.progress_bar.setValue(progress)

    def process_response(self, response: bool):
        """Enregistre la réponse et passe à la suivante"""
        current_question = self.questions[self.current_question_index]
        
        self.cursor.execute(
            "INSERT OR REPLACE INTO responses VALUES (?, ?)",
            (current_question['id'], response)
        )
        self.conn.commit()
        
        # Met à jour le cache local
        self.responses[current_question['id']] = response
        
        # Passe à la question suivante
        self.show_next_unanswered_question()
        self.update_score()

    def handle_action(self):
        """Ouvre l'URL d'action et marque comme fait"""
        current_question = self.questions[self.current_question_index]
        webbrowser.open(current_question['action_url'])
        self.process_response(True)  # Considère comme fait

    def update_score(self):
        """Calcule le score actuel"""
        total = sum(q['weight'] for q in self.questions)
        score = sum(
            q['weight'] for q in self.questions 
            if self.responses.get(q['id'], False)
        )
        
        self.current_score = int((score / total) * 100) if total > 0 else 0

    def show_summary(self):
        """Affiche le récapitulatif final"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        container = QWidget()
        layout = QVBoxLayout()
        
        # Titre
        title = QLabel("Récapitulatif de votre présence marketing")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #ffffff;
            padding-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # Score
        score_label = QLabel(f"Score global: {self.current_score}%")
        score_label.setStyleSheet("""
            font-size: 18px;
            color: #a29bfe;
            padding-bottom: 30px;
        """)
        layout.addWidget(score_label)
        
        # Liste des questions
        for question in self.questions:
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setStyleSheet("background: rgba(255, 255, 255, 0.05); border-radius: 8px;")
            
            item_layout = QHBoxLayout()
            
            # Checkbox interactive
            chk = QCheckBox()
            chk.setChecked(self.responses.get(question['id'], False))
            chk.stateChanged.connect(
                lambda state, qid=question['id']: self.toggle_response(qid, state)
            )
            item_layout.addWidget(chk)
            
            # Texte de la question
            lbl = QLabel(question['text'])
            lbl.setWordWrap(True)
            lbl.setStyleSheet("""
                font-size: 16px;
                color: %s;
                padding: 8px;
            """ % ("#2ecc71" if self.responses.get(question['id'], False) else "#e74c3c"))
            item_layout.addWidget(lbl, 1)
            
            # Bouton d'action si applicable
            if question['action_url']:
                btn = GlassButton("Ouvrir", ":/icons/link.png", self)
                btn.setFixedSize(80, 30)
                btn.clicked.connect(
                    lambda _, url=question['action_url']: webbrowser.open(url)
                )
                item_layout.addWidget(btn)
            
            frame.setLayout(item_layout)
            layout.addWidget(frame)
        
        # Bouton de fermeture
        close_btn = GlassButton("Terminer", ":/icons/check.png", self)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, 0, Qt.AlignRight)
        
        container.setLayout(layout)
        scroll.setWidget(container)
        
        # Remplace le contenu principal
        self.layout().removeItem(self.layout().itemAt(1))
        self.layout().addWidget(scroll, 1)
        
        # Désactive les particules en arrière-plan
        # self.bg.setVisible(False)


        
    def toggle_response(self, question_id: int, state: int):
        """Basculer une réponse dans la base de données"""
        response = state == Qt.Checked
        self.cursor.execute(
            "INSERT OR REPLACE INTO responses VALUES (?, ?)",
            (question_id, response)
        )
        self.conn.commit()
        self.responses[question_id] = response
        self.update_score()

    def get_results(self) -> Dict:
        """Retourne les résultats pour BaseDialog"""
        return {
            'score': self.current_score,
            'completed': len([r for r in self.responses.values() if r]),
            'total': len(self.questions)
        }

    def closeEvent(self, event):
        """Nettoyage à la fermeture"""
        if self.conn:
            self.conn.close()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Style global
    app.setStyle("Fusion")
    
    window = MarketingPresenceApp()
    window.show()
    
    sys.exit(app.exec_())