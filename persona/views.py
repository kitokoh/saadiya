from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QListWidget, QListWidgetItem, QLabel, QLineEdit, QTextEdit,
    QSpinBox, QComboBox, QPushButton, QFormLayout, QSplitter,
    QMessageBox, QInputDialog, QFileDialog, QToolBar, QStatusBar,
    QApplication, QDialog, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction
from models import Persona, Goal, PainPoint, Behavior, Quote, Scenario
import resources_rc  # Fichier de ressources généré par pyrcc5

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Persona Designer")
        self.setMinimumSize(1024, 768)
        
        # Création des composants principaux
        self._create_actions()
        self._create_menu_bar()
        self._create_tool_bar()
        self._create_status_bar()
        self._create_central_widget()
        
        # Initialisation de la base de données
        from database import DatabaseManager
        self.db = DatabaseManager()
        self.db.database_updated.connect(self._refresh_personas_list)
        
        # Charger les personas
        self._refresh_personas_list()
    
    def _create_actions(self):
        # Action Nouveau Persona
        self.new_persona_action = QAction(QIcon(":/icons/add.png"), "&Nouveau Persona", self)
        self.new_persona_action.setShortcut("Ctrl+N")
        self.new_persona_action.setStatusTip("Créer un nouveau persona")
        self.new_persona_action.triggered.connect(self._create_new_persona)
        
        # Action Supprimer Persona
        self.delete_persona_action = QAction(QIcon(":/icons/delete.png"), "&Supprimer", self)
        self.delete_persona_action.setShortcut("Del")
        self.delete_persona_action.setStatusTip("Supprimer le persona sélectionné")
        self.delete_persona_action.triggered.connect(self._delete_current_persona)
        
        # Action Exporter
        self.export_action = QAction(QIcon(":/icons/export.png"), "&Exporter...", self)
        self.export_action.setStatusTip("Exporter le persona")
        self.export_action.triggered.connect(self._export_persona)
        
        # Action Importer
        self.import_action = QAction(QIcon(":/icons/import.png"), "&Importer...", self)
        self.import_action.setStatusTip("Importer un persona")
        self.import_action.triggered.connect(self._import_persona)
        
        # Action Quitter
        self.quit_action = QAction("&Quitter", self)
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.setStatusTip("Quitter l'application")
        self.quit_action.triggered.connect(self.close)
    
    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        
        # Menu Fichier
        file_menu = menu_bar.addMenu("&Fichier")
        file_menu.addAction(self.new_persona_action)
        file_menu.addAction(self.export_action)
        file_menu.addAction(self.import_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)
        
        # Menu Edition
        edit_menu = menu_bar.addMenu("&Edition")
        edit_menu.addAction(self.delete_persona_action)
    
    def _create_tool_bar(self):
        tool_bar = self.addToolBar("Outils")
        tool_bar.setIconSize(QSize(24, 24))
        tool_bar.addAction(self.new_persona_action)
        tool_bar.addAction(self.delete_persona_action)
        tool_bar.addSeparator()
        tool_bar.addAction(self.export_action)
        tool_bar.addAction(self.import_action)
    
    def _create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt")
    
    def _create_central_widget(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter pour la liste des personas et les détails
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Liste des personas
        self.personas_list = QListWidget()
        self.personas_list.setMaximumWidth(250)
        self.personas_list.itemSelectionChanged.connect(self._display_persona_details)
        splitter.addWidget(self.personas_list)
        
        # Zone de détails avec onglets
        self.details_tabs = QTabWidget()
        self._setup_details_tabs()
        splitter.addWidget(self.details_tabs)
        
        splitter.setStretchFactor(1, 1)
        main_layout.addWidget(splitter)
    
    def _setup_details_tabs(self):
        # Onglet Informations de base
        self.basic_info_tab = QWidget()
        self._setup_basic_info_tab()
        self.details_tabs.addTab(self.basic_info_tab, "Informations")
        
        # Onglet Objectifs
        self.goals_tab = QWidget()
        self._setup_goals_tab()
        self.details_tabs.addTab(self.goals_tab, "Objectifs")
        
        # Onglet Points de douleur
        self.pain_points_tab = QWidget()
        self._setup_pain_points_tab()
        self.details_tabs.addTab(self.pain_points_tab, "Points de douleur")
        
        # Onglet Comportements
        self.behaviors_tab = QWidget()
        self._setup_behaviors_tab()
        self.details_tabs.addTab(self.behaviors_tab, "Comportements")
        
        # Onglet Citations
        self.quotes_tab = QWidget()
        self._setup_quotes_tab()
        self.details_tabs.addTab(self.quotes_tab, "Citations")
        
        # Onglet Scénarios
        self.scenarios_tab = QWidget()
        self._setup_scenarios_tab()
        self.details_tabs.addTab(self.scenarios_tab, "Scénarios")
    
    def _setup_basic_info_tab(self):
        layout = QFormLayout(self.basic_info_tab)
        
        self.name_edit = QLineEdit()
        self.role_edit = QLineEdit()
        self.age_spin = QSpinBox()
        self.age_spin.setRange(0, 120)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["", "Homme", "Femme", "Non-binaire", "Autre"])
        self.location_edit = QLineEdit()
        self.education_combo = QComboBox()
        self.education_combo.addItems([
            "", "Primaire", "Secondaire", "Baccalauréat", 
            "Licence", "Master", "Doctorat", "Autre"
        ])
        self.income_combo = QComboBox()
        self.income_combo.addItems([
            "", "Faible", "Moyen", "Élevé", "Très élevé"
        ])
        
        layout.addRow("Nom:", self.name_edit)
        layout.addRow("Rôle:", self.role_edit)
        layout.addRow("Âge:", self.age_spin)
        layout.addRow("Genre:", self.gender_combo)
        layout.addRow("Localisation:", self.location_edit)
        layout.addRow("Éducation:", self.education_combo)
        layout.addRow("Niveau de revenu:", self.income_combo)
        
        # Bouton de sauvegarde
        self.save_button = QPushButton("Enregistrer les modifications")
        self.save_button.clicked.connect(self._save_persona_changes)
        layout.addRow(self.save_button)
    
    def _setup_goals_tab(self):
        layout = QVBoxLayout(self.goals_tab)
        
        self.goals_table = QTableWidget()
        self.goals_table.setColumnCount(3)
        self.goals_table.setHorizontalHeaderLabels(["Description", "Priorité", "Actions"])
        self.goals_table.horizontalHeader().setStretchLastSection(True)
        
        self.add_goal_button = QPushButton("Ajouter un objectif")
        self.add_goal_button.clicked.connect(self._add_goal)
        
        layout.addWidget(self.goals_table)
        layout.addWidget(self.add_goal_button)
    
    def _setup_pain_points_tab(self):
        layout = QVBoxLayout(self.pain_points_tab)
        
        self.pain_points_table = QTableWidget()
        self.pain_points_table.setColumnCount(3)
        self.pain_points_table.setHorizontalHeaderLabels(["Description", "Sévérité", "Actions"])
        self.pain_points_table.horizontalHeader().setStretchLastSection(True)
        
        self.add_pain_point_button = QPushButton("Ajouter un point de douleur")
        self.add_pain_point_button.clicked.connect(self._add_pain_point)
        
        layout.addWidget(self.pain_points_table)
        layout.addWidget(self.add_pain_point_button)
    
    def _setup_behaviors_tab(self):
        layout = QVBoxLayout(self.behaviors_tab)
        
        self.behaviors_table = QTableWidget()
        self.behaviors_table.setColumnCount(3)
        self.behaviors_table.setHorizontalHeaderLabels(["Description", "Fréquence", "Actions"])
        self.behaviors_table.horizontalHeader().setStretchLastSection(True)
        
        self.add_behavior_button = QPushButton("Ajouter un comportement")
        self.add_behavior_button.clicked.connect(self._add_behavior)
        
        layout.addWidget(self.behaviors_table)
        layout.addWidget(self.add_behavior_button)
    
    def _setup_quotes_tab(self):
        layout = QVBoxLayout(self.quotes_tab)
        
        self.quotes_table = QTableWidget()
        self.quotes_table.setColumnCount(3)
        self.quotes_table.setHorizontalHeaderLabels(["Citation", "Contexte", "Actions"])
        self.quotes_table.horizontalHeader().setStretchLastSection(True)
        
        self.add_quote_button = QPushButton("Ajouter une citation")
        self.add_quote_button.clicked.connect(self._add_quote)
        
        layout.addWidget(self.quotes_table)
        layout.addWidget(self.add_quote_button)
    
    def _setup_scenarios_tab(self):
        layout = QVBoxLayout(self.scenarios_tab)
        
        self.scenarios_table = QTableWidget()
        self.scenarios_table.setColumnCount(3)
        self.scenarios_table.setHorizontalHeaderLabels(["Titre", "Description", "Actions"])
        self.scenarios_table.horizontalHeader().setStretchLastSection(True)
        
        self.add_scenario_button = QPushButton("Ajouter un scénario")
        self.add_scenario_button.clicked.connect(self._add_scenario)
        
        layout.addWidget(self.scenarios_table)
        layout.addWidget(self.add_scenario_button)
    
    def _refresh_personas_list(self):
        self.personas_list.clear()
        personas = self.db.get_all_personas()
        for persona in personas:
            item = QListWidgetItem(persona[1])  # persona[1] est le nom
            item.setData(Qt.ItemDataRole.UserRole, persona[0])  # persona[0] est l'ID
            self.personas_list.addItem(item)
    
    def _display_persona_details(self):
        selected_items = self.personas_list.selectedItems()
        if not selected_items:
            return
            
        persona_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        persona_data = self.db.get_persona_details(persona_id)
        
        if persona_data:
            # Informations de base
            persona = persona_data['persona']
            self.name_edit.setText(persona[1])
            self.role_edit.setText(persona[2])
            self.age_spin.setValue(persona[3] if persona[3] else 0)
            self.gender_combo.setCurrentText(persona[4])
            self.location_edit.setText(persona[5])
            self.education_combo.setCurrentText(persona[6])
            self.income_combo.setCurrentText(persona[7])
            
            # Objectifs
            self._populate_table(self.goals_table, persona_data['goals'], self._edit_goal, self._delete_goal)
            
            # Points de douleur
            self._populate_table(self.pain_points_table, persona_data['pain_points'], self._edit_pain_point, self._delete_pain_point)
            
            # Comportements
            self._populate_table(self.behaviors_table, persona_data['behaviors'], self._edit_behavior, self._delete_behavior)
            
            # Citations
            self._populate_table(self.quotes_table, persona_data['quotes'], self._edit_quote, self._delete_quote)
            
            # Scénarios
            self._populate_table(self.scenarios_table, persona_data['scenarios'], self._edit_scenario, self._delete_scenario)
    
    def _populate_table(self, table, data, edit_callback, delete_callback):
        table.setRowCount(len(data))
        
        for row, item in enumerate(data):
            # Colonnes de données
            for col in range(len(item)-1):  # On ignore l'ID
                table.setItem(row, col, QTableWidgetItem(str(item[col+1])))
            
            # Boutons d'actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_button = QPushButton("✏️")
            edit_button.setMaximumWidth(30)
            edit_button.clicked.connect(lambda _, r=row: edit_callback(r))
            
            delete_button = QPushButton("🗑️")
            delete_button.setMaximumWidth(30)
            delete_button.clicked.connect(lambda _, r=row: delete_callback(r))
            
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_layout.addStretch()
            
            table.setCellWidget(row, len(item)-1, actions_widget)
        
        table.resizeColumnsToContents()
    
    def _create_new_persona(self):
        name, ok = QInputDialog.getText(self, "Nouveau Persona", "Nom du persona:")
        if ok and name:
            persona_data = {
                'name': name,
                'role': '',
                'age': 0,
                'gender': '',
                'location': '',
                'education': '',
                'income_level': ''
            }
            self.db.add_persona(persona_data)
    
    def _save_persona_changes(self):
        selected_items = self.personas_list.selectedItems()
        if not selected_items:
            return
            
        persona_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        updated_data = {
            'name': self.name_edit.text(),
            'role': self.role_edit.text(),
            'age': self.age_spin.value(),
            'gender': self.gender_combo.currentText(),
            'location': self.location_edit.text(),
            'education': self.education_combo.currentText(),
            'income_level': self.income_combo.currentText()
        }
        self.db.update_persona(persona_id, updated_data)
        self.status_bar.showMessage("Persona mis à jour avec succès", 3000)
    
    def _delete_current_persona(self):
        selected_items = self.personas_list.selectedItems()
        if not selected_items:
            return
            
        reply = QMessageBox.question(
            self, 'Confirmation',
            "Êtes-vous sûr de vouloir supprimer ce persona?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            persona_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
            self.db.delete_persona(persona_id)
    
    def _add_goal(self):
        self._add_table_item("Objectif", "Entrez la description de l'objectif:", self.db.add_goal)
    
    def _edit_goal(self, row):
        self._edit_table_item(row, self.goals_table, "Objectif", self.db.execute_query)
    
    def _delete_goal(self, row):
        self._delete_table_item(row, self.goals_table, "objectif", self.db.execute_query)
    
    # Méthodes similaires pour pain_points, behaviors, quotes, scenarios...
    # (Le code est similaire, seul le nom de la table change)
    
    def _export_persona(self):
        selected_items = self.personas_list.selectedItems()
        if not selected_items:
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Exporter le persona", "", "Fichiers JSON (*.json)"
        )
        
        if file_name:
            # Implémentez la logique d'export ici
            pass
    
    def _import_persona(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Importer un persona", "", "Fichiers JSON (*.json)"
        )
        
        if file_name:
            # Implémentez la logique d'import ici
            pass
    
    def _add_table_item(self, item_type, prompt_text, db_add_function):
        selected_items = self.personas_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un persona d'abord")
            return
            
        persona_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        text, ok = QInputDialog.getText(self, f"Ajouter un {item_type}", prompt_text)
        
        if ok and text:
            db_add_function(persona_id, text, 1)  # Priorité/Sévérité par défaut à 1
    
    def _edit_table_item(self, row, table, item_type, db_update_function):
        item_id = int(table.item(row, 0).text())  # Supposant que l'ID est dans la première colonne
        current_text = table.item(row, 1).text()  # Supposant que le texte est dans la deuxième colonne
        
        new_text, ok = QInputDialog.getText(
            self, f"Modifier {item_type}", 
            f"Nouvelle description pour {item_type}:", 
            text=current_text
        )
        
        if ok and new_text:
            query = f"UPDATE {item_type.lower()}s SET description = ? WHERE id = ?"
            db_update_function(query, (new_text, item_id))
    
    def _delete_table_item(self, row, table, item_type, db_delete_function):
        item_id = int(table.item(row, 0).text())
        
        reply = QMessageBox.question(
            self, 'Confirmation',
            f"Êtes-vous sûr de vouloir supprimer ce {item_type}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            query = f"DELETE FROM {item_type.lower()}s WHERE id = ?"
            db_delete_function(query, (item_id,))

            