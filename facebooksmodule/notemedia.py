import sqlite3
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QTextEdit, QPushButton, QLabel, 
                            QFrame, QHeaderView, QAbstractItemView, QSizePolicy)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QLinearGradient, QPainter, QPen
from PyQt5.QtWidgets import QApplication

class GradientFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(4)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#667eea"))
        gradient.setColorAt(0.5, QColor("#764ba2"))
        gradient.setColorAt(1, QColor("#6B46C1"))
        painter.fillRect(event.rect(), gradient)

class ModernButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet('''
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5a67d8;
            }
            QPushButton:pressed {
                background-color: #4c51bf;
            }
        ''')

class MediaEditorModal(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_database()
        self.init_ui()
        self.setup_animations()
        self.load_data()
        
    def setup_database(self):
        """Initialise la base de données SQLite"""
        self.conn = sqlite3.connect('media_database.db')
        self.cursor = self.conn.cursor()
        
        # Créer la table si elle n'existe pas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS media_descriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                media_name TEXT NOT NULL,
                description TEXT NOT NULL,
                default_description TEXT,
                prompt TEXT
            )
        ''')
        self.conn.commit()
        
        # Insérer les médias initiaux si la table est vide
        self.cursor.execute('SELECT COUNT(*) FROM media_descriptions')
        if self.cursor.fetchone()[0] == 0:
            for i in range(1, 11):
                self.cursor.execute('''
                    INSERT INTO media_descriptions 
                    (media_name, description, default_description, prompt)
                    VALUES (?, ?, ?, ?)
                ''', (f"Media {i}", f"Description par défaut {i}", "", ""))
            self.conn.commit()

    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(950, 750)
        
        # Conteneur principal avec ombre
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("mainFrame")
        self.main_frame.setStyleSheet('''
            #mainFrame {
                background: #ffffff;
                border-radius: 14px;
                border: none;
                box-shadow: 0 12px 35px rgba(0, 0, 0, 0.25);
            }
        ''')
        
        # Layout principal
        main_layout = QVBoxLayout(self.main_frame)
        main_layout.setContentsMargins(25, 20, 25, 25)
        main_layout.setSpacing(20)
        
        # Barre de gradient
        self.gradient_bar = GradientFrame()
        
        # En-tête avec titre et bouton fermer
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(15)
        
        self.title_label = QLabel("ÉDITEUR DE MÉDIAS")
        self.title_label.setStyleSheet('''
            QLabel {
                font-size: 22px;
                font-weight: 700;
                color: #2d3748;
                letter-spacing: 1px;
                padding: 5px 0;
            }
        ''')
        
        # Bouton de fermeture iconique
        self.close_btn = QPushButton()
        self.close_btn.setIcon(QIcon.fromTheme("window-close"))
        self.close_btn.setFlat(True)
        self.close_btn.setFixedSize(36, 36)
        self.close_btn.setStyleSheet('''
            QPushButton {
                border-radius: 18px;
                background: transparent;
                padding: 8px;
            }
            QPushButton:hover {
                background: #fed7d7;
            }
            QPushButton:pressed {
                background: #feb2b2;
            }
        ''')
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.close_btn)
        
        # Tableau des médias
        self.media_table = QTableWidget(10, 2)
        self.media_table.setHorizontalHeaderLabels(["MÉDIA", "DESCRIPTION"])
        self.media_table.horizontalHeader().setStyleSheet('''
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 12px 15px;
                font-weight: 600;
                color: #4a5568;
                border: none;
                font-size: 13px;
                border-bottom: 2px solid #e2e8f0;
            }
        ''')
        self.media_table.verticalHeader().setVisible(False)
        self.media_table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.media_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.media_table.setStyleSheet('''
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                background-color: white;
                gridline-color: #edf2f7;
            }
            QTableWidget::item {
                padding: 12px 15px;
                border-bottom: 1px solid #edf2f7;
                font-size: 14px;
            }
            QTableWidget::item[column="0"] {
                background-color: #f8fafc;
                color: #4a5568;
                font-weight: 500;
            }
        ''')
        
        # Remplir le tableau
        for row in range(10):
            media_item = QTableWidgetItem(f"Media {row+1}")
            media_item.setFlags(media_item.flags() & ~Qt.ItemIsEditable)
            media_item.setBackground(QColor(248, 250, 252))
            self.media_table.setItem(row, 0, media_item)
            
            desc_item = QTableWidgetItem()
            desc_item.setFlags(desc_item.flags() | Qt.ItemIsEditable)
            self.media_table.setItem(row, 1, desc_item)
        
        self.media_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.media_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        
        # Zone Prompt et Description par défaut (côte à côte)
        text_edit_layout = QHBoxLayout()
        text_edit_layout.setSpacing(25)
        
        # Conteneur pour Prompt
        prompt_container = QFrame()
        prompt_container.setStyleSheet("QFrame { background: transparent; }")
        prompt_layout = QVBoxLayout(prompt_container)
        prompt_layout.setContentsMargins(0, 0, 0, 0)
        prompt_layout.setSpacing(8)
        
        self.prompt_label = QLabel("PROMPT")
        self.prompt_label.setStyleSheet('''
            QLabel {
                font-weight: 600;
                color: #4a5568;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                font-size: 13px;
                padding-bottom: 3px;
                border-bottom: 2px solid #e2e8f0;
            }
        ''')
        
        self.prompt_edit = QTextEdit()
        self.prompt_edit.setStyleSheet('''
            QTextEdit {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
                min-height: 120px;
                background: #ffffff;
            }
            QTextEdit:focus {
                border: 2px solid #667eea;
            }
        ''')
        self.prompt_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        prompt_layout.addWidget(self.prompt_label)
        prompt_layout.addWidget(self.prompt_edit)
        
        # Conteneur pour Description par défaut
        default_desc_container = QFrame()
        default_desc_container.setStyleSheet("QFrame { background: transparent; }")
        default_desc_layout = QVBoxLayout(default_desc_container)
        default_desc_layout.setContentsMargins(0, 0, 0, 0)
        default_desc_layout.setSpacing(8)
        
        self.default_desc_label = QLabel("DESCRIPTION PAR DÉFAUT")
        self.default_desc_label.setStyleSheet(self.prompt_label.styleSheet())
        
        self.default_desc_edit = QTextEdit()
        self.default_desc_edit.setStyleSheet(self.prompt_edit.styleSheet())
        self.default_desc_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        default_desc_layout.addWidget(self.default_desc_label)
        default_desc_layout.addWidget(self.default_desc_edit)
        
        text_edit_layout.addWidget(prompt_container)
        text_edit_layout.addWidget(default_desc_container)
        
        # Barre de boutons en bas
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setSpacing(15)
        button_layout.addStretch()
        
        # Bouton Fermer
        self.close_button = ModernButton("Fermer")
        self.close_button.setStyleSheet('''
            QPushButton {
                background-color: #e2e8f0;
                color: #4a5568;
            }
            QPushButton:hover {
                background-color: #cbd5e0;
            }
            QPushButton:pressed {
                background-color: #a0aec0;
            }
        ''')
        
        button_layout.addWidget(self.close_button)
        
        # Assemblage
        main_layout.addWidget(self.gradient_bar)
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.media_table, 1)
        main_layout.addLayout(text_edit_layout, 1)
        main_layout.addLayout(button_layout)
        
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.main_frame)
        
        # Connexions
        self.close_btn.clicked.connect(self.hide_modal)
        self.close_button.clicked.connect(self.hide_modal)
        self.media_table.cellChanged.connect(self.save_description)
        self.prompt_edit.textChanged.connect(self.save_prompt)
        self.default_desc_edit.textChanged.connect(self.save_default_description)
    
    def setup_animations(self):
        """Configure les animations d'ouverture/fermeture"""
        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(300)
        
        self.scale_anim = QPropertyAnimation(self.main_frame, b"geometry")
        self.scale_anim.setDuration(350)
        self.scale_anim.setEasingCurve(QEasingCurve.OutBack)
    
    def show_modal(self):
        """Affiche le modal avec animation"""
        # Position au centre de l'écran
        screen_geo = QApplication.desktop().screenGeometry()
        self.move(screen_geo.center() - self.rect().center())
        
        # Préparation animation
        self.setWindowOpacity(0)
        self.main_frame.setGeometry(0, 0, 10, 10)
        self.show()
        
        # Animation
        self.scale_anim.setStartValue(self.main_frame.geometry())
        self.scale_anim.setEndValue(self.main_frame.rect())
        self.opacity_anim.setStartValue(0)
        self.opacity_anim.setEndValue(1)
        
        self.scale_anim.start()
        self.opacity_anim.start()
    
    def hide_modal(self):
        """Ferme le modal avec animation"""
        self.scale_anim.setDirection(QPropertyAnimation.Backward)
        self.opacity_anim.setDirection(QPropertyAnimation.Backward)
        
        def on_finished():
            self.hide()
            self.scale_anim.setDirection(QPropertyAnimation.Forward)
            self.opacity_anim.setDirection(QPropertyAnimation.Forward)
        
        self.scale_anim.finished.connect(on_finished)
        self.scale_anim.start()
        self.opacity_anim.start()
    
    def load_data(self):
        """Charge les données depuis la base SQLite"""
        # Charger les descriptions
        self.cursor.execute('SELECT media_name, description FROM media_descriptions ORDER BY id')
        media_data = self.cursor.fetchall()
        
        for row, (media_name, description) in enumerate(media_data):
            if row < self.media_table.rowCount():
                self.media_table.item(row, 1).setText(description)
        
        # Charger le prompt
        self.cursor.execute('SELECT prompt FROM media_descriptions LIMIT 1')
        prompt_result = self.cursor.fetchone()
        if prompt_result:
            self.prompt_edit.setPlainText(prompt_result[0])
        
        # Charger la description par défaut
        self.cursor.execute('SELECT default_description FROM media_descriptions LIMIT 1')
        default_desc_result = self.cursor.fetchone()
        if default_desc_result:
            self.default_desc_edit.setPlainText(default_desc_result[0])
    
    def save_description(self, row, column):
        """Sauvegarde la description modifiée"""
        if column == 1:  # Seulement la colonne description
            media_name = self.media_table.item(row, 0).text()
            description = self.media_table.item(row, 1).text()
            
            self.cursor.execute('''
                UPDATE media_descriptions 
                SET description = ? 
                WHERE media_name = ?
            ''', (description, media_name))
            self.conn.commit()
    
    def save_prompt(self):
        """Sauvegarde le prompt"""
        prompt = self.prompt_edit.toPlainText()
        self.cursor.execute('UPDATE media_descriptions SET prompt = ?', (prompt,))
        self.conn.commit()
    
    def save_default_description(self):
        """Sauvegarde la description par défaut"""
        default_desc = self.default_desc_edit.toPlainText()
        self.cursor.execute('UPDATE media_descriptions SET default_description = ?', (default_desc,))
        self.conn.commit()
    
    def get_prompt(self):
        """Retourne le texte du prompt"""
        return self.prompt_edit.toPlainText()
    
    def get_default_description(self):
        """Retourne la description par défaut"""
        return self.default_desc_edit.toPlainText()
    
    def get_media_descriptions(self):
        """Retourne toutes les descriptions des médias"""
        descriptions = []
        for row in range(self.media_table.rowCount()):
            media_name = self.media_table.item(row, 0).text()
            description = self.media_table.item(row, 1).text()
            descriptions.append((media_name, description))
        return descriptions
    
    def closeEvent(self, event):
        """Ferme proprement la connexion à la base de données"""
        self.conn.close()
        super().closeEvent(event)