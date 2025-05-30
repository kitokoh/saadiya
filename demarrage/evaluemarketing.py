import sys
import sqlite3
from pathlib import Path
from PyQt5.QtCore import (Qt, pyqtSignal, pyqtProperty, QPropertyAnimation, 
                         QEasingCurve, QRectF, QSize, QPoint)
from PyQt5.QtGui import (QPainter, QColor, QPen, QFont, QLinearGradient,
                        QPixmap, QIcon, QBrush, QRadialGradient)
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QWidget, QFrame, QStackedWidget, 
                            QScrollArea, QGraphicsOpacityEffect, 
                            QGraphicsDropShadowEffect, QProgressBar)
from typing import List, Dict, Optional, Tuple, Callable


class CleanQuestionCard(QFrame):
    """Carte de question épurée avec interactions fluides"""
    
    answered = pyqtSignal(int, bool)  # question_id, is_correct
    
    def __init__(self, question_data: Dict, parent=None):
        super().__init__(parent)
        self.question_data = question_data
        self._setup_ui()
        self._setup_effects()
        
    def _setup_ui(self):
        self.setFixedHeight(350)
        self.setStyleSheet("""
            CleanQuestionCard {
                background: rgba(30, 35, 45, 0.9);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.08);
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.question_num = QLabel(f"Q{self.question_data['id']}")
        self.question_num.setStyleSheet("""
            QLabel {
                color: #6c8dfa;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        self.category = QLabel(self.question_data['category'].upper())
        self.category.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.6);
                font-size: 11px;
                letter-spacing: 1px;
            }
        """)
        
        header_layout.addWidget(self.question_num)
        header_layout.addStretch()
        header_layout.addWidget(self.category)
        
        # Question text
        self.question_text = QLabel(self.question_data['text'])
        self.question_text.setWordWrap(True)
        self.question_text.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                line-height: 1.4;
            }
        """)
        
        # Explanation (hidden by default)
        self.explanation = QLabel(self.question_data.get('explanation', ''))
        self.explanation.setWordWrap(True)
        self.explanation.setStyleSheet("""
            QLabel {
                color: rgba(200, 200, 255, 0.8);
                font-size: 13px;
                font-style: italic;
                padding: 12px;
                background: rgba(0, 0, 0, 0.2);
                border-radius: 8px;
                border-left: 2px solid #6c8dfa;
            }
        """)
        self.explanation.hide()
        
        # Buttons
        self.btn_yes = self._create_button("Oui", "#4CAF50")
        self.btn_no = self._create_button("Non", "#F44336")
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.addWidget(self.btn_yes)
        buttons_layout.addWidget(self.btn_no)
        
        # Signals
        self.btn_yes.clicked.connect(lambda: self._handle_response(True))
        self.btn_no.clicked.connect(lambda: self._handle_response(False))
        
        # Assembly
        layout.addWidget(header)
        layout.addWidget(self.question_text, 1)
        layout.addWidget(self.explanation)
        layout.addLayout(buttons_layout)
    
    def _setup_effects(self):
        # Shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
    
    def _create_button(self, text: str, color: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedHeight(45)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color}, stop:1 rgba(255,255,255,0.1));
            }}
        """)
        return btn
    
    def _handle_response(self, response: bool):
        self.btn_yes.setEnabled(False)
        self.btn_no.setEnabled(False)
        self.answered.emit(self.question_data['id'], response)

class ResultsView(QScrollArea):
    """Vue des résultats minimaliste et efficace"""
    
    def __init__(self, results_data: Dict, parent=None):
        super().__init__(parent)
        self.results_data = results_data
        self._setup_ui()
    
    def _setup_ui(self):
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        container = QWidget()
        self.setWidget(container)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # Header
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4b6cb7, stop:1 #182848);
                border-radius: 12px;
            }
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 30, 30, 30)
        
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        
        title = QLabel("Résultats de l'Évaluation")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        
        subtitle = QLabel(self._get_summary_text())
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                margin-top: 5px;
            }
        """)
        subtitle.setWordWrap(True)
        
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)
        text_layout.addStretch()
        
        # Progress circle
        self.progress = MinimalProgressCircle()
        self.progress.set_value_animated(self.results_data['score'])
        
        header_layout.addWidget(text_widget)
        header_layout.addWidget(self.progress)
        
        # Categories
        for cat, data in self.results_data['categories'].items():
            cat_widget = self._create_category_widget(cat, data)
            layout.addWidget(cat_widget)
        
        layout.addWidget(header)
        layout.addStretch()
    
    def _create_category_widget(self, category: str, data: Dict) -> QWidget:
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background: rgba(40, 45, 55, 0.8);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Category header
        header = QHBoxLayout()
        
        cat_label = QLabel(category.upper())
        cat_label.setStyleSheet("""
            QLabel {
                color: #6c8dfa;
                font-weight: bold;
                font-size: 14px;
                letter-spacing: 1px;
            }
        """)
        
        score_label = QLabel(f"{data['score']}%")
        score_label.setStyleSheet("""
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
        
        header.addWidget(cat_label)
        header.addStretch()
        header.addWidget(score_label)
        
        # Progress bar
        progress = QProgressBar()
        progress.setValue(data['score'])
        progress.setTextVisible(False)
        progress.setFixedHeight(6)
        progress.setStyleSheet("""
            QProgressBar {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6c8dfa, stop:1 #4b6cb7);
                border-radius: 3px;
            }
        """)
        
        # Recommendations
        rec_label = QLabel("• " + "\n• ".join(data.get('recommendations', [])))
        rec_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 13px;
                margin-top: 10px;
            }
        """)
        rec_label.setWordWrap(True)
        
        layout.addLayout(header)
        layout.addWidget(progress)
        layout.addWidget(rec_label)
        
        return widget
    
    def _get_summary_text(self) -> str:
        score = self.results_data['score']
        if score >= 80:
            return "Performance exceptionnelle ! Votre stratégie marketing est excellente."
        elif score >= 60:
            return "Bonnes performances. Quelques optimisations possibles."
        elif score >= 40:
            return "Potentiel à développer. Des améliorations significatives sont possibles."
        else:
            return "Des progrès importants sont nécessaires. Concentrez-vous sur les fondamentaux."

class MinimalProgressCircle(QWidget):
    """Cercle de progression minimaliste avec animation fluide"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self._value = 0
        self._max = 100
        self._thickness = 8
        self._bg_color = QColor(255, 255, 255, 20)
        self._fg_gradient = QLinearGradient(0, 0, 100, 100)
        self._fg_gradient.setColorAt(0, QColor(100, 149, 237))  # Cornflower blue
        self._fg_gradient.setColorAt(1, QColor(65, 105, 225))    # Royal blue
        
        self.animation = QPropertyAnimation(self, b"value")
        self.animation.setDuration(800)
        self.animation.setEasingCurve(QEasingCurve.OutExpo)
    
    @pyqtProperty(int)
    def value(self):
        return self._value
    
    @value.setter
    def value(self, v):
        self._value = max(0, min(v, self._max))
        self.update()
    
    def set_value_animated(self, value):
        self.animation.stop()
        self.animation.setStartValue(self._value)
        self.animation.setEndValue(value)
        self.animation.start()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = QRectF(self._thickness, self._thickness,
                     self.width() - 2*self._thickness,
                     self.height() - 2*self._thickness)
        
        # Fond
        painter.setPen(QPen(self._bg_color, self._thickness))
        painter.drawEllipse(rect)
        
        # Progression
        if self._value > 0:
            angle = int(360 * self._value / self._max)
            painter.setPen(QPen(QBrush(self._fg_gradient), self._thickness))
            painter.drawArc(rect, 90*16, -angle*16)
        
        # Texte
        painter.setPen(Qt.white)
        font = QFont("Arial", 12, QFont.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, f"{self._value}%")



import sys
import sqlite3
from pathlib import Path
from typing import Dict, List
from PyQt5.QtCore import (Qt, pyqtSignal, pyqtProperty, QPropertyAnimation, 
                         QEasingCurve, QRectF, QSize, QRect, QPoint)
from PyQt5.QtGui import (QPainter, QColor, QPen, QFont, QLinearGradient,
                        QPixmap, QIcon, QBrush, QRadialGradient)
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QWidget, QFrame, QStackedWidget, 
                            QScrollArea, QGraphicsOpacityEffect, 
                            QGraphicsDropShadowEffect, QProgressBar, QCheckBox,
                            QLineEdit, QSpacerItem, QSizePolicy)

from demarrage.baseDialog import BaseDialog
from PyQt5.QtCore import QParallelAnimationGroup
from demarrage.modules import ParticleSystem
class MarketingEvaluationDialog(BaseDialog):
    """Évaluation marketing moderne et épurée"""
    
    def init_ui(self):
        # Configuration de base
        self.setWindowTitle("Évaluation Marketing")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(900, 700)
        
        # Fond avec particules animées (si ParticleSystem est disponible)
        if hasattr(self, 'ParticleSystem'):
            self.bg = ParticleSystem(self)
            self.bg.setGeometry(0, 0, self.width(), self.height())
        
        # Conteneur principal
        self.container = QWidget(self)
        self.container.setGeometry(50, 50, 800, 600)
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            #container {
                background: rgba(30, 35, 45, 0.95);
                border-radius: 25px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
            }
        """)
        
        # Ombre portée
        self.container_shadow = QGraphicsDropShadowEffect(self.container)
        self.container_shadow.setBlurRadius(40)
        self.container_shadow.setColor(QColor(0, 0, 0, 200))
        self.container_shadow.setOffset(0, 15)
        self.container.setGraphicsEffect(self.container_shadow)
        
        # Layout principal
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Initialisation des données
        self._init_db()
        self._load_questions()
        
        # Barre de navigation
        self.setup_nav_bar(layout)
        
        # Stack de contenu
        self.content_stack = QStackedWidget()
        layout.addWidget(self.content_stack)
        
        # Écrans
        self.setup_welcome_screen()
        self.setup_questions_screen()
        
        # Bouton de fermeture
        self.setup_close_button()
        
        # Animation d'ouverture
        self.open_animation()
        
        # Style supplémentaire
        self.apply_styles()
    
    def _init_db(self):
        """Initialise la base de données SQLite"""
        db_path = Path.home() / "marketing_evalol.db"
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
        # Create tables if not exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                category TEXT NOT NULL,
                weight INTEGER DEFAULT 1,
                explanation TEXT,
                action_url TEXT
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS responses (
                question_id INTEGER PRIMARY KEY,
                response BOOLEAN NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(question_id) REFERENCES questions(id)
            )
        """)
        
        # Insert sample questions if empty
        if not self.cursor.execute("SELECT 1 FROM questions LIMIT 1").fetchone():
            self._insert_sample_questions()
        
        self.conn.commit()
    
    def _insert_sample_questions(self):
        """Insère des questions exemple"""
        questions = [
            {
                'id': 1,
                'text': "Avez-vous une stratégie de marque documentée ?",
                'category': "Branding",
                'weight': 2,
                'explanation': "Une stratégie claire améliore la reconnaissance de marque.",
                'action_url': "https://example.com/brand-strategy"
            },
            {
                'id': 2,
                'text': "Utilisez-vous des outils d'analyse marketing ?",
                'category': "Analytics",
                'weight': 1,
                'explanation': "Les données permettent des décisions éclairées.",
                'action_url': "https://example.com/analytics-tools"
            }
        ]
        
        self.cursor.executemany("""
            INSERT INTO questions (id, text, category, weight, explanation, action_url)
            VALUES (:id, :text, :category, :weight, :explanation, :action_url)
        """, questions)
    
    def _load_questions(self):
        """Charge les questions depuis la base de données"""
        self.cursor.execute("""
            SELECT id, text, category, weight, explanation, action_url
            FROM questions
            ORDER BY weight DESC, id
        """)
        self.questions = [dict(row) for row in self.cursor.fetchall()]
        self.responses = {}
        
        # Load existing responses
        self.cursor.execute("SELECT question_id, response FROM responses")
        self.responses = {row[0]: row[1] for row in self.cursor.fetchall()}
        
        self.current_question_idx = 0
        self._current_score = 0
    
    def setup_nav_bar(self, layout):
        """Configure la barre de navigation supérieure"""
        self.nav_bar = QFrame()
        self.nav_bar.setFixedHeight(60)
        self.nav_bar.setStyleSheet("""
            QFrame {
                background: rgba(35, 40, 50, 0.8);
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }
        """)
        
        nav_layout = QHBoxLayout(self.nav_bar)
        nav_layout.setContentsMargins(20, 10, 20, 10)
        
        # Titre
        title = QLabel("Évaluation Marketing")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedWidth(150)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background: #6c8dfa;
                border-radius: 3px;
            }
        """)
        
        # Score
        self.score_label = QLabel("Score: 0%")
        self.score_label.setStyleSheet("""
            QLabel {
                color: white;
                font-weight: bold;
                min-width: 80px;
            }
        """)
        
        nav_layout.addWidget(title)
        nav_layout.addStretch()
        nav_layout.addWidget(self.progress_bar)
        nav_layout.addWidget(self.score_label)
        
        layout.addWidget(self.nav_bar)
    
    def setup_welcome_screen(self):
        """Configure l'écran d'accueil"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4b6cb7, stop:1 #182848);
            }
        """)
        header.setFixedHeight(200)
        
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(40, 40, 40, 40)
        
        title = QLabel("Évaluation Marketing")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
            }
        """)
        
        subtitle = QLabel("Évaluez votre stratégie marketing en questions clés")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                margin-top: 5px;
            }
        """)
        subtitle.setWordWrap(True)
        
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.addStretch()
        
        # Content
        content = QFrame()
        content.setStyleSheet("background: white;")
        
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 40, 40, 40)
        
        desc = QLabel("""
            <p>Cette évaluation vous permettra de:</p>
            <ul>
                <li>Mesurer l'efficacité de votre stratégie</li>
                <li>Identifier les axes d'amélioration</li>
                <li>Recevoir des recommandations personnalisées</li>
            </ul>
            <p>Durée estimée: 5 minutes</p>
        """)
        desc.setStyleSheet("font-size: 15px;")
        desc.setWordWrap(True)
        
        start_btn = QPushButton("Commencer")
        start_btn.setStyleSheet("""
            QPushButton {
                background: #4b6cb7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
                font-size: 16px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                background: #3a5a9b;
            }
        """)
        start_btn.clicked.connect(self._start_evaluation)
        
        content_layout.addWidget(desc)
        content_layout.addWidget(start_btn, 0, Qt.AlignCenter)
        content_layout.addStretch()
        
        layout.addWidget(header)
        layout.addWidget(content)
        
        self.content_stack.addWidget(widget)
    
    def setup_questions_screen(self):
        """Configure l'écran des questions"""
        self.questions_widget = QWidget()
        questions_layout = QVBoxLayout(self.questions_widget)
        questions_layout.setContentsMargins(40, 20, 40, 40)
        
        self.question_stack = QStackedWidget()
        questions_layout.addWidget(self.question_stack)
        
        self.content_stack.addWidget(self.questions_widget)
    
    def setup_close_button(self):
        self.close_btn = QPushButton("✕", self.container)
        self.close_btn.setGeometry(750, 20, 40, 40)
        self.close_btn.setStyleSheet("""
            QPushButton {
                color: white;
                background: transparent;
                border: none;
                font-size: 20px;
                font-weight: bold;
                border-radius: 20px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
            }
        """)
        self.close_btn.clicked.connect(self.close_with_animation)
    
    def open_animation(self):
        self.anim_group = QParallelAnimationGroup(self)
        
        # Animation d'opacité
        opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        opacity_anim.setDuration(350)
        opacity_anim.setStartValue(0)
        opacity_anim.setEndValue(1)
        
        # Animation de scale
        scale_anim = QPropertyAnimation(self.container, b"geometry")
        scale_anim.setDuration(500)
        scale_anim.setStartValue(QRect(50, 150, 800, 0))
        scale_anim.setEndValue(QRect(50, 50, 800, 600))
        scale_anim.setEasingCurve(QEasingCurve.OutBack)
        
        self.anim_group.addAnimation(opacity_anim)
        self.anim_group.addAnimation(scale_anim)
        self.anim_group.start()
    
    def close_with_animation(self):
        self.close_anim = QParallelAnimationGroup(self)
        
        opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        opacity_anim.setDuration(300)
        opacity_anim.setStartValue(1)
        opacity_anim.setEndValue(0)
        
        scale_anim = QPropertyAnimation(self.container, b"geometry")
        scale_anim.setDuration(400)
        scale_anim.setStartValue(QRect(50, 50, 800, 600))
        scale_anim.setEndValue(QRect(50, 150, 800, 0))
        scale_anim.setEasingCurve(QEasingCurve.InBack)
        
        self.close_anim.addAnimation(opacity_anim)
        self.close_anim.addAnimation(scale_anim)
        self.close_anim.finished.connect(self.accept)
        self.close_anim.start()
    
    def apply_styles(self):
        self.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 10px;
                margin: 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                min-height: 30px;
                border-radius: 5px;
            }
        """)
    
    def _start_evaluation(self):
        """Démarre l'évaluation"""
        self.current_question_idx = 0
        self._prepare_questions()
        self.content_stack.setCurrentIndex(1)
        self._show_current_question()
    
    def _prepare_questions(self):
        """Prépare toutes les cartes de questions"""
        # self.question_stack.clear()

        # OU Méthode 2: Plus concise
        for i in reversed(range(self.question_stack.count())):
            self.question_stack.removeWidget(self.question_stack.widget(i))


        for question in self.questions:
            card = CleanQuestionCard(question)
            card.answered.connect(self._handle_answer)
            self.question_stack.addWidget(card)
    
    def _show_current_question(self):
        """Affiche la question actuelle"""
        if self.current_question_idx >= len(self.questions):
            self._show_results()
            return
            
        self.question_stack.setCurrentIndex(self.current_question_idx)
        
        # Update progress
        progress = int((self.current_question_idx / len(self.questions)) * 100)
        self.progress_bar.setValue(progress)
        
        # Update window title
        self.setWindowTitle(f"Question {self.current_question_idx + 1}/{len(self.questions)}")
    
    def _handle_answer(self, question_id: int, response: bool):
        """Enregistre une réponse"""
        # Save to database
        self.cursor.execute("""
            INSERT OR REPLACE INTO responses (question_id, response)
            VALUES (?, ?)
        """, (question_id, response))
        
        self.conn.commit()
        self.responses[question_id] = response
        
        # Next question
        self.current_question_idx += 1
        self._update_score()
        self._show_current_question()
    
    def _update_score(self):
        """Calcule et met à jour le score"""
        total = sum(q['weight'] for q in self.questions)
        achieved = sum(q['weight'] for q in self.questions if self.responses.get(q['id'], False))
        
        new_score = int((achieved / total) * 100) if total > 0 else 0
        
        # Animate score change
        anim = QPropertyAnimation(self, b"current_score")
        anim.setDuration(500)
        anim.setEasingCurve(QEasingCurve.OutQuad)
        anim.setStartValue(self._current_score)
        anim.setEndValue(new_score)
        anim.start()
        
        self._current_score = new_score
    
    def _show_results(self):
        """Affiche les résultats finaux"""
        results = self._compile_results()
        results_view = ResultsView(results)
        
        self.content_stack.addWidget(results_view)
        self.content_stack.setCurrentIndex(2)
    
    def _compile_results(self) -> Dict:
        """Compile les résultats"""
        categories = {}
        
        for q in self.questions:
            if q['category'] not in categories:
                categories[q['category']] = {'total': 0, 'score': 0}
            
            categories[q['category']]['total'] += q['weight']
            if self.responses.get(q['id'], False):
                categories[q['category']]['score'] += q['weight']
        
        # Convert to percentages
        for cat in categories.values():
            cat['score'] = int((cat['score'] / cat['total']) * 100) if cat['total'] > 0 else 0
            cat['recommendations'] = self._generate_recommendations(cat['score'])
        
        # Global score
        total = sum(q['weight'] for q in self.questions)
        achieved = sum(q['weight'] for q in self.questions if self.responses.get(q['id'], False))
        global_score = int((achieved / total) * 100) if total > 0 else 0
        
        return {
            'score': global_score,
            'categories': categories,
            'total_questions': len(self.questions),
            'answered': len(self.responses)
        }
    
    def _generate_recommendations(self, score: int) -> List[str]:
        """Génère des recommandations basées sur le score"""
        if score < 40:
            return [
                "Priorisez les fondamentaux",
                "Consultez nos guides pour débutants",
                "Allouez des ressources dédiées"
            ]
        elif score < 70:
            return [
                "Optimisez vos processus",
                "Formez votre équipe",
                "Mettez en place des tests"
            ]
        else:
            return [
                "Maintenez vos résultats",
                "Explorez des innovations",
                "Partagez vos bonnes pratiques"
            ]
    
    @pyqtProperty(int)
    def current_score(self):
        return self._current_score
    
    @current_score.setter
    def current_score(self, value):
        self._current_score = value
        self._update_score_display()
    
    def _update_score_display(self):
        """Met à jour l'affichage du score"""
        color = (
            "#F44336" if self._current_score < 40
            else "#FFC107" if self._current_score < 70
            else "#4CAF50"
        )
        
        self.score_label.setText(f"Score: {self._current_score}%")
        self.score_label.setStyleSheet(f"color: {color}; font-weight: bold;")
    
    def closeEvent(self, event):
        """Ferme la base de données à la fermeture"""
        self.conn.close()
        super().closeEvent(event)
    def _insert_sample_questions(self):
        """Insère des questions exemple"""
        questions = [
            {'id': 1, 'text': "Avez-vous une stratégie de marque documentée ?", 'category': "Branding", 'weight': 2},
            {'id': 2, 'text': "Utilisez-vous des outils d'analyse marketing ?", 'category': "Analytics", 'weight': 1},
            {'id': 3, 'text': "Segmenter-vous votre audience pour vos campagnes ?", 'category': "Targeting", 'weight': 1},
            {'id': 4, 'text': "Avez-vous défini des personas clients ?", 'category': "Targeting", 'weight': 1},
            {'id': 5, 'text': "Mesurez-vous le ROI de vos actions marketing ?", 'category': "Analytics", 'weight': 2},
            {'id': 6, 'text': "Utilisez-vous le marketing automation ?", 'category': "Technology", 'weight': 1},
            {'id': 7, 'text': "Avez-vous une présence sur les réseaux sociaux ?", 'category': "Digital", 'weight': 1},
            {'id': 8, 'text': "Produisez-vous du contenu marketing régulièrement ?", 'category': "Content", 'weight': 1},
            {'id': 9, 'text': "Faites-vous des tests A/B sur vos campagnes ?", 'category': "Optimization", 'weight': 1},
            {'id': 10, 'text': "Avez-vous un plan de communication annuel ?", 'category': "Planning", 'weight': 2}
        ]
        
        self.cursor.executemany("""
            INSERT INTO questions (id, text, category, weight)
            VALUES (:id, :text, :category, :weight)
        """, questions)
    def _show_current_question(self):
        """Affiche la question actuelle"""
        if self.current_question_idx >= len(self.questions):
            self._show_results()
            return
            
        self.question_stack.setCurrentIndex(self.current_question_idx)
        
        # Update progress
        progress = int((self.current_question_idx / len(self.questions)) * 100)
        self.progress_bar.setValue(progress)
        
        # Update window title
        self.setWindowTitle(f"Question {self.current_question_idx + 1}/{len(self.questions)}")

# Les autres classes (CleanQuestionCard, ResultsView, MinimalProgressCircle) restent identiques
# à votre version originale et doivent être incluses dans le même fichier
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Set dark palette
    palette = app.palette()
    palette.setColor(palette.Window, QColor(25, 30, 40))
    palette.setColor(palette.WindowText, Qt.white)
    palette.setColor(palette.Base, QColor(35, 40, 50))
    palette.setColor(palette.AlternateBase, QColor(45, 50, 60))
    palette.setColor(palette.Text, Qt.white)
    palette.setColor(palette.Button, QColor(50, 55, 70))
    palette.setColor(palette.ButtonText, Qt.white)
    palette.setColor(palette.Highlight, QColor(100, 149, 237))
    palette.setColor(palette.HighlightedText, Qt.white)
    app.setPalette(palette)
    
    window = MarketingEvaluationDialog()
    window.show()
    sys.exit(app.exec_())

