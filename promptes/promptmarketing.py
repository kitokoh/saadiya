import sys
import random
import time
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QTextEdit, QPushButton, QRadioButton, QButtonGroup, 
                             QFrame, QScrollArea, QSpacerItem, QSizePolicy, QStackedWidget,
                             QProgressBar, QSystemTrayIcon, QMenu, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QSize, QThread, pyqtSignal, QPoint, QEasingCurve, QUrl
from PyQt5.QtGui import (QFont, QColor, QPalette, QPixmap, QIcon, QLinearGradient, 
                         QPainter, QCursor, QDesktopServices, QTextCursor)
from PyQt5.QtMultimedia import QSound
import sqlite3
from sqlite3 import Error
import json
import webbrowser
import markdown2
import platform
import os
from plyer import notification
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QComboBox, QGroupBox, QCheckBox, QLineEdit, QDialog
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtCore import QRect

from PyQt5.QtGui import QMovie      # :contentReference[oaicite:3]{index=3}

class AnalysisThread(QThread):
    """Thread séparé pour l'analyse du prompt"""
    analysis_complete = pyqtSignal(str, list)
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int)

    def __init__(self, prompt_text, db_path):
        super().__init__()
        self.prompt_text = prompt_text
        self.db_path = db_path
        self._is_running = True


    def runN(self):
        conn = None
        try:
            # ... (code existant jusqu'à la génération de l'analyse) ...
            
            # Générer le texte d'analyse
            analysis_text = self.generate_detailed_analysis(prompt_lower, detected)
            
            # Préparer la liste des plateformes détectées (sans les templates)
            detected_platforms = [(keyword, platform) for keyword, platform, _ in detected]
            
            # Émettre les résultats séparément
            self.analysis_complete.emit(analysis_text, detected_platforms)
            
        except Exception as e:
            self.error_occurred.emit(f"Erreur d'analyse : {str(e)}")
        finally:
            if conn:
                conn.close()        
    def run(self):
        conn = None
        try:
            # Créer une nouvelle connexion dans ce thread
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Simulation de progression
            for i in range(1, 101):
                if not self._is_running:
                    return
                time.sleep(0.02)
                self.progress_updated.emit(i)
            
            # Analyse réelle
            prompt_lower = self.prompt_text.lower()
            detected = []
            
            cursor.execute('SELECT keyword, platform, response_template FROM detection_rules')
            rules = cursor.fetchall()
            
            for keyword, platform, template in rules:
                if not self._is_running:
                    return
                if keyword in prompt_lower:
                    detected.append((keyword, platform, template))
            
            # Générer le texte d'analyse
            analysis_text = self.generate_detailed_analysis(prompt_lower, detected)



            # Préparer la liste des plateformes détectées (sans les templates)
            detected_platforms = [(keyword, platform) for keyword, platform, _ in detected]
            
            # Émettre les résultats séparément
            self.analysis_complete.emit(analysis_text, detected_platforms)
            # Émettre les résultats séparément (pas comme un tuple)
            # self.analysis_complete.emit(analysis_text, detected)
            
        except Exception as e:
            self.error_occurred.emit(f"Erreur d'analyse : {str(e)}")
        finally:
            if conn:
                conn.close()
                
    def run1(self):
        conn = None
        try:
            # Créer une nouvelle connexion dans ce thread
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Simulation de progression
            for i in range(1, 101):
                if not self._is_running:
                    return
                time.sleep(0.02)
                self.progress_updated.emit(i)
            
            # Analyse réelle
            prompt_lower = self.prompt_text.lower()
            detected = []
            
            cursor.execute('SELECT keyword, platform, response_template FROM detection_rules')
            rules = cursor.fetchall()
            
            for keyword, platform, template in rules:
                if not self._is_running:
                    return
                if keyword in prompt_lower:
                    detected.append((keyword, platform, template))
            
            analysis_text = self.generate_detailed_analysis(prompt_lower, detected)
            self.analysis_complete.emit(analysis_text, detected)
            
        except Exception as e:
            self.error_occurred.emit(f"Erreur d'analyse : {str(e)}")
        finally:
            if conn:
                conn.close()

    def stop(self):
        """Arrête proprement le thread"""
        self._is_running = False
        self.wait()

    def generate_detailed_analysis(self, prompt_lower, detected):
        """Génère un rapport d'analyse détaillé avec données fictives"""
        analysis_text = "## 📊 Analyse approfondie de votre demande\n\n"
        
        if not detected:
            analysis_text += ("Je comprends que vous souhaitez promouvoir votre contenu ou produit. "
                            "Voici des recommandations générales basées sur les meilleures pratiques marketing actuelles.\n\n")
        else:
            unique_platforms = list(set([p[1] for p in detected]))
            if len(unique_platforms) == 1:
                analysis_text += f"### Plateforme principale : **{unique_platforms[0].capitalize()}**\n\n"
            else:
                platforms_str = ', '.join([p.capitalize() for p in unique_platforms])
                analysis_text += f"### Plateformes concernées : **{platforms_str}**\n\n"
            
            # Détails par plateforme
            analysis_text += "## 🔍 Opportunités identifiées\n"
            for keyword, platform, template in detected:
                analysis_text += f"### {platform.capitalize()}\n"
                analysis_text += f"- **Mot-clé détecté** : {keyword}\n"
                analysis_text += f"- **Recommandation** : {template}\n"
                
                # Ajout de données fictives spécifiques
                if platform == "instagram":
                    analysis_text += (
                        "- **Statistiques fictives** :\n"
                        "  - Taux d'engagement moyen : 4.2%\n"
                        "  - Meilleur moment pour poster : 17h-19h\n"
                        "  - Hashtags recommandés : #marketingdigital #socialmedia #growth\n\n"
                    )
                elif platform == "facebook":
                    analysis_text += (
                        "- **Statistiques fictives** :\n"
                        "  - Portée moyenne des publications : 1,200 personnes\n"
                        "  - Taux de clic moyen : 3.8%\n"
                        "  - Coût moyen par clic (CPC) : €0.45\n\n"
                    )
                elif platform == "linkedin":
                    analysis_text += (
                        "- **Statistiques fictives** :\n"
                        "  - Taux de conversion moyen : 2.1%\n"
                        "  - Meilleur jour pour poster : Mercredi\n"
                        "  - Durée idéale des publications : 1,500-2,000 caractères\n\n"
                    )
            
            # Analyse sémantique fictive
            analysis_text += "## 🧠 Analyse sémantique avancée\n"
            sentiment = self.detect_sentiment(prompt_lower)
            analysis_text += f"- **Ton détecté** : {sentiment}\n"
            
            keywords_count = {
                "marketing": prompt_lower.count("marketing"),
                "réseaux": prompt_lower.count("réseaux"),
                "publicité": prompt_lower.count("publicité"),
                "vente": prompt_lower.count("vente")
            }
            top_keywords = [k for k, v in sorted(keywords_count.items(), key=lambda item: item[1], reverse=True) if v > 0]
            
            if top_keywords:
                analysis_text += f"- **Mots-clés dominants** : {', '.join(top_keywords[:3])}\n"
            
            # Recommandations basées sur l'analyse
            analysis_text += "\n## 🚀 Plan d'action recommandé\n"
            if "instagram" in [p[1] for p in detected]:
                analysis_text += ("1. **Stratégie Instagram**\n"
                                "   - Créer 3 posts/semaine avec visuels haute qualité\n"
                                "   - Publier 5 stories/semaine avec liens swipe-up\n"
                                "   - Collaborer avec 2 influenceurs/mois\n\n")
            
            if "facebook" in [p[1] for p in detected]:
                analysis_text += ("2. **Campagne Facebook Ads**\n"
                                "   - Budget recommandé : €500/mois\n"
                                "   - Cibler les 25-45 ans intéressés par le marketing\n"
                                "   - Tester 3 créations différentes\n\n")
            
            if not detected:
                analysis_text += ("1. **Audit marketing complet**\n"
                                "   - Analyser votre présence actuelle sur les réseaux\n"
                                "   - Identifier vos canaux les plus performants\n"
                                "   - Élaborer une stratégie cross-canal\n\n")
        
        # Conseils supplémentaires avec données
        analysis_text += "\n## 💡 Insights et bonnes pratiques\n"
        tips = [
            f"📈 **Performance moyenne du secteur** : Taux d'engagement de 3.5% sur les réseaux sociaux",
            f"⏱️ **Timing optimal** : Meilleures heures d'engagement entre 18h et 21h",
            f"📱 **Format préféré** : Les vidéos courtes génèrent 35% plus d'engagement que les images",
            f"💰 **ROI moyen** : €2.50 retournés pour chaque €1 dépensé en publicité sociale"
        ]
        analysis_text += "\n".join(f"- {tip}\n" for tip in tips)
        
        # Exemple de tableau de données fictif
        analysis_text += "\n## 📋 Tableau comparatif des plateformes\n"
        analysis_text += (
            "| Plateforme | Coût moyen | Taux d'engagement | Audience cible |\n"
            "|------------|------------|-------------------|----------------|\n"
            "| Instagram  | €0.30/click | 4.2%              | 18-34 ans      |\n"
            "| Facebook   | €0.45/click | 3.8%              | 25-65 ans      |\n"
            "| LinkedIn   | €1.20/click | 2.1%              | Professionnels |\n"
            "| TikTok     | €0.25/click | 8.5%              | 16-30 ans      |\n"
        )
        
        # return analysis_text
        return analysis_text, [(keyword, platform) for keyword, platform, _ in detected]

    def detect_sentiment(self, text):
        """Détecte le sentiment du texte (simulation)"""
        positive_words = ["excellent", "super", "génial", "fantastique", "réussir"]
        negative_words = ["problème", "difficile", "compliqué", "échec", "cher"]
        
        pos_count = sum(text.count(word) for word in positive_words)
        neg_count = sum(text.count(word) for word in negative_words)
        
        if pos_count > neg_count:
            return "Positif 😊"
        elif neg_count > pos_count:
            return "Négatif 😟"
        else:
            return "Neutre 😐"


class MarketingAIAnalyzer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Leopardo - Assistant Marketing IA")
        self.setMinimumSize(1000, 700)
        
        # Configuration initiale
        self.current_user = "Utilisateur"
        self.history = []
        self.settings = {
            "dark_mode": False,
            "animations": True,
            "notifications": True,
            "auto_save": True
        }
        
        # Initialisation des composants
        self.init_db()
        self.init_ui()
        self.load_settings()
        
        # Style global
        self.update_styles()
        
        # Dictionnaire des actions disponibles
        self.available_actions = {
            'instagram': self.launch_instagram_guide,
            'facebook': self.launch_facebook_guide,
            'linkedin': self.launch_linkedin_guide,
            'tiktok': self.launch_tiktok_guide,
            'email': self.launch_email_guide,
            'whatsapp': self.launch_whatsapp_guide,
            'twitter': self.launch_twitter_guide,
            'youtube': self.launch_youtube_guide,
            'analytics': self.show_analytics_tips,
            'content': self.show_content_tips
        }

    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Création de la barre d'outils
        self.create_toolbar()
        
        # Zone de contenu principale
        self.content_area = QWidget()
        self.content_area.setObjectName("contentArea")
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        # Stacked widget pour les différentes vues
        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)
        
        # Vue principale
        self.main_view = QWidget()
        self.setup_main_view()
        self.stacked_widget.addWidget(self.main_view)
        
        # Vue historique
        self.history_view = QWidget()
        self.setup_history_view()
        self.stacked_widget.addWidget(self.history_view)
        
        # Vue paramètres
        self.settings_view = QWidget()
        self.setup_settings_view()
        self.stacked_widget.addWidget(self.settings_view)
        
        self.main_layout.addWidget(self.content_area, stretch=1)
        
        # Barre de statut
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Prêt")

    def create_toolbar(self):
        """Crée une barre d'outils personnalisée"""
        toolbar = QWidget()
        toolbar.setObjectName("mainToolbar")
        toolbar.setFixedHeight(50)
        
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(15, 0, 15, 0)
        toolbar_layout.setSpacing(20)
        
        # Logo
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap(self.resource_path("assets/logo.png")).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # Boutons de navigation
        self.home_btn = QPushButton("Accueil")
        self.home_btn.setObjectName("navButton")
        self.home_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        self.history_btn = QPushButton("Historique")
        self.history_btn.setObjectName("navButton")
        self.history_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        self.settings_btn = QPushButton("Paramètres")
        self.settings_btn.setObjectName("navButton")
        self.settings_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        
        # Espacement
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # Bouton utilisateur
        self.user_btn = QPushButton(self.current_user)
        self.user_btn.setObjectName("userButton")
        self.user_btn.setIcon(QIcon(self.resource_path("assets/user.png")))
        self.user_btn.setIconSize(QSize(24, 24))
        
        toolbar_layout.addWidget(self.logo_label)
        toolbar_layout.addWidget(self.home_btn)
        toolbar_layout.addWidget(self.history_btn)
        toolbar_layout.addWidget(self.settings_btn)
        toolbar_layout.addWidget(spacer)
        toolbar_layout.addWidget(self.user_btn)
        
        self.main_layout.addWidget(toolbar)

    def setup_main_view(self):
        """Configure la vue principale avec UX optimisée"""
        layout = QVBoxLayout(self.main_view)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Fond dégradé
        self.main_view.setStyleSheet("background: qlineargradient(x1:0, y1:0, x1:1, y1:1, stop:0 #f8fafc, stop:1 #e0e7ff);")
        
        # Conteneur central
        center_container = QWidget()
        center_container.setMaximumWidth(900)
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(30, 30, 30, 30)
        center_layout.setSpacing(0)
        
        # En-tête conversationnelle
        header = QLabel("🤖  Bonjour, je suis Leopardo")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #1e40af;
            margin-bottom: 5px;
        """)
        
        subheader = QLabel("Comment puis-je vous aider aujourd'hui?")
        subheader.setStyleSheet("""
            font-size: 16px;
            color: #4b5563;
            margin-bottom: 30px;
        """)
        
        center_layout.addWidget(header)
        center_layout.addWidget(subheader)
        
        # Zone de message unifiée
        self.setup_prompt_section()
        center_layout.addWidget(self.prompt_container)
        
        # Barre de progression (initialement cachée)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                height: 6px;
                background: white;
            }
            QProgressBar::chunk {
                background: #3b82f6;
                border-radius: 8px;
            }
        """)
        self.progress_bar.hide()
        center_layout.addWidget(self.progress_bar)
        
        # Suggestions de prompts (boutons intelligents)
        self.setup_smart_prompts()
        center_layout.addLayout(self.smart_prompts_layout)
        
        # Zone de résultats avec animation
        self.setup_analysis_display()
        center_layout.addWidget(self.analysis_container)
        
        # Centrage vertical
        layout.addStretch()
        layout.addWidget(center_container)
        layout.addStretch()

    def setup_prompt_section(self):
        """Crée une zone de message moderne et unifiée"""
        self.prompt_container = QWidget()
        self.prompt_container.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 16px;
                border: 1px solid #d1d5db;
            }
        """)

        container_layout = QVBoxLayout(self.prompt_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Champ de texte élégant
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Décrivez votre besoin marketing... (ex: Je veux promouvoir mon nouveau produit sur les réseaux sociaux)")
        self.prompt_input.setStyleSheet("""
            QTextEdit {
                background: transparent;
                border: none;
                font-size: 16px;
                padding: 20px;
                border-radius: 16px;
                min-height: 120px;
            }
        """)
        
        # Bouton d'envoi flottant
        self.send_btn = QPushButton()
        self.send_btn.setIcon(QIcon.fromTheme("mail-send"))
        self.send_btn.setIconSize(QSize(24, 24))
        self.send_btn.setCursor(Qt.PointingHandCursor)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background: #3b82f6;
                border: none;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                margin: 10px;
            }
            QPushButton:hover {
                background: #2563eb;
            }
            QPushButton:disabled {
                background: #93c5fd;
            }
        """)
        self.send_btn.clicked.connect(self.analyze_prompt)
        
        # Overlay du bouton sur le QTextEdit
        self.btn_overlay = QWidget(self.prompt_input)
        self.btn_overlay_layout = QHBoxLayout(self.btn_overlay)
        self.btn_overlay_layout.addWidget(self.send_btn)
        self.btn_overlay_layout.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.btn_overlay.setStyleSheet("background: transparent;")
        
        container_layout.addWidget(self.prompt_input)

    def resizeEvent(self, event):
        """Redimensionne le bouton flottant quand la fenêtre change de taille"""
        super().resizeEvent(event)
        if hasattr(self, 'btn_overlay'):
            self.btn_overlay.setGeometry(QRect(
                self.prompt_input.width() - 60, 
                self.prompt_input.height() - 60, 
                50, 
                50
            ))

    def setup_smart_prompts(self):
        """Suggestions de prompts contextuelles"""
        self.smart_prompts_layout = QVBoxLayout()
        self.smart_prompts_layout.setSpacing(10)
        
        title = QLabel("Suggestions rapides:")
        title.setStyleSheet("font-size: 14px; color: #6b7280; margin-top: 15px;")
        self.smart_prompts_layout.addWidget(title)
        
        prompts_grid = QGridLayout()
        prompts_grid.setSpacing(10)
        
        self.prompt_buttons = []
        suggestions = [
            ("📱 Stratégie réseaux sociaux", "Crée une stratégie complète pour Instagram et TikTok"),
            ("📈 Analyse de marché", "Analyse le marché des produits similaires au mien"),
            ("✉️ Email marketing", "Rédige un email de newsletter engageant"),
            ("🎯 Audience cible", "Quelle est la meilleure audience pour mon produit?"),
            ("💰 Campagne publicitaire", "Suggestions pour une campagne Facebook Ads"),
            ("🔄 Optimisation", "Comment améliorer mes conversions?")
        ]
        
        for i, (emoji, text) in enumerate(suggestions):
            btn = QPushButton(f"{emoji} {text.split(' ')[0]}")
            btn.setToolTip(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: white;
                    border: 1px solid #e5e7eb;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 14px;
                    text-align: left;
                }
                QPushButton:hover {
                    background: #f3f4f6;
                    border-color: #d1d5db;
                }
            """)
            btn.clicked.connect(lambda _, t=text: self.prompt_input.setPlainText(t))
            prompts_grid.addWidget(btn, i//2, i%2)
            self.prompt_buttons.append(btn)
        
        self.smart_prompts_layout.addLayout(prompts_grid)

    def setup_analysis_display(self):
        """Zone de résultats avec interactions riches"""
        self.analysis_container = QWidget()
        self.analysis_container.setVisible(False)
        self.analysis_container.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout(self.analysis_container)
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(15)
        
        # Conteneur des résultats
        result_frame = QWidget()
        result_frame.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 16px;
                border: 1px solid #e5e7eb;
            }
        """)
        
        result_layout = QVBoxLayout(result_frame)
        result_layout.setContentsMargins(0, 0, 0, 0)
        
        # Barre d'outils des résultats
        toolbar = QWidget()
        toolbar.setStyleSheet("background: #f9fafb; border-radius: 16px 16px 0 0;")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(15, 10, 15, 10)
        
        self.copy_btn = QPushButton("📋 Copier")
        self.copy_btn.setStyleSheet("""
            QPushButton {
                font-size: 13px; 
                color: #4b5563; 
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: #e5e7eb;
            }
        """)
        self.copy_btn.clicked.connect(self.copy_results)
        
        toolbar_layout.addWidget(QLabel("💡 Résultats"))
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.copy_btn)
        
        # Affichage des résultats avec contenu cliquable
        self.analysis_result = QTextBrowser()
        self.analysis_result.setOpenExternalLinks(True)
        self.analysis_result.setStyleSheet("""
            QTextBrowser {
                background: white;
                border: none;
                padding: 20px;
                font-size: 15px;
                border-radius: 0 0 16px 16px;
            }
            a {
                color: #3b82f6;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        """)
        self.analysis_result.anchorClicked.connect(self.handle_link_click)
        
        # Indicateur visuel pendant l'analyse
        self.loading_indicator = QLabel()
        self.loading_movie = QMovie()
        self.loading_movie.setFileName(self.resource_path("assets/loading.gif"))
        self.loading_indicator.setMovie(self.loading_movie)
        self.loading_indicator.setAlignment(Qt.AlignCenter)
        self.loading_indicator.hide()
        
        result_layout.addWidget(toolbar)
        result_layout.addWidget(self.analysis_result)
        result_layout.addWidget(self.loading_indicator)
        
        layout.addWidget(result_frame)
        
        # Actions rapides
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        action_btns = [
            ("🔄 Raffiner", self.refine_analysis),
            ("📤 Partager", self.share_results),
            ("💾 Enregistrer", self.save_analysis)
        ]
        
        for emoji, callback in action_btns:
            btn = QPushButton(emoji)
            btn.setStyleSheet("""
                QPushButton {
                    background: white;
                    border: 1px solid #e5e7eb;
                    border-radius: 8px;
                    padding: 8px 15px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: #f3f4f6;
                }
            """)
            btn.clicked.connect(callback)
            actions_layout.addWidget(btn)
        
        actions_layout.addStretch()
        layout.addLayout(actions_layout)

    def handle_link_click(self, url):
        """Gère les clics sur les liens dans les résultats"""
        if url.scheme() == "action":
            platform = url.toString().replace("action://", "")
            if platform in self.available_actions:
                self.available_actions[platform]()
            else:
                self.show_notification("Action", f"Aucune action définie pour {platform}")
        else:
            QDesktopServices.openUrl(url)

    def analyze_prompt1(self):
        """Analyse le prompt avec feedback visuel amélioré"""
        prompt_text = self.prompt_input.toPlainText().strip()
        if not prompt_text:
            self.show_animation("shake", self.prompt_container)
            self.show_notification("Erreur", "Veuillez saisir un message à analyser")
            return
        
        # Feedback visuel
        self.send_btn.setEnabled(False)
        self.loading_movie.start()
        self.loading_indicator.show()
        self.analysis_result.hide()
        self.analysis_container.setVisible(True)
        self.progress_bar.show()
        
        # Animation d'envoi
        self.show_animation("fade_out", self.prompt_container)
        
        # Création et démarrage du thread d'analyse
        self.analysis_thread = AnalysisThread(prompt_text, self.conn)
        self.analysis_thread.analysis_complete.connect(self.handle_analysis_result)
        self.analysis_thread.error_occurred.connect(self.handle_analysis_error)
        self.analysis_thread.progress_updated.connect(self.progress_bar.setValue)
        self.analysis_thread.start()
        
        # Sauvegarde automatique si activée
        if self.settings["auto_save"]:
            self.save_to_history(prompt_text)
    def analyze_prompt(self):
        """Analyse le prompt avec feedback visuel amélioré"""
        prompt_text = self.prompt_input.toPlainText().strip()
        if not prompt_text:
            self.show_animation("shake", self.prompt_container)
            self.show_notification("Erreur", "Veuillez saisir un message à analyser")
            return
        
        # Feedback visuel
        self.send_btn.setEnabled(False)
        self.loading_movie.start()
        self.loading_indicator.show()
        self.analysis_result.hide()
        self.analysis_container.setVisible(True)
        self.progress_bar.show()
        
        # Animation d'envoi
        self.show_animation("fade_out", self.prompt_container)
        
        # Passez le chemin de la base de données au lieu de la connexion
        db_path = self.resource_path("marketing_ai.db")
        self.analysis_thread = AnalysisThread(prompt_text, db_path)
        self.analysis_thread.analysis_complete.connect(self.handle_analysis_result)
        self.analysis_thread.error_occurred.connect(self.handle_analysis_error)
        self.analysis_thread.progress_updated.connect(self.progress_bar.setValue)
        self.analysis_thread.start()
        
        # Sauvegarde automatique si activée
        if self.settings["auto_save"]:
            self.save_to_history(prompt_text)
            
    def handle_analysis_result1(self, analysis_text, detected_platforms):
        """Affiche les résultats de l'analyse"""
        self.loading_movie.stop()
        self.loading_indicator.hide()
        self.analysis_result.show()
        self.progress_bar.hide()
        self.send_btn.setEnabled(True)
        
        # Conversion markdown vers HTML avec des styles améliorés
        html_content = markdown2.markdown(analysis_text)
        
        # Styles CSS pour une meilleure présentation
        styled_html = f"""
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            h1, h2, h3, h4 {{
                color: #1e40af;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
            }}
            h1 {{ font-size: 24px; }}
            h2 {{ font-size: 20px; border-bottom: 1px solid #e5e7eb; padding-bottom: 5px; }}
            h3 {{ font-size: 18px; }}
            ul, ol {{ padding-left: 25px; }}
            li {{ margin-bottom: 8px; }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #3b82f6;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f8fafc;
            }}
            a {{
                color: #3b82f6;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .highlight {{
                background-color: #fef08a;
                padding: 2px 4px;
                border-radius: 3px;
            }}
        </style>
        <div class="analysis-report">
            {html_content}
            <div class="actions-section">
                <h3>🚀 Actions immédiates</h3>
                {self.generate_action_buttons(detected_platforms)}
            </div>
        </div>
        """
        
        self.analysis_result.setHtml(styled_html)
        self.show_animation("fade_in", self.analysis_container)
        self.show_animation("pulse", self.send_btn)

    def generate_action_buttons1(self, platforms):
        """Génère des boutons d'action cliquables"""
        if not platforms:
            return "<p>Aucune action spécifique requise</p>"
        
        platform_data = {
            "instagram": {"color": "#E1306C", "icon": "📸"},
            "facebook": {"color": "#1877F2", "icon": "👍"},
            "linkedin": {"color": "#0077B5", "icon": "💼"},
            "tiktok": {"color": "#000000", "icon": "🎵"},
            "email": {"color": "#EA4335", "icon": "✉️"},
            "whatsapp": {"color": "#25D366", "icon": "💬"},
            "twitter": {"color": "#1DA1F2", "icon": "🐦"},
            "youtube": {"color": "#FF0000", "icon": "▶️"}
        }
        
        buttons_html = '<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;">'
        
        for _, platform in platforms:
            platform_lower = platform.lower()
            data = platform_data.get(platform_lower, {"color": "#3b82f6", "icon": "⚡"})
            
            buttons_html += f"""
            <a href='action://{platform_lower}' 
            style='text-decoration: none; color: white;'>
                <div style='
                    background-color: {data["color"]};
                    padding: 10px 15px;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    cursor: pointer;
                    transition: all 0.3s;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                ' 
                onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.15)'"
                onmouseout="this.style.transform='none'; this.style.boxShadow='0 2px 5px rgba(0,0,0,0.1)'">
                    <span style='font-size: 18px;'>{data["icon"]}</span>
                    <span>{platform.capitalize()} Guide</span>
                </div>
            </a>
            """
        
        buttons_html += "</div>"
        return buttons_html
    def generate_action_buttons(self, platforms):
        """Génère des boutons d'action cliquables"""
        if not platforms:
            return "<p>Aucune action spécifique requise</p>"
        
        platform_data = {
            "instagram": {"color": "#E1306C", "icon": "📸"},
            "facebook": {"color": "#1877F2", "icon": "👍"},
            "linkedin": {"color": "#0077B5", "icon": "💼"},
            "tiktok": {"color": "#000000", "icon": "🎵"},
            "email": {"color": "#EA4335", "icon": "✉️"},
            "whatsapp": {"color": "#25D366", "icon": "💬"},
            "twitter": {"color": "#1DA1F2", "icon": "🐦"},
            "youtube": {"color": "#FF0000", "icon": "▶️"}
        }
        
        buttons_html = '<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;">'
        
        for item in platforms:
            # Gérer différents formats de données
            if isinstance(item, tuple) and len(item) >= 2:
                _, platform = item[0], item[1]
            elif isinstance(item, str):
                platform = item
            else:
                continue
                
            platform_lower = platform.lower()
            data = platform_data.get(platform_lower, {"color": "#3b82f6", "icon": "⚡"})
            
            buttons_html += f"""
            <a href='action://{platform_lower}' 
            style='text-decoration: none; color: white;'>
                <div style='
                    background-color: {data["color"]};
                    padding: 10px 15px;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    cursor: pointer;
                    transition: all 0.3s;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                ' 
                onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.15)'"
                onmouseout="this.style.transform='none'; this.style.boxShadow='0 2px 5px rgba(0,0,0,0.1)'">
                    <span style='font-size: 18px;'>{data["icon"]}</span>
                    <span>{platform.capitalize()} Guide</span>
                </div>
            </a>
            """
        
        buttons_html += "</div>"
        return buttons_html
    
   
    def handle_analysis_result(self, analysis_text, detected_platforms):
        """Affiche les résultats de l'analyse"""
        self.loading_movie.stop()
        self.loading_indicator.hide()
        self.analysis_result.show()
        self.progress_bar.hide()
        self.send_btn.setEnabled(True)
        
        # Conversion markdown vers HTML avec des styles améliorés
        html_content = markdown2.markdown(analysis_text)
        
        # Vérifiez et formatez correctement les plateformes détectées
        formatted_platforms = []
        for item in detected_platforms:
            if isinstance(item, tuple) and len(item) >= 2:
                formatted_platforms.append((None, item[1]))  # (keyword, platform)
        
        # Styles CSS pour une meilleure présentation
        styled_html = f"""
        <style>
            /* ... (votre CSS existant) ... */
        </style>
        <div class="analysis-report">
            {html_content}
            <div class="actions-section">
                <h3>🚀 Actions immédiates</h3>
                {self.generate_action_buttons(formatted_platforms)}
            </div>
        </div>
        """
        
        self.analysis_result.setHtml(styled_html)
        self.show_animation("fade_in", self.analysis_container)
        self.show_animation("pulse", self.send_btn)
        
    def handle_analysis_error(self, error_msg):
        """Gère les erreurs d'analyse"""
        self.loading_movie.stop()
        self.loading_indicator.hide()
        self.progress_bar.hide()
        self.send_btn.setEnabled(True)
        
        self.analysis_result.setHtml(f"""
        <div style='color: #dc2626; padding: 20px;'>
            <h3>❌ Erreur lors de l'analyse</h3>
            <p>{error_msg}</p>
            <p>Veuillez réessayer ou contacter le support.</p>
        </div>
        """)
        self.analysis_result.show()

    def show_animation(self, anim_type, widget):
        """Joue différentes animations"""
        if not self.settings["animations"]:
            return
            
        if anim_type == "shake":
            animation = QPropertyAnimation(widget, b"pos")
            animation.setDuration(300)
            animation.setLoopCount(2)
            animation.setKeyValueAt(0, widget.pos())
            animation.setKeyValueAt(0.2, widget.pos() + QPoint(-5, 0))
            animation.setKeyValueAt(0.4, widget.pos() + QPoint(5, 0))
            animation.setKeyValueAt(0.6, widget.pos() + QPoint(-5, 0))
            animation.setKeyValueAt(0.8, widget.pos() + QPoint(5, 0))
            animation.setKeyValueAt(1, widget.pos())
            animation.start()
            
        elif anim_type == "fade_in":
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(500)
            animation.setStartValue(0)
            animation.setEndValue(1)
            animation.start()
            
        elif anim_type == "fade_out":
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(300)
            animation.setStartValue(1)
            animation.setEndValue(0.5)
            animation.start()
            
        elif anim_type == "pulse":
            animation = QPropertyAnimation(widget, b"geometry")
            animation.setDuration(300)
            animation.setKeyValueAt(0, widget.geometry())
            animation.setKeyValueAt(0.5, widget.geometry().adjusted(-5, -5, 5, 5))
            animation.setKeyValueAt(1, widget.geometry())
            animation.start()

    def copy_results(self):
        """Copie les résultats dans le presse-papier"""
        self.analysis_result.selectAll()
        self.analysis_result.copy()
        self.analysis_result.moveCursor(QTextCursor.End)
        self.show_notification("Succès", "Résultats copiés dans le presse-papier")

    def refine_analysis(self):
        """Raffine l'analyse existante"""
        current_text = self.prompt_input.toPlainText()
        self.prompt_input.setPlainText(f"Affiner cette analyse : \n\n{current_text}")
        self.prompt_input.setFocus()
        self.show_animation("pulse", self.prompt_container)

    def share_results(self):
        """Partage les résultats"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Partager les résultats")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        label = QLabel("Choisissez une méthode de partage:")
        layout.addWidget(label)
        
        # Options de partage
        email_btn = QPushButton("📧 Par email")
        email_btn.clicked.connect(lambda: self.share_via_email())
        
        file_btn = QPushButton("💾 Enregistrer dans un fichier")
        file_btn.clicked.connect(lambda: self.save_analysis())
        
        clipboard_btn = QPushButton("📋 Copier dans le presse-papier")
        clipboard_btn.clicked.connect(self.copy_results)
        
        layout.addWidget(email_btn)
        layout.addWidget(file_btn)
        layout.addWidget(clipboard_btn)
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec_()

    def share_via_email(self):
        """Ouvre le client email par défaut avec les résultats"""
        subject = "Résultats d'analyse marketing"
        body = self.analysis_result.toPlainText()
        mailto_url = f"mailto:?subject={subject}&body={body}"
        QDesktopServices.openUrl(QUrl(mailto_url))

    def save_analysis(self):
        """Enregistre l'analyse dans un fichier"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer l'analyse", "", 
            "Fichiers HTML (*.html);;Fichiers texte (*.txt);;Fichiers PDF (*.pdf)", 
            options=options)
        
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    if file_name.endswith('.html'):
                        f.write(self.analysis_result.toHtml())
                    else:
                        f.write(self.analysis_result.toPlainText())
                
                self.show_notification("Succès", "Analyse sauvegardée avec succès")
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Impossible d'enregistrer : {str(e)}")

    def setup_history_view(self):
        """Configure la vue historique"""
        layout = QVBoxLayout(self.history_view)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("📚 Historique des analyses")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1e40af;")
        layout.addWidget(title)
        
        # Barre de recherche
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher dans l'historique...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                font-size: 14px;
            }
        """)
        search_btn = QPushButton("🔍")
        search_btn.setStyleSheet("padding: 10px; border-radius: 8px;")
        search_btn.clicked.connect(self.search_history)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)
        
        # Zone de défilement
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none; background: transparent;")
        
        self.history_content = QWidget()
        self.history_content_layout = QVBoxLayout(self.history_content)
        self.history_content_layout.setSpacing(15)
        
        # Charger l'historique factice pour la démo
        self.load_demo_history()
        
        scroll_area.setWidget(self.history_content)
        layout.addWidget(scroll_area)

    def search_history(self):
        """Filtre l'historique selon la recherche"""
        search_text = self.search_input.text().lower()
        
        for i in range(self.history_content_layout.count()):
            item = self.history_content_layout.itemAt(i)
            if item.widget():
                item.widget().setVisible(search_text in item.widget().text().lower())

    def load_demo_history(self):
        """Charge un historique de démonstration"""
        demo_items = [
            ("Stratégie réseaux sociaux pour startup", "2023-10-15 14:30"),
            ("Analyse de marché produits tech", "2023-10-14 09:15"),
            ("Campagne email pour client premium", "2023-10-12 16:45"),
            ("Optimisation SEO site web", "2023-10-10 11:20"),
            ("Plan de contenu pour le trimestre", "2023-10-08 15:30")
        ]
        
        for text, date in demo_items:
            item = QPushButton(f"{date} - {text}")
            item.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 15px;
                    border: 1px solid #e5e7eb;
                    border-radius: 8px;
                    background: white;
                }
                QPushButton:hover {
                    background: #f3f4f6;
                }
            """)
            item.clicked.connect(lambda _, t=text: self.load_history_item(t))
            self.history_content_layout.addWidget(item)
        
        self.history_content_layout.addStretch()

    def load_history_item(self, text):
        """Charge un élément de l'historique"""
        self.prompt_input.setPlainText(text)
        self.stacked_widget.setCurrentIndex(0)
        self.show_animation("fade_in", self.prompt_container)

    def setup_settings_view(self):
        """Configure la vue des paramètres"""
        layout = QVBoxLayout(self.settings_view)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("⚙️ Paramètres")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1e40af;")
        layout.addWidget(title)
        
        # Groupe d'options d'affichage
        display_group = QGroupBox("Affichage")
        display_layout = QVBoxLayout()
        
        self.dark_mode_check = QCheckBox("Mode sombre")
        self.dark_mode_check.setChecked(self.settings["dark_mode"])
        self.dark_mode_check.stateChanged.connect(self.toggle_dark_mode)
        
        self.animations_check = QCheckBox("Animations")
        self.animations_check.setChecked(self.settings["animations"])
        self.animations_check.stateChanged.connect(lambda: self.update_setting("animations", self.animations_check.isChecked()))
        
        display_layout.addWidget(self.dark_mode_check)
        display_layout.addWidget(self.animations_check)
        display_group.setLayout(display_layout)
        
        # Groupe d'options de fonctionnement
        behavior_group = QGroupBox("Fonctionnement")
        behavior_layout = QVBoxLayout()
        
        self.notifications_check = QCheckBox("Notifications")
        self.notifications_check.setChecked(self.settings["notifications"])
        self.notifications_check.stateChanged.connect(lambda: self.update_setting("notifications", self.notifications_check.isChecked()))
        
        self.auto_save_check = QCheckBox("Sauvegarde automatique")
        self.auto_save_check.setChecked(self.settings["auto_save"])
        self.auto_save_check.stateChanged.connect(lambda: self.update_setting("auto_save", self.auto_save_check.isChecked()))
        
        behavior_layout.addWidget(self.notifications_check)
        behavior_layout.addWidget(self.auto_save_check)
        behavior_group.setLayout(behavior_layout)
        
        layout.addWidget(display_group)
        layout.addWidget(behavior_group)
        layout.addStretch()

    def toggle_dark_mode(self, state):
        """Active/désactive le mode sombre"""
        self.settings["dark_mode"] = state == Qt.Checked
        self.update_styles()
        self.save_settings()

    def update_setting(self, key, value):
        """Met à jour un paramètre"""
        self.settings[key] = value
        self.save_settings()

    def save_to_history(self, prompt_text):
        """Enregistre le prompt dans l'historique"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.history.append((prompt_text[:50] + "...", timestamp))
        
        # Ajoute un nouvel élément à l'historique
        item = QPushButton(f"{timestamp} - {prompt_text[:50]}...")
        item.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 15px;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                background: white;
            }
            QPushButton:hover {
                background: #f3f4f6;
            }
        """)
        item.clicked.connect(lambda _, t=prompt_text: self.load_history_item(t))
        
        # Insère au début de la liste
        self.history_content_layout.insertWidget(0, item)

    def show_notification(self, title, message):
        """Affiche une notification stylisée"""
        if not self.settings["notifications"]:
            return
            
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("""
            QMessageBox {
                background: white;
                font-family: 'Segoe UI', sans-serif;
            }
            QMessageBox QLabel {
                color: #1e293b;
                font-size: 14px;
            }
        """)
        msg.exec_()

    def init_db1(self):
        """Initialise la base de données SQLite"""
        try:
            db_path = self.resource_path("marketing_ai1.db")
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            
            # Table des prompts
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_text TEXT NOT NULL,
                    analysis_result TEXT,
                    actions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table des règles de détection
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS detection_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    response_template TEXT NOT NULL
                )
            ''')
            
            # Insérer des règles de démonstration si la table est vide
            self.cursor.execute('SELECT COUNT(*) FROM detection_rules')
            if self.cursor.fetchone()[0] == 0:
                demo_rules = [
                    ("instagram", "instagram", "Créez du contenu visuel attractif pour Instagram"),
                    ("facebook", "facebook", "Lancez une campagne publicitaire ciblée sur Facebook"),
                    ("linkedin", "linkedin", "Publiez des articles professionnels sur LinkedIn"),
                    ("tiktok", "tiktok", "Créez des vidéos courtes et engageantes pour TikTok"),
                    ("email", "email", "Développez une stratégie d'email marketing personnalisée"),
                    ("whatsapp", "whatsapp", "Utilisez WhatsApp Business pour engager vos clients")
                ]
                
                for platform, keyword, template in demo_rules:
                    self.cursor.execute('''
                        INSERT INTO detection_rules (keyword, platform, response_template)
                        VALUES (?, ?, ?)
                    ''', (keyword, platform, template))
            
            self.conn.commit()
            
        except Error as e:
            print(f"Erreur de base de données : {e}")
    def init_db(self):
        """Initialise la base de données SQLite"""
        db_path = self.resource_path("marketing_ai2.db")
        
        # Vérifie si le dossier existe, sinon le crée
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        try:
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            
            # Table des prompts
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_text TEXT NOT NULL,
                    analysis_result TEXT,
                    actions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table des règles de détection
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS detection_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    response_template TEXT NOT NULL
                )
            ''')
            
            # Insérer des règles de démonstration si la table est vide
            self.cursor.execute('SELECT COUNT(*) FROM detection_rules')
            if self.cursor.fetchone()[0] == 0:
                demo_rules = [
                    ("instagram", "instagram", "Créez du contenu visuel attractif pour Instagram"),
                    ("facebook", "facebook", "Lancez une campagne publicitaire ciblée sur Facebook"),
                    ("linkedin", "linkedin", "Publiez des articles professionnels sur LinkedIn"),
                    ("tiktok", "tiktok", "Créez des vidéos courtes et engageantes pour TikTok"),
                    ("email", "email", "Développez une stratégie d'email marketing personnalisée"),
                    ("whatsapp", "whatsapp", "Utilisez WhatsApp Business pour engager vos clients")
                ]
                
                for platform, keyword, template in demo_rules:
                    self.cursor.execute('''
                        INSERT INTO detection_rules (keyword, platform, response_template)
                        VALUES (?, ?, ?)
                    ''', (keyword, platform, template))
            
            self.conn.commit()
            
        except Error as e:
            print(f"Erreur de base de données : {e}")
            # Essayez de créer une nouvelle base de données si la connexion échoue
            try:
                self.conn = sqlite3.connect(db_path)
                self.cursor = self.conn.cursor()
            except Error as e:
                print(f"Échec de la création de la base de données : {e}")
                
    def load_settings(self):
        """Charge les paramètres depuis un fichier"""
        try:
            settings_path = self.resource_path("settings.json")
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    self.settings.update(json.load(f))
        except Exception as e:
            print(f"Erreur de chargement des paramètres : {e}")

    def save_settings(self):
        """Sauvegarde les paramètres dans un fichier"""
        try:
            settings_path = self.resource_path("settings.json")
            with open(settings_path, 'w') as f:
                json.dump(self.settings, f)
        except Exception as e:
            print(f"Erreur de sauvegarde des paramètres : {e}")

    def resource_path(self, relative_path):
        """Gère les chemins des ressources pour le déploiement"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)

    def update_styles(self):
        """Met à jour les styles CSS de l'application"""
        if self.settings["dark_mode"]:
            self.set_dark_theme()
        else:
            self.set_light_theme()

    def set_light_theme(self):
        """Applique le thème clair"""
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #f8fafc;
            }
            #sidebar {
                background-color: #ffffff;
                border-right: 1px solid #e2e8f0;
            }
            #contentArea {
                background-color: #f8fafc;
            }
            QTextEdit, QLineEdit, QComboBox {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                color: #334155;
            }
            QLabel {
                color: #334155;
            }
            #mainToolbar {
                background-color: #ffffff;
                border-bottom: 1px solid #e2e8f0;
            }
            #navButton {
                background: transparent;
                border: none;
                color: #334155;
                padding: 8px 12px;
                border-radius: 6px;
            }
            #navButton:hover {
                background-color: #f1f5f9;
            }
            #userButton {
                background: transparent;
                border: none;
                color: #334155;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QGroupBox {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 20px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

    def set_dark_theme(self):
        """Applique le thème sombre"""
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1e293b;
            }
            #sidebar {
                background-color: #334155;
                border-right: 1px solid #475569;
            }
            #contentArea {
                background-color: #1e293b;
            }
            QTextEdit, QLineEdit, QComboBox {
                background-color: #334155;
                border: 1px solid #475569;
                color: #f8fafc;
            }
            QLabel {
                color: #f8fafc;
            }
            #mainToolbar {
                background-color: #334155;
                border-bottom: 1px solid #475569;
            }
            #navButton {
                background: transparent;
                border: none;
                color: #f8fafc;
                padding: 8px 12px;
                border-radius: 6px;
            }
            #navButton:hover {
                background-color: #475569;
            }
            #userButton {
                background: transparent;
                border: none;
                color: #f8fafc;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QGroupBox {
                border: 1px solid #475569;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 20px;
                font-weight: bold;
                color: #f8fafc;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #f8fafc;
            }
        """)

    def closeEvent(self, event):
        """Gère la fermeture de l'application"""
        try:
            if hasattr(self, 'analysis_thread') and self.analysis_thread.isRunning():
                self.analysis_thread.stop()
            
            self.conn.close()
            self.save_settings()
        except Exception as e:
            print(f"Erreur lors de la fermeture : {e}")
        
        event.accept()

    # === Méthodes d'action pour chaque plateforme ===
    
    def launch_instagram_guide(self):
        """Lance le guide Instagram"""
        guide_html = """
        <h2>Guide Instagram Marketing</h2>
        <p>Voici vos prochaines étapes pour Instagram:</p>
        <ol>
            <li>Optimisez votre profil bio avec des mots-clés</li>
            <li>Planifiez un calendrier de contenu (3-5 posts/semaine)</li>
            <li>Utilisez des hashtags pertinents (5-10 par post)</li>
            <li>Créez des Stories quotidiennes</li>
            <li>Engagez avec votre audience (répondez aux commentaires)</li>
        </ol>
        <p><a href='https://business.instagram.com/'>Ressources Officielles</a></p>
        """
        self.show_action_modal("Instagram Guide", guide_html)
        
    def launch_facebook_guide(self):
        """Lance le guide Facebook"""
        guide_html = """
        <h2>Guide Facebook Marketing</h2>
        <p>Stratégie recommandée pour Facebook:</p>
        <ul>
            <li>Créez une Page Business complète</li>
            <li>Publiez du contenu varié (texte, images, vidéos)</li>
            <li>Utilisez Facebook Ads pour cibler précisément</li>
            <li>Créez des événements pour engager votre communauté</li>
            <li>Analysez vos insights régulièrement</li>
        </ul>
        <p><a href='https://www.facebook.com/business/learn'>Centre d'apprentissage Facebook</a></p>
        """
        self.show_action_modal("Facebook Guide", guide_html)
    
    def launch_linkedin_guide(self):
        """Lance le guide LinkedIn"""
        guide_html = """
        <h2>Guide LinkedIn Marketing</h2>
        <p>Approche professionnelle pour LinkedIn:</p>
        <ul>
            <li>Optimisez votre profil et page entreprise</li>
            <li>Publiez des articles longs (1-2/mois)</li>
            <li>Partagez des mises à jour courtes (2-3/semaine)</li>
            <li>Participez à des groupes pertinents</li>
            <li>Utilisez LinkedIn Sales Navigator pour le B2B</li>
        </ul>
        <p><a href='https://business.linkedin.com/marketing-solutions'>Solutions Marketing LinkedIn</a></p>
        """
        self.show_action_modal("LinkedIn Guide", guide_html)
    
    def launch_tiktok_guide(self):
        """Lance le guide TikTok"""
        guide_html = """
        <h2>Guide TikTok Marketing</h2>
        <p>Stratégie virale pour TikTok:</p>
        <ul>
            <li>Créez des vidéos courtes et engageantes</li>
            <li>Suivez les tendances et challenges</li>
            <li>Utilisez des effets et du son populaires</li>
            <li>Postez régulièrement (1-2 vidéos/jour idéal)</li>
            <li>Collaborez avec des créateurs</li>
        </ul>
        <p><a href='https://www.tiktok.com/business/'>TikTok Business</a></p>
        """
        self.show_action_modal("TikTok Guide", guide_html)
    
    def launch_email_guide(self):
        """Lance le guide Email Marketing"""
        guide_html = """
        <h2>Guide Email Marketing</h2>
        <p>Meilleures pratiques pour les emails:</p>
        <ul>
            <li>Segmentez votre liste d'emails</li>
            <li>Personnalisez les sujets et contenus</li>
            <li>Optimisez pour mobile (50% des ouvertures)</li>
            <li>Testez A/B différents éléments</li>
            <li>Analysez les taux d'ouverture et clics</li>
        </ul>
        <p><a href='https://mailchimp.com/resources/email-marketing-guide/'>Guide complet Mailchimp</a></p>
        """
        self.show_action_modal("Email Marketing Guide", guide_html)
    
    def launch_whatsapp_guide(self):
        """Lance le guide WhatsApp Business"""
        guide_html = """
        <h2>Guide WhatsApp Business</h2>
        <p>Stratégie pour WhatsApp:</p>
        <ul>
            <li>Configurez un profil Business complet</li>
            <li>Utilisez des messages automatisés pour les FAQs</li>
            <li>Créez des listes de diffusion ciblées</li>
            <li>Répondez rapidement aux messages</li>
            <li>Utilisez WhatsApp Web pour plus d'efficacité</li>
        </ul>
        <p><a href='https://www.whatsapp.com/business/'>WhatsApp Business</a></p>
        """
        self.show_action_modal("WhatsApp Business Guide", guide_html)
    
    def launch_twitter_guide(self):
        """Lance le guide Twitter/X"""
        guide_html = """
        <h2>Guide Twitter/X Marketing</h2>
        <p>Stratégie pour Twitter:</p>
        <ul>
            <li>Tweetez régulièrement (3-5 fois/jour)</li>
            <li>Utilisez des hashtags pertinents (1-2 par tweet)</li>
            <li>Engagez avec les tendances du moment</li>
            <li>Répondez aux mentions et messages</li>
            <li>Utilisez des médias visuels (images, vidéos)</li>
        </ul>
        <p><a href='https://business.twitter.com/'>Twitter Business</a></p>
        """
        self.show_action_modal("Twitter Guide", guide_html)
    
    def launch_youtube_guide(self):
        """Lance le guide YouTube"""
        guide_html = """
        <h2>Guide YouTube Marketing</h2>
        <p>Stratégie vidéo pour YouTube:</p>
        <ul>
            <li>Créez un calendrier de contenu régulier</li>
            <li>Optimisez les titres et descriptions (SEO)</li>
            <li>Utilisez des miniatures attrayantes</li>
            <li>Ajoutez des sous-titres et transcriptions</li>
            <li>Interagissez avec les commentaires</li>
        </ul>
        <p><a href='https://www.youtube.com/intl/fr/creators/'>YouTube Creators</a></p>
        """
        self.show_action_modal("YouTube Guide", guide_html)
    
    def show_analytics_tips(self):
        """Affiche des conseils d'analyse"""
        tips_html = """
        <h2>Conseils d'Analyse Marketing</h2>
        <p>Mesurez efficacement vos performances:</p>
        <ul>
            <li>Trackez les KPI clés (taux de conversion, ROI)</li>
            <li>Utilisez Google Analytics et Google Search Console</li>
            <li>Configurez des tableaux de bord personnalisés</li>
            <li>Analysez le parcours client</li>
            <li>Testez régulièrement (A/B testing)</li>
        </ul>
        <p><a href='https://analytics.google.com/'>Google Analytics</a></p>
        """
        self.show_action_modal("Analytics Tips", tips_html)
    
    def show_content_tips(self):
        """Affiche des conseils de contenu"""
        tips_html = """
        <h2>Stratégie de Contenu</h2>
        <p>Créez un contenu engageant:</p>
        <ul>
            <li>Développez un calendrier éditorial</li>
            <li>Variez les formats (blog, vidéo, infographie)</li>
            <li>Adaptez le ton à votre audience</li>
            <li>Optimisez pour le SEO</li>
            <li>Recyclez et repromouvez le contenu performant</li>
        </ul>
        <p><a href='https://contentmarketinginstitute.com/'>Content Marketing Institute</a></p>
        """
        self.show_action_modal("Content Strategy", tips_html)
    
    def show_action_modal(self, title, content):
        """Affiche une modale avec le contenu de l'action"""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Zone de contenu
        content_browser = QTextBrowser()
        content_browser.setOpenExternalLinks(True)
        content_browser.setHtml(content)
        content_browser.setStyleSheet("""
            QTextBrowser {
                font-size: 14px;
                line-height: 1.5;
            }
            a {
                color: #3b82f6;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        """)
        
        # Boutons
        btn_layout = QHBoxLayout()
        copy_btn = QPushButton("Copier les conseils")
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(content))
        copy_btn.setStyleSheet("padding: 8px;")
        
        open_btn = QPushButton("Ouvrir la ressource")
        open_btn.clicked.connect(lambda: self.open_resource_from_content(content))
        open_btn.setStyleSheet("padding: 8px;")
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(dialog.close)
        close_btn.setStyleSheet("padding: 8px;")
        
        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(open_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        
        layout.addWidget(content_browser)
        layout.addLayout(btn_layout)
        
        dialog.exec_()
    
    def copy_to_clipboard(self, html_content):
        """Copie le contenu texte (sans balises) dans le presse-papier"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text()
        
        clipboard = QApplication.clipboard()
        clipboard.setText(text_content)
        
        self.show_notification("Succès", "Contenu copié dans le presse-papier")
    
    def open_resource_from_content(self, html_content):
        """Ouvre le premier lien trouvé dans le contenu HTML"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        link = soup.find('a')
        
        if link and link.has_attr('href'):
            url = link['href']
            QDesktopServices.openUrl(QUrl(url))
        else:
            self.show_notification("Information", "Aucun lien trouvé dans ce contenu")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Définir une police moderne
    font = QFont()
    font.setFamily("Segoe UI" if platform.system() == "Windows" else "Helvetica Neue")
    font.setFamily("Segoe UI" if platform.system() == "Windows" else "Helvetica Neue")
    font.setPointSize(10)
    app.setFont(font)
    
    # Style de fusion pour des widgets plus modernes
    app.setStyle("Fusion")
    
    # Palette de couleurs moderne
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(248, 250, 252))
    palette.setColor(QPalette.WindowText, QColor(15, 23, 42))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(241, 245, 249))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(15, 23, 42))
    palette.setColor(QPalette.Text, QColor(15, 23, 42))
    palette.setColor(QPalette.Button, QColor(241, 245, 249))
    palette.setColor(QPalette.ButtonText, QColor(15, 23, 42))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Highlight, QColor(59, 130, 246))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    # Créer et afficher la fenêtre principale
    window = MarketingAIAnalyzer()
    window.show()
    
    
    sys.exit(app.exec_())