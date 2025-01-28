import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton,
    QVBoxLayout, QWidget, QDialog, QLabel, QLineEdit, QTextEdit, QFileDialog,
    QMessageBox, QComboBox, QHBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sqlite3

# Chemin de la base de données
DB_PATH = "database.db"
MEDIA_FOLDER = "roaming_saaadiya_resourcesses"

# Créer le dossier pour les médias s'il n'existe pas
if not os.path.exists(MEDIA_FOLDER):
    os.makedirs(MEDIA_FOLDER)

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Classe principale de l'application
class ProductManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Produits")
        self.setGeometry(100, 100, 1000, 600)

        # Widgets
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Description", "Catégorie", "Prix", "Actions"])
        self.table.setColumnWidth(5, 200)

        self.add_button = QPushButton("Ajouter un Produit")
        self.add_button.clicked.connect(self.show_add_product_dialog)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.add_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Charger les produits
        self.load_products()

    def load_products(self):
        self.table.setRowCount(0)
        conn = get_db_connection()
        produits = conn.execute("""
            SELECT p.id, p.nom, p.description, c.nom AS categorie
            FROM produits p
            LEFT JOIN categories c ON p.categorie_id = c.id
            WHERE p.deleted_at IS NULL
        """).fetchall()
        for produit in produits:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            # Afficher les informations du produit
            self.table.setItem(row_position, 0, QTableWidgetItem(str(produit["id"])))
            self.table.setItem(row_position, 1, QTableWidgetItem(produit["nom"]))
            self.table.setItem(row_position, 2, QTableWidgetItem(produit["description"]))
            self.table.setItem(row_position, 3, QTableWidgetItem(produit["categorie"] if produit["categorie"] else "Aucune"))

            # Afficher les prix
            prix = conn.execute("SELECT * FROM prix WHERE produit_id = ?", (produit["id"],)).fetchall()
            prix_text = ", ".join([f"{p['montant']} {p['devise']}" for p in prix])
            self.table.setItem(row_position, 4, QTableWidgetItem(prix_text))

            # Boutons d'actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)

            edit_button = QPushButton("Modifier")
            edit_button.clicked.connect(lambda _, id=produit["id"]: self.show_edit_product_dialog(id))
            actions_layout.addWidget(edit_button)

            delete_button = QPushButton("Supprimer")
            delete_button.clicked.connect(lambda _, id=produit["id"]: self.delete_product(id))
            actions_layout.addWidget(delete_button)

            view_button = QPushButton("Voir")
            view_button.clicked.connect(lambda _, id=produit["id"]: self.view_product(id))
            actions_layout.addWidget(view_button)

            actions_widget.setLayout(actions_layout)
            self.table.setCellWidget(row_position, 5, actions_widget)

        conn.close()

    def show_add_product_dialog(self):
        dialog = AddProductDialog(self)
        dialog.exec_()
        self.load_products()

    def show_edit_product_dialog(self, product_id):
        dialog = EditProductDialog(product_id, self)
        dialog.exec_()
        self.load_products()

    def delete_product(self, product_id):
        confirm = QMessageBox.question(self, "Confirmer", "Êtes-vous sûr de vouloir supprimer ce produit ?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            conn = get_db_connection()
            conn.execute("UPDATE produits SET deleted_at = ? WHERE id = ?", (datetime.now(), product_id))
            conn.commit()
            conn.close()
            self.load_products()

    def view_product(self, product_id):
        dialog = ViewProductDialog(product_id, self)
        dialog.exec_()

# Dialogue pour ajouter un produit
class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un Produit")
        self.setModal(True)

        # Widgets
        self.nom_input = QLineEdit()
        self.description_input = QTextEdit()
        self.categorie_input = QComboBox()
        self.load_categories()
        self.prix_input = QLineEdit()
        self.devise_input = QComboBox()
        self.devise_input.addItems(["USD", "EUR", "GBP"])
        self.media_input = QPushButton("Sélectionner des médias")
        self.media_input.clicked.connect(self.select_media)
        self.media_files = []

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nom:"))
        layout.addWidget(self.nom_input)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)
        layout.addWidget(QLabel("Catégorie:"))
        layout.addWidget(self.categorie_input)
        layout.addWidget(QLabel("Prix:"))
        layout.addWidget(self.prix_input)
        layout.addWidget(QLabel("Devise:"))
        layout.addWidget(self.devise_input)
        layout.addWidget(self.media_input)
        layout.addWidget(QLabel("Médias sélectionnés: Aucun"))

        self.submit_button = QPushButton("Ajouter")
        self.submit_button.clicked.connect(self.add_product)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def load_categories(self):
        conn = get_db_connection()
        categories = conn.execute("SELECT * FROM categories WHERE deleted_at IS NULL").fetchall()
        conn.close()
        self.categorie_input.clear()
        self.categorie_input.addItem("Aucune", None)
        for categorie in categories:
            self.categorie_input.addItem(categorie["nom"], categorie["id"])

    def select_media(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Sélectionner des médias", "", "Images (*.png *.jpg *.jpeg);;Vidéos (*.mp4 *.avi)")
        if files:
            self.media_files = files
            QMessageBox.information(self, "Médias sélectionnés", f"{len(files)} fichiers sélectionnés.")

    def add_product(self):
        nom = self.nom_input.text()
        description = self.description_input.toPlainText()
        categorie_id = self.categorie_input.currentData()
        prix = self.prix_input.text()
        devise = self.devise_input.currentText()

        if not nom or not prix:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produits (nom, description, categorie_id) VALUES (?, ?, ?)", (nom, description, categorie_id))
        product_id = cursor.lastrowid

        cursor.execute("INSERT INTO prix (montant, devise, produit_id) VALUES (?, ?, ?)", (float(prix), devise, product_id))

        for file in self.media_files:
            file_name = os.path.basename(file)
            destination = os.path.join(MEDIA_FOLDER, file_name)
            os.rename(file, destination)
            cursor.execute("INSERT INTO medias (chemin, type, produit_id) VALUES (?, ?, ?)",
                           (destination, "image" if file_name.lower().endswith((".png", ".jpg", ".jpeg")) else "video", product_id))

        conn.commit()
        conn.close()
        self.accept()

# Dialogue pour modifier un produit
class EditProductDialog(AddProductDialog):
    def __init__(self, product_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modifier un Produit")
        self.product_id = product_id

        conn = get_db_connection()
        produit = conn.execute("SELECT * FROM produits WHERE id = ?", (product_id,)).fetchone()
        prix = conn.execute("SELECT * FROM prix WHERE produit_id = ?", (product_id,)).fetchone()
        conn.close()

        self.nom_input.setText(produit["nom"])
        self.description_input.setText(produit["description"])
        self.categorie_input.setCurrentIndex(self.categorie_input.findData(produit["categorie_id"]))
        self.prix_input.setText(str(prix["montant"]))
        self.devise_input.setCurrentText(prix["devise"])

    def add_product(self):
        nom = self.nom_input.text()
        description = self.description_input.toPlainText()
        categorie_id = self.categorie_input.currentData()
        prix = self.prix_input.text()
        devise = self.devise_input.currentText()

        if not nom or not prix:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        conn = get_db_connection()
        conn.execute("UPDATE produits SET nom = ?, description = ?, categorie_id = ?, updated_at = ? WHERE id = ?",
                     (nom, description, categorie_id, datetime.now(), self.product_id))
        conn.execute("UPDATE prix SET montant = ?, devise = ? WHERE produit_id = ?",
                     (float(prix), devise, self.product_id))
        conn.commit()
        conn.close()
        self.accept()

# Dialogue pour voir un produit
class ViewProductDialog(QDialog):
    def __init__(self, product_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Détails du Produit")
        self.setModal(True)

        conn = get_db_connection()
        produit = conn.execute("""
            SELECT p.id, p.nom, p.description, c.nom AS categorie
            FROM produits p
            LEFT JOIN categories c ON p.categorie_id = c.id
            WHERE p.id = ?
        """, (product_id,)).fetchone()
        prix = conn.execute("SELECT * FROM prix WHERE produit_id = ?", (product_id,)).fetchone()
        medias = conn.execute("SELECT * FROM medias WHERE produit_id = ?", (product_id,)).fetchall()
        conn.close()

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Nom: {produit['nom']}"))
        layout.addWidget(QLabel(f"Description: {produit['description']}"))
        layout.addWidget(QLabel(f"Catégorie: {produit['categorie'] if produit['categorie'] else 'Aucune'}"))
        layout.addWidget(QLabel(f"Prix: {prix['montant']} {prix['devise']}"))

        for media in medias:
            if media["type"] == "image":
                pixmap = QPixmap(media["chemin"])
                label = QLabel()
                label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
                layout.addWidget(label)
            else:
                layout.addWidget(QLabel(f"Vidéo: {media['chemin']}"))

        self.setLayout(layout)

# Exécution de l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductManagementApp()
    window.show()
    sys.exit(app.exec_())

    