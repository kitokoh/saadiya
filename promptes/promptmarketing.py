# import sys
# import os
# import sqlite3
# import json
# import time
# from datetime import datetime
# from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
#                              QLabel, QPushButton, QTextEdit, QProgressBar, QScrollArea, 
#                              QGroupBox, QCheckBox, QFileDialog, QMessageBox, QStackedWidget, 
#                              QSizePolicy, QLineEdit, QGridLayout, QFrame)
# from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QUrl, QSize, QRect, QPropertyAnimation, QEasingCurve
# from PyQt5.QtGui import QIcon, QPixmap, QTextCursor, QDesktopServices, QMovie, QPainter, QColor, QFont, QPalette
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtWebChannel import QWebChannel
# from PyQt5.QtCore import QObject

# class ActionHandler(QObject):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.parent = parent
    
#     @pyqtSlot(str)
#     def handleAction(self, action_data):
#         try:
#             data = json.loads(action_data)
#             self.parent.execute_action(data)
#         except Exception as e:
#             print(f"Error handling action: {e}")

# class AnalysisThread(QThread):
#     analysis_complete = pyqtSignal(str, list)
#     error_occurred = pyqtSignal(str)
#     progress_updated = pyqtSignal(int)

#     def __init__(self, prompt_text, db_path):
#         super().__init__()
#         self.prompt_text = prompt_text
#         self.db_path = db_path
#         self._is_running = True

#     def run(self):
#         conn = None
#         try:
#             conn = sqlite3.connect(self.db_path)
#             cursor = conn.cursor()
            
#             # Simulation de progression
#             for i in range(1, 101):
#                 if not self._is_running:
#                     return
#                 time.sleep(0.02)
#                 self.progress_updated.emit(i)
            
#             # Analyse réelle
#             prompt_lower = self.prompt_text.lower()
#             detected = []
            
#             cursor.execute('SELECT keyword, platform, response_template, action_type FROM detection_rules')
#             rules = cursor.fetchall()
            
#             for keyword, platform, template, action_type in rules:
#                 if not self._is_running:
#                     return
#                 if keyword in prompt_lower:
#                     detected.append((keyword, platform, template, action_type))
            
#             analysis_text = self.generate_analysis_html(prompt_lower, detected)
#             self.analysis_complete.emit(analysis_text, detected)
            
#         except Exception as e:
#             self.error_occurred.emit(f"Erreur d'analyse : {str(e)}")
#         finally:
#             if conn:
#                 conn.close()

#     def generate_analysis_html(self, prompt, detected):
#         html = """
#         <style>
#             :root {
#                 --primary: #4f46e5;
#                 --primary-hover: #4338ca;
#                 --background: #ffffff;
#                 --text: #1e293b;
#                 --text-secondary: #64748b;
#                 --card-bg: #f8fafc;
#                 --card-border: #e2e8f0;
#                 --success: #10b981;
#                 --error: #ef4444;
#             }
            
#             body {
#                 font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
#                 background: var(--background);
#                 color: var(--text);
#                 line-height: 1.5;
#                 padding: 0;
#                 margin: 0;
#             }
            
#             .container {
#                 max-width: 800px;
#                 margin: 0 auto;
#                 padding: 20px;
#             }
            
#             .platform-section {
#                 margin-bottom: 1.5rem;
#                 background: var(--background);
#                 border-radius: 12px;
#                 border: 1px solid var(--card-border);
#                 overflow: hidden;
#                 box-shadow: 0 1px 3px rgba(0,0,0,0.05);
#             }
            
#             .platform-header {
#                 padding: 1rem 1.5rem;
#                 background: var(--card-bg);
#                 border-bottom: 1px solid var(--card-border);
#                 display: flex;
#                 align-items: center;
#             }
            
#             .platform-icon {
#                 font-size: 1.5rem;
#                 margin-right: 0.75rem;
#             }
            
#             .platform-title {
#                 font-size: 1.125rem;
#                 font-weight: 600;
#                 margin: 0;
#             }
            
#             .options-container {
#                 padding: 1rem 1.5rem;
#             }
            
#             .option-card {
#                 padding: 1rem;
#                 margin-bottom: 0.75rem;
#                 background: var(--card-bg);
#                 border: 1px solid var(--card-border);
#                 border-radius: 8px;
#                 transition: all 0.2s ease;
#                 cursor: pointer;
#             }
            
#             .option-card:hover {
#                 transform: translateY(-2px);
#                 box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
#                 border-color: var(--primary);
#             }
            
#             .option-title {
#                 font-weight: 600;
#                 margin-bottom: 0.25rem;
#             }
            
#             .option-desc {
#                 color: var(--text-secondary);
#                 font-size: 0.875rem;
#                 margin-bottom: 0.75rem;
#             }
            
#             .action-btn {
#                 display: inline-flex;
#                 align-items: center;
#                 justify-content: center;
#                 background: var(--primary);
#                 color: white;
#                 border: none;
#                 padding: 0.5rem 1rem;
#                 border-radius: 6px;
#                 font-size: 0.875rem;
#                 font-weight: 500;
#                 cursor: pointer;
#                 transition: background 0.2s;
#             }
            
#             .action-btn:hover {
#                 background: var(--primary-hover);
#             }
            
#             .keyword-tag {
#                 display: inline-block;
#                 background: #e0e7ff;
#                 color: #4f46e5;
#                 padding: 0.25rem 0.5rem;
#                 border-radius: 4px;
#                 font-size: 0.75rem;
#                 margin-right: 0.5rem;
#                 margin-bottom: 0.5rem;
#             }
#         </style>
        
#         <div class="container">
#             <h1 style="font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">✨ Suggestions</h1>
#             <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">Voici ce que je peux faire pour vous :</p>
#         """
        
#         if not detected:
#             html += """
#             <div class="platform-section">
#                 <div class="platform-header">
#                     <div class="platform-icon">💡</div>
#                     <h2 class="platform-title">Conseils généraux</h2>
#                 </div>
#                 <div class="options-container">
#                     <p style="margin-bottom: 1rem;">Je n'ai pas détecté de demande spécifique. Voici des suggestions :</p>
#                     <button class="action-btn" onclick='pyHandler.handleAction(`{"type":"general_advice"}`)'>
#                         Voir les conseils marketing
#                     </button>
#                 </div>
#             </div>
#             """
#         else:
#             platforms = {}
#             for item in detected:
#                 platform = item[1]
#                 if platform not in platforms:
#                     platforms[platform] = []
#                 platforms[platform].append(item)
            
#             for platform, items in platforms.items():
#                 icon = {
#                     'whatsapp': '💬',
#                     'instagram': '📸',
#                     'facebook': '👍',
#                     'linkedin': '💼',
#                     'tiktok': '🎵',
#                     'email': '✉️',
#                     'twitter': '🐦',
#                     'youtube': '▶️',
#                     'analytics': '📊',
#                     'seo': '🔍'
#                 }.get(platform, '📌')
                
#                 html += f"""
#                 <div class="platform-section">
#                     <div class="platform-header">
#                         <div class="platform-icon">{icon}</div>
#                         <h2 class="platform-title">{platform.capitalize()}</h2>
#                     </div>
#                     <div class="options-container">
#                 """
                
#                 for idx, (keyword, platform, template, action_type) in enumerate(items):
#                     html += f"""
#                     <div class="option-card" onclick='pyHandler.handleAction(`{{
#                         "type": "platform_action",
#                         "platform": "{platform}",
#                         "action": "{action_type}"
#                     }}`)'>
#                         <div class="option-title">{template}</div>
#                         <div class="option-desc">Basé sur votre mention : <span class="keyword-tag">{keyword}</span></div>
#                         <button class="action-btn">
#                             Exécuter cette action
#                         </button>
#                     </div>
#                     """
                
#                 html += """
#                     </div>
#                 </div>
#                 """
        
#         html += "</div>"
#         return html

# class MarketingAIAnalyzer(QMainWindow):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Leopardo - Assistant Marketing IA")
#         self.setMinimumSize(1000, 700)
        
#         # Configuration
#         self.current_user = "Utilisateur"
#         self.settings = {
#             "dark_mode": False,
#             "animations": True
#         }
        
#         # Initialisation
#         self.init_db()
#         self.init_ui()
        
#     def init_db(self):
#         """Initialise la base de données avec un jeu de données complet"""
#         self.db_path = "marketing_a1i.db"
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
        
#         # Création des tables
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS detection_rules (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 keyword TEXT NOT NULL,
#                 platform TEXT NOT NULL,
#                 response_template TEXT NOT NULL,
#                 action_type TEXT NOT NULL
#             )
#         ''')
        
#         # Vérification des données existantes
#         cursor.execute("SELECT COUNT(*) FROM detection_rules")
#         if cursor.fetchone()[0] == 0:
#             # Insertion d'un jeu de données complet
#             rules = [
#                 # WhatsApp
#                 ("whatsapp", "whatsapp", "Automatisation WhatsApp complète", "whatsapp_auto"),
#                 ("message whatsapp", "whatsapp", "Envoyer un message WhatsApp personnel", "whatsapp_personal"),
#                 ("groupe whatsapp", "whatsapp", "Envoyer un message à un groupe WhatsApp", "whatsapp_group"),
#                 ("campagne whatsapp", "whatsapp", "Lancer une campagne WhatsApp", "whatsapp_campaign"),
#                 ("automatiser whatsapp", "whatsapp", "Automatiser les réponses WhatsApp", "whatsapp_auto_reply"),
                
#                 # Instagram
#                 ("instagram", "instagram", "Créer une publication Instagram", "instagram_post"),
#                 ("story instagram", "instagram", "Créer une story Instagram", "instagram_story"),
#                 ("reels instagram", "instagram", "Créer un Reel Instagram", "instagram_reel"),
#                 ("campagne instagram", "instagram", "Lancer une campagne publicitaire Instagram", "instagram_ads"),
#                 ("hashtag instagram", "instagram", "Générer des hashtags optimisés", "instagram_hashtags"),
                
#                 # Facebook
#                 ("facebook", "facebook", "Créer un post Facebook", "facebook_post"),
#                 ("publicité facebook", "facebook", "Lancer une publicité Facebook", "facebook_ads"),
#                 ("page facebook", "facebook", "Optimiser votre page Facebook", "facebook_page"),
                
#                 # Autres plateformes
#                 ("linkedin", "linkedin", "Créer un post LinkedIn", "linkedin_post"),
#                 ("tiktok", "tiktok", "Créer une vidéo TikTok", "tiktok_video"),
#                 ("youtube", "youtube", "Optimiser une vidéo YouTube", "youtube_optimize"),
#                 ("email", "email", "Créer une campagne email", "email_campaign"),
#                 ("newsletter", "email", "Créer une newsletter", "email_newsletter"),
                
#                 # Général
#                 ("stratégie", "general", "Élaborer une stratégie marketing", "marketing_strategy"),
#                 ("analyse", "analytics", "Analyser les performances", "performance_analysis"),
#                 ("seo", "seo", "Optimisation SEO", "seo_optimization"),
#                 ("contenu", "content", "Planifier du contenu", "content_planning")
#             ]
            
#             cursor.executemany('''
#                 INSERT INTO detection_rules (keyword, platform, response_template, action_type)
#                 VALUES (?, ?, ?, ?)
#             ''', rules)
#             conn.commit()
        
#         conn.close()
        
#     def init_ui(self):
#         """Initialise l'interface utilisateur avec un design moderne"""
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
        
#         self.main_layout = QVBoxLayout(self.central_widget)
#         self.main_layout.setContentsMargins(0, 0, 0, 0)
#         self.main_layout.setSpacing(0)
        
#         # Barre d'outils
#         self.create_toolbar()
        
#         # Zone de contenu principale
#         self.content_area = QWidget()
#         self.content_area.setObjectName("contentArea")
#         self.content_layout = QVBoxLayout(self.content_area)
#         self.content_layout.setContentsMargins(0, 0, 0, 0)
        
#         # Stack pour les différentes vues
#         self.stacked_widget = QStackedWidget()
#         self.content_layout.addWidget(self.stacked_widget)
        
#         # Vue principale
#         self.setup_main_view()
        
#         self.main_layout.addWidget(self.content_area)
        
#         # Appliquer le style global
#         self.update_styles()
        
#     def create_toolbar(self):
#         """Crée une barre d'outils moderne avec dégradé"""
#         toolbar = QWidget()
#         toolbar.setObjectName("mainToolbar")
#         toolbar.setFixedHeight(60)
        
#         layout = QHBoxLayout(toolbar)
#         layout.setContentsMargins(20, 0, 20, 0)
#         layout.setSpacing(20)
        
#         # Logo
#         logo = QLabel("LEOPARDO AI")
#         logo.setStyleSheet("""
#             color: white;
#             font-size: 18px;
#             font-weight: bold;
#             font-family: 'Segoe UI', sans-serif;
#         """)
        
#         # Boutons de navigation
#         nav_btns = [
#             ("Accueil", "home", lambda: self.stacked_widget.setCurrentIndex(0)),
#             ("Historique", "history", lambda: self.stacked_widget.setCurrentIndex(1)),
#             ("Paramètres", "settings", lambda: self.stacked_widget.setCurrentIndex(2))
#         ]
        
#         layout.addWidget(logo)
        
#         for text, icon, callback in nav_btns:
#             btn = QPushButton(text)
#             btn.setIcon(QIcon.fromTheme(icon))
#             btn.setCursor(Qt.PointingHandCursor)
#             btn.setStyleSheet("""
#                 QPushButton {
#                     color: white;
#                     background: transparent;
#                     border: none;
#                     padding: 8px 12px;
#                     border-radius: 4px;
#                     font-family: 'Segoe UI', sans-serif;
#                 }
#                 QPushButton:hover {
#                     background: rgba(255,255,255,0.1);
#                 }
#             """)
#             btn.clicked.connect(callback)
#             layout.addWidget(btn)
        
#         layout.addStretch()
        
#         # Bouton utilisateur
#         user_btn = QPushButton(self.current_user)
#         user_btn.setIcon(QIcon.fromTheme("user"))
#         user_btn.setStyleSheet("""
#             QPushButton {
#                 color: white;
#                 background: rgba(255,255,255,0.1);
#                 border: none;
#                 padding: 6px 12px;
#                 border-radius: 16px;
#                 font-family: 'Segoe UI', sans-serif;
#             }
#             QPushButton:hover {
#                 background: rgba(255,255,255,0.2);
#             }
#         """)
#         layout.addWidget(user_btn)
        
#         self.main_layout.addWidget(toolbar)
        
#     def setup_main_view(self):
#         """Configure la vue principale avec une UX optimisée"""
#         main_view = QWidget()
#         main_view.setObjectName("mainView")
#         layout = QVBoxLayout(main_view)
#         layout.setContentsMargins(40, 40, 40, 40)
#         layout.setSpacing(0)
        
#         # Conteneur central pour centrer le contenu
#         center_container = QWidget()
#         center_container.setMaximumWidth(800)
#         center_layout = QVBoxLayout(center_container)
#         center_layout.setContentsMargins(0, 0, 0, 0)
#         center_layout.setSpacing(0)
        
#         # En-tête
#         header = QLabel("Assistant Marketing IA")
#         header.setObjectName("mainHeader")
        
#         subheader = QLabel("Décrivez votre besoin marketing pour obtenir des solutions personnalisées")
#         subheader.setObjectName("mainSubheader")
        
#         # Zone de prompt unifiée avec bouton
#         prompt_container = QWidget()
#         prompt_container.setObjectName("promptContainer")
#         prompt_layout = QVBoxLayout(prompt_container)
#         prompt_layout.setContentsMargins(0, 0, 0, 0)
#         prompt_layout.setSpacing(0)
        
#         # Zone de texte avec placeholder stylisé
#         self.prompt_input = QTextEdit()
#         self.prompt_input.setObjectName("promptInput")
#         self.prompt_input.setPlaceholderText("Ex: Je veux automatiser mes publications WhatsApp pour mon entreprise de vêtements...")
        
#         # Bouton d'envoi intégré
#         self.send_btn = QPushButton("Analyser")
#         self.send_btn.setObjectName("sendButton")
#         self.send_btn.setIcon(QIcon.fromTheme("edit-find"))
#         self.send_btn.clicked.connect(self.analyze_prompt)
        
#         # Barre de progression
#         self.progress_bar = QProgressBar()
#         self.progress_bar.setObjectName("progressBar")
#         self.progress_bar.setRange(0, 100)
#         self.progress_bar.setTextVisible(False)
#         self.progress_bar.hide()
        
#         # Suggestions de prompts
#         self.setup_prompt_suggestions()
        
#         # Zone de résultats
#         self.analysis_display = QWebEngineView()
#         self.analysis_display.setObjectName("analysisDisplay")
#         self.analysis_display.hide()
        
#         # Configuration du canal de communication
#         self.channel = QWebChannel()
#         self.handler = ActionHandler(self)
#         self.channel.registerObject('pyHandler', self.handler)
#         self.analysis_display.page().setWebChannel(self.channel)
        
#         # Assemblage des composants
#         prompt_layout.addWidget(self.prompt_input)
#         prompt_layout.addWidget(self.send_btn, alignment=Qt.AlignRight)
#         prompt_layout.addWidget(self.progress_bar)
        
#         center_layout.addWidget(header)
#         center_layout.addWidget(subheader)
#         center_layout.addSpacing(20)
#         center_layout.addWidget(prompt_container)
#         center_layout.addSpacing(15)
#         center_layout.addLayout(self.suggestions_layout)
#         center_layout.addSpacing(20)
#         center_layout.addWidget(self.analysis_display)
#         center_layout.addStretch()
        
#         layout.addWidget(center_container, alignment=Qt.AlignCenter)
        
#         self.stacked_widget.addWidget(main_view)
        
#     def setup_prompt_suggestions(self):
#         """Configure les suggestions de prompts prédéfinis"""
#         self.suggestions_layout = QVBoxLayout()
#         self.suggestions_layout.setContentsMargins(0, 0, 0, 0)
#         self.suggestions_layout.setSpacing(10)
        
#         title = QLabel("💡 Exemples de requêtes:")
#         title.setObjectName("suggestionsTitle")
        
#         suggestions_grid = QGridLayout()
#         suggestions_grid.setContentsMargins(0, 0, 0, 0)
#         suggestions_grid.setSpacing(10)
        
#         suggestions = [
#             ("📱", "Réseaux sociaux", "Créer une stratégie pour Instagram et Facebook"),
#             ("📈", "Analyse", "Analyser les performances de ma dernière campagne"),
#             ("✉️", "Email", "Rédiger une newsletter pour mes clients"),
#             ("💬", "WhatsApp", "Automatiser les messages WhatsApp pour mon commerce"),
#             ("🔍", "SEO", "Optimiser mon site web pour le référencement"),
#             ("📊", "Rapport", "Générer un rapport marketing mensuel")
#         ]
        
#         for i, (icon, title_text, prompt_text) in enumerate(suggestions):
#             btn = QPushButton(f"{icon} {title_text}")
#             btn.setToolTip(prompt_text)
#             btn.setCursor(Qt.PointingHandCursor)
#             btn.setObjectName("suggestionButton")
#             btn.clicked.connect(lambda _, text=prompt_text: self.prompt_input.setPlainText(text))
#             suggestions_grid.addWidget(btn, i // 2, i % 2)
        
#         self.suggestions_layout.addWidget(title)
#         self.suggestions_layout.addLayout(suggestions_grid)
        
#     def update_styles(self):
#         """Applique les styles CSS à l'application"""
#         self.setStyleSheet("""
#             QWidget {
#                 font-family: 'Segoe UI', sans-serif;
#             }
            
#             QWidget#contentArea {
#                 background: #f8fafc;
#             }
            
#             QWidget#mainToolbar {
#                 background: qlineargradient(x1:0, y1:0, x1:1, y1:0, stop:0 #4f46e5, stop:1 #7c3aed);
#                 border-bottom: 1px solid #4f46e5;
#             }
            
#             QLabel#mainHeader {
#                 font-size: 28px;
#                 font-weight: bold;
#                 color: #1e293b;
#                 margin-bottom: 5px;
#             }
            
#             QLabel#mainSubheader {
#                 font-size: 16px;
#                 color: #64748b;
#                 margin-bottom: 30px;
#             }
            
#             QWidget#promptContainer {
#                 background: white;
#                 border-radius: 12px;
#                 border: 1px solid #e2e8f0;
#                 padding: 1px;
#             }
            
#             QTextEdit#promptInput {
#                 background: white;
#                 border: none;
#                 font-size: 16px;
#                 padding: 20px;
#                 border-radius: 12px;
#                 min-height: 120px;
#                 color: #1e293b;
#             }
            
#             QTextEdit#promptInput:focus {
#                 border: none;
#             }
            
#             QPushButton#sendButton {
#                 background: #4f46e5;
#                 color: white;
#                 border: none;
#                 padding: 12px 24px;
#                 border-radius: 8px;
#                 font-size: 16px;
#                 margin: 10px;
#                 margin-top: 0;
#             }
            
#             QPushButton#sendButton:hover {
#                 background: #4338ca;
#             }
            
#             QPushButton#sendButton:disabled {
#                 background: #a5b4fc;
#             }
            
#             QProgressBar#progressBar {
#                 height: 6px;
#                 background: #e2e8f0;
#                 border-radius: 3px;
#                 margin: 0 10px 10px 10px;
#             }
            
#             QProgressBar#progressBar::chunk {
#                 background: #4f46e5;
#                 border-radius: 3px;
#             }
            
#             QLabel#suggestionsTitle {
#                 font-size: 14px;
#                 color: #64748b;
#                 margin-bottom: 5px;
#             }
            
#             QPushButton#suggestionButton {
#                 background: white;
#                 border: 1px solid #e2e8f0;
#                 border-radius: 8px;
#                 padding: 12px;
#                 font-size: 14px;
#                 text-align: left;
#                 color: #1e293b;
#             }
            
#             QPushButton#suggestionButton:hover {
#                 background: #f1f5f9;
#                 border-color: #cbd5e1;
#             }
            
#             QWebEngineView#analysisDisplay {
#                 background: white;
#                 border-radius: 12px;
#                 border: 1px solid #e2e8f0;
#             }
#         """)
        
#     def analyze_prompt(self):
#         """Lance l'analyse du prompt"""
#         prompt = self.prompt_input.toPlainText().strip()
#         if not prompt:
#             self.show_error("Veuillez saisir votre demande")
#             return
        
#         # Désactiver le bouton pendant l'analyse
#         self.send_btn.setEnabled(False)
#         self.progress_bar.show()
#         self.analysis_display.hide()
        
#         # Animation de chargement
#         self.loading_animation = QPropertyAnimation(self.progress_bar, b"value")
#         self.loading_animation.setDuration(2000)
#         self.loading_animation.setStartValue(0)
#         self.loading_animation.setEndValue(100)
#         self.loading_animation.setEasingCurve(QEasingCurve.InOutQuad)
#         self.loading_animation.start()
        
#         # Lancer l'analyse dans un thread séparé
#         self.analysis_thread = AnalysisThread(prompt, self.db_path)
#         self.analysis_thread.analysis_complete.connect(self.show_results)
#         self.analysis_thread.error_occurred.connect(self.show_error)
#         self.analysis_thread.progress_updated.connect(self.progress_bar.setValue)
#         self.analysis_thread.start()
        
#     def show_results(self, html, detected_platforms):
#         """Affiche les résultats de l'analyse"""
#         self.send_btn.setEnabled(True)
#         self.progress_bar.hide()
#         self.analysis_display.setHtml(html)
#         self.analysis_display.show()
        
#         # Animation d'apparition
#         fade_in = QPropertyAnimation(self.analysis_display, b"windowOpacity")
#         fade_in.setDuration(300)
#         fade_in.setStartValue(0)
#         fade_in.setEndValue(1)
#         fade_in.start()
        
#     def show_error(self, message):
#         """Affiche un message d'erreur"""
#         self.send_btn.setEnabled(True)
#         self.progress_bar.hide()
#         self.analysis_display.setHtml(f"""
#             <div style="padding: 20px; font-family: 'Segoe UI', sans-serif;">
#                 <h3 style="color: #ef4444;">❌ Erreur</h3>
#                 <p style="color: #64748b;">{message}</p>
#             </div>
#         """)
#         self.analysis_display.show()
        
#     def execute_action(self, action_data):
#         """Exécute une action spécifique"""
#         try:
#             data = json.loads(action_data)
#             action_type = data.get("type")
            
#             if action_type == "platform_action":
#                 platform = data.get("platform")
#                 action = data.get("action")
                
#                 if platform == "whatsapp":
#                     self.handle_whatsapp_action(action)
#                 elif platform == "instagram":
#                     self.handle_instagram_action(action)
#                 # Ajouter d'autres plateformes ici...
                
#         except Exception as e:
#             print(f"Erreur d'exécution: {e}")
            
#     def handle_whatsapp_action(self, action):
#         """Gère les actions WhatsApp"""
#         if action == "whatsapp_personal":
#             self.show_whatsapp_personal_ui()
#         elif action == "whatsapp_group":
#             self.show_whatsapp_group_ui()
#         else:
#             self.show_whatsapp_general_ui()
            
#     def show_whatsapp_personal_ui(self):
#         """Affiche l'interface pour les messages personnels WhatsApp"""
#         html = """
#         <div style="padding: 20px; font-family: 'Segoe UI', sans-serif;">
#             <h2 style="color: #1e293b; margin-bottom: 20px;">💬 Message WhatsApp Personnel</h2>
            
#             <div style="background: #f8fafc; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
#                 <h3 style="color: #1e293b; margin-bottom: 15px;">📋 Paramètres du message</h3>
                
#                 <div style="margin-bottom: 15px;">
#                     <label style="display: block; color: #64748b; margin-bottom: 8px;">Type de message :</label>
#                     <select style="width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #e2e8f0;">
#                         <option>Message standard</option>
#                         <option>Message avec image</option>
#                         <option>Message avec document</option>
#                     </select>
#                 </div>
                
#                 <div style="margin-bottom: 15px;">
#                     <label style="display: block; color: #64748b; margin-bottom: 8px;">Contenu du message :</label>
#                     <textarea style="width: 100%; height: 100px; padding: 10px; border-radius: 6px; border: 1px solid #e2e8f0;"></textarea>
#                 </div>
#             </div>
            
#             <button style="background: #25D366; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 16px; cursor: pointer;"
#                     onclick="pyHandler.handleAction(`{'type':'whatsapp_send','message_type':'personal'}`)">
#                 Envoyer le message
#             </button>
#         </div>
#         """
#         self.analysis_display.setHtml(html)
        
#     def show_whatsapp_group_ui(self):
#         """Affiche l'interface pour les messages de groupe WhatsApp"""
#         html = """
#         <div style="padding: 20px; font-family: 'Segoe UI', sans-serif;">
#             <h2 style="color: #1e293b; margin-bottom: 20px;">👥 Message de Groupe WhatsApp</h2>
            
#             <div style="background: #f8fafc; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
#                 <h3 style="color: #1e293b; margin-bottom: 15px;">📋 Sélection des groupes</h3>
                
#                 <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px;">
#                     <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid #e2e8f0;">
#                         <input type="checkbox" style="margin-right: 8px;"> Groupe Clients
#                     </label>
#                     <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid #e2e8f0;">
#                         <input type="checkbox" style="margin-right: 8px;"> Groupe Fournisseurs
#                     </label>
#                     <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid #e2e8f0;">
#                         <input type="checkbox" style="margin-right: 8px;"> Groupe Équipe
#                     </label>
#                     <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid #e2e8f0;">
#                         <input type="checkbox" style="margin-right: 8px;"> Groupe VIP
#                     </label>
#                 </div>
                
#                 <div style="margin-bottom: 15px;">
#                     <label style="display: block; color: #64748b; margin-bottom: 8px;">Contenu du message :</label>
#                     <textarea style="width: 100%; height: 100px; padding: 10px; border-radius: 6px; border: 1px solid #e2e8f0;"></textarea>
#                 </div>
                
#                 <div style="display: flex; gap: 10px;">
#                     <button style="flex: 1; background: white; border: 1px solid #e2e8f0; padding: 10px; border-radius: 6px; cursor: pointer;">
#                         Ajouter une pièce jointe
#                     </button>
#                     <button style="flex: 1; background: white; border: 1px solid #e2e8f0; padding: 10px; border-radius: 6px; cursor: pointer;">
#                         Prévisualiser
#                     </button>
#                 </div>
#             </div>
            
#             <button style="background: #25D366; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 16px; cursor: pointer;"
#                     onclick="pyHandler.handleAction(`{'type':'whatsapp_send','message_type':'group'}`)">
#                 Envoyer aux groupes sélectionnés
#             </button>
#         </div>
#         """
#         self.analysis_display.setHtml(html)
        
#     def show_whatsapp_general_ui(self):
#         """Affiche l'interface générale WhatsApp"""
#         html = """
#         <div style="padding: 20px; font-family: 'Segoe UI', sans-serif;">
#             <h2 style="color: #1e293b; margin-bottom: 20px;">📱 Automatisation WhatsApp</h2>
            
#             <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 20px;">
#                 <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 20px; cursor: pointer;"
#                      onclick="pyHandler.handleAction(`{'type':'whatsapp_action','action':'personal'}`)">
#                     <h3 style="color: #166534; margin-bottom: 10px;">💬 Messages personnels</h3>
#                     <p style="color: #64748b;">Envoyer des messages individuels à vos contacts</p>
#                 </div>
                
#                 <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 20px; cursor: pointer;"
#                      onclick="pyHandler.handleAction(`{'type':'whatsapp_action','action':'group'}`)">
#                     <h3 style="color: #075985; margin-bottom: 10px;">👥 Messages de groupe</h3>
#                     <p style="color: #64748b;">Envoyer des messages à plusieurs groupes</p>
#                 </div>
                
#                 <div style="background: #f5f3ff; border: 1px solid #ddd6fe; border-radius: 8px; padding: 20px; cursor: pointer;"
#                      onclick="pyHandler.handleAction(`{'type':'whatsapp_action','action':'auto_reply'}`)">
#                     <h3 style="color: #6d28d9; margin-bottom: 10px;">🤖 Réponses automatiques</h3>
#                     <p style="color: #64748b;">Configurer des réponses automatiques</p>
#                 </div>
                
#                 <div style="background: #fff7ed; border: 1px solid #fed7aa; border-radius: 8px; padding: 20px; cursor: pointer;"
#                      onclick="pyHandler.handleAction(`{'type':'whatsapp_action','action':'campaign'}`)">
#                     <h3 style="color: #9a3412; margin-bottom: 10px;">📢 Campagne</h3>
#                     <p style="color: #64748b;">Lancer une campagne WhatsApp</p>
#                 </div>
#             </div>
            
#             <div style="background: #f8fafc; border-radius: 8px; padding: 20px;">
#                 <h3 style="color: #1e293b; margin-bottom: 15px;">📊 Statistiques récentes</h3>
                
#                 <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 15px;">
#                     <div style="background: white; border-radius: 6px; padding: 15px; text-align: center;">
#                         <div style="font-size: 24px; font-weight: bold; color: #4f46e5;">42</div>
#                         <div style="color: #64748b; font-size: 14px;">Messages envoyés</div>
#                     </div>
#                     <div style="background: white; border-radius: 6px; padding: 15px; text-align: center;">
#                         <div style="font-size: 24px; font-weight: bold; color: #10b981;">78%</div>
#                         <div style="color: #64748b; font-size: 14px;">Taux de lecture</div>
#                     </div>
#                     <div style="background: white; border-radius: 6px; padding: 15px; text-align: center;">
#                         <div style="font-size: 24px; font-weight: bold; color: #ef4444;">12</div>
#                         <div style="color: #64748b; font-size: 14px;">Contacts bloqués</div>
#                     </div>
#                 </div>
                
#                 <button style="background: #4f46e5; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer;">
#                     Voir le rapport complet
#                 </button>
#             </div>
#         </div>
#         """
#         self.analysis_display.setHtml(html)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyle("Fusion")
    
#     # Définir la palette de couleurs pour un look moderne
#     palette = QPalette()
#     palette.setColor(QPalette.Window, QColor(248, 250, 252))
#     palette.setColor(QPalette.WindowText, QColor(30, 41, 59))
#     palette.setColor(QPalette.Base, QColor(255, 255, 255))
#     palette.setColor(QPalette.AlternateBase, QColor(243, 244, 246))
#     palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
#     palette.setColor(QPalette.ToolTipText, QColor(30, 41, 59))
#     palette.setColor(QPalette.Text, QColor(30, 41, 59))
#     palette.setColor(QPalette.Button, QColor(226, 232, 240))
#     palette.setColor(QPalette.ButtonText, QColor(30, 41, 59))
#     palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
#     palette.setColor(QPalette.Highlight, QColor(79, 70, 229))
#     palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
#     app.setPalette(palette)
    
#     window = MarketingAIAnalyzer()
#     window.show()
    
#     sys.exit(app.exec_())


import sys
import os
import sqlite3
import json
import time
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTextEdit, QProgressBar, QScrollArea, 
                             QGroupBox, QCheckBox, QFileDialog, QMessageBox, QStackedWidget, 
                             QSizePolicy, QLineEdit, QGridLayout, QFrame, QSpacerItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QUrl, QSize, QRect, QPropertyAnimation, QEasingCurve, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor, QDesktopServices, QMovie, QPainter, QColor, QFont, QPalette
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject

class ActionHandler(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    
    @pyqtSlot(str)
    def handleAction(self, action_data):
        try:
            data = json.loads(action_data)
            self.parent.execute_action(data)
        except Exception as e:
            print(f"Error handling action: {e}")

class AnalysisThread(QThread):
    analysis_complete = pyqtSignal(str, list)
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int)

    def __init__(self, prompt_text, db_path):
        super().__init__()
        self.prompt_text = prompt_text
        self.db_path = db_path
        self._is_running = True

    def run(self):
        conn = None
        try:
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
            
            cursor.execute('SELECT keyword, platform, response_template, action_type FROM detection_rules')
            rules = cursor.fetchall()
            
            for keyword, platform, template, action_type in rules:
                if not self._is_running:
                    return
                if keyword in prompt_lower:
                    detected.append((keyword, platform, template, action_type))
            
            analysis_text = self.generate_analysis_html(prompt_lower, detected)
            self.analysis_complete.emit(analysis_text, detected)
            
        except Exception as e:
            self.error_occurred.emit(f"Erreur d'analyse : {str(e)}")
        finally:
            if conn:
                conn.close()

    def generate_analysis_html(self, prompt, detected):
        html = """
        <style>
            :root {
                --primary: #4f46e5;
                --primary-hover: #4338ca;
                --background: #ffffff;
                --text: #1e293b;
                --text-secondary: #64748b;
                --card-bg: #f8fafc;
                --card-border: #e2e8f0;
                --success: #10b981;
                --error: #ef4444;
            }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: var(--background);
                color: var(--text);
                line-height: 1.5;
                padding: 0;
                margin: 0;
            }
            
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .platform-section {
                margin-bottom: 1.5rem;
                background: var(--background);
                border-radius: 12px;
                border: 1px solid var(--card-border);
                overflow: hidden;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            
            .platform-header {
                padding: 1rem 1.5rem;
                background: var(--card-bg);
                border-bottom: 1px solid var(--card-border);
                display: flex;
                align-items: center;
            }
            
            .platform-icon {
                font-size: 1.5rem;
                margin-right: 0.75rem;
            }
            
            .platform-title {
                font-size: 1.125rem;
                font-weight: 600;
                margin: 0;
            }
            
            .options-container {
                padding: 1rem 1.5rem;
            }
            
            .option-card {
                padding: 1rem;
                margin-bottom: 0.75rem;
                background: var(--card-bg);
                border: 1px solid var(--card-border);
                border-radius: 8px;
                transition: all 0.2s ease;
                cursor: pointer;
            }
            
            .option-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
                border-color: var(--primary);
            }
            
            .option-title {
                font-weight: 600;
                margin-bottom: 0.25rem;
            }
            
            .option-desc {
                color: var(--text-secondary);
                font-size: 0.875rem;
                margin-bottom: 0.75rem;
            }
            
            .action-btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background: var(--primary);
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 6px;
                font-size: 0.875rem;
                font-weight: 500;
                cursor: pointer;
                transition: background 0.2s;
            }
            
            .action-btn:hover {
                background: var(--primary-hover);
            }
            
            .keyword-tag {
                display: inline-block;
                background: #e0e7ff;
                color: #4f46e5;
                padding: 0.25rem 0.5rem;
                border-radius: 4px;
                font-size: 0.75rem;
                margin-right: 0.5rem;
                margin-bottom: 0.5rem;
            }
        </style>
        
        <div class="container">
            <h1 style="font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">✨ Suggestions</h1>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">Voici ce que je peux faire pour vous :</p>
        """
        
        if not detected:
            html += """
            <div class="platform-section">
                <div class="platform-header">
                    <div class="platform-icon">💡</div>
                    <h2 class="platform-title">Conseils généraux</h2>
                </div>
                <div class="options-container">
                    <p style="margin-bottom: 1rem;">Je n'ai pas détecté de demande spécifique. Voici des suggestions :</p>
                    <button class="action-btn" onclick='pyHandler.handleAction(`{"type":"general_advice"}`)'>
                        Voir les conseils marketing
                    </button>
                </div>
            </div>
            """
        else:
            platforms = {}
            for item in detected:
                platform = item[1]
                if platform not in platforms:
                    platforms[platform] = []
                platforms[platform].append(item)
            
            for platform, items in platforms.items():
                icon = {
                    'whatsapp': '💬',
                    'instagram': '📸',
                    'facebook': '👍',
                    'linkedin': '💼',
                    'tiktok': '🎵',
                    'email': '✉️',
                    'twitter': '🐦',
                    'youtube': '▶️',
                    'analytics': '📊',
                    'seo': '🔍'
                }.get(platform, '📌')
                
                html += f"""
                <div class="platform-section">
                    <div class="platform-header">
                        <div class="platform-icon">{icon}</div>
                        <h2 class="platform-title">{platform.capitalize()}</h2>
                    </div>
                    <div class="options-container">
                """
                
                for idx, (keyword, platform, template, action_type) in enumerate(items):
                    html += f"""
                    <div class="option-card" onclick='pyHandler.handleAction(`{{
                        "type": "platform_action",
                        "platform": "{platform}",
                        "action": "{action_type}"
                    }}`)'>
                        <div class="option-title">{template}</div>
                        <div class="option-desc">Basé sur votre mention : <span class="keyword-tag">{keyword}</span></div>
                        <button class="action-btn">
                            Exécuter cette action
                        </button>
                    </div>
                    """
                
                html += """
                    </div>
                </div>
                """
        
        html += "</div>"
        return html

class MarketingAIAnalyzer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Leopardo - Assistant Marketing IA"))
        self.setMinimumSize(1000, 700)
        
        # Configuration
        self.current_user = self.tr("Utilisateur")
        self.settings = {
            "dark_mode": False,
            "animations": True
        }
        
        # Initialisation
        self.init_db()
        self.init_ui()
        
    def init_db(self):
        """Initialise la base de données avec un jeu de données complet"""
        self.db_path = "marketing_a1i.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Création des tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detection_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                platform TEXT NOT NULL,
                response_template TEXT NOT NULL,
                action_type TEXT NOT NULL
            )
        ''')
        
        # Vérification des données existantes
        cursor.execute("SELECT COUNT(*) FROM detection_rules")
        if cursor.fetchone()[0] == 0:
            # Insertion d'un jeu de données complet
            rules = [
                # WhatsApp
                ("whatsapp", "whatsapp", self.tr("Automatisation WhatsApp complète"), "whatsapp_auto"),
                ("message whatsapp", "whatsapp", self.tr("Envoyer un message WhatsApp personnel"), "whatsapp_personal"),
                ("groupe whatsapp", "whatsapp", self.tr("Envoyer un message à un groupe WhatsApp"), "whatsapp_group"),
                ("campagne whatsapp", "whatsapp", self.tr("Lancer une campagne WhatsApp"), "whatsapp_campaign"),
                ("automatiser whatsapp", "whatsapp", self.tr("Automatiser les réponses WhatsApp"), "whatsapp_auto_reply"),
                
                # Instagram
                ("instagram", "instagram", self.tr("Créer une publication Instagram"), "instagram_post"),
                ("story instagram", "instagram", self.tr("Créer une story Instagram"), "instagram_story"),
                ("reels instagram", "instagram", self.tr("Créer un Reel Instagram"), "instagram_reel"),
                ("campagne instagram", "instagram", self.tr("Lancer une campagne publicitaire Instagram"), "instagram_ads"),
                ("hashtag instagram", "instagram", self.tr("Générer des hashtags optimisés"), "instagram_hashtags"),
                
                # Facebook
                ("facebook", "facebook", self.tr("Créer un post Facebook"), "facebook_post"),
                ("publicité facebook", "facebook", self.tr("Lancer une publicité Facebook"), "facebook_ads"),
                ("page facebook", "facebook", self.tr("Optimiser votre page Facebook"), "facebook_page"),
                
                # Autres plateformes
                ("linkedin", "linkedin", self.tr("Créer un post LinkedIn"), "linkedin_post"),
                ("tiktok", "tiktok", self.tr("Créer une vidéo TikTok"), "tiktok_video"),
                ("youtube", "youtube", self.tr("Optimiser une vidéo YouTube"), "youtube_optimize"),
                ("email", "email", self.tr("Créer une campagne email"), "email_campaign"),
                ("newsletter", "email", self.tr("Créer une newsletter"), "email_newsletter"),
                
                # Général
                ("stratégie", "general", self.tr("Élaborer une stratégie marketing"), "marketing_strategy"),
                ("analyse", "analytics", self.tr("Analyser les performances"), "performance_analysis"),
                ("seo", "seo", self.tr("Optimisation SEO"), "seo_optimization"),
                ("contenu", "content", self.tr("Planifier du contenu"), "content_planning")
            ]
            
            cursor.executemany('''
                INSERT INTO detection_rules (keyword, platform, response_template, action_type)
                VALUES (?, ?, ?, ?)
            ''', rules)
            conn.commit()
        
        conn.close()
        
    def init_ui(self):
        """Initialise l'interface utilisateur avec un design moderne"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Barre d'outils
        self.create_toolbar()
        
        # Zone de contenu principale
        self.content_area = QWidget()
        self.content_area.setObjectName("contentArea")
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Stack pour les différentes vues
        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)
        
        # Vue principale
        self.setup_main_view()
        
        self.main_layout.addWidget(self.content_area)
        
        # Appliquer le style global
        self.update_styles()
        
    def create_toolbar(self):
        """Crée une barre d'outils moderne avec dégradé"""
        toolbar = QWidget()
        toolbar.setObjectName("mainToolbar")
        toolbar.setFixedHeight(60)
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(20)
        
        # Logo
        logo = QLabel(self.tr("LEOPARDO AI"))
        logo.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
            font-family: 'Segoe UI', sans-serif;
        """)
        
        # Boutons de navigation
        nav_btns = [
            (self.tr("Accueil"), "home", lambda: self.stacked_widget.setCurrentIndex(0)),
            (self.tr("Historique"), "history", lambda: self.stacked_widget.setCurrentIndex(1)),
            (self.tr("Paramètres"), "settings", lambda: self.stacked_widget.setCurrentIndex(2))
        ]
        
        layout.addWidget(logo)
        
        for text, icon, callback in nav_btns:
            btn = QPushButton(text)
            btn.setIcon(QIcon.fromTheme(icon))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    background: transparent;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 4px;
                    font-family: 'Segoe UI', sans-serif;
                }
                QPushButton:hover {
                    background: rgba(255,255,255,0.1);
                }
            """)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Bouton utilisateur
        user_btn = QPushButton(self.current_user)
        user_btn.setIcon(QIcon.fromTheme("user"))
        user_btn.setStyleSheet("""
            QPushButton {
                color: white;
                background: rgba(255,255,255,0.1);
                border: none;
                padding: 6px 12px;
                border-radius: 16px;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.2);
            }
        """)
        layout.addWidget(user_btn)
        
        self.main_layout.addWidget(toolbar)
        
    def setup_main_view(self):
        """Configure la vue principale avec une UX optimisée"""
        main_view = QWidget()
        main_view.setObjectName("mainView")
        layout = QVBoxLayout(main_view)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(0)
        
        # Conteneur central pour centrer le contenu
        center_container = QWidget()
        center_container.setMaximumWidth(800)
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        
        # En-tête
        header = QLabel(self.tr("Assistant Marketing IA"))
        header.setObjectName("mainHeader")
        
        subheader = QLabel(self.tr("Décrivez votre besoin marketing pour obtenir des solutions personnalisées"))
        subheader.setObjectName("mainSubheader")
        
        # Zone de prompt unifiée avec bouton
        prompt_container = QWidget()
        prompt_container.setObjectName("promptContainer")
        prompt_layout = QVBoxLayout(prompt_container)
        prompt_layout.setContentsMargins(0, 0, 0, 0)
        prompt_layout.setSpacing(0)
        
        # Zone de texte avec placeholder stylisé
        self.prompt_input = QTextEdit()
        self.prompt_input.setObjectName("promptInput")
        self.prompt_input.setPlaceholderText(self.tr("Ex: Je veux automatiser mes publications WhatsApp pour mon entreprise de vêtements..."))
        
        # Bouton d'envoi intégré
        self.send_btn = QPushButton(self.tr("Analyser"))
        self.send_btn.setObjectName("sendButton")
        self.send_btn.setIcon(QIcon.fromTheme("edit-find"))
        self.send_btn.clicked.connect(self.analyze_prompt)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        
        # Suggestions de prompts
        self.setup_prompt_suggestions()
        
        # Zone de résultats
        self.analysis_display = QWebEngineView()
        self.analysis_display.setObjectName("analysisDisplay")
        self.analysis_display.hide()
        
        # Configuration du canal de communication
        self.channel = QWebChannel()
        self.handler = ActionHandler(self)
        self.channel.registerObject('pyHandler', self.handler)
        self.analysis_display.page().setWebChannel(self.channel)
        
        # Espaceur pour pousser le contenu vers le haut
        self.top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        # Espaceur pour centrer le contenu
        self.bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        # Assemblage des composants
        prompt_layout.addWidget(self.prompt_input)
        prompt_layout.addWidget(self.send_btn, alignment=Qt.AlignRight)
        prompt_layout.addWidget(self.progress_bar)
        
        center_layout.addItem(self.top_spacer)
        center_layout.addWidget(header)
        center_layout.addWidget(subheader)
        center_layout.addSpacing(20)
        center_layout.addWidget(prompt_container)
        center_layout.addSpacing(15)
        center_layout.addLayout(self.suggestions_layout)
        center_layout.addSpacing(20)
        center_layout.addWidget(self.analysis_display)
        center_layout.addItem(self.bottom_spacer)
        
        layout.addWidget(center_container, alignment=Qt.AlignCenter)
        
        self.stacked_widget.addWidget(main_view)
        
    def setup_prompt_suggestions(self):
        """Configure les suggestions de prompts prédéfinis"""
        self.suggestions_layout = QVBoxLayout()
        self.suggestions_layout.setContentsMargins(0, 0, 0, 0)
        self.suggestions_layout.setSpacing(10)
        
        title = QLabel(self.tr("💡 Exemples de requêtes:"))
        title.setObjectName("suggestionsTitle")
        
        suggestions_grid = QGridLayout()
        suggestions_grid.setContentsMargins(0, 0, 0, 0)
        suggestions_grid.setSpacing(10)
        
        suggestions = [
            ("📱", self.tr("Réseaux sociaux"), self.tr("Créer une stratégie pour Instagram et Facebook")),
            ("📈", self.tr("Analyse"), self.tr("Analyser les performances de ma dernière campagne")),
            ("✉️", self.tr("Email"), self.tr("Rédiger une newsletter pour mes clients")),
            ("💬", self.tr("WhatsApp"), self.tr("Automatiser les messages WhatsApp pour mon commerce")),
            ("🔍", self.tr("SEO"), self.tr("Optimiser mon site web pour le référencement")),
            ("📊", self.tr("Rapport"), self.tr("Générer un rapport marketing mensuel"))
        ]
        
        for i, (icon, title_text, prompt_text) in enumerate(suggestions):
            btn = QPushButton(f"{icon} {title_text}")
            btn.setToolTip(prompt_text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setObjectName("suggestionButton")
            btn.clicked.connect(lambda _, text=prompt_text: self.prompt_input.setPlainText(text))
            suggestions_grid.addWidget(btn, i // 2, i % 2)
        
        self.suggestions_layout.addWidget(title)
        self.suggestions_layout.addLayout(suggestions_grid)
        
    def update_styles(self):
        """Applique les styles CSS à l'application"""
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', sans-serif;
            }
            
            QWidget#contentArea {
                background: #f8fafc;
            }
            
            QWidget#mainToolbar {
                background: qlineargradient(x1:0, y1:0, x1:1, y1:0, stop:0 #4f46e5, stop:1 #7c3aed);
                border-bottom: 1px solid #4f46e5;
            }
            
            QLabel#mainHeader {
                font-size: 28px;
                font-weight: bold;
                color: #1e293b;
                margin-bottom: 5px;
            }
            
            QLabel#mainSubheader {
                font-size: 16px;
                color: #64748b;
                margin-bottom: 30px;
            }
            
            QWidget#promptContainer {
                background: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                padding: 1px;
            }
            
            QTextEdit#promptInput {
                background: white;
                border: none;
                font-size: 16px;
                padding: 20px;
                border-radius: 12px;
                min-height: 120px;
                color: #1e293b;
            }
            
            QTextEdit#promptInput:focus {
                border: none;
            }
            
            QPushButton#sendButton {
                background: #4f46e5;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                margin: 10px;
                margin-top: 0;
            }
            
            QPushButton#sendButton:hover {
                background: #4338ca;
            }
            
            QPushButton#sendButton:disabled {
                background: #a5b4fc;
            }
            
            QProgressBar#progressBar {
                height: 6px;
                background: #e2e8f0;
                border-radius: 3px;
                margin: 0 10px 10px 10px;
            }
            
            QProgressBar#progressBar::chunk {
                background: #4f46e5;
                border-radius: 3px;
            }
            
            QLabel#suggestionsTitle {
                font-size: 14px;
                color: #64748b;
                margin-bottom: 5px;
            }
            
            QPushButton#suggestionButton {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                text-align: left;
                color: #1e293b;
            }
            
            QPushButton#suggestionButton:hover {
                background: #f1f5f9;
                border-color: #cbd5e1;
            }
            
            QWebEngineView#analysisDisplay {
                background: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                min-height: 300px;
            }
        """)
        
    def analyze_prompt(self):
        """Lance l'analyse du prompt"""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            self.show_error(self.tr("Veuillez saisir votre demande"))
            return
        
        # Désactiver le bouton pendant l'analyse
        self.send_btn.setEnabled(False)
        self.progress_bar.show()
        self.analysis_display.hide()
        
        # Réduire l'espace au-dessus pour centrer le contenu
        self.top_spacer.changeSize(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        # Animation de chargement
        self.loading_animation = QPropertyAnimation(self.progress_bar, b"value")
        self.loading_animation.setDuration(2000)
        self.loading_animation.setStartValue(0)
        self.loading_animation.setEndValue(100)
        self.loading_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.loading_animation.start()
        
        # Lancer l'analyse dans un thread séparé
        self.analysis_thread = AnalysisThread(prompt, self.db_path)
        self.analysis_thread.analysis_complete.connect(self.show_results)
        self.analysis_thread.error_occurred.connect(self.show_error)
        self.analysis_thread.progress_updated.connect(self.progress_bar.setValue)
        self.analysis_thread.start()
        
    def show_results(self, html, detected_platforms):
        """Affiche les résultats de l'analyse"""
        self.send_btn.setEnabled(True)
        self.progress_bar.hide()
        self.analysis_display.setHtml(html)
        self.analysis_display.show()
        
        # Ajuster les espaceurs pour pousser le contenu vers le haut
        self.top_spacer.changeSize(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.bottom_spacer.changeSize(20, 10, QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        # Animation d'apparition
        fade_in = QPropertyAnimation(self.analysis_display, b"windowOpacity")
        fade_in.setDuration(300)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)
        fade_in.start()
        
    def show_error(self, message):
        """Affiche un message d'erreur"""
        self.send_btn.setEnabled(True)
        self.progress_bar.hide()
        self.analysis_display.setHtml(f"""
            <div style="padding: 20px; font-family: 'Segoe UI', sans-serif;">
                <h3 style="color: #ef4444;">❌ {self.tr('Erreur')}</h3>
                <p style="color: #64748b;">{message}</p>
            </div>
        """)
        self.analysis_display.show()
        
    def execute_action(self, action_data):
        """Exécute une action spécifique"""
        try:
            data = json.loads(action_data)
            action_type = data.get("type")
            
            if action_type == "platform_action":
                platform = data.get("platform")
                action = data.get("action")
                
                if platform == "whatsapp":
                    self.handle_whatsapp_action(action)
                elif platform == "instagram":
                    self.handle_instagram_action(action)
                # Ajouter d'autres plateformes ici...
                
        except Exception as e:
            print(f"Erreur d'exécution: {e}")
            
    def handle_whatsapp_action(self, action):
        """Gère les actions WhatsApp"""
        if action == "whatsapp_personal":
            self.show_whatsapp_personal_ui()
        elif action == "whatsapp_group":
            self.show_whatsapp_group_ui()
        else:
            self.show_whatsapp_general_ui()
            
    def show_whatsapp_personal_ui(self):
        """Affiche l'interface pour les messages personnels WhatsApp"""
        html = f"""
        <div style="padding: 20px; font-family: 'Segoe UI', sans-serif;">
            <h2 style="color: #1e293b; margin-bottom: 20px;">💬 {self.tr('Message WhatsApp Personnel')}</h2>
            
            <div style="background: #f8fafc; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
                <h3 style="color: #1e293b; margin-bottom: 15px;">📋 {self.tr('Paramètres du message')}</h3>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; color: #64748b; margin-bottom: 8px;">{self.tr('Type de message')} :</label>
                    <select style="width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #e2e8f0;">
                        <option>{self.tr('Message standard')}</option>
                        <option>{self.tr('Message avec image')}</option>
                        <option>{self.tr('Message avec document')}</option>
                    </select>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; color: #64748b; margin-bottom: 8px;">{self.tr('Contenu du message')} :</label>
                    <textarea style="width: 100%; height: 100px; padding: 10px; border-radius: 6px; border: 1px solid #e2e8f0;"></textarea>
                </div>
            </div>
            
            <button style="background: #25D366; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 16px; cursor: pointer;"
                    onclick="pyHandler.handleAction(`{{'type':'whatsapp_send','message_type':'personal'}}`)">
                {self.tr('Envoyer le message')}
            </button>
        </div>
        """
        self.analysis_display.setHtml(html)
        
    def show_whatsapp_group_ui(self):
        """Affiche l'interface pour les messages de groupe WhatsApp"""
        html = f"""
        <div style="padding: 20px; font-family: 'Segoe UI', sans-serif;">
            <h2 style="color: #1e293b; margin-bottom: 20px;">👥 {self.tr('Message de Groupe WhatsApp')}</h2>
            
            <div style="background: #f8fafc; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
                <h3 style="color: #1e293b; margin-bottom: 15px;">📋 {self.tr('Sélection des groupes')}</h3>
                
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px;">
                    <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid #e2e8f0;">
                        <input type="checkbox" style="margin-right: 8px;"> {self.tr('Groupe Clients')}
                    </label>
                    <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid #e2e8f0;">
                        <input type="checkbox" style="margin-right: 8px;"> {self.tr('Groupe Fournisseurs')}
                    </label>
                    <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid #e2e8f0;">
                        <input type="checkbox" style="margin-right: 8px;"> {self.tr('Groupe Équipe')}
                    </label>
                    <label style="display: flex; align-items: center; padding: 10px; background: white; border-radius: 6px; border: 1px solid #e2e8f0;">
                        <input type="checkbox" style="margin-right: 8px;"> {self.tr('Groupe VIP')}
                    </label>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; color: #64748b; margin-bottom: 8px;">{self.tr('Contenu du message')} :</label>
                    <textarea style="width: 100%; height: 100px; padding: 10px; border-radius: 6px; border: 1px solid #e2e8f0;"></textarea>
                </div>
                
                <div style="display: flex; gap: 10px;">
                    <button style="flex: 1; background: white; border: 1px solid #e2e8f0; padding: 10px; border-radius: 6px; cursor: pointer;">
                        {self.tr('Ajouter une pièce jointe')}
                    </button>
                    <button style="flex: 1; background: white; border: 1px solid #e2e8f0; padding: 10px; border-radius: 6px; cursor: pointer;">
                        {self.tr('Prévisualiser')}
                    </button>
                </div>
            </div>
            
            <button style="background: #25D366; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 16px; cursor: pointer;"
                    onclick="pyHandler.handleAction(`{{'type':'whatsapp_send','message_type':'group'}}`)">
                {self.tr('Envoyer aux groupes sélectionnés')}
            </button>
        </div>
        """
        self.analysis_display.setHtml(html)
        
    def show_whatsapp_general_ui(self):
        """Affiche l'interface générale WhatsApp"""
        html = f"""
        <div style="padding: 20px; font-family: 'Segoe UI', sans-serif;">
            <h2 style="color: #1e293b; margin-bottom: 20px;">📱 {self.tr('Automatisation WhatsApp')}</h2>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 20px;">
                <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 20px; cursor: pointer;"
                     onclick="pyHandler.handleAction(`{{'type':'whatsapp_action','action':'personal'}}`)">
                    <h3 style="color: #166534; margin-bottom: 10px;">💬 {self.tr('Messages personnels')}</h3>
                    <p style="color: #64748b;">{self.tr('Envoyer des messages individuels à vos contacts')}</p>
                </div>
                
                <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 20px; cursor: pointer;"
                     onclick="pyHandler.handleAction(`{{'type':'whatsapp_action','action':'group'}}`)">
                    <h3 style="color: #075985; margin-bottom: 10px;">👥 {self.tr('Messages de groupe')}</h3>
                    <p style="color: #64748b;">{self.tr('Envoyer des messages à plusieurs groupes')}</p>
                </div>
                
                <div style="background: #f5f3ff; border: 1px solid #ddd6fe; border-radius: 8px; padding: 20px; cursor: pointer;"
                     onclick="pyHandler.handleAction(`{{'type':'whatsapp_action','action':'auto_reply'}}`)">
                    <h3 style="color: #6d28d9; margin-bottom: 10px;">🤖 {self.tr('Réponses automatiques')}</h3>
                    <p style="color: #64748b;">{self.tr('Configurer des réponses automatiques')}</p>
                </div>
                
                <div style="background: #fff7ed; border: 1px solid #fed7aa; border-radius: 8px; padding: 20px; cursor: pointer;"
                     onclick="pyHandler.handleAction(`{{'type':'whatsapp_action','action':'campaign'}}`)">
                    <h3 style="color: #9a3412; margin-bottom: 10px;">📢 {self.tr('Campagne')}</h3>
                    <p style="color: #64748b;">{self.tr('Lancer une campagne WhatsApp')}</p>
                </div>
            </div>
            
            <div style="background: #f8fafc; border-radius: 8px; padding: 20px;">
                <h3 style="color: #1e293b; margin-bottom: 15px;">📊 {self.tr('Statistiques récentes')}</h3>
                
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 15px;">
                    <div style="background: white; border-radius: 6px; padding: 15px; text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #4f46e5;">42</div>
                        <div style="color: #64748b; font-size: 14px;">{self.tr('Messages envoyés')}</div>
                    </div>
                    <div style="background: white; border-radius: 6px; padding: 15px; text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #10b981;">78%</div>
                        <div style="color: #64748b; font-size: 14px;">{self.tr('Taux de lecture')}</div>
                    </div>
                    <div style="background: white; border-radius: 6px; padding: 15px; text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #ef4444;">12</div>
                        <div style="color: #64748b; font-size: 14px;">{self.tr('Contacts bloqués')}</div>
                    </div>
                </div>
                
                <button style="background: #4f46e5; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer;">
                    {self.tr('Voir le rapport complet')}
                </button>
            </div>
        </div>
        """
        self.analysis_display.setHtml(html)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Définir la palette de couleurs pour un look moderne
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(248, 250, 252))
    palette.setColor(QPalette.WindowText, QColor(30, 41, 59))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(243, 244, 246))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(30, 41, 59))
    palette.setColor(QPalette.Text, QColor(30, 41, 59))
    palette.setColor(QPalette.Button, QColor(226, 232, 240))
    palette.setColor(QPalette.ButtonText, QColor(30, 41, 59))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Highlight, QColor(79, 70, 229))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    window = MarketingAIAnalyzer()
    window.show()
    
    sys.exit(app.exec_())