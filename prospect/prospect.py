import sys
import csv
from datetime import datetime
from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem, QColor, QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableView,
    QPushButton, QLineEdit, QComboBox, QLabel, QFormLayout, QStackedWidget,
    QMessageBox, QToolBar, QStatusBar, QFileDialog, QStyledItemDelegate, QHeaderView,
    QListWidget, QAbstractItemView, QTabWidget, QTextEdit, QCheckBox
)


# ---- MODÈLE DE DONNÉES ----
class Prospect:
    def __init__(self, name="", phone="", email="", tags=None, stage="Nouveau", needs=None, notes=""):
        self.name = name
        self.phone = phone
        self.email = email
        self.tags = tags or []
        self.stage = stage
        self.needs = needs or []
        self.notes = notes
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "tags": "|".join(self.tags),
            "stage": self.stage,
            "needs": "|".join(self.needs),
            "notes": self.notes,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M")
        }
    
    @classmethod
    def from_dict(cls, data):
        prospect = cls()
        prospect.name = data.get("name", "")
        prospect.phone = data.get("phone", "")
        prospect.email = data.get("email", "")
        prospect.tags = data.get("tags", "").split("|") if data.get("tags") else []
        prospect.stage = data.get("stage", "Nouveau")
        prospect.needs = data.get("needs", "").split("|") if data.get("needs") else []
        prospect.notes = data.get("notes", "")
        prospect.created_at = datetime.strptime(data["created_at"], "%Y-%m-%d %H:%M")
        prospect.updated_at = datetime.strptime(data["updated_at"], "%Y-%m-%d %H:%M")
        return prospect


class ProspectsModel:
    def __init__(self):
        self.prospects = []
        self.tags = ["Chaud", "Froid", "Relancé", "B2B", "Urgent"]
        self.stages = ["Nouveau", "À relancer", "En négociation", "Converti", "Perdu"]
    
    def add_prospect(self, prospect):
        self.prospects.append(prospect)
    
    def remove_prospect(self, index):
        if 0 <= index < len(self.prospects):
            self.prospects.pop(index)
    
    def update_prospect(self, index, prospect):
        if 0 <= index < len(self.prospects):
            self.prospects[index] = prospect
    
    def get_prospect(self, index):
        if 0 <= index < len(self.prospects):
            return self.prospects[index]
        return None
    
    def export_csv(self, filename):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=[
                "name", "phone", "email", "tags", "stage", "needs", "notes", "created_at", "updated_at"
            ])
            writer.writeheader()
            for prospect in self.prospects:
                writer.writerow(prospect.to_dict())
    
    def import_csv(self, filename):
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.prospects.append(Prospect.from_dict(row))
            return True
        except Exception as e:
            print(f"Import error: {e}")
            return False


# ---- VUES PERSONNALISÉES ----
class TagDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if index.column() == 3:  # Colonne des tags
            tags = index.data().split("|")
            rect = option.rect
            x = rect.x() + 2
            y = rect.y() + 2
            
            for tag in tags:
                color = QColor("#4CAF50") if tag == "Chaud" else QColor("#2196F3")
                painter.fillRect(x, y, 60, 20, color)
                painter.setPen(Qt.GlobalColor.white)
                painter.drawText(x + 5, y + 15, tag)
                x += 70
        else:
            super().paint(painter, option, index)


class StageComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItems(["Nouveau", "À relancer", "En négociation", "Converti", "Perdu"])
        self.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)


# ---- INTERFACE PRINCIPALE ----
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ProspectManager")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(1200, 800)
        
        # Modèle
        self.model = ProspectsModel()
        
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        self.main_layout = QHBoxLayout(self.central_widget)
        
        # Barre latérale
        self.sidebar = self.create_sidebar()
        self.main_layout.addWidget(self.sidebar, stretch=1)
        
        # Zone de contenu
        self.content_stack = QStackedWidget()
        self.main_layout.addWidget(self.content_stack, stretch=4)
        
        # Vues
        self.list_view = self.create_list_view()
        self.add_view = self.create_add_view()
        self.detail_view = self.create_detail_view()
        
        self.content_stack.addWidget(self.list_view)
        self.content_stack.addWidget(self.add_view)
        self.content_stack.addWidget(self.detail_view)
        
        # Barre d'outils
        self.create_toolbar()
        
        # Barre de statut
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Données de test
        self.load_sample_data()
    
    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # Actions
        add_action = QAction(QIcon("icons/add.png"), "Ajouter", self)
        add_action.triggered.connect(self.show_add_view)
        toolbar.addAction(add_action)
        
        import_action = QAction(QIcon("icons/import.png"), "Importer", self)
        import_action.triggered.connect(self.import_data)
        toolbar.addAction(import_action)
        
        export_action = QAction(QIcon("icons/export.png"), "Exporter", self)
        export_action.triggered.connect(self.export_data)
        toolbar.addAction(export_action)
        
        toolbar.addSeparator()
        
        stats_action = QAction(QIcon("icons/stats.png"), "Statistiques", self)
        toolbar.addAction(stats_action)
    
    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setStyleSheet("background-color: #f5f5f5;")
        layout = QVBoxLayout(sidebar)
        
        # Filtres
        filters_group = QWidget()
        filters_layout = QVBoxLayout(filters_group)
        
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Rechercher...")
        search_bar.textChanged.connect(self.filter_prospects)
        search_bar.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-bottom: 10px;
            }
        """)
        
        stage_filter = QComboBox()
        stage_filter.addItem("Tous les stades")
        stage_filter.addItems(self.model.stages)
        stage_filter.currentTextChanged.connect(self.filter_prospects)
        
        tag_filter = QComboBox()
        tag_filter.addItem("Tous les tags")
        tag_filter.addItems(self.model.tags)
        tag_filter.currentTextChanged.connect(self.filter_prospects)
        
        filters_layout.addWidget(QLabel("Filtres"))
        filters_layout.addWidget(search_bar)
        filters_layout.addWidget(stage_filter)
        filters_layout.addWidget(tag_filter)
        filters_layout.addStretch()
        
        # Menu rapide
        quick_menu = QListWidget()
        quick_menu.addItems(["Tous les prospects", "À relancer", "Nouveaux", "Convertis"])
        quick_menu.currentRowChanged.connect(self.quick_filter)
        quick_menu.setCurrentRow(0)
        
        layout.addWidget(filters_group)
        layout.addWidget(quick_menu)
        layout.addStretch()
        
        return sidebar
    
    def create_list_view(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        
        # Tableau
        self.table = QTableView()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.doubleClicked.connect(self.show_detail_view)
        
        # Modèle de tableau
        self.table_model = QStandardItemModel()
        self.table_model.setHorizontalHeaderLabels([
            "Nom", "Téléphone", "Email", "Tags", "Stade", "Dernière MAJ"
        ])
        self.table.setModel(self.table_model)
        
        # Personnalisation
        self.table.setItemDelegateForColumn(3, TagDelegate())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableView {
                alternate-background-color: #f9f9f9;
                selection-background-color: #e3f2fd;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                padding: 5px;
            }
        """)
        
        layout.addWidget(self.table)
        return container
    
    def create_add_view(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Champs
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.stage_input = StageComboBox()
        
        # Tags
        self.tags_widget = QWidget()
        tags_layout = QHBoxLayout(self.tags_widget)
        self.tag_checkboxes = []
        for tag in self.model.tags:
            cb = QCheckBox(tag)
            self.tag_checkboxes.append(cb)
            tags_layout.addWidget(cb)
        
        # Besoins
        self.needs_input = QTextEdit()
        self.needs_input.setPlaceholderText("Un besoin par ligne")
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Notes supplémentaires...")
        
        # Ajout au formulaire
        form.addRow("Nom complet:", self.name_input)
        form.addRow("Téléphone:", self.phone_input)
        form.addRow("Email:", self.email_input)
        form.addRow("Stade:", self.stage_input)
        form.addRow("Tags:", self.tags_widget)
        form.addRow("Besoins:", self.needs_input)
        form.addRow("Notes:", self.notes_input)
        
        # Boutons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(self.save_prospect)
        save_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.show_list_view)
        cancel_btn.setStyleSheet("background-color: #f44336; color: white;")
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(form)
        layout.addLayout(button_layout)
        return container
    
    def create_detail_view(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        
        self.tabs = QTabWidget()
        
        # Onglet Infos
        info_tab = QWidget()
        info_layout = QFormLayout(info_tab)
        
        self.detail_name = QLabel()
        self.detail_phone = QLabel()
        self.detail_email = QLabel()
        self.detail_stage = QLabel()
        self.detail_tags = QLabel()
        self.detail_needs = QLabel()
        self.detail_created = QLabel()
        self.detail_updated = QLabel()
        
        info_layout.addRow("Nom:", self.detail_name)
        info_layout.addRow("Téléphone:", self.detail_phone)
        info_layout.addRow("Email:", self.detail_email)
        info_layout.addRow("Stade:", self.detail_stage)
        info_layout.addRow("Tags:", self.detail_tags)
        info_layout.addRow("Besoins:", self.detail_needs)
        info_layout.addRow("Créé le:", self.detail_created)
        info_layout.addRow("Mis à jour:", self.detail_updated)
        
        # Onglet Historique
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)
        self.history_list = QListWidget()
        history_layout.addWidget(self.history_list)
        
        # Onglet Actions
        action_tab = QWidget()
        action_layout = QVBoxLayout(action_tab)
        
        whatsapp_btn = QPushButton("Ouvrir WhatsApp")
        whatsapp_btn.clicked.connect(self.open_whatsapp)
        whatsapp_btn.setStyleSheet("background-color: #25D366; color: white;")
        
        email_btn = QPushButton("Envoyer Email")
        email_btn.clicked.connect(self.send_email)
        email_btn.setStyleSheet("background-color: #4285F4; color: white;")
        
        call_btn = QPushButton("Appeler")
        call_btn.clicked.connect(self.make_call)
        
        action_layout.addWidget(whatsapp_btn)
        action_layout.addWidget(email_btn)
        action_layout.addWidget(call_btn)
        action_layout.addStretch()
        
        self.tabs.addTab(info_tab, "Informations")
        self.tabs.addTab(history_tab, "Historique")
        self.tabs.addTab(action_tab, "Actions")
        
        # Boutons
        button_layout = QHBoxLayout()
        edit_btn = QPushButton("Modifier")
        edit_btn.clicked.connect(self.edit_prospect)
        
        delete_btn = QPushButton("Supprimer")
        delete_btn.clicked.connect(self.delete_prospect)
        delete_btn.setStyleSheet("background-color: #f44336; color: white;")
        
        back_btn = QPushButton("Retour")
        back_btn.clicked.connect(self.show_list_view)
        
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(back_btn)
        
        layout.addWidget(self.tabs)
        layout.addLayout(button_layout)
        return container
    
    # ---- LOGIQUE D'APPLICATION ----
    def load_sample_data(self):
        """Charge des données de démonstration"""
        samples = [
            Prospect("Jean Dupont", "+33123456789", "jean@example.com", ["Chaud", "B2B"], "En négociation", ["Presse hydraulique"], "Client sérieux"),
            Prospect("Marie Martin", "+33698765432", "marie@entreprise.com", ["Froid"], "À relancer", ["Transport", "Logistique"], "A relancer fin du mois"),
            Prospect("Pierre Durand", "+32456789123", "pierre@durand.com", ["Relancé"], "Nouveau", ["Infos produit"], "Demande catalogue")
        ]
        for prospect in samples:
            self.model.add_prospect(prospect)
        self.update_table()
    
    def update_table(self, prospects=None):
        """Met à jour la table avec les prospects"""
        self.table_model.clear()
        self.table_model.setHorizontalHeaderLabels([
            "Nom", "Téléphone", "Email", "Tags", "Stade", "Dernière MAJ"
        ])
        
        prospects = prospects or self.model.prospects
        for prospect in prospects:
            row = [
                QStandardItem(prospect.name),
                QStandardItem(prospect.phone),
                QStandardItem(prospect.email),
                QStandardItem("|".join(prospect.tags)),
                QStandardItem(prospect.stage),
                QStandardItem(prospect.updated_at.strftime("%Y-%m-%d %H:%M"))
            ]
            self.table_model.appendRow(row)
    
    def filter_prospects(self):
        """Filtre les prospects selon les critères"""
        search_text = self.sender().parent().findChild(QLineEdit).text().lower()
        stage_filter = self.sender().parent().findChild(QComboBox).currentText()
        tag_filter = self.sender().parent().findChild(QComboBox, 1).currentText()
        
        filtered = []
        for prospect in self.model.prospects:
            # Filtre recherche
            matches_search = (search_text in prospect.name.lower() or 
                            search_text in prospect.phone or 
                            any(search_text in need.lower() for need in prospect.needs))
            
            # Filtre stade
            matches_stage = (stage_filter == "Tous les stades" or 
                           prospect.stage == stage_filter)
            
            # Filtre tag
            matches_tag = (tag_filter == "Tous les tags" or 
                         tag_filter in prospect.tags)
            
            if matches_search and matches_stage and matches_tag:
                filtered.append(prospect)
        
        self.update_table(filtered)
    
    def quick_filter(self, index):
        """Filtre rapide depuis le menu latéral"""
        filters = {
            0: lambda p: True,
            1: lambda p: p.stage == "À relancer",
            2: lambda p: p.stage == "Nouveau",
            3: lambda p: p.stage == "Converti"
        }
        filtered = [p for p in self.model.prospects if filters[index](p)]
        self.update_table(filtered)
    
    def save_prospect(self):
        """Enregistre un nouveau prospect"""
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        
        if not name or not phone:
            QMessageBox.warning(self, "Champs requis", "Le nom et le téléphone sont obligatoires")
            return
        
        # Récupère les tags cochés
        tags = []
        for cb in self.tag_checkboxes:
            if cb.isChecked():
                tags.append(cb.text())
        
        # Crée le prospect
        prospect = Prospect(
            name=name,
            phone=phone,
            email=email,
            tags=tags,
            stage=self.stage_input.currentText(),
            needs=self.needs_input.toPlainText().split("\n"),
            notes=self.notes_input.toPlainText()
        )
        
        self.model.add_prospect(prospect)
        self.update_table()
        self.show_list_view()
        self.status_bar.showMessage(f"Prospect {name} ajouté avec succès", 3000)
    
    def show_add_view(self):
        """Affiche la vue d'ajout"""
        # Réinitialise les champs
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.stage_input.setCurrentIndex(0)
        for cb in self.tag_checkboxes:
            cb.setChecked(False)
        self.needs_input.clear()
        self.notes_input.clear()
        
        self.content_stack.setCurrentWidget(self.add_view)
    
    def show_list_view(self):
        """Affiche la vue liste"""
        self.content_stack.setCurrentWidget(self.list_view)
    
    def show_detail_view(self):
        """Affiche la vue détail du prospect sélectionné"""
        index = self.table.currentIndex().row()
        prospect = self.model.get_prospect(index)
        if not prospect:
            return
        
        # Remplit les champs
        self.detail_name.setText(prospect.name)
        self.detail_phone.setText(prospect.phone)
        self.detail_email.setText(prospect.email)
        self.detail_stage.setText(prospect.stage)
        self.detail_tags.setText(", ".join(prospect.tags))
        self.detail_needs.setText("\n".join(prospect.needs))
        self.detail_created.setText(prospect.created_at.strftime("%Y-%m-%d %H:%M"))
        self.detail_updated.setText(prospect.updated_at.strftime("%Y-%m-%d %H:%M"))
        
        # Historique (simulé)
        self.history_list.clear()
        self.history_list.addItems([
            f"{prospect.created_at.strftime('%Y-%m-%d')} - Prospect créé",
            f"{prospect.updated_at.strftime('%Y-%m-%d')} - Dernière mise à jour"
        ])
        
        self.current_prospect_index = index
        self.content_stack.setCurrentWidget(self.detail_view)
    
    def edit_prospect(self):
        """Passe en mode édition du prospect"""
        prospect = self.model.get_prospect(self.current_prospect_index)
        if not prospect:
            return
        
        # Pré-remplit le formulaire
        self.name_input.setText(prospect.name)
        self.phone_input.setText(prospect.phone)
        self.email_input.setText(prospect.email)
        self.stage_input.setCurrentText(prospect.stage)
        for cb in self.tag_checkboxes:
            cb.setChecked(cb.text() in prospect.tags)
        self.needs_input.setPlainText("\n".join(prospect.needs))
        self.notes_input.setPlainText(prospect.notes)
        
        # Change de vue
        self.content_stack.setCurrentWidget(self.add_view)
        self.editing_prospect = True
    
    def delete_prospect(self):
        """Supprime le prospect actuel"""
        reply = QMessageBox.question(
            self, "Confirmation",
            "Voulez-vous vraiment supprimer ce prospect?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.model.remove_prospect(self.current_prospect_index)
            self.update_table()
            self.show_list_view()
            self.status_bar.showMessage("Prospect supprimé", 3000)
    
    def open_whatsapp(self):
        """Ouvre WhatsApp avec le numéro du prospect"""
        prospect = self.model.get_prospect(self.current_prospect_index)
        if prospect and prospect.phone:
            import webbrowser
            webbrowser.open(f"https://wa.me/{prospect.phone}")
    
    def send_email(self):
        """Ouvre le client mail avec l'email du prospect"""
        prospect = self.model.get_prospect(self.current_prospect_index)
        if prospect and prospect.email:
            import webbrowser
            webbrowser.open(f"mailto:{prospect.email}")
    
    def make_call(self):
        """Simule un appel (sur mobile déclencherait l'appel réel)"""
        prospect = self.model.get_prospect(self.current_prospect_index)
        if prospect and prospect.phone:
            QMessageBox.information(self, "Appel", f"Appel vers {prospect.phone} simulé")
    
    def import_data(self):
        """Importe des prospects depuis un CSV"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Importer des prospects", "", "CSV Files (*.csv)")
        
        if filename:
            success = self.model.import_csv(filename)
            if success:
                self.update_table()
                self.status_bar.showMessage(f"Import réussi - {len(self.model.prospects)} prospects", 3000)
            else:
                QMessageBox.critical(self, "Erreur", "Échec de l'importation")
    
    def export_data(self):
        """Exporte les prospects en CSV"""
        if not self.model.prospects:
            QMessageBox.warning(self, "Export", "Aucun prospect à exporter")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Exporter les prospects", "prospects.csv", "CSV Files (*.csv)")
        
        if filename:
            self.model.export_csv(filename)
            self.status_bar.showMessage(f"Export réussi - {len(self.model.prospects)} prospects", 3000)


# ---- LANCEMENT ----
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Style moderne
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QMainWindow {
            background-color: #fafafa;
        }
        QPushButton {
            padding: 8px;
            border-radius: 4px;
            min-width: 80px;
        }
        QLineEdit, QTextEdit, QComboBox {
            padding: 6px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
    """)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())