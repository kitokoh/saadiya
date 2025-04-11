import sys
import random
import time
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QTextEdit, QPushButton, QRadioButton, QButtonGroup, 
                             QFrame, QScrollArea, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap, QIcon
import sqlite3
from sqlite3 import Error

class MarketingAIAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Marketing AI Assistant")
        self.setMinimumSize(800, 600)
        
        # Initialisation de la base de données
        self.init_db()
        
        # Style de l'application
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QTextEdit {
                background-color: white;
                border: 2px solid #d1d5db;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #374151;
            }
            QTextEdit:focus {
                border: 2px solid #3b82f6;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            QLabel {
                color: #374151;
                font-size: 14px;
            }
            .header {
                font-size: 24px;
                font-weight: bold;
                color: #1f2937;
            }
            .section {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }
            .analysis-section {
                background-color: #f0fdf4;
                border: 1px solid #bbf7d0;
                border-radius: 12px;
                padding: 20px;
            }
            .option-button {
                text-align: left;
                padding: 12px 16px;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                margin-bottom: 8px;
            }
            .option-button:hover {
                background-color: #e5e7eb;
            }
            .option-button:checked {
                background-color: #dbeafe;
                border: 1px solid #3b82f6;
            }
        """)
        
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)
        
        # En-tête
        self.header = QLabel("Marketing AI Assistant")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #1e40af;
            margin-bottom: 10px;
        """)
        self.main_layout.addWidget(self.header)
        
        # Sous-titre
        self.subheader = QLabel("Obtenez des recommandations marketing basées sur votre prompt")
        self.subheader.setAlignment(Qt.AlignCenter)
        self.subheader.setStyleSheet("font-size: 16px; color: #6b7280;")
        self.main_layout.addWidget(self.subheader)
        
        # Zone de prompt
        self.prompt_section = QWidget()
        self.prompt_section.setStyleSheet(".section;")
        self.prompt_layout = QVBoxLayout(self.prompt_section)
        self.prompt_layout.setContentsMargins(15, 15, 15, 15)
        self.prompt_layout.setSpacing(15)
        
        self.prompt_label = QLabel("Décrivez votre besoin marketing:")
        self.prompt_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Ex: Je veux promouvoir mon nouveau produit dans des groupes Facebook ciblant les entrepreneurs...")
        self.prompt_input.setMinimumHeight(120)
        
        self.analyze_button = QPushButton("Analyser le prompt")
        self.analyze_button.setIcon(QIcon.fromTheme("edit-find"))
        self.analyze_button.clicked.connect(self.analyze_prompt)
        
        self.prompt_layout.addWidget(self.prompt_label)
        self.prompt_layout.addWidget(self.prompt_input)
        self.prompt_layout.addWidget(self.analyze_button, alignment=Qt.AlignRight)
        
        #self.main_layout.addWidget(self.prompt_section)
        self.setup_prompt_section()        
        # Section d'analyse (initialement cachée)
        self.analysis_section = QWidget()
        self.analysis_section.setStyleSheet(".analysis-section;")
        self.analysis_section.hide()
        self.analysis_layout = QVBoxLayout(self.analysis_section)
        self.analysis_layout.setContentsMargins(20, 20, 20, 20)
        self.analysis_layout.setSpacing(15)
        
        self.analysis_header = QLabel("Analyse du prompt")
        self.analysis_header.setStyleSheet("font-weight: bold; font-size: 18px; color: #065f46;")
        
        self.analysis_result = QLabel()
        self.analysis_result.setWordWrap(True)
        self.analysis_result.setStyleSheet("font-size: 15px;")
        
        self.analysis_layout.addWidget(self.analysis_header)
        self.analysis_layout.addWidget(self.analysis_result)
        
        # Options de marketing
        self.options_section = QWidget()
        self.options_section.hide()
        self.options_layout = QVBoxLayout(self.options_section)
        self.options_layout.setContentsMargins(0, 20, 0, 0)
        self.options_layout.setSpacing(10)
        
        self.options_header = QLabel("Actions recommandées:")
        self.options_header.setStyleSheet("font-weight: bold; font-size: 16px; color: #1e40af;")
        self.options_layout.addWidget(self.options_header)
        
        self.button_group = QButtonGroup()
        self.options_layout.addWidget(self.create_option("Publier dans des groupes Facebook", "facebook"))
        self.options_layout.addWidget(self.create_option("Envoyer des messages WhatsApp", "whatsapp"))
        self.options_layout.addWidget(self.create_option("Créer une campagne email", "email"))
        self.options_layout.addWidget(self.create_option("Lancer une publicité Instagram", "instagram"))
        self.options_layout.addWidget(self.create_option("Créer une vidéo TikTok", "tiktok"))
        
        self.execute_button = QPushButton("Exécuter l'action")
        self.execute_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.execute_button.clicked.connect(self.execute_action)
        self.execute_button.hide()
        self.options_layout.addWidget(self.execute_button, alignment=Qt.AlignRight)
        
        self.analysis_layout.addWidget(self.options_section)
        self.main_layout.addWidget(self.analysis_section)
        
        # Espace flexible en bas
        self.main_layout.addStretch()
        
        # Footer
        self.footer = QLabel("© 2023 Marketing AI Assistant - Version 1.0")
        self.footer.setAlignment(Qt.AlignCenter)
        self.footer.setStyleSheet("color: #9ca3af; font-size: 12px;")
        self.main_layout.addWidget(self.footer)

    def keyPressEvent(self, event):
        """Gère les raccourcis clavier"""
        if event.key() == Qt.Key_Return and (event.modifiers() & Qt.ControlModifier):
            self.analyze_prompt()
            return
        super().keyPressEvent(event)



    def setup_prompt_section(self):
        """Configure la section du prompt avec un style similaire à ChatGPT"""
        
        # Conteneur principal
        self.prompt_container = QWidget()
        self.prompt_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                padding: 0px;
            }
        """)
        
        # Layout principal
        self.prompt_layout = QVBoxLayout(self.prompt_container)
        self.prompt_layout.setContentsMargins(0, 0, 0, 0)
        self.prompt_layout.setSpacing(0)

        # Champ de texte (entrée de prompt)
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Décrivez votre besoin marketing... (Ex: Comment promouvoir mon nouveau produit sur les réseaux sociaux?)")
        self.prompt_input.setMinimumHeight(120)
        self.prompt_input.setMaximumHeight(180)
        self.prompt_input.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: none;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                padding: 16px;
                font-size: 15px;
                color: #374151;
            }
            QTextEdit:focus {
                background-color: white;
            }
        """)

        # Conteneur du bouton (barre inférieure)
        self.button_container = QWidget()
        self.button_container.setStyleSheet("""
            QWidget {
                background-color: #f9fafb;
                border-bottom-left-radius: 12px;
                border-bottom-right-radius: 12px;
                border-top: 1px solid #e5e7eb;
            }
        """)
        
        # Layout du bouton
        self.button_layout = QHBoxLayout(self.button_container)
        self.button_layout.setContentsMargins(12, 8, 12, 8)
        self.button_layout.setSpacing(8)

        # Espaceur pour aligner le bouton à droite
        self.button_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Bouton d'envoi rond
        self.analyze_button = QPushButton()
        self.analyze_button.setIcon(QIcon(":/icons/send.png"))  # Remplacez par votre icône
        self.analyze_button.setIconSize(QSize(20, 20))
        self.analyze_button.setFixedSize(36, 36)
        self.analyze_button.setStyleSheet("""
            QPushButton {
                background-color: #4f46e5;
                border: none;
                border-radius: 18px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
            QPushButton:pressed {
                background-color: #3730a3;
            }
            QPushButton:disabled {
                background-color: #a5b4fc;
            }
        """)
        self.analyze_button.clicked.connect(self.analyze_prompt)
        self.analyze_button.setToolTip("Analyser le prompt (Ctrl+Entrée)")

        # Ajout du bouton au layout
        self.button_layout.addWidget(self.analyze_button)

        # Assemblage final du layout principal
        self.prompt_layout.addWidget(self.prompt_input)
        self.prompt_layout.addWidget(self.button_container)
        
        # Remplacer l'ancienne section prompt dans le layout principal
        self.main_layout.insertWidget(2, self.prompt_container)  # Position 2 après le header en terme de style




    def create_option(self, text, platform):
        option = QRadioButton(text)
        option.setStyleSheet(".option-button;")
        option.setIconSize(QSize(24, 24))
        
        # Ajouter une icône selon la plateforme
        if platform == "facebook":
            option.setIcon(QIcon(":/icons/facebook.png"))  # Remplacez par une vraie icône
        elif platform == "whatsapp":
            option.setIcon(QIcon(":/icons/whatsapp.png"))
        elif platform == "email":
            option.setIcon(QIcon(":/icons/email.png"))
        elif platform == "instagram":
            option.setIcon(QIcon(":/icons/instagram.png"))
        elif platform == "tiktok":
            option.setIcon(QIcon(":/icons/tiktok.png"))
        
        self.button_group.addButton(option)
        return option
    
    def init_db(self):
        """Initialise la base de données SQLite"""
        try:
            self.conn = sqlite3.connect('marketing_ai.db')
            self.cursor = self.conn.cursor()
            
            # Créer la table pour les prompts et analyses
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_text TEXT NOT NULL,
                    analysis_result TEXT,
                    actions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Créer la table pour les règles de détection
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS detection_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    response_template TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insérer des règles de base si la table est vide
            self.cursor.execute('SELECT COUNT(*) FROM detection_rules')
            if self.cursor.fetchone()[0] == 0:
                base_rules = [
                    ('facebook', 'facebook', 'Publication dans des groupes Facebook ciblés'),
                    ('groupes', 'facebook', 'Publication dans des groupes Facebook ciblés'),
                    ('whatsapp', 'whatsapp', 'Envoi de messages WhatsApp personnalisés'),
                    ('email', 'email', 'Campagne email marketing'),
                    ('instagram', 'instagram', 'Publicité Instagram ciblée'),
                    ('tiktok', 'tiktok', 'Création de vidéo TikTok promotionnelle'),
                    ('réseaux sociaux', 'multi', 'Campagne multi-plateformes sur les réseaux sociaux'),
                ]
                
                self.cursor.executemany('''
                    INSERT INTO detection_rules (keyword, platform, response_template)
                    VALUES (?, ?, ?)
                ''', base_rules)
                self.conn.commit()
                
        except Error as e:
            print(f"Erreur de base de données: {e}")
    
    def analyze_prompt(self):
        """Analyse le prompt de l'utilisateur"""
        prompt_text = self.prompt_input.toPlainText().strip()
        if not prompt_text:
            return
        
        # Enregistrer le prompt dans la base de données
        self.cursor.execute('''
            INSERT INTO prompts (prompt_text) VALUES (?)
        ''', (prompt_text,))
        self.conn.commit()
        prompt_id = self.cursor.lastrowid
        
        # Afficher la section d'analyse avec un effet de chargement
        self.analysis_section.show()
        self.analysis_result.setText("Analyse en cours...")
        self.options_section.hide()
        
        # Simuler un temps d'analyse avec QTimer
        QTimer.singleShot(1500, lambda: self.display_analysis_results(prompt_text, prompt_id))
    
    def display_analysis_results(self, prompt_text, prompt_id):
        """Affiche les résultats de l'analyse"""
        # Analyser le prompt pour détecter les plateformes
        detected_platforms = self.detect_platforms(prompt_text)
        
        # Générer un texte d'analyse
        analysis_text = "Si j'ai bien compris, vous souhaitez:\n\n"
        
        if not detected_platforms:
            analysis_text += "Promouvoir votre contenu/produit sur les canaux marketing.\n\n"
            analysis_text += "Voici quelques options recommandées:"
        else:
            unique_platforms = list(set([p[1] for p in detected_platforms]))
            if len(unique_platforms) == 1:
                analysis_text += f"Utiliser la plateforme {unique_platforms[0].capitalize()} pour votre campagne.\n\n"
            else:
                analysis_text += f"Utiliser plusieurs plateformes ({', '.join([p.capitalize() for p in unique_platforms])}) pour votre campagne.\n\n"
            
            analysis_text += "Voici les actions spécifiques recommandées:"
        
        self.analysis_result.setText(analysis_text)
        
        # Mettre à jour la base de données avec les résultats
        self.cursor.execute('''
            UPDATE prompts 
            SET analysis_result = ?, actions = ?
            WHERE id = ?
        ''', (analysis_text, ','.join([p[1] for p in detected_platforms]), prompt_id))
        self.conn.commit()
        
        # Afficher les options
        self.show_relevant_options(detected_platforms)
        self.options_section.show()
        self.execute_button.show()
    
    def detect_platforms(self, prompt_text):
        """Détecte les plateformes pertinentes basées sur le prompt"""
        prompt_lower = prompt_text.lower()
        detected = []
        
        # Chercher dans la base de données des règles de correspondance
        self.cursor.execute('SELECT keyword, platform, response_template FROM detection_rules')
        rules = self.cursor.fetchall()
        
        for keyword, platform, template in rules:
            if keyword in prompt_lower:
                detected.append((keyword, platform, template))
        
        return detected
    
    def show_relevant_options(self, detected_platforms):
        """Affiche les options pertinentes selon l'analyse"""
        # Cacher toutes les options d'abord
        for button in self.button_group.buttons():
            button.hide()
        
        # Si aucune détection, montrer toutes les options
        if not detected_platforms:
            for button in self.button_group.buttons():
                button.show()
            return
        
        # Sinon, montrer seulement les options pertinentes
        platforms_to_show = list(set([p[1] for p in detected_platforms]))
        
        for button in self.button_group.buttons():
            button_text_lower = button.text().lower()
            for platform in platforms_to_show:
                if platform in button_text_lower:
                    button.show()
                    break
            else:
                # Pour le cas "multi" ou autres règles spéciales
                if "multi" in platforms_to_show:
                    button.show()
    
    def execute_action(self):
        """Exécute l'action sélectionnée"""
        selected_button = self.button_group.checkedButton()
        if not selected_button:
            return
        
        action = selected_button.text()
        
        # Enregistrer l'action dans la base de données (dans une vraie app, vous auriez une table séparée)
        self.cursor.execute('''
            INSERT INTO prompts (prompt_text, analysis_result, actions)
            VALUES (?, ?, ?)
        ''', (f"Action exécutée: {action}", "Action complétée", action))
        self.conn.commit()
        
        # Afficher un message de confirmation
        self.analysis_result.setText(
            self.analysis_result.text() + f"\n\n✔ Action exécutée: {action}\n"
            "L'opération a été réalisée avec succès."
        )
        
        # Cacher le bouton d'exécution
        self.execute_button.hide()
    
    def closeEvent(self, event):
        """Fermeture propre de l'application"""
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Définir une police moderne
    font = QFont()
    font.setFamily("Segoe UI")  # Ou une autre police moderne
    font.setPointSize(10)
    app.setFont(font)
    
    window = MarketingAIAnalyzer()
    window.show()
    sys.exit(app.exec_())