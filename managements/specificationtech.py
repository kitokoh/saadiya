import sys
import sqlite3
import os
import json
import webbrowser
import urllib.parse
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportLabImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import tempfile
import shutil

class DatabaseManager:
    def __init__(self, db_path="specifications.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table des produits
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                description TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des spécifications
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS specifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                field_name TEXT NOT NULL,
                field_value TEXT,
                field_type TEXT DEFAULT 'text',
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Table des médias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                media_type TEXT NOT NULL,
                media_path TEXT,
                media_url TEXT,
                description TEXT,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)

class MediaWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.media_list = []
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Boutons d'ajout de média
        buttons_layout = QHBoxLayout()
        self.add_image_btn = QPushButton("Ajouter Image")
        self.add_video_btn = QPushButton("Ajouter Vidéo")
        self.add_url_btn = QPushButton("Ajouter URL/YouTube")
        
        self.add_image_btn.clicked.connect(self.add_image)
        self.add_video_btn.clicked.connect(self.add_video)
        self.add_url_btn.clicked.connect(self.add_url)
        
        buttons_layout.addWidget(self.add_image_btn)
        buttons_layout.addWidget(self.add_video_btn)
        buttons_layout.addWidget(self.add_url_btn)
        
        # Liste des médias
        self.media_list_widget = QListWidget()
        self.media_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.media_list_widget.customContextMenuRequested.connect(self.show_context_menu)
        
        layout.addLayout(buttons_layout)
        layout.addWidget(QLabel("Médias associés:"))
        layout.addWidget(self.media_list_widget)
        
        self.setLayout(layout)
    
    def add_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Sélectionner une image", 
            "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self.add_media_item("image", file_path, os.path.basename(file_path))
    
    def add_video(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Sélectionner une vidéo", 
            "", "Vidéos (*.mp4 *.avi *.mov *.wmv *.flv)"
        )
        if file_path:
            self.add_media_item("video", file_path, os.path.basename(file_path))
    
    def add_url(self):
        url, ok = QInputDialog.getText(self, "Ajouter URL", "URL (YouTube, etc.):")
        if ok and url:
            description, ok2 = QInputDialog.getText(self, "Description", "Description:")
            if ok2:
                self.add_media_item("url", url, description or "Lien")
    
    def add_media_item(self, media_type, path_or_url, description):
        media_item = {
            'type': media_type,
            'path': path_or_url,
            'description': description
        }
        self.media_list.append(media_item)
        self.refresh_media_list()
    
    def refresh_media_list(self):
        self.media_list_widget.clear()
        for i, media in enumerate(self.media_list):
            item_text = f"[{media['type'].upper()}] {media['description']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, i)
            self.media_list_widget.addItem(item)
    
    def show_context_menu(self, position):
        item = self.media_list_widget.itemAt(position)
        if item:
            menu = QMenu()
            delete_action = menu.addAction("Supprimer")
            view_action = menu.addAction("Voir/Ouvrir")
            
            action = menu.exec_(self.media_list_widget.mapToGlobal(position))
            
            if action == delete_action:
                index = item.data(Qt.UserRole)
                del self.media_list[index]
                self.refresh_media_list()
            elif action == view_action:
                index = item.data(Qt.UserRole)
                media = self.media_list[index]
                if media['type'] == 'url':
                    webbrowser.open(media['path'])
                else:
                    os.startfile(media['path']) if os.name == 'nt' else os.system(f'open "{media["path"]}"')
    
    def load_media(self, media_list):
        self.media_list = media_list
        self.refresh_media_list()
    
    def get_media_list(self):
        return self.media_list

class SpecificationForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.spec_fields = []
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Zone de scroll pour les spécifications
        scroll = QScrollArea()
        scroll_widget = QWidget()
        self.specs_layout = QVBoxLayout(scroll_widget)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        
        # Bouton pour ajouter un champ
        add_field_btn = QPushButton("+ Ajouter un champ de spécification")
        add_field_btn.clicked.connect(self.add_specification_field)
        
        layout.addWidget(QLabel("Spécifications techniques:"))
        layout.addWidget(add_field_btn)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
        
        # Ajouter quelques champs par défaut
        self.add_specification_field("Nom du produit", "text")
        self.add_specification_field("Dimensions", "text")
        self.add_specification_field("Poids", "text")
        self.add_specification_field("Conditions d'utilisation", "textarea")
    
    def add_specification_field(self, field_name="", field_type="text"):
        field_widget = QWidget()
        field_layout = QHBoxLayout(field_widget)
        
        # Nom du champ
        name_edit = QLineEdit()
        name_edit.setPlaceholderText("Nom du champ")
        if field_name:
            name_edit.setText(field_name)
        
        # Type de champ
        type_combo = QComboBox()
        type_combo.addItems(["text", "textarea", "number", "date"])
        if field_type:
            type_combo.setCurrentText(field_type)
        
        # Valeur du champ
        value_widget = self.create_value_widget(field_type)
        
        # Bouton supprimer
        delete_btn = QPushButton("×")
        delete_btn.setMaximumWidth(30)
        delete_btn.clicked.connect(lambda: self.remove_field(field_widget))
        
        # Mise à jour du widget de valeur quand le type change
        type_combo.currentTextChanged.connect(
            lambda new_type: self.update_value_widget(field_layout, new_type, 2)
        )
        
        field_layout.addWidget(QLabel("Champ:"))
        field_layout.addWidget(name_edit)
        field_layout.addWidget(QLabel("Type:"))
        field_layout.addWidget(type_combo)
        field_layout.addWidget(QLabel("Valeur:"))
        field_layout.addWidget(value_widget)
        field_layout.addWidget(delete_btn)
        
        self.specs_layout.addWidget(field_widget)
        self.spec_fields.append({
            'widget': field_widget,
            'name_edit': name_edit,
            'type_combo': type_combo,
            'value_widget': value_widget
        })
    
    def create_value_widget(self, field_type):
        if field_type == "textarea":
            widget = QTextEdit()
            widget.setMaximumHeight(100)
        elif field_type == "number":
            widget = QSpinBox()
            widget.setMaximum(999999)
        elif field_type == "date":
            widget = QDateEdit()
            widget.setDate(QDate.currentDate())
        else:  # text
            widget = QLineEdit()
        return widget
    
    def update_value_widget(self, layout, new_type, position):
        # Supprimer l'ancien widget de valeur
        old_widget = layout.itemAt(position).widget()
        layout.removeWidget(old_widget)
        old_widget.deleteLater()
        
        # Créer et insérer le nouveau widget
        new_widget = self.create_value_widget(new_type)
        layout.insertWidget(position, new_widget)
        
        # Mettre à jour la référence dans spec_fields
        for field in self.spec_fields:
            if field['value_widget'] == old_widget:
                field['value_widget'] = new_widget
                break
    
    def remove_field(self, field_widget):
        # Supprimer de la liste
        self.spec_fields = [f for f in self.spec_fields if f['widget'] != field_widget]
        # Supprimer du layout
        self.specs_layout.removeWidget(field_widget)
        field_widget.deleteLater()
    
    def get_specifications(self):
        specs = []
        for field in self.spec_fields:
            name = field['name_edit'].text()
            field_type = field['type_combo'].currentText()
            
            if field_type == "textarea":
                value = field['value_widget'].toPlainText()
            elif field_type == "number":
                value = str(field['value_widget'].value())
            elif field_type == "date":
                value = field['value_widget'].date().toString()
            else:
                value = field['value_widget'].text()
            
            if name:  # Ne pas ajouter si le nom est vide
                specs.append({
                    'name': name,
                    'value': value,
                    'type': field_type
                })
        return specs
    
    def load_specifications(self, specs):
        # Vider les champs existants
        for field in self.spec_fields[:]:
            self.remove_field(field['widget'])
        
        # Charger les nouvelles spécifications
        for spec in specs:
            self.add_specification_field(spec['name'], spec['type'])
            field = self.spec_fields[-1]
            
            if spec['type'] == "textarea":
                field['value_widget'].setPlainText(spec['value'])
            elif spec['type'] == "number":
                field['value_widget'].setValue(int(spec['value']) if spec['value'].isdigit() else 0)
            elif spec['type'] == "date":
                date = QDate.fromString(spec['value'])
                if date.isValid():
                    field['value_widget'].setDate(date)
            else:
                field['value_widget'].setText(spec['value'])

class ProductSearchDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.selected_product = None
        self.setup_ui()
        self.load_products()
    
    def setup_ui(self):
        self.setWindowTitle("Rechercher un produit")
        self.setModal(True)
        self.resize(600, 400)
        
        layout = QVBoxLayout()
        
        # Barre de recherche
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Rechercher par nom ou catégorie...")
        self.search_edit.textChanged.connect(self.filter_products)
        search_layout.addWidget(QLabel("Recherche:"))
        search_layout.addWidget(self.search_edit)
        
        # Liste des produits
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(4)
        self.products_table.setHorizontalHeaderLabels(["ID", "Nom", "Catégorie", "Date création"])
        self.products_table.horizontalHeader().setStretchLastSection(True)
        self.products_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.products_table.doubleClicked.connect(self.accept)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        self.select_btn = QPushButton("Sélectionner")
        self.cancel_btn = QPushButton("Annuler")
        self.delete_btn = QPushButton("Supprimer")
        
        self.select_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        self.delete_btn.clicked.connect(self.delete_product)
        
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.select_btn)
        buttons_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(search_layout)
        layout.addWidget(self.products_table)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def load_products(self):
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, category, created_date FROM products ORDER BY created_date DESC")
        products = cursor.fetchall()
        conn.close()
        
        self.products_table.setRowCount(len(products))
        for row, product in enumerate(products):
            for col, value in enumerate(product):
                item = QTableWidgetItem(str(value))
                self.products_table.setItem(row, col, item)
    
    def filter_products(self):
        search_text = self.search_edit.text().lower()
        for row in range(self.products_table.rowCount()):
            match = False
            for col in range(self.products_table.columnCount()):
                item = self.products_table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.products_table.setRowHidden(row, not match)
    
    def delete_product(self):
        current_row = self.products_table.currentRow()
        if current_row >= 0:
            product_id = self.products_table.item(current_row, 0).text()
            product_name = self.products_table.item(current_row, 1).text()
            
            reply = QMessageBox.question(
                self, "Confirmer la suppression", 
                f"Êtes-vous sûr de vouloir supprimer le produit '{product_name}' ?\n"
                "Toutes les spécifications et médias associés seront également supprimés."
            )
            
            if reply == QMessageBox.Yes:
                conn = self.db_manager.get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM media WHERE product_id = ?", (product_id,))
                cursor.execute("DELETE FROM specifications WHERE product_id = ?", (product_id,))
                cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
                conn.commit()
                conn.close()
                
                self.load_products()
                QMessageBox.information(self, "Succès", "Produit supprimé avec succès!")
    
    def accept(self):
        current_row = self.products_table.currentRow()
        if current_row >= 0:
            self.selected_product = {
                'id': int(self.products_table.item(current_row, 0).text()),
                'name': self.products_table.item(current_row, 1).text(),
                'category': self.products_table.item(current_row, 2).text()
            }
        super().accept()

class ShareDialog(QDialog):
    def __init__(self, product_data, media_list, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.media_list = media_list
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Partager le produit")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel(f"Partager: {self.product_data.get('name', 'Produit')}"))
        
        # Options de partage
        self.whatsapp_btn = QPushButton("Partager via WhatsApp Web")
        self.email_btn = QPushButton("Partager via Email")
        self.copy_info_btn = QPushButton("Copier les informations")
        
        self.whatsapp_btn.clicked.connect(self.share_whatsapp)
        self.email_btn.clicked.connect(self.share_email)
        self.copy_info_btn.clicked.connect(self.copy_info)
        
        layout.addWidget(self.whatsapp_btn)
        layout.addWidget(self.email_btn)
        layout.addWidget(self.copy_info_btn)
        
        # Zone de prévisualisation du message
        layout.addWidget(QLabel("Prévisualisation du message:"))
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMaximumHeight(150)
        
        message = self.generate_share_message()
        self.preview_text.setPlainText(message)
        
        layout.addWidget(self.preview_text)
        
        # Bouton fermer
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def generate_share_message(self):
        message = f"🔧 SPÉCIFICATIONS TECHNIQUES\n\n"
        message += f"📦 Produit: {self.product_data.get('name', 'N/A')}\n"
        if self.product_data.get('category'):
            message += f"📂 Catégorie: {self.product_data['category']}\n"
        
        message += "\n📋 DÉTAILS:\n"
        for spec in self.product_data.get('specifications', []):
            message += f"• {spec['name']}: {spec['value']}\n"
        
        if self.media_list:
            message += f"\n📎 Médias associés: {len(self.media_list)} fichier(s)\n"
            for media in self.media_list:
                if media['type'] == 'url':
                    message += f"🔗 {media['description']}: {media['path']}\n"
                else:
                    message += f"📁 {media['description']}\n"
        
        return message
    
    def share_whatsapp(self):
        message = self.generate_share_message()
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://web.whatsapp.com/send?text={encoded_message}"
        webbrowser.open(whatsapp_url)
    
    def share_email(self):
        message = self.generate_share_message()
        subject = f"Spécifications - {self.product_data.get('name', 'Produit')}"
        mailto_url = f"mailto:?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(message)}"
        webbrowser.open(mailto_url)
    
    def copy_info(self):
        message = self.generate_share_message()
        clipboard = QApplication.clipboard()
        clipboard.setText(message)
        QMessageBox.information(self, "Copié", "Les informations ont été copiées dans le presse-papiers!")

class PDFGenerator:
    @staticmethod
    def generate_pdf(product_data, specifications, media_list, output_path):
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Titre
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.darkblue,
            alignment=1  # Center
        )
        
        title = Paragraph(f"SPÉCIFICATIONS TECHNIQUES<br/>{product_data.get('name', 'Produit')}", title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Informations générales
        if product_data.get('category'):
            story.append(Paragraph(f"<b>Catégorie:</b> {product_data['category']}", styles['Normal']))
            story.append(Spacer(1, 10))
        
        # Spécifications
        story.append(Paragraph("<b>SPÉCIFICATIONS DÉTAILLÉES</b>", styles['Heading2']))
        story.append(Spacer(1, 10))
        
        # Tableau des spécifications
        spec_data = [['Caractéristique', 'Valeur']]
        for spec in specifications:
            spec_data.append([spec['name'], spec['value']])
        
        if len(spec_data) > 1:
            table = Table(spec_data, colWidths=[2*inch, 4*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)
        
        # Médias
        if media_list:
            story.append(Spacer(1, 20))
            story.append(Paragraph("<b>MÉDIAS ASSOCIÉS</b>", styles['Heading2']))
            story.append(Spacer(1, 10))
            
            for media in media_list:
                if media['type'] == 'url':
                    story.append(Paragraph(f"🔗 <b>{media['description']}:</b> {media['path']}", styles['Normal']))
                else:
                    story.append(Paragraph(f"📁 <b>{media['description']}:</b> {os.path.basename(media['path'])}", styles['Normal']))
                story.append(Spacer(1, 5))
        
        # Pied de page avec date
        story.append(Spacer(1, 30))
        story.append(Paragraph(f"<i>Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</i>", styles['Normal']))
        
        doc.build(story)

class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.db_manager = DatabaseManager()
        self.current_product_id = None
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Gestionnaire de Spécifications Techniques")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Panneau gauche - Informations produit
        left_panel = QWidget()
        left_panel.setMaximumWidth(400)
        left_layout = QVBoxLayout(left_panel)
        
        # Informations de base du produit
        product_group = QGroupBox("Informations du produit")
        product_layout = QVBoxLayout(product_group)
        
        self.product_name_edit = QLineEdit()
        self.product_name_edit.setPlaceholderText("Nom du produit")
        
        self.product_category_edit = QLineEdit()
        self.product_category_edit.setPlaceholderText("Catégorie")
        
        self.product_description_edit = QTextEdit()
        self.product_description_edit.setPlaceholderText("Description du produit")
        self.product_description_edit.setMaximumHeight(100)
        
        product_layout.addWidget(QLabel("Nom:"))
        product_layout.addWidget(self.product_name_edit)
        product_layout.addWidget(QLabel("Catégorie:"))
        product_layout.addWidget(self.product_category_edit)
        product_layout.addWidget(QLabel("Description:"))
        product_layout.addWidget(self.product_description_edit)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        self.search_btn = QPushButton("Rechercher")
        self.new_btn = QPushButton("Nouveau")
        self.save_btn = QPushButton("Sauvegarder")
        
        self.search_btn.clicked.connect(self.search_product)
        self.new_btn.clicked.connect(self.new_product)
        self.save_btn.clicked.connect(self.save_product)
        
        buttons_layout.addWidget(self.search_btn)
        buttons_layout.addWidget(self.new_btn)
        buttons_layout.addWidget(self.save_btn)
        
        # Boutons d'export et partage
        export_layout = QHBoxLayout()
        self.export_pdf_btn = QPushButton("Exporter PDF")
        self.share_btn = QPushButton("Partager")
        
        self.export_pdf_btn.clicked.connect(self.export_pdf)
        self.share_btn.clicked.connect(self.share_product)
        
        export_layout.addWidget(self.export_pdf_btn)
        export_layout.addWidget(self.share_btn)
        
        left_layout.addWidget(product_group)
        left_layout.addLayout(buttons_layout)
        left_layout.addLayout(export_layout)
        left_layout.addStretch()
        
        # Panneau droit - Spécifications et médias
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Onglets pour spécifications et médias
        tabs = QTabWidget()
        
        # Onglet spécifications
        self.spec_form = SpecificationForm()
        tabs.addTab(self.spec_form, "Spécifications")
        
        # Onglet médias
        self.media_widget = MediaWidget()
        tabs.addTab(self.media_widget, "Médias")
        
        right_layout.addWidget(tabs)
        
        # Ajout des panneaux au layout principal
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 2)
        
        # Status bar
        self.statusBar().showMessage("Prêt")
    
    def search_product(self):
        dialog = ProductSearchDialog(self.db_manager, self)
        if dialog.exec_() == QDialog.Accepted and dialog.selected_product:
            self.load_product(dialog.selected_product['id'])
    
    def new_product(self):
        self.current_product_id = None
        self.product_name_edit.clear()
        self.product_category_edit.clear()
        self.product_description_edit.clear()
        
        # Réinitialiser les spécifications avec des champs par défaut
        default_specs = [
            {'name': 'Nom du produit', 'value': '', 'type': 'text'},
            {'name': 'Dimensions', 'value': '', 'type': 'text'},
            {'name': 'Poids', 'value': '', 'type': 'text'},
            {'name': 'Conditions d\'utilisation', 'value': '', 'type': 'textarea'}
        ]
        self.spec_form.load_specifications(default_specs)
        self.media_widget.load_media([])
        
        self.statusBar().showMessage("Nouveau produit")
    
    def load_product(self, product_id):
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        # Charger les informations du produit
        cursor.execute("SELECT name, category, description FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        
        if product:
            self.current_product_id = product_id
            self.product_name_edit.setText(product[0])
            self.product_category_edit.setText(product[1] or "")
            self.product_description_edit.setPlainText(product[2] or "")
            
            # Charger les spécifications
            cursor.execute("SELECT field_name, field_value, field_type FROM specifications WHERE product_id = ?", (product_id,))
            specs_data = cursor.fetchall()
            specs = [{'name': spec[0], 'value': spec[1], 'type': spec[2]} for spec in specs_data]
            self.spec_form.load_specifications(specs)
            
            # Charger les médias
            cursor.execute("SELECT media_type, media_path, media_url, description FROM media WHERE product_id = ?", (product_id,))
            media_data = cursor.fetchall()
            media_list = []
            for media in media_data:
                media_list.append({
                    'type': media[0],
                    'path': media[1] or media[2],
                    'description': media[3]
                })
            self.media_widget.load_media(media_list)
            
            self.statusBar().showMessage(f"Produit chargé: {product[0]}")
        
        conn.close()
    
    def save_product(self):
        if not self.product_name_edit.text().strip():
            QMessageBox.warning(self, "Erreur", "Le nom du produit est obligatoire!")
            return
        
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.current_product_id:
                # Mise à jour d'un produit existant
                cursor.execute("""
                    UPDATE products 
                    SET name = ?, category = ?, description = ?, updated_date = CURRENT_TIMESTAMP 
                    WHERE id = ?
                """, (
                    self.product_name_edit.text(),
                    self.product_category_edit.text(),
                    self.product_description_edit.toPlainText(),
                    self.current_product_id
                ))
                
                # Supprimer les anciennes spécifications et médias
                cursor.execute("DELETE FROM specifications WHERE product_id = ?", (self.current_product_id,))
                cursor.execute("DELETE FROM media WHERE product_id = ?", (self.current_product_id,))
                
                product_id = self.current_product_id
            else:
                # Nouveau produit
                cursor.execute("""
                    INSERT INTO products (name, category, description) 
                    VALUES (?, ?, ?)
                """, (
                    self.product_name_edit.text(),
                    self.product_category_edit.text(),
                    self.product_description_edit.toPlainText()
                ))
                product_id = cursor.lastrowid
                self.current_product_id = product_id
            
            # Sauvegarder les spécifications
            specifications = self.spec_form.get_specifications()
            for spec in specifications:
                cursor.execute("""
                    INSERT INTO specifications (product_id, field_name, field_value, field_type) 
                    VALUES (?, ?, ?, ?)
                """, (product_id, spec['name'], spec['value'], spec['type']))
            
            # Sauvegarder les médias
            media_list = self.media_widget.get_media_list()
            for media in media_list:
                if media['type'] == 'url':
                    cursor.execute("""
                        INSERT INTO media (product_id, media_type, media_url, description) 
                        VALUES (?, ?, ?, ?)
                    """, (product_id, media['type'], media['path'], media['description']))
                else:
                    cursor.execute("""
                        INSERT INTO media (product_id, media_type, media_path, description) 
                        VALUES (?, ?, ?, ?)
                    """, (product_id, media['type'], media['path'], media['description']))
            
            conn.commit()
            self.statusBar().showMessage("Produit sauvegardé avec succès!")
            QMessageBox.information(self, "Succès", "Produit sauvegardé avec succès!")
            
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la sauvegarde: {str(e)}")
        finally:
            conn.close()
    
    def export_pdf(self):
        if not self.current_product_id:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord sauvegarder le produit!")
            return
        
        # Sélectionner le fichier de sortie
        file_dialog = QFileDialog()
        default_name = f"Specifications_{self.product_name_edit.text().replace(' ', '_')}.pdf"
        file_path, _ = file_dialog.getSaveFileName(
            self, "Exporter en PDF", default_name, "PDF Files (*.pdf)"
        )
        
        if file_path:
            try:
                # Préparer les données
                product_data = {
                    'name': self.product_name_edit.text(),
                    'category': self.product_category_edit.text(),
                    'description': self.product_description_edit.toPlainText()
                }
                
                specifications = self.spec_form.get_specifications()
                media_list = self.media_widget.get_media_list()
                
                # Générer le PDF
                PDFGenerator.generate_pdf(product_data, specifications, media_list, file_path)
                
                self.statusBar().showMessage(f"PDF exporté: {file_path}")
                QMessageBox.information(self, "Succès", f"PDF exporté avec succès!\n{file_path}")
                
                # Demander si l'utilisateur veut ouvrir le PDF
                reply = QMessageBox.question(self, "Ouvrir le PDF", "Voulez-vous ouvrir le PDF généré?")
                if reply == QMessageBox.Yes:
                    if os.name == 'nt':  # Windows
                        os.startfile(file_path)
                    elif os.name == 'posix':  # macOS et Linux
                        os.system(f'open "{file_path}"' if sys.platform == 'darwin' else f'xdg-open "{file_path}"')
                        
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export PDF: {str(e)}")
    
    def share_product(self):
        if not self.current_product_id:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord sauvegarder le produit!")
            return
        
        # Préparer les données pour le partage
        product_data = {
            'name': self.product_name_edit.text(),
            'category': self.product_category_edit.text(),
            'description': self.product_description_edit.toPlainText(),
            'specifications': self.spec_form.get_specifications()
        }
        
        media_list = self.media_widget.get_media_list()
        
        # Ouvrir la dialog de partage
        dialog = ShareDialog(product_data, media_list, self)
        dialog.exec_()

def main():
    app = QApplication(sys.argv)
    
    # Style de l'application
    app.setStyle('Fusion')
    
    # Palette de couleurs moderne
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)
    
    # Créer et afficher la fenêtre principale
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()