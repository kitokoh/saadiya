from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QWidget, QStackedWidget, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from  demarrage.baseDialog import BaseDialog

from PyQt5.QtWidgets import QProgressBar

class TutorialDialog(BaseDialog):
    def init_ui(self):
        # Configuration de base
        self.setWindowTitle("Bienvenue dans Léopardo AI")
        self.setMinimumSize(800, 600)
        
        # Style général
        self.setStyleSheet("""
            TutorialDialog {
                background-color: #ffffff;
                border-radius: 12px;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
            QLabel#step_title {
                font-size: 18px;
                font-weight: 600;
                color: #4a6fa5;
                margin-bottom: 5px;
            }
            QPushButton {
                background-color: #4a6fa5;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #3a5a80;
            }
            QPushButton#secondary {
                background-color: #e1e5eb;
                color: #2c3e50;
            }
            QPushButton#secondary:hover {
                background-color: #d1d5db;
            }
            QProgressBar {
                border: 1px solid #dcdcdc;
                border-radius: 6px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4a6fa5;
                border-radius: 5px;
            }
        """)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header avec logo et titre
        header = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.logo = QLabel()
        self.logo.setPixmap(QIcon(":/icons/leopardo_logo.png").pixmap(64, 64))
        self.logo.setAlignment(Qt.AlignLeft)
        
        self.title = QLabel("Bienvenue dans Léopardo AI")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignLeft)
        
        header_layout.addWidget(self.logo)
        header_layout.addWidget(self.title)
        header_layout.addStretch()
        header.setLayout(header_layout)
        
        # Contenu avec système d'étapes
        self.stacked_widget = QStackedWidget()
        
        # Création des étapes du tutoriel
        self.create_welcome_step()
        self.create_features_step()
        self.create_publication_step()
        self.create_prospection_step()
        self.create_final_step()
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 4)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        
        # Contrôles de navigation
        controls = QWidget()
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(0, 0, 0, 0)
        
        self.back_btn = QPushButton("Retour")
        self.back_btn.setObjectName("secondary")
        self.back_btn.setIcon(QIcon(":/icons/arrow_left.png"))
        self.back_btn.setEnabled(False)
        self.back_btn.clicked.connect(self.previous_step)
        
        self.next_btn = QPushButton("Suivant")
        self.next_btn.setIcon(QIcon(":/icons/arrow_right.png"))
        self.next_btn.clicked.connect(self.next_step)
        
        self.skip_btn = QPushButton("Passer le tutoriel")
        self.skip_btn.setObjectName("secondary")
        self.skip_btn.clicked.connect(self.reject)
        
        controls_layout.addWidget(self.skip_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(self.back_btn)
        controls_layout.addWidget(self.next_btn)
        controls.setLayout(controls_layout)
        
        # Ajout des éléments au layout principal
        main_layout.addWidget(header)
        main_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(controls)
        
        self.setLayout(main_layout)
        
        # Animation d'entrée
        self.fade_in_animation()
    
    def fade_in_animation(self):
        """Animation de fondu à l'ouverture"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
    
    def create_welcome_step(self):
        """Étape 1: Message de bienvenue"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("Découvrez Léopardo AI")
        title.setObjectName("step_title")
        
        content = QLabel(
            "Nous sommes ravis de vous accueillir dans Léopardo AI, votre assistant "
            "complet pour le marketing digital.\n\n"
            "Ce tutoriel rapide vous présentera les principales fonctionnalités "
            "pour vous aider à démarrer en quelques minutes."
        )
        content.setWordWrap(True)
        
        image = QLabel()
        image.setPixmap(QPixmap(":/images/welcome_tutorial.png"))
        image.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(content)
        layout.addWidget(image)
        layout.addStretch()
        
        widget.setLayout(layout)
        self.stacked_widget.addWidget(widget)
    
    def create_features_step(self):
        """Étape 2: Présentation des fonctionnalités"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("Fonctionnalités clés")
        title.setObjectName("step_title")
        
        features = [
            ("Planification", "Planifiez vos publications sur les réseaux sociaux à l'avance"),
            ("Bibliothèque", "Centralisez vos médias et descriptions marketing"),
            ("Prospection", "Suivez vos leads avant qu'ils ne deviennent clients"),
            ("Publication assistée", "Automatisez vos publications répétitives")
        ]
        
        for icon_name, text in features:
            feature_layout = QHBoxLayout()
            feature_layout.setSpacing(15)
            
            icon = QLabel()
            icon.setPixmap(QIcon(f":/icons/{icon_name.lower()}.png").pixmap(32, 32))
            
            label = QLabel(text)
            label.setWordWrap(True)
            
            feature_layout.addWidget(icon)
            feature_layout.addWidget(label)
            feature_layout.addStretch()
            
            layout.addLayout(feature_layout)
        
        layout.addStretch()
        widget.setLayout(layout)
        self.stacked_widget.addWidget(widget)
    
    def create_publication_step(self):
        """Étape 3: Démo publication"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("Planification de publications")
        title.setObjectName("step_title")
        
        content = QLabel(
            "Planifiez vos publications en quelques clics:\n\n"
            "1. Sélectionnez vos médias\n"
            "2. Rédigez ou choisissez une description\n"
            "3. Définissez la date et l'heure\n"
            "4. Activez la répétition si nécessaire"
        )
        content.setWordWrap(True)
        
        demo_image = QLabel()
        demo_image.setPixmap(QPixmap(":/images/demo_publication.png"))
        demo_image.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(content)
        layout.addWidget(demo_image)
        layout.addStretch()
        
        widget.setLayout(layout)
        self.stacked_widget.addWidget(widget)
    
    def create_prospection_step(self):
        """Étape 4: Module prospection"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("Gestion des prospects")
        title.setObjectName("step_title")
        
        content = QLabel(
            "Le module prospection vous permet de:\n\n"
            "• Enregistrer les détails des prospects\n"
            "• Suivre leurs besoins spécifiques\n"
            "• Définir des échéances de suivi\n"
            "• Convertir en clients facilement"
        )
        content.setWordWrap(True)
        
        tips = QLabel(
            "<b>Astuce:</b> Utilisez les tags pour organiser vos prospects "
            "par secteur d'activité ou potentiel."
        )
        tips.setWordWrap(True)
        tips.setStyleSheet("color: #4a6fa5; font-style: italic;")
        
        layout.addWidget(title)
        layout.addWidget(content)
        layout.addWidget(tips)
        layout.addStretch()
        
        widget.setLayout(layout)
        self.stacked_widget.addWidget(widget)
    
    def create_final_step(self):
        """Étape finale"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title = QLabel("Vous êtes prêt!")
        title.setObjectName("step_title")
        title.setAlignment(Qt.AlignCenter)
        
        content = QLabel(
            "Vous maîtrisez maintenant les bases de Léopardo AI.\n\n"
            "N'hésitez pas à explorer les différents modules à votre rythme. "
            "Vous pouvez toujours accéder à ce tutoriel depuis le menu Aide."
        )
        content.setWordWrap(True)
        content.setAlignment(Qt.AlignCenter)
        
        start_btn = QPushButton("Commencer à utiliser Léopardo AI")
        start_btn.clicked.connect(self.accept)
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                font-size: 16px;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #219955;
            }
        """)
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(content)
        layout.addWidget(start_btn, 0, Qt.AlignCenter)
        layout.addStretch()
        
        widget.setLayout(layout)
        self.stacked_widget.addWidget(widget)
    
    def next_step(self):
        """Passe à l'étape suivante"""
        current = self.stacked_widget.currentIndex()
        if current < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(current + 1)
            self.update_navigation()
    
    def previous_step(self):
        """Retourne à l'étape précédente"""
        current = self.stacked_widget.currentIndex()
        if current > 0:
            self.stacked_widget.setCurrentIndex(current - 1)
            self.update_navigation()
    
    def update_navigation(self):
        """Met à jour les boutons de navigation et la barre de progression"""
        current = self.stacked_widget.currentIndex()
        max_step = self.stacked_widget.count() - 1
        
        # Boutons précédent/suivant
        self.back_btn.setEnabled(current > 0)
        
        if current < max_step:
            self.next_btn.setText("Suivant")
            self.next_btn.setIcon(QIcon(":/icons/arrow_right.png"))
        else:
            self.next_btn.setText("Terminer")
            self.next_btn.setIcon(QIcon())
            self.next_btn.clicked.disconnect()
            self.next_btn.clicked.connect(self.accept)
        
        # Barre de progression
        self.progress_bar.setValue(current)
        
        # Bouton Passer
        self.skip_btn.setVisible(current < max_step)