import sys
import sqlite3
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, 
                            QDateEdit, QStackedWidget, QListWidget, QListWidgetItem, 
                            QFileDialog, QMessageBox, QCheckBox, QSpinBox, QGroupBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QPixmap, QIcon

class AdCreatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assistant de Publication d'Ads - Simple & Complet")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QPushButton {
                background-color: #4a6fa5;
                color: white;
                border-radius: 5px;
                padding: 8px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #3a5a80;
            }
            QLineEdit, QTextEdit, QComboBox, QDateEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
            QLabel {
                color: #333;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
            }
        """)
        
        # Initialisation de la DB
        self.init_db()
        
        # Création de l'interface
        self.create_ui()
        
        # Charger les données existantes
        self.load_campaigns()
        
        # Démarrer avec le guide
        self.show_guide("Bienvenue dans l'Assistant de Publication d'Ads!\n\nSuivez les étapes pour créer et publier vos publicités facilement.")

    def init_db(self):
        """Initialise la base de données SQLite"""
        self.conn = sqlite3.connect('ads_manager.db')
        self.cursor = self.conn.cursor()
        
        # Table des campagnes
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            name TEXT,
            objective TEXT,
            audience TEXT,
            budget REAL,
            start_date TEXT,
            end_date TEXT,
            status TEXT DEFAULT 'Brouillon',
            created_at TEXT
        )
        ''')
        
        # Table des créatifs
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS creatives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            title TEXT,
            text TEXT,
            image_path TEXT,
            call_to_action TEXT,
            url TEXT,
            FOREIGN KEY(campaign_id) REFERENCES campaigns(id)
        )
        ''')
        
        # Table des étapes complétées
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS completed_steps (
            campaign_id INTEGER,
            step_name TEXT,
            completed BOOLEAN,
            PRIMARY KEY (campaign_id, step_name)
        )
        ''')
        
        self.conn.commit()

    def create_ui(self):
        """Crée l'interface utilisateur"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #e1e5eb;
                border: none;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #d1d5db;
            }
            QListWidget::item:selected {
                background-color: #4a6fa5;
                color: white;
            }
        """)
        main_layout.addWidget(self.sidebar)
        
        # Contenu principal
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack, 1)
        
        # Pages de l'application
        self.create_welcome_page()
        self.create_campaign_selection_page()
        self.create_platform_selection_page()
        self.create_objective_page()
        self.create_audience_page()
        self.create_budget_page()
        self.create_schedule_page()
        self.create_creative_page()
        self.create_review_page()
        self.create_publish_page()
        self.create_tracking_page()
        
        # Connecter la sidebar
        self.sidebar.currentRowChanged.connect(self.content_stack.setCurrentIndex)
        
        # Initialiser la sidebar
        self.update_sidebar()

    def update_sidebar(self, campaign_id=None):
        """Met à jour la sidebar en fonction de l'état actuel"""
        self.sidebar.clear()
        
        items = [
            "Accueil",
            "Sélection de campagne",
            "Plateforme",
            "Objectif",
            "Audience",
            "Budget",
            "Planning",
            "Créatifs",
            "Vérification",
            "Publication",
            "Suivi"
        ]
        
        for i, item in enumerate(items):
            list_item = QListWidgetItem(item)
            
            # Vérifier si les étapes sont complétées (si une campagne est sélectionnée)
            if campaign_id and i > 1:  # Les étapes après "Sélection de campagne"
                step_name = item.lower().replace(" ", "_")
                self.cursor.execute(
                    "SELECT completed FROM completed_steps WHERE campaign_id=? AND step_name=?",
                    (campaign_id, step_name)
                )
                result = self.cursor.fetchone()
                if result and result[0]:
                    list_item.setIcon(QIcon(":/icons/checked.png"))
                    list_item.setBackground(Qt.green)
            
            self.sidebar.addItem(list_item)

    def create_welcome_page(self):
        """Page d'accueil avec guide"""
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # Image/titre
        title = QLabel("Assistant de Publication d'Ads")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Image (remplacer par une vraie image si disponible)
        image_label = QLabel()
        image_label.setPixmap(QPixmap("ad_icon.png").scaled(200, 200, Qt.KeepAspectRatio))
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)
        
        # Guide
        self.guide_label = QLabel()
        self.guide_label.setWordWrap(True)
        self.guide_label.setFont(QFont("Arial", 12))
        self.guide_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.guide_label)
        
        # Boutons
        btn_layout = QHBoxLayout()
        
        new_campaign_btn = QPushButton("Nouvelle Campagne")
        new_campaign_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(1))
        btn_layout.addWidget(new_campaign_btn)
        
        load_campaign_btn = QPushButton("Charger Campagne Existante")
        load_campaign_btn.clicked.connect(self.load_existing_campaign)
        btn_layout.addWidget(load_campaign_btn)
        
        layout.addLayout(btn_layout)
        
        self.content_stack.addWidget(page)

    def show_guide(self, message):
        """Affiche un message dans le guide"""
        self.guide_label.setText(message)

    def create_campaign_selection_page(self):
        """Page de sélection/création de campagne"""
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # Titre
        title = QLabel("Gérer les Campagnes")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Liste des campagnes existantes
        self.campaign_list = QListWidget()
        self.campaign_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.campaign_list)
        
        # Boutons
        btn_layout = QHBoxLayout()
        
        new_btn = QPushButton("Nouvelle Campagne")
        new_btn.clicked.connect(self.create_new_campaign)
        btn_layout.addWidget(new_btn)
        
        load_btn = QPushButton("Charger Campagne")
        load_btn.clicked.connect(self.load_selected_campaign)
        btn_layout.addWidget(load_btn)
        
        delete_btn = QPushButton("Supprimer")
        delete_btn.clicked.connect(self.delete_campaign)
        btn_layout.addWidget(delete_btn)
        
        layout.addLayout(btn_layout)
        
        # Bouton retour
        back_btn = QPushButton("Retour à l'accueil")
        back_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(0))
        layout.addWidget(back_btn)
        
        self.content_stack.addWidget(page)

    def load_campaigns(self):
        """Charge la liste des campagnes"""
        self.campaign_list.clear()
        self.cursor.execute("SELECT id, name, platform, status FROM campaigns ORDER BY created_at DESC")
        campaigns = self.cursor.fetchall()
        
        for campaign in campaigns:
            item = QListWidgetItem(f"{campaign[0]} - {campaign[1]} ({campaign[2]}, {campaign[3]})")
            item.setData(Qt.UserRole, campaign[0])  # Stocker l'ID
            self.campaign_list.addItem(item)

    def create_new_campaign(self):
        """Crée une nouvelle campagne"""
        # Demander le nom de la campagne
        name, ok = QInputDialog.getText(
            self, "Nouvelle Campagne", 
            "Nommez votre nouvelle campagne:"
        )
        
        if ok and name:
            # Insérer dans la base de données
            self.cursor.execute(
                "INSERT INTO campaigns (name, created_at) VALUES (?, ?)",
                (name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            self.conn.commit()
            
            # Charger cette campagne
            campaign_id = self.cursor.lastrowid
            self.current_campaign_id = campaign_id
            self.load_campaigns()
            self.update_sidebar(campaign_id)
            self.content_stack.setCurrentIndex(2)  # Aller à la page Plateforme
            self.show_guide("Étape 1: Choisissez la plateforme pour votre campagne (ex: Facebook, Google Ads)")

    def load_selected_campaign(self):
        """Charge la campagne sélectionnée"""
        selected = self.campaign_list.currentItem()
        if selected:
            campaign_id = selected.data(Qt.UserRole)
            self.current_campaign_id = campaign_id
            self.update_sidebar(campaign_id)
            self.content_stack.setCurrentIndex(2)  # Aller à la page Plateforme
            self.show_guide(f"Campagne chargée. Vous pouvez continuer là où vous vous étiez arrêté.")

    def load_existing_campaign(self):
        """Charge une campagne existante depuis l'accueil"""
        self.content_stack.setCurrentIndex(1)  # Page de sélection
        self.show_guide("Sélectionnez une campagne existante ou créez-en une nouvelle")

    def delete_campaign(self):
        """Supprime la campagne sélectionnée"""
        selected = self.campaign_list.currentItem()
        if selected:
            reply = QMessageBox.question(
                self, 'Confirmation',
                'Voulez-vous vraiment supprimer cette campagne?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                campaign_id = selected.data(Qt.UserRole)
                self.cursor.execute("DELETE FROM campaigns WHERE id=?", (campaign_id,))
                self.cursor.execute("DELETE FROM creatives WHERE campaign_id=?", (campaign_id,))
                self.cursor.execute("DELETE FROM completed_steps WHERE campaign_id=?", (campaign_id,))
                self.conn.commit()
                self.load_campaigns()

    def create_platform_selection_page(self):
        """Page de sélection de plateforme"""
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # Titre
        title = QLabel("1. Choisissez une Plateforme")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Sur quelle plateforme souhaitez-vous publier votre publicité?")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)
        
        # Boutons de plateforme
        platforms = [
            ("Facebook Ads", "Icône pour Facebook"),
            ("Google Ads", "Icône pour Google Ads"),
            ("Instagram", "Icône pour Instagram"),
            ("LinkedIn", "Icône pour LinkedIn"),
            ("Twitter/X", "Icône pour Twitter")
        ]
        
        btn_layout = QVBoxLayout()
        
        for platform, icon in platforms:
            btn = QPushButton(platform)
            btn.setIcon(QIcon(icon))
            btn.setStyleSheet("text-align: left; padding: 15px;")
            btn.clicked.connect(lambda _, p=platform: self.select_platform(p))
            btn_layout.addWidget(btn)
        
        layout.addLayout(btn_layout)
        
        # Boutons de navigation
        nav_layout = QHBoxLayout()
        
        back_btn = QPushButton("Retour")
        back_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(1))
        nav_layout.addWidget(back_btn)
        
        layout.addLayout(nav_layout)
        
        self.content_stack.addWidget(page)

    def select_platform(self, platform):
        """Enregistre la plateforme sélectionnée"""
        if hasattr(self, 'current_campaign_id'):
            self.cursor.execute(
                "UPDATE campaigns SET platform=? WHERE id=?",
                (platform, self.current_campaign_id)
            )
            self.conn.commit()
            
            # Marquer l'étape comme complétée
            self.cursor.execute(
                "INSERT OR REPLACE INTO completed_steps VALUES (?, ?, ?)",
                (self.current_campaign_id, "plateforme", True)
            )
            self.conn.commit()
            
            self.update_sidebar(self.current_campaign_id)
            self.content_stack.setCurrentIndex(3)  # Aller à la page Objectif
            self.show_guide("Étape 2: Définissez l'objectif principal de votre campagne (ex: Ventes, Notoriété)")

    def create_objective_page(self):
        """Page de sélection d'objectif"""
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # Titre
        title = QLabel("2. Définissez l'Objectif")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Que souhaitez-vous accomplir avec cette campagne?")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)
        
        # Options d'objectif
        self.objective_combo = QComboBox()
        objectives = [
            "Augmenter les ventes",
            "Générer des leads",
            "Augmenter la notoriété",
            "Engagement (J'aime, partages)",
            "Trafic vers un site web",
            "Installations d'applications"
        ]
        self.objective_combo.addItems(objectives)
        layout.addWidget(self.objective_combo)
        
        # Explications pour chaque objectif
        self.objective_explanation = QLabel()
        self.objective_explanation.setWordWrap(True)
        self.objective_explanation.setStyleSheet("font-style: italic; color: #666;")
        layout.addWidget(self.objective_explanation)
        
        # Mettre à jour l'explication quand l'objectif change
        self.objective_combo.currentIndexChanged.connect(self.update_objective_explanation)
        self.update_objective_explanation(0)
        
        # Boutons de navigation
        nav_layout = QHBoxLayout()
        
        back_btn = QPushButton("Retour")
        back_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(2))
        nav_layout.addWidget(back_btn)
        
        next_btn = QPushButton("Suivant")
        next_btn.clicked.connect(self.save_objective)
        nav_layout.addWidget(next_btn)
        
        layout.addLayout(nav_layout)
        
        self.content_stack.addWidget(page)

    def update_objective_explanation(self, index):
        """Met à jour l'explication de l'objectif"""
        explanations = [
            "Idéal pour promouvoir des produits spécifiques et augmenter les conversions.",
            "Parfait pour collecter des informations sur des clients potentiels.",
            "Augmentez la visibilité de votre marque auprès d'une nouvelle audience.",
            "Encouragez les interactions avec votre contenu (commentaires, partages).",
            "Dirigez les gens vers votre site web ou une page spécifique.",
            "Incitez les utilisateurs à télécharger votre application mobile."
        ]
        self.objective_explanation.setText(explications[index])

    def save_objective(self):
        """Enregistre l'objectif sélectionné"""
        if hasattr(self, 'current_campaign_id'):
            objective = self.objective_combo.currentText()
            self.cursor.execute(
                "UPDATE campaigns SET objective=? WHERE id=?",
                (objective, self.current_campaign_id)
            )
            self.conn.commit()
            
            # Marquer l'étape comme complétée
            self.cursor.execute(
                "INSERT OR REPLACE INTO completed_steps VALUES (?, ?, ?)",
                (self.current_campaign_id, "objectif", True)
            )
            self.conn.commit()
            
            self.update_sidebar(self.current_campaign_id)
            self.content_stack.setCurrentIndex(4)  # Aller à la page Audience
            self.show_guide("Étape 3: Définissez votre audience cible (démographie, centres d'intérêt)")

    # ... (Les autres pages suivent le même modèle: audience, budget, planning, créatifs, etc.)

    def create_audience_page(self):
        """Page de définition de l'audience"""
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # Titre
        title = QLabel("3. Définissez Votre Audience")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Groupe Démographie
        demo_group = QGroupBox("Démographie")
        demo_layout = QVBoxLayout()
        
        # Âge
        age_layout = QHBoxLayout()
        age_layout.addWidget(QLabel("Âge:"))
        self.age_min = QSpinBox()
        self.age_min.setRange(13, 65)
        self.age_min.setValue(18)
        age_layout.addWidget(self.age_min)
        age_layout.addWidget(QLabel("à"))
        self.age_max = QSpinBox()
        self.age_max.setRange(18, 99)
        self.age_max.setValue(65)
        age_layout.addWidget(self.age_max)
        demo_layout.addLayout(age_layout)
        
        # Genre
        gender_layout = QHBoxLayout()
        gender_layout.addWidget(QLabel("Genre:"))
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Tous", "Hommes", "Femmes"])
        gender_layout.addWidget(self.gender_combo)
        demo_layout.addLayout(gender_layout)
        
        # Localisation
        location_layout = QHBoxLayout()
        location_layout.addWidget(QLabel("Localisation:"))
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Ex: France, Paris, etc.")
        location_layout.addWidget(self.location_input)
        demo_layout.addLayout(location_layout)
        
        demo_group.setLayout(demo_layout)
        layout.addWidget(demo_group)
        
        # Groupe Centres d'intérêt
        interest_group = QGroupBox("Centres d'intérêt")
        interest_layout = QVBoxLayout()
        
        self.interest_input = QLineEdit()
        self.interest_input.setPlaceholderText("Ex: Technologie, Cuisine, Voyage...")
        interest_layout.addWidget(self.interest_input)
        
        interest_group.setLayout(interest_layout)
        layout.addWidget(interest_group)
        
        # Boutons de navigation
        nav_layout = QHBoxLayout()
        
        back_btn = QPushButton("Retour")
        back_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(3))
        nav_layout.addWidget(back_btn)
        
        next_btn = QPushButton("Suivant")
        next_btn.clicked.connect(self.save_audience)
        nav_layout.addWidget(next_btn)
        
        layout.addLayout(nav_layout)
        
        self.content_stack.addWidget(page)

    def save_audience(self):
        """Enregistre les paramètres d'audience"""
        if hasattr(self, 'current_campaign_id'):
            audience = {
                "age_min": self.age_min.value(),
                "age_max": self.age_max.value(),
                "gender": self.gender_combo.currentText(),
                "location": self.location_input.text(),
                "interests": self.interest_input.text()
            }
            
            self.cursor.execute(
                "UPDATE campaigns SET audience=? WHERE id=?",
                (str(audience), self.current_campaign_id)
            )
            self.conn.commit()
            
            # Marquer l'étape comme complétée
            self.cursor.execute(
                "INSERT OR REPLACE INTO completed_steps VALUES (?, ?, ?)",
                (self.current_campaign_id, "audience", True)
            )
            self.conn.commit()
            
            self.update_sidebar(self.current_campaign_id)
            self.content_stack.setCurrentIndex(5)  # Aller à la page Budget
            self.show_guide("Étape 4: Définissez votre budget quotidien ou total pour la campagne")

    # ... (Les autres méthodes pour budget, planning, créatifs, etc.)

    def create_budget_page(self):
        """Page de définition du budget"""
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # Titre
        title = QLabel("4. Définissez Votre Budget")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Type de budget
        budget_type_group = QGroupBox("Type de Budget")
        budget_type_layout = QHBoxLayout()
        
        self.budget_type_combo = QComboBox()
        self.budget_type_combo.addItems(["Budget quotidien", "Budget total"])
        budget_type_layout.addWidget(self.budget_type_combo)
        
        budget_type_group.setLayout(budget_type_layout)
        layout.addWidget(budget_type_group)
        
        # Montant
        amount_group = QGroupBox("Montant")
        amount_layout = QHBoxLayout()
        
        amount_layout.addWidget(QLabel("Montant:"))
        self.budget_amount = QSpinBox()
        self.budget_amount.setRange(1, 100000)
        self.budget_amount.setValue(50)
        self.budget_amount.setPrefix("$ ")
        amount_layout.addWidget(self.budget_amount)
        
        amount_group.setLayout(amount_layout)
        layout.addWidget(amount_group)
        
        # Estimation de portée
        self.reach_estimate = QLabel("Estimation de portée: 1 000 - 2 000 personnes")
        self.reach_estimate.setAlignment(Qt.AlignCenter)
        self.reach_estimate.setStyleSheet("font-style: italic; color: #666;")
        layout.addWidget(self.reach_estimate)
        
        # Boutons de navigation
        nav_layout = QHBoxLayout()
        
        back_btn = QPushButton("Retour")
        back_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(4))
        nav_layout.addWidget(back_btn)
        
        next_btn = QPushButton("Suivant")
        next_btn.clicked.connect(self.save_budget)
        nav_layout.addWidget(next_btn)
        
        layout.addLayout(nav_layout)
        
        self.content_stack.addWidget(page)

    def save_budget(self):
        """Enregistre le budget"""
        if hasattr(self, 'current_campaign_id'):
            budget = self.budget_amount.value()
            self.cursor.execute(
                "UPDATE campaigns SET budget=? WHERE id=?",
                (budget, self.current_campaign_id)
            )
            self.conn.commit()
            
            # Marquer l'étape comme complétée
            self.cursor.execute(
                "INSERT OR REPLACE INTO completed_steps VALUES (?, ?, ?)",
                (self.current_campaign_id, "budget", True)
            )
            self.conn.commit()
            
            self.update_sidebar(self.current_campaign_id)
            self.content_stack.setCurrentIndex(6)  # Aller à la page Planning
            self.show_guide("Étape 5: Planifiez les dates de début et fin de votre campagne")

    def create_schedule_page(self):
        """Page de planification des dates"""
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # Titre
        title = QLabel("5. Planifiez Votre Campagne")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Dates
        dates_group = QGroupBox("Dates de la Campagne")
        dates_layout = QVBoxLayout()
        
        # Date de début
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Date de début:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setCalendarPopup(True)
        start_layout.addWidget(self.start_date)
        dates_layout.addLayout(start_layout)
        
        # Date de fin
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("Date de fin:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate().addDays(7))
        self.end_date.setCalendarPopup(True)
        end_layout.addWidget(self.end_date)
        dates_layout.addLayout(end_layout)
        
        dates_group.setLayout(dates_layout)
        layout.addWidget(dates_group)
        
        # Options de planning
        options_group = QGroupBox("Options de Planning")
        options_layout = QVBoxLayout()
        
        self.run_continuously = QCheckBox("Exécuter continuellement (pas de date de fin")
        options_layout.addWidget(self.run_continuously)
        
        self.pause_campaign = QCheckBox("Mettre en pause après approbation")
        options_layout.addWidget(self.pause_campaign)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Boutons de navigation
        nav_layout = QHBoxLayout()
        
        back_btn = QPushButton("Retour")
        back_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(5))
        nav_layout.addWidget(back_btn)
        
        next_btn = QPushButton("Suivant")
        next_btn.clicked.connect(self.save_schedule)
        nav_layout.addWidget(next_btn)
        
        layout.addLayout(nav_layout)
        
        self.content_stack.addWidget(page)

    def save_schedule(self):
        """Enregistre le planning"""
        if hasattr(self, 'current_campaign_id'):
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = "" if self.run_continuously.isChecked() else self.end_date.date().toString("yyyy-MM-dd")
            
            self.cursor.execute(
                "UPDATE campaigns SET start_date=?, end_date=? WHERE id=?",
                (start_date, end_date, self.current_campaign_id)
            )
            self.conn.commit()
            
            # Marquer l'étape comme complétée
            self.cursor.execute(
                "INSERT OR REPLACE INTO completed_steps VALUES (?, ?, ?)",
                (self.current_campaign_id, "planning", True)
            )
            self.conn.commit()
            
            self.update_sidebar(self.current_campaign_id)
            self.content_stack.setCurrentIndex(7)  # Aller à la page Créatifs
            self.show_guide("Étape 6: Créez vos visuels et textes publicitaires")

    def create_creative_page(self):
        """Page de création des créatifs"""
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # Titre
        title = QLabel("6. Créez Vos Créatifs")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Onglets pour différents types de créatifs
        self.creative_tabs = QTabWidget()
        
        # Onglet Image
        self.create_image_tab()
        
        # Onglet Vidéo
        self.create_video_tab()
        
        # Onglet Carrousel
        self.create_carousel_tab()
        
        layout.addWidget(self.creative_tabs)
        
        # Boutons de navigation
        nav_layout = QHBoxLayout()
        
        back_btn = QPushButton("Retour")
        back_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(6))
        nav_layout.addWidget(back_btn)
        
        next_btn = QPushButton("Suivant")
        next_btn.clicked.connect(self.save_creative)
        nav_layout.addWidget(next_btn)
        
        layout.addLayout(nav_layout)
        
        self.content_stack.addWidget(page)

    def create_image_tab(self):
        """Onglet pour les créatifs image"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Titre
        title = QLabel("Publicité avec Image")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Ajouter une image
        self.image_btn = QPushButton("Ajouter une Image")
        self.image_btn.clicked.connect(self.add_image)
        layout.addWidget(self.image_btn)
        
        # Aperçu de l'image
        self.image_preview = QLabel()
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setFixedSize(300, 300)
        self.image_preview.setStyleSheet("border: 1px dashed #ccc;")
        layout.addWidget(self.image_preview)
        
        # Texte principal
        layout.addWidget(QLabel("Texte Principal:"))
        self.primary_text = QTextEdit()
        self.primary_text.setPlaceholderText("Écrivez le message principal de votre publicité...")
        layout.addWidget(self.primary_text)
        
        # Titre
        layout.addWidget(QLabel("Titre:"))
        self.headline = QLineEdit()
        self.headline.setPlaceholderText("Titre accrocheur (max 25 caractères)"))
        layout.addWidget(self.headline)
        
        # Description
        layout.addWidget(QLabel("Description:"))
        self.description = QLineEdit()
        self.description.setPlaceholderText("Description courte (max 30 caractères)"))
        layout.addWidget(self.description)
        
        # Appel à l'action
        layout.addWidget(QLabel("Appel à l'action:"))
        self.cta_combo = QComboBox()
        self.cta_combo.addItems([
            "Acheter maintenant", 
            "En savoir plus", 
            "Inscrivez-vous", 
            "Télécharger",
            "Contactez-nous"
        ])
        layout.addWidget(self.cta_combo)
        
        # URL
        layout.addWidget(QLabel("URL de destination:"))
        self.destination_url = QLineEdit()
        self.destination_url.setPlaceholderText("https://www.example.com")
        layout.addWidget(self.destination_url)
        
        self.creative_tabs.addTab(tab, "Image")

    def add_image(self):
        """Ajoute une image au créatif"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner une image", 
            "", "Images (*.png *.jpg *.jpeg *.gif)"
        )
        
        if file_path:
            pixmap = QPixmap(file_path)
            self.image_preview.setPixmap(pixmap.scaled(
                self.image_preview.width(), 
                self.image_preview.height(),
                Qt.KeepAspectRatio
            ))
            self.current_image_path = file_path

    def create_video_tab(self):
        """Onglet pour les créatifs vidéo"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Titre
        title = QLabel("Publicité avec Vidéo")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Ajouter une vidéo
        self.video_btn = QPushButton("Ajouter une Vidéo")
        self.video_btn.clicked.connect(self.add_video)
        layout.addWidget(self.video_btn)
        
        # Aperçu vidéo (juste une vignette dans cette version simplifiée)
        self.video_preview = QLabel("Aperçu vidéo apparaîtra ici")
        self.video_preview.setAlignment(Qt.AlignCenter)
        self.video_preview.setFixedSize(300, 300)
        self.video_preview.setStyleSheet("border: 1px dashed #ccc;")
        layout.addWidget(self.video_preview)
        
        # Texte principal
        layout.addWidget(QLabel("Texte Principal:"))
        self.video_primary_text = QTextEdit()
        self.video_primary_text.setPlaceholderText("Écrivez le message principal de votre publicité...")
        layout.addWidget(self.video_primary_text)
        
        self.creative_tabs.addTab(tab, "Vidéo")

    def add_video(self):
        """Ajoute une vidéo au créatif"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner une vidéo", 
            "", "Vidéos (*.mp4 *.mov *.avi)"
        )
        
        if file_path:
            # Dans une vraie application, vous pourriez charger une vignette
            self.video_preview.setText(f"Vidéo sélectionnée:\n{file_path}")
            self.current_video_path = file_path

    def create_carousel_tab(self):
        """Onglet pour les créatifs carrousel"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Titre
        title = QLabel("Publicité Carrousel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Ajouter des images
        self.add_carousel_btn = QPushButton("Ajouter des Images au Carrousel")
        self.add_carousel_btn.clicked.connect(self.add_carousel_images)
        layout.addWidget(self.add_carousel_btn)
        
        # Liste des images
        self.carousel_list = QListWidget()
        layout.addWidget(self.carousel_list)
        
        # Texte principal
        layout.addWidget(QLabel("Texte Principal:"))
        self.carousel_primary_text = QTextEdit()
        self.carousel_primary_text.setPlaceholderText("Écrivez le message principal de votre publicité...")
        layout.addWidget(self.carousel_primary_text)
        
        self.creative_tabs.addTab(tab, "Carrousel")

    def add_carousel_images(self):
        """Ajoute des images à un carrousel"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Sélectionner des images", 
            "", "Images (*.png *.jpg *.jpeg *.gif)"
        )
        
        if file_paths:
            self.carousel_list.clear()
            for path in file_paths:
                self.carousel_list.addItem(path)
            self.current_carousel_paths = file_paths

    def save_creative(self):
        """Enregistre le créatif"""
        if hasattr(self, 'current_campaign_id'):
            creative_type = self.creative_tabs.tabText(self.creative_tabs.currentIndex())
            
            if creative_type == "Image":
                primary_text = self.primary_text.toPlainText()
                headline = self.headline.text()
                description = self.description.text()
                cta = self.cta_combo.currentText()
                url = self.destination_url.text()
                
                if hasattr(self, 'current_image_path'):
                    self.cursor.execute(
                        "INSERT INTO creatives (campaign_id, title, text, image_path, call_to_action, url) VALUES (?, ?, ?, ?, ?, ?)",
                        (self.current_campaign_id, headline, primary_text, self.current_image_path, cta, url)
                    )
                    self.conn.commit()
            
            # Marquer l'étape comme complétée
            self.cursor.execute(
                "INSERT OR REPLACE INTO completed_steps VALUES (?, ?, ?)",
                (self.current_campaign_id, "créatifs", True)
            )
            self.conn.commit()
            
            self.update_sidebar(self.current_campaign_id)
            self.content_stack.setCurrentIndex(8)  # Aller à la page Vérification
            self.show_guide("Étape 7: Vérifiez tous les détails avant publication")

    def create_review_page(self):
        """Page de vérification avant publication"""
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # Titre
        title = QLabel("7. Vérifiez Votre Campagne")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Résumé de la campagne
        self.review_summary = QTextEdit()
        self.review_summary.setReadOnly(True)
        layout.addWidget(self.review_summary)
        
        # Boutons de navigation
        nav_layout = QHBoxLayout()
        
        back_btn = QPushButton("Retour")
        back_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(7))
        nav_layout.addWidget(back_btn)
        
        publish_btn = QPushButton("Publier Maintenant")
        publish_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(9))
        nav_layout.addWidget(publish_btn)
        
        schedule_btn = QPushButton("Planifier Plus Tard")
        schedule_btn.clicked.connect(self.schedule_for_later)
        nav_layout.addWidget(schedule_btn)
        
        layout.addLayout(nav_layout)
        
        self.content_stack.addWidget(page)

    def update_review_summary(self):
        """Met à jour le résumé de la campagne"""
        if hasattr(self, 'current_campaign_id'):
            self.cursor.execute("SELECT * FROM campaigns WHERE id=?", (self.current_campaign_id,))
            campaign = self.cursor.fetchone()
            
            self.cursor.execute("SELECT * FROM creatives WHERE campaign_id=?", (self.current_campaign_id,))
            creatives = self.cursor.fetchall()
            
            summary = f"""
            <h2>Résumé de la Campagne</h2>
            <p><b>Nom:</b> {campaign[2]}</p>
            <p><b>Plateforme:</b> {campaign[1]}</p>
            <p><b>Objectif:</b> {campaign[3]}</p>
            <p><b>Budget:</b> ${campaign[5]} ({'Quotidien' if campaign[5] < 100 else 'Total'})</p>
            <p><b>Dates:</b> Du {campaign[6]} au {campaign[7] or 'Indéfinie'}</p>
            
            <h3>Créatifs</h3>
            """
            
            for creative in creatives:
                summary += f"""
                <p><b>Titre:</b> {creative[2]}</p>
                <p><b>Texte:</b> {creative[3]}</p>
                <p><b>Image:</b> {creative[4] or 'Aucune'}</p>
                <p><b>Vidéo:</b> {creative[5] or 'Aucune'}</p>
                <p><b>CTA:</b> {creative[6]}</p>
                <p><b>URL:</b> {creative[7]}</p>
                <hr>
                """
            
            self.review_summary.setHtml(summary)

    def schedule_for_later(self):
        """Planifie la campagne pour plus tard"""
        QMessageBox.information(
            self, "Campagne Planifiée",
            "Votre campagne a été enregistrée et pourra être publiée plus tard."
        )
        self.content_stack.setCurrentIndex(0)  # Retour à l'accueil

    def create_publish_page(self):
        """Page de publication"""
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # Titre
        title = QLabel("8. Publier Votre Campagne")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Statut de publication
        self.publish_status = QLabel()
        self.publish_status.setAlignment(Qt.AlignCenter)
        self.publish_status.setWordWrap(True)
        layout.addWidget(self.publish_status)
        
        # Bouton de publication
        self.publish_btn = QPushButton("Publier sur la Plateforme")
        self.publish_btn.clicked.connect(self.publish_campaign)
        layout.addWidget(self.publish_btn)
        
        # Bouton suivant
        next_btn = QPushButton("Suivre les Résultats")
        next_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(10))
        layout.addWidget(next_btn)
        
        self.content_stack.addWidget(page)

    def publish_campaign(self):
        """Publie la campagne (simulation)"""
        if hasattr(self, 'current_campaign_id'):
            self.publish_status.setText("Publication en cours...")
            self.publish_btn.setEnabled(False)
            
            # Simuler un délai de publication
            import time
            time.sleep(2)
            
            # Mettre à jour le statut dans la base de données
            self.cursor.execute(
                "UPDATE campaigns SET status='Publiée' WHERE id=?",
                (self.current_campaign_id,)
            )
            self.conn.commit()
            
            # Marquer l'étape comme complétée
            self.cursor.execute(
                "INSERT OR REPLACE INTO completed_steps VALUES (?, ?, ?)",
                (self.current_campaign_id, "publication", True)
            )
            self.conn.commit()
            
            self.publish_status.setText(
                "Votre campagne a été publiée avec succès!\n\n"
                "Vous pouvez maintenant suivre ses performances."
            )
            
            self.update_sidebar(self.current_campaign_id)

    def create_tracking_page(self):
        """Page de suivi des résultats"""
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # Titre
        title = QLabel("Suivi des Résultats")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Statistiques (simulées)
        stats_group = QGroupBox("Statistiques de la Campagne")
        stats_layout = QVBoxLayout()
        
        # Métriques
        metrics = [
            ("Portée", "1,245 personnes"),
            ("Impressions", "3,567"),
            ("Clics", "189"),
            ("CTR", "5.3%"),
            ("Coût par clic", "$0.42"),
            ("Montant dépensé", "$79.38")
        ]
        
        for metric, value in metrics:
            metric_layout = QHBoxLayout()
            metric_layout.addWidget(QLabel(f"{metric}:"))
            metric_layout.addWidget(QLabel(value))
            metric_layout.addStretch()
            stats_layout.addLayout(metric_layout)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Graphique (simulé)
        graph_label = QLabel("[Graphique des performances apparaîtrait ici]")
        graph_label.setAlignment(Qt.AlignCenter)
        graph_label.setStyleSheet("border: 1px solid #ccc; padding: 50px;")
        layout.addWidget(graph_label)
        
        # Bouton de retour
        back_btn = QPushButton("Retour à l'accueil")
        back_btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(0))
        layout.addWidget(back_btn)
        
        self.content_stack.addWidget(page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdCreatorApp()
    window.show()
    sys.exit(app.exec_())