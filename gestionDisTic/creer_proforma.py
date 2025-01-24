import sys
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QLabel, QMessageBox, QFileDialog, QTextEdit, QComboBox, QHBoxLayout, QFormLayout, QInputDialog,
    QListWidget, QListWidgetItem, QDialog, QDateEdit, QCheckBox, QGroupBox
)

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox, QGroupBox, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtSql import QSqlQuery

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox, QGroupBox, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QColor, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QPixmap, QColor
from openpyxl import load_workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

from PyQt5.QtGui import QIcon

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtSql import QSqlQuery

class EditModeleModal(QDialog):
    def __init__(self, modele_id, parent=None):
        super().__init__(parent)
        self.modele_id = modele_id
        self.setWindowTitle("Éditer un Modèle")
        self.layout = QVBoxLayout(self)

        # Champ pour le nom du modèle
        self.nom_input = QLineEdit()
        self.layout.addWidget(QLabel("Nom du Modèle:"))
        self.layout.addWidget(self.nom_input)

        # Champ pour le contenu du modèle
        self.contenu_input = QTextEdit()
        self.layout.addWidget(QLabel("Contenu du Modèle:"))
        self.layout.addWidget(self.contenu_input)

        # Boutons pour enregistrer ou annuler
        button_layout = QHBoxLayout()

        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(self.save_modele)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("Annuler")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        self.layout.addLayout(button_layout)

        # Charger les informations du modèle
        self.load_modele()

    def load_modele(self):
        query = QSqlQuery()
        query.prepare("SELECT nom, contenu FROM modeles_proforma WHERE id = ?")
        query.addBindValue(self.modele_id)
        if query.exec() and query.next():
            nom = query.value(0)
            contenu = query.value(1)

            # Afficher les informations du modèle
            self.nom_input.setText(nom)
            self.contenu_input.setText(contenu)
        else:
            QMessageBox.critical(self, "Erreur", "Impossible de charger les informations du modèle")

    def save_modele(self):
        nom = self.nom_input.text()
        contenu = self.contenu_input.toPlainText()

        if not nom or not contenu:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")
            return

        query = QSqlQuery()
        query.prepare("UPDATE modeles_proforma SET nom = ?, contenu = ? WHERE id = ?")
        query.addBindValue(nom)
        query.addBindValue(contenu)
        query.addBindValue(self.modele_id)
        if not query.exec():
            QMessageBox.critical(self, "Erreur", "Impossible de mettre à jour le modèle")
        else:
            QMessageBox.information(self, "Succès", "Modèle mis à jour avec succès")
            self.parent().load_modeles()  # Recharger la liste des modèles dans la fenêtre principale
            self.close()


class GestionPiecesJointesModal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestion des Pièces Jointes")
        self.layout = QVBoxLayout(self)

        # Liste des pièces jointes
        self.pieces_jointes_list = QListWidget()
        self.layout.addWidget(self.pieces_jointes_list)

        # Boutons pour ajouter, modifier, supprimer et affecter des pièces jointes
        button_layout = QHBoxLayout()

        add_button = QPushButton("Ajouter")
        add_button.clicked.connect(self.add_piece_jointe)
        button_layout.addWidget(add_button)

        edit_button = QPushButton("Modifier")
        edit_button.clicked.connect(self.edit_piece_jointe)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Supprimer")
        delete_button.clicked.connect(self.delete_piece_jointe)
        button_layout.addWidget(delete_button)

        affect_button = QPushButton("Affecter au Modèle de Mail")
        affect_button.clicked.connect(self.affect_piece_jointe)
        button_layout.addWidget(affect_button)

        self.layout.addLayout(button_layout)

        # Charger les pièces jointes existantes
        self.load_pieces_jointes()

    def load_pieces_jointes(self):
        self.pieces_jointes_list.clear()
        query = QSqlQuery("SELECT id, nom FROM pieces_jointes")
        while query.next():
            item = QListWidgetItem(query.value(1))
            item.setData(Qt.UserRole, query.value(0))  # Stocker l'ID de la pièce jointe
            self.pieces_jointes_list.addItem(item)

    def add_piece_jointe(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Ajouter une pièce jointe", "", "Tous les fichiers (*)")
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    fichier = file.read()
                    nom = os.path.basename(file_path)

                    query = QSqlQuery()
                    query.prepare("INSERT INTO pieces_jointes (nom, fichier) VALUES (?, ?)")
                    query.addBindValue(nom)
                    query.addBindValue(fichier)
                    if not query.exec():
                        raise Exception("Erreur lors de l'ajout de la pièce jointe")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", str(e))
            else:
                self.load_pieces_jointes()

    def edit_piece_jointe(self):
        selected_item = self.pieces_jointes_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une pièce jointe")
            return

        piece_jointe_id = selected_item.data(Qt.UserRole)
        file_path, _ = QFileDialog.getOpenFileName(self, "Modifier la pièce jointe", "", "Tous les fichiers (*)")
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    fichier = file.read()
                    nom = os.path.basename(file_path)

                    query = QSqlQuery()
                    query.prepare("UPDATE pieces_jointes SET nom = ?, fichier = ? WHERE id = ?")
                    query.addBindValue(nom)
                    query.addBindValue(fichier)
                    query.addBindValue(piece_jointe_id)
                    if not query.exec():
                        raise Exception("Erreur lors de la modification de la pièce jointe")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", str(e))
            else:
                self.load_pieces_jointes()

    def delete_piece_jointe(self):
        selected_item = self.pieces_jointes_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une pièce jointe")
            return

        piece_jointe_id = selected_item.data(Qt.UserRole)
        reply = QMessageBox.question(self, "Supprimer", "Êtes-vous sûr de vouloir supprimer cette pièce jointe ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                query = QSqlQuery()
                query.prepare("DELETE FROM pieces_jointes WHERE id = ?")
                query.addBindValue(piece_jointe_id)
                if not query.exec():
                    raise Exception("Erreur lors de la suppression de la pièce jointe")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", str(e))
            else:
                self.load_pieces_jointes()

    def affect_piece_jointe(self):
        selected_item = self.pieces_jointes_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une pièce jointe")
            return

        piece_jointe_id = selected_item.data(Qt.UserRole)
        try:
            query = QSqlQuery()
            query.prepare("UPDATE parametres SET piece_jointe_id = ? WHERE id = 1")
            query.addBindValue(piece_jointe_id)
            if not query.exec():
                raise Exception("Erreur lors de l'affectation de la pièce jointe")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))
        else:
            QMessageBox.information(self, "Succès", "Pièce jointe affectée avec succès")


class SendProformaModal(QDialog):
    def __init__(self, proforma_id, parent=None):
        super().__init__(parent)
        self.proforma_id = proforma_id
        self.setWindowTitle("Envoyer Proforma par Mail")
        self.layout = QVBoxLayout(self)

        # Champ pour le sujet du mail
        self.sujet_input = QLineEdit()
        self.sujet_input.setPlaceholderText("Sujet du mail")
        self.layout.addWidget(self.sujet_input)

        # Champ pour le corps du mail
        self.corps_input = QTextEdit()
        self.corps_input.setPlaceholderText("Corps du mail")
        self.layout.addWidget(self.corps_input)

        # Bouton pour envoyer le mail
        send_button = QPushButton("Envoyer")
        send_button.clicked.connect(self.send_mail)
        self.layout.addWidget(send_button)

    def send_mail(self):
        sujet = self.sujet_input.text()
        corps = self.corps_input.toPlainText()

        if not sujet or not corps:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir le sujet et le corps du mail")
            return

        # Récupérer l'email du contact à partir du proforma
        contact_email = self.get_contact_email()
        if not contact_email:
            return  # If email could not be retrieved, the method exits early

        # Récupérer la pièce jointe si elle existe
        piece_jointe_info = self.get_attachment()
        if piece_jointe_info is None:
            return  # If no attachment found, method exits

        # Envoyer l'email
        try:
            self.send_email(contact_email, sujet, corps, piece_jointe_info)
            QMessageBox.information(self, "Succès", "Email envoyé avec succès")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'envoi de l'email: {e}")

    def get_contact_email(self):
        """Récupère l'email du contact lié au proforma."""
        query = QSqlQuery()
        query.prepare("SELECT contact_id FROM proformas WHERE id = ?")
        query.addBindValue(self.proforma_id)
        if not query.exec() or not query.next():
            QMessageBox.critical(self, "Erreur", "Impossible de récupérer les informations du proforma")
            return None

        contact_id = query.value(0)
        query.prepare("SELECT email FROM contacts WHERE id = ?")
        query.addBindValue(contact_id)
        if not query.exec() or not query.next():
            QMessageBox.critical(self, "Erreur", "Impossible de récupérer l'email du contact")
            return None

        return query.value(0)

    def get_attachment(self):
        """Récupère la pièce jointe affectée au modèle de mail."""
        query = QSqlQuery()
        query.prepare("SELECT piece_jointe_id FROM parametres WHERE id = 1")
        if not query.exec() or not query.next():
            QMessageBox.critical(self, "Erreur", "Impossible de récupérer la pièce jointe affectée")
            return None

        piece_jointe_id = query.value(0)
        if piece_jointe_id:
            query.prepare("SELECT nom, fichier FROM pieces_jointes WHERE id = ?")
            query.addBindValue(piece_jointe_id)
            if not query.exec() or not query.next():
                QMessageBox.critical(self, "Erreur", "Impossible de récupérer la pièce jointe")
                return None

            return query.value(0), query.value(1)  # Return name and file content of attachment
        return None

    def send_email(self, to_email, subject, body, attachment_info=None):
        """Envoie un email avec ou sans pièce jointe."""
        msg = MIMEMultipart()
        msg['From'] = self.parent().email_entreprise_input.text()  # Assuming parent has email input
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachment_info:
            # Attach the file if there's one
            file_name, file_data = attachment_info
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file_data)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={file_name}')
            msg.attach(part)

        # Send the email via SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.parent().email_entreprise_input.text(), "votre_mot_de_passe")  # Replace with actual password
        server.send_message(msg)
        server.quit()



class AddContactModal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un Contact")
        
        # Create layout
        self.layout = QFormLayout(self)

        # Input fields for contact details
        self.name_input = QLineEdit()
        self.phone_number_input = QLineEdit()
        self.email_input = QLineEdit()
        self.category_input = QLineEdit()
        self.description_input = QLineEdit()
        self.note_input = QLineEdit()

        # Add input fields to the form layout
        self.layout.addRow("Nom:", self.name_input)
        self.layout.addRow("Téléphone:", self.phone_number_input)
        self.layout.addRow("Email:", self.email_input)
        self.layout.addRow("Catégorie:", self.category_input)
        self.layout.addRow("Description:", self.description_input)
        self.layout.addRow("Note:", self.note_input)

        # Save button for saving the new contact
        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.save_contact)
        self.layout.addRow(self.save_button)

    def save_contact(self):
        # Get data from input fields
        name = self.name_input.text()
        phone_number = self.phone_number_input.text()
        email = self.email_input.text()
        category = self.category_input.text()
        description = self.description_input.text()
        note = self.note_input.text()

        # Validate the required fields
        if not name:
            QMessageBox.warning(self, "Erreur", "Le nom est obligatoire")
            return

        # Prepare the SQL query to insert the new contact
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO contacts (name, phone_number, email, category, description, note) 
            VALUES (?, ?, ?, ?, ?, ?)
        """)
        query.addBindValue(name)
        query.addBindValue(phone_number)
        query.addBindValue(email)
        query.addBindValue(category)
        query.addBindValue(description)
        query.addBindValue(note)

        # Execute the query and handle success or failure
        if not query.exec():
            QMessageBox.critical(self, "Erreur", "Impossible d'ajouter le contact")
        else:
            # Reload the contact list after adding the new contact
            self.parent().load_contacts()
            self.close()

class EditContactModal(QDialog):
    def __init__(self, contact_id, parent=None):
        super().__init__(parent)
        self.contact_id = contact_id
        self.setWindowTitle("Éditer un Contact")
        
        # Create layout
        self.layout = QFormLayout(self)

        # Input fields for contact details
        self.name_input = QLineEdit()
        self.phone_number_input = QLineEdit()
        self.email_input = QLineEdit()
        self.category_input = QLineEdit()
        self.description_input = QLineEdit()
        self.note_input = QLineEdit()

        # Add input fields to layout
        self.layout.addRow("Nom:", self.name_input)
        self.layout.addRow("Téléphone:", self.phone_number_input)
        self.layout.addRow("Email:", self.email_input)
        self.layout.addRow("Catégorie:", self.category_input)
        self.layout.addRow("Description:", self.description_input)
        self.layout.addRow("Note:", self.note_input)

        # Save button for saving contact changes
        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.save_contact)
        self.layout.addRow(self.save_button)

        # Load contact details to populate fields
        self.load_contact()

    def load_contact(self):
        # Query to fetch the contact details from the database
        query = QSqlQuery()
        query.prepare("SELECT name, phone_number, email, category, description, note FROM contacts WHERE id = ?")
        query.addBindValue(self.contact_id)
        
        if query.exec() and query.next():
            # Populate input fields with the retrieved contact details
            self.name_input.setText(query.value(0))
            self.phone_number_input.setText(query.value(1))
            self.email_input.setText(query.value(2))
            self.category_input.setText(query.value(3))
            self.description_input.setText(query.value(4))
            self.note_input.setText(query.value(5))

    def save_contact(self):
        # Get data from input fields
        name = self.name_input.text()
        phone_number = self.phone_number_input.text()
        email = self.email_input.text()
        category = self.category_input.text()
        description = self.description_input.text()
        note = self.note_input.text()

        # Validate the required fields
        if not name:
            QMessageBox.warning(self, "Erreur", "Le nom est obligatoire")
            return

        # Prepare the SQL query to update the contact details
        query = QSqlQuery()
        query.prepare("""
            UPDATE contacts 
            SET name = ?, phone_number = ?, email = ?, category = ?, description = ?, note = ? 
            WHERE id = ?
        """)
        query.addBindValue(name)
        query.addBindValue(phone_number)
        query.addBindValue(email)
        query.addBindValue(category)
        query.addBindValue(description)
        query.addBindValue(note)
        query.addBindValue(self.contact_id)

        # Execute the query and handle success or failure
        if not query.exec():
            QMessageBox.critical(self, "Erreur", "Impossible de mettre à jour le contact")
        else:
            # Reload the contact list after the update
            self.parent().load_contacts()
            self.close()

class ImportModeleModal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Importer un Modèle")
        
        # Create layout
        self.layout = QVBoxLayout(self)

        # File selection label and button
        self.file_label = QLabel("Sélectionner un fichier HTML/CSS:")
        self.layout.addWidget(self.file_label)

        self.file_button = QPushButton("Parcourir...")
        self.file_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.file_button)

        # Input field for model name
        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Nom du modèle")
        self.layout.addWidget(self.nom_input)

        # Import button
        self.save_button = QPushButton("Importer")
        self.save_button.clicked.connect(self.import_modele)
        self.layout.addWidget(self.save_button)

        self.file_path = ""  # Initialize file_path as empty string

    def select_file(self):
        # Open file dialog to select HTML or CSS file
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier HTML/CSS", "", "HTML Files (*.html);;CSS Files (*.css)")

    def import_modele(self):
        # Ensure that a file has been selected
        if not self.file_path:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un fichier")
            return

        # Ensure the model name is provided
        nom = self.nom_input.text()
        if not nom:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom pour le modèle")
            return

        # Read the contents of the selected file
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                contenu = file.read()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la lecture du fichier : {str(e)}")
            return

        # Insert the model into the database
        query = QSqlQuery()
        query.prepare("INSERT INTO modeles_proforma (nom, contenu) VALUES (?, ?)")
        query.addBindValue(nom)
        query.addBindValue(contenu)

        if not query.exec():
            QMessageBox.critical(self, "Erreur", "Impossible d'importer le modèle")
        else:
            # Notify parent to reload models
            self.parent().load_modeles()
            self.close()


class ShowContactModal(QDialog):
    def __init__(self, contact_id, parent=None):
        super().__init__(parent)
        self.contact_id = contact_id
        self.setWindowTitle("Détails du Contact")
        
        # Create layout and widgets
        self.layout = QFormLayout(self)
        
        self.name_label = QLabel()
        self.phone_number_label = QLabel()
        self.email_label = QLabel()
        self.category_label = QLabel()
        self.description_label = QLabel()
        self.note_label = QLabel()

        # Add rows to layout
        self.layout.addRow("Nom:", self.name_label)
        self.layout.addRow("Téléphone:", self.phone_number_label)
        self.layout.addRow("Email:", self.email_label)
        self.layout.addRow("Catégorie:", self.category_label)
        self.layout.addRow("Description:", self.description_label)
        self.layout.addRow("Note:", self.note_label)

        # Load the contact details from the database
        self.load_contact()

    def load_contact(self):
        # Prepare and execute the SQL query to fetch the contact data
        query = QSqlQuery()
        query.prepare("SELECT name, phone_number, email, category, description, note FROM contacts WHERE id = ?")
        query.addBindValue(self.contact_id)

        if query.exec() and query.next():
            # Populate the labels with the fetched data
            self.name_label.setText(query.value(0))
            self.phone_number_label.setText(query.value(1))
            self.email_label.setText(query.value(2))
            self.category_label.setText(query.value(3))
            self.description_label.setText(query.value(4))
            self.note_label.setText(query.value(5))



class ProformaGenerator:
    @staticmethod
    def generate_proforma(contact, modele, output_path):
        """
        Génère un proforma à partir d'un modèle et des informations de contact.

        :param contact: Dictionnaire contenant les informations du contact (nom, email, téléphone).
        :param modele: Identifiant du modèle à utiliser pour générer le proforma.
        :param output_path: Chemin de sortie pour enregistrer le fichier proforma généré.
        """
        # Vérification des informations de contact
        if not all(key in contact for key in ["name", "email", "phone_number"]):
            raise ValueError("Les informations du contact sont incomplètes.")

        # Récupérer le contenu du modèle depuis la base de données
        template = ProformaGenerator._get_template_from_db(modele)
        if not template:
            raise Exception(f"Modèle avec ID {modele} non trouvé dans la base de données.")

        # Remplacer les placeholders dans le template
        template = ProformaGenerator._replace_placeholders(template, contact)

        # Enregistrer le proforma généré dans le fichier de sortie
        ProformaGenerator._save_proforma(output_path, template)

    @staticmethod
    def _get_template_from_db(modele):
        """
        Récupère le contenu du modèle de proforma depuis la base de données.

        :param modele: Identifiant du modèle à récupérer.
        :return: Le contenu du modèle sous forme de chaîne, ou None si le modèle n'est pas trouvé.
        """
        query = QSqlQuery()
        query.prepare("SELECT contenu FROM modeles_proforma WHERE id = ?")
        query.addBindValue(modele)
        if query.exec() and query.next():
            return query.value(0)
        return None

    @staticmethod
    def _replace_placeholders(template, contact):
        """
        Remplace les placeholders dans le template par les informations de contact.

        :param template: Le contenu du modèle avec des placeholders.
        :param contact: Dictionnaire contenant les informations du contact.
        :return: Le template avec les placeholders remplacés.
        """
        # Utilisation des f-strings pour un remplacement plus lisible
        return template.format(
            nom=contact["name"],
            email=contact["email"],
            telephone=contact["phone_number"],
            date=QDate.currentDate().toString("yyyy-MM-dd")
        )

    @staticmethod
    def _save_proforma(output_path, content):
        """
        Enregistre le proforma généré dans un fichier.

        :param output_path: Chemin du fichier de sortie.
        :param content: Contenu du proforma à enregistrer.
        """
        # Vérifier si le répertoire existe, sinon le créer
        directory = os.path.dirname(output_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Enregistrer le contenu dans le fichier de sortie
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)


class AddContactModal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un Contact")
        
        # Create layout
        self.layout = QFormLayout(self)

        # Input fields for contact details
        self.name_input = QLineEdit()
        self.phone_number_input = QLineEdit()
        self.email_input = QLineEdit()
        self.category_input = QLineEdit()
        self.description_input = QLineEdit()
        self.note_input = QLineEdit()

        # Add input fields to the form layout
        self.layout.addRow("Nom:", self.name_input)
        self.layout.addRow("Téléphone:", self.phone_number_input)
        self.layout.addRow("Email:", self.email_input)
        self.layout.addRow("Catégorie:", self.category_input)
        self.layout.addRow("Description:", self.description_input)
        self.layout.addRow("Note:", self.note_input)

        # Save button for saving the new contact
        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.save_contact)
        self.layout.addRow(self.save_button)

    def save_contact(self):
        # Get data from input fields
        name = self.name_input.text()
        phone_number = self.phone_number_input.text()
        email = self.email_input.text()
        category = self.category_input.text()
        description = self.description_input.text()
        note = self.note_input.text()

        # Validate the required fields
        if not name:
            QMessageBox.warning(self, "Erreur", "Le nom est obligatoire")
            return

        # Prepare the SQL query to insert the new contact
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO contacts (name, phone_number, email, category, description, note) 
            VALUES (?, ?, ?, ?, ?, ?)
        """)
        query.addBindValue(name)
        query.addBindValue(phone_number)
        query.addBindValue(email)
        query.addBindValue(category)
        query.addBindValue(description)
        query.addBindValue(note)

        # Execute the query and handle success or failure
        if not query.exec():
            QMessageBox.critical(self, "Erreur", "Impossible d'ajouter le contact")
        else:
            # Reload the contact list after adding the new contact
            self.parent().load_contacts()
            self.close()
class ShowVersionsModal(QDialog):
    def __init__(self, modele_id, parent=None):
        super().__init__(parent)
        self.modele_id = modele_id
        self.setWindowTitle("Versions du Modèle")
        self.layout = QVBoxLayout(self)

        # Tableau pour afficher les versions
        self.versions_table = QTableWidget()
        self.versions_table.setColumnCount(3)
        self.versions_table.setHorizontalHeaderLabels(["Version ID", "Date", "Contenu"])
        self.versions_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.versions_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.versions_table)

        # Boutons pour charger ou fermer
        button_layout = QHBoxLayout()

        load_button = QPushButton("Charger la Version")
        load_button.clicked.connect(self.load_selected_version)
        button_layout.addWidget(load_button)

        close_button = QPushButton("Fermer")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)

        self.layout.addLayout(button_layout)

        # Charger les versions du modèle
        self.load_versions()

    def load_versions(self):
        query = QSqlQuery()
        query.prepare("SELECT id, date_created, contenu FROM modeles_versions WHERE modele_id = ? ORDER BY date_created DESC")
        query.addBindValue(self.modele_id)

        if query.exec():
            self.versions_table.setRowCount(0)  # Clear table
            while query.next():
                row_position = self.versions_table.rowCount()
                self.versions_table.insertRow(row_position)

                version_id = query.value(0)
                date_created = query.value(1)
                contenu = query.value(2)

                self.versions_table.setItem(row_position, 0, QTableWidgetItem(str(version_id)))
                self.versions_table.setItem(row_position, 1, QTableWidgetItem(date_created))
                self.versions_table.setItem(row_position, 2, QTableWidgetItem(contenu[:50] + "..."))  # Display a preview
        else:
            QMessageBox.critical(self, "Erreur", "Impossible de charger les versions")

    def load_selected_version(self):
        selected_row = self.versions_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une version")
            return

        version_id = self.versions_table.item(selected_row, 0).text()

        # Charger les détails de la version sélectionnée
        query = QSqlQuery()
        query.prepare("SELECT contenu FROM modeles_versions WHERE id = ?")
        query.addBindValue(version_id)

        if query.exec() and query.next():
            contenu = query.value(0)
            QMessageBox.information(self, "Version Chargée", f"Contenu de la version:\n\n{contenu}")
        else:
            QMessageBox.critical(self, "Erreur", "Impossible de charger cette version")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion de Proformas")
        self.setGeometry(100, 100, 1200, 900)

        # Initialisation de la base de données
        self.init_db()

        # Création des onglets
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Onglet Gestion des Contacts
        self.contacts_tab = QWidget()
        self.tabs.addTab(self.contacts_tab, "Contacts")
        self.init_contacts_tab()

        # Onglet Création de Proformas
        self.proformas_tab = QWidget()
        self.tabs.addTab(self.proformas_tab, "Créer Proforma")
        self.init_proformas_tab()

        # Onglet Gestion des Modèles
        self.modeles_tab = QWidget()
        self.tabs.addTab(self.modeles_tab, "Modèles")
        self.init_modeles_tab()

        # Onglet Paramètres
        self.settings_tab = QWidget()
        self.tabs.addTab(self.settings_tab, "Paramètres")
        self.init_settings_tab()

        # Appliquer des styles CSS modernes
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                background-color: #fff;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border-radius: 4px;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTableWidget {
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit, QTextEdit, QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
                font-size: 14px;
            }
            QDialog {
                background-color: #fff;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                font-size: 14px;
            }
        """)
        self.add_contact_button = QPushButton("add contact")
        self.import_modele_button = QPushButton("import button")

        self.set_default_modele_button = QPushButton("import button")
        self.send_proforma_button = QPushButton("import button")

        self.show_versions_button = QPushButton("import button")
 # Ajouter des icônes aux boutons
        self.add_contact_button.setIcon(QIcon("icons/add_contact.png"))
        self.import_modele_button.setIcon(QIcon("icons/import_modele.png"))
        self.set_default_modele_button.setIcon(QIcon("icons/default_modele.png"))
        self.send_proforma_button.setIcon(QIcon("icons/send_proforma.png"))
        self.show_versions_button.setIcon(QIcon("icons/show_versions.png"))

        # Ajouter des animations
        self.add_contact_button.setStyleSheet("QPushButton { transition: background-color 0.3s; }")
        self.import_modele_button.setStyleSheet("QPushButton { transition: background-color 0.3s; }")
        self.set_default_modele_button.setStyleSheet("QPushButton { transition: background-color 0.3s; }")
        self.send_proforma_button.setStyleSheet("QPushButton { transition: background-color 0.3s; }")
        self.show_versions_button.setStyleSheet("QPushButton { transition: background-color 0.3s; }")


        self.filter_date_input = QDateEdit()
        self.filter_date_input.setDate(QDate.currentDate())
        self.filter_status_combo = QComboBox()
        self.filter_status_combo.addItems(["Tous", "En attente", "Validé", "Rejeté"])

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filtrer par date:"))
        filter_layout.addWidget(self.filter_date_input)
        filter_layout.addWidget(QLabel("Filtrer par statut:"))
        filter_layout.addWidget(self.filter_status_combo)

        filter_button = QPushButton("Filtrer")
        filter_button.clicked.connect(self.filter_proformas)
        filter_layout.addWidget(filter_button)

        self.proformas_tab.layout().addLayout(filter_layout)
       # Bouton pour afficher les versions d'un proforma
        self.show_versions_button = QPushButton("Afficher les Versions")
        self.show_versions_button.clicked.connect(self.open_show_versions_modal)
        self.proformas_tab.layout().addWidget(self.show_versions_button)
        # Bouton pour gérer les pièces jointes
        self.gestion_pieces_jointes_button = QPushButton("Gérer les Pièces Jointes")
        self.gestion_pieces_jointes_button.clicked.connect(self.open_gestion_pieces_jointes_modal)
        self.settings_tab.layout().addWidget(self.gestion_pieces_jointes_button)

    def open_gestion_pieces_jointes_modal(self):
        self.gestion_pieces_jointes_modal = GestionPiecesJointesModal(self)
        self.gestion_pieces_jointes_modal.exec_()
    def open_show_versions_modal(self):
        selected_row = self.proformas_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un proforma")
            return

        proforma_id = self.proformas_table.item(selected_row, 0).data(0)
        self.show_versions_modal = ShowVersionsModal(proforma_id, self)
        self.show_versions_modal.exec_()

    def filter_proformas(self):
        date_filter = self.filter_date_input.date().toString("yyyy-MM-dd")
        status_filter = self.filter_status_combo.currentText()

        query = QSqlQuery()
        if status_filter == "Tous":
            query.prepare("SELECT id, contact_id, modele_id, date_creation, contenu FROM proformas WHERE date_creation = ?")
            query.addBindValue(date_filter)
        else:
            query.prepare("SELECT id, contact_id, modele_id, date_creation, contenu FROM proformas WHERE date_creation = ? AND statut = ?")
            query.addBindValue(date_filter)
            query.addBindValue(status_filter)

        if not query.exec():
            QMessageBox.critical(self, "Erreur", "Impossible de filtrer les proformas")
            return

        self.proformas_table.setRowCount(0)
        while query.next():
            row = self.proformas_table.rowCount()
            self.proformas_table.insertRow(row)
            for col in range(4):
                self.proformas_table.setItem(row, col, QTableWidgetItem(query.value(col + 1)))

            # Ajouter les boutons d'action
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)

            edit_button = QPushButton("Éditer")
            edit_button.clicked.connect(lambda _, id=query.value(0): self.open_edit_proforma_modal(id))
            action_layout.addWidget(edit_button)

            delete_button = QPushButton("Supprimer")
            delete_button.clicked.connect(lambda _, id=query.value(0): self.delete_proforma(id))
            action_layout.addWidget(delete_button)

            show_button = QPushButton("Afficher")
            show_button.clicked.connect(lambda _, id=query.value(0): self.open_show_proforma_modal(id))
            action_layout.addWidget(show_button)

            self.proformas_table.setCellWidget(row, 4, action_widget)
    def init_db(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        db_path = os.path.join(os.getenv('APPDATA'), 'saadiya', 'ressources', 'proformas1.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db.setDatabaseName(db_path)
        if not self.db.open():
            QMessageBox.critical(self, "Erreur", "Impossible d'ouvrir la base de données")
            sys.exit(1)

        # Création des tables si elles n'existent pas
        query = QSqlQuery()
        query.exec("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone_number TEXT,
                email TEXT,
                category TEXT,
                description TEXT,
                note TEXT
            )
        """)
        query.exec("""
            CREATE TABLE IF NOT EXISTS proformas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER,
                modele_id INTEGER,
                date_creation DATE,
                contenu TEXT,
                FOREIGN KEY (contact_id) REFERENCES contacts(id),
                FOREIGN KEY (modele_id) REFERENCES modeles_proforma(id)
            )
        """)
        query.exec("""
            CREATE TABLE IF NOT EXISTS modeles_proforma (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                contenu TEXT,
                est_par_defaut BOOLEAN DEFAULT 0
            )
        """)
        query.exec("""
            CREATE TABLE IF NOT EXISTS parametres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                logo_entreprise BLOB,
                nom_entreprise TEXT,
                adresse_entreprise TEXT,
                telephone_entreprise TEXT,
                email_entreprise TEXT,
                modele_message TEXT
            )
        """)
        query.exec("""
            CREATE TABLE IF NOT EXISTS pieces_jointes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                fichier BLOB
            )
        """)

    def init_contacts_tab(self):
        layout = QVBoxLayout()

        # Bouton pour ajouter un contact
        add_button = QPushButton("Ajouter Contact")
        add_button.clicked.connect(self.open_add_contact_modal)
        layout.addWidget(add_button)

        # Tableau pour afficher les contacts
        self.contacts_table = QTableWidget()
        self.contacts_table.setColumnCount(7)
        self.contacts_table.setHorizontalHeaderLabels(["Nom", "Téléphone", "Email", "Catégorie", "Description", "Note", "Actions"])
        layout.addWidget(self.contacts_table)

        self.contacts_tab.setLayout(layout)
        self.load_contacts()

    def open_add_contact_modal(self):
        self.add_contact_modal = AddContactModal(self)
        self.add_contact_modal.exec_()

    def load_contacts(self):
        self.contacts_table.setRowCount(0)
        query = QSqlQuery("SELECT id, name, phone_number, email, category, description, note FROM contacts")
        while query.next():
            row = self.contacts_table.rowCount()
            self.contacts_table.insertRow(row)
            for col in range(6):
                self.contacts_table.setItem(row, col, QTableWidgetItem(query.value(col + 1)))

            # Ajouter les boutons d'action
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)

            edit_button = QPushButton("Éditer")
            edit_button.clicked.connect(lambda _, id=query.value(0): self.open_edit_contact_modal(id))
            action_layout.addWidget(edit_button)

            delete_button = QPushButton("Supprimer")
            delete_button.clicked.connect(lambda _, id=query.value(0): self.delete_contact(id))
            action_layout.addWidget(delete_button)

            show_button = QPushButton("Afficher")
            show_button.clicked.connect(lambda _, id=query.value(0): self.open_show_contact_modal(id))
            action_layout.addWidget(show_button)

            self.contacts_table.setCellWidget(row, 6, action_widget)

    def open_edit_contact_modal(self, contact_id):
        self.edit_contact_modal = EditContactModal(contact_id, self)
        self.edit_contact_modal.exec_()

    def delete_contact(self, contact_id):
        reply = QMessageBox.question(self, "Supprimer Contact", "Êtes-vous sûr de vouloir supprimer ce contact ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            query = QSqlQuery()
            query.prepare("DELETE FROM contacts WHERE id = ?")
            query.addBindValue(contact_id)
            if not query.exec():
                QMessageBox.critical(self, "Erreur", "Impossible de supprimer le contact")
            else:
                self.load_contacts()

    def open_show_contact_modal(self, contact_id):
        self.show_contact_modal = ShowContactModal(contact_id, self)
        self.show_contact_modal.exec_()

    def init_proformas_tab(self):
        layout = QVBoxLayout()

        # Sélection du contact
        self.contact_combo = QComboBox()
        self.load_contacts_combo()
        layout.addWidget(QLabel("Sélectionner un contact:"))
        layout.addWidget(self.contact_combo)

        # Sélection du modèle de proforma
        self.modele_combo = QComboBox()
        self.load_modeles_combo()
        layout.addWidget(QLabel("Sélectionner un modèle de proforma:"))
        layout.addWidget(self.modele_combo)

        # Bouton pour générer le proforma
        generate_button = QPushButton("Générer Proforma")
        generate_button.clicked.connect(self.generate_proforma)
        layout.addWidget(generate_button)

        self.proformas_tab.setLayout(layout)

    def load_contacts_combo(self):
        self.contact_combo.clear()
        query = QSqlQuery("SELECT id, name FROM contacts")
        while query.next():
            self.contact_combo.addItem(query.value(1), query.value(0))

    def load_modeles_combo(self):
        self.modele_combo.clear()
        query = QSqlQuery("SELECT id, nom FROM modeles_proforma")
        while query.next():
            self.modele_combo.addItem(query.value(1), query.value(0))

    def generate_proforma(self):
        contact_id = self.contact_combo.currentData()
        modele_id = self.modele_combo.currentData()

        if not contact_id or not modele_id:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un contact et un modèle")
            return

        # Récupérer les informations du contact
        query = QSqlQuery()
        query.prepare("SELECT name, phone_number, email FROM contacts WHERE id = ?")
        query.addBindValue(contact_id)
        if not query.exec() or not query.next():
            QMessageBox.critical(self, "Erreur", "Impossible de récupérer les informations du contact")
            return

        contact = {
            "name": query.value(0),
            "phone_number": query.value(1),
            "email": query.value(2)
        }

        # Générer le proforma
        output_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le Proforma", "", "HTML Files (*.html)")
        if not output_path:
            return

        try:
            ProformaGenerator.generate_proforma(contact, modele_id, output_path)
            QMessageBox.information(self, "Succès", "Proforma généré avec succès")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération du proforma: {e}")

    def init_modeles_tab(self):
        layout = QVBoxLayout()

        # Bouton pour importer un modèle
        import_button = QPushButton("Importer Modèle")
        import_button.clicked.connect(self.open_import_modele_modal)
        layout.addWidget(import_button)

        # Liste des modèles
        self.modeles_table = QTableWidget()
        self.modeles_table.setColumnCount(3)
        self.modeles_table.setHorizontalHeaderLabels(["Nom", "Par Défaut", "Actions"])
        layout.addWidget(self.modeles_table)

        self.modeles_tab.setLayout(layout)
        self.load_modeles()

    def open_import_modele_modal(self):
        self.import_modele_modal = ImportModeleModal(self)
        self.import_modele_modal.exec_()

    def load_modeles(self):
        self.modeles_table.setRowCount(0)
        query = QSqlQuery("SELECT id, nom, est_par_defaut FROM modeles_proforma")
        while query.next():
            row = self.modeles_table.rowCount()
            self.modeles_table.insertRow(row)
            self.modeles_table.setItem(row, 0, QTableWidgetItem(query.value(1)))
            self.modeles_table.setItem(row, 1, QTableWidgetItem("Oui" if query.value(2) else "Non"))

            # Ajouter les boutons d'action
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)

            edit_button = QPushButton("Éditer")
            edit_button.clicked.connect(lambda _, id=query.value(0): self.open_edit_modele_modal(id))
            action_layout.addWidget(edit_button)

            delete_button = QPushButton("Supprimer")
            delete_button.clicked.connect(lambda _, id=query.value(0): self.delete_modele(id))
            action_layout.addWidget(delete_button)

            show_button = QPushButton("Afficher")
            show_button.clicked.connect(lambda _, id=query.value(0): self.open_show_modele_modal(id))
            action_layout.addWidget(show_button)

            self.modeles_table.setCellWidget(row, 2, action_widget)

    def open_edit_modele_modal(self, modele_id):
        self.edit_modele_modal = EditModeleModal(modele_id, self)
        self.edit_modele_modal.exec_()

    def delete_modele(self, modele_id):
        reply = QMessageBox.question(self, "Supprimer Modèle", "Êtes-vous sûr de vouloir supprimer ce modèle ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            query = QSqlQuery()
            query.prepare("DELETE FROM modeles_proforma WHERE id = ?")
            query.addBindValue(modele_id)
            if not query.exec():
                QMessageBox.critical(self, "Erreur", "Impossible de supprimer le modèle")
            else:
                self.load_modeles()

    def open_show_modele_modal(self, modele_id):
        self.show_modele_modal = ShowModeleModal(modele_id, self)
        self.show_modele_modal.exec_()

    def init_settings_tab(self):
        layout = QVBoxLayout()

        # Vérifier si des paramètres existent
        query = QSqlQuery("SELECT COUNT(*) FROM parametres WHERE id = 1")
        if query.next() and query.value(0) > 0:
            self.parametres_existants = True
        else:
            self.parametres_existants = False

        # Bouton pour ouvrir la modale des paramètres
        self.parametres_button = QPushButton("Modifier Paramètres" if self.parametres_existants else "Ajouter Paramètres")
        self.parametres_button.clicked.connect(self.open_parametres_modal)
        layout.addWidget(self.parametres_button)

        # Afficher les paramètres existants
        if self.parametres_existants:
            self.parametres_label = QLabel("Paramètres existants :")
            layout.addWidget(self.parametres_label)

            query = QSqlQuery("SELECT nom_entreprise, adresse_entreprise, telephone_entreprise, email_entreprise FROM parametres WHERE id = 1")
            if query.next():
                self.nom_entreprise_label = QLabel(f"Nom de l'entreprise: {query.value(0)}")
                self.adresse_entreprise_label = QLabel(f"Adresse: {query.value(1)}")
                self.telephone_entreprise_label = QLabel(f"Téléphone: {query.value(2)}")
                self.email_entreprise_label = QLabel(f"Email: {query.value(3)}")

                layout.addWidget(self.nom_entreprise_label)
                layout.addWidget(self.adresse_entreprise_label)
                layout.addWidget(self.telephone_entreprise_label)
                layout.addWidget(self.email_entreprise_label)
        else:
            self.parametres_label = QLabel("Aucun paramètre enregistré.")
            layout.addWidget(self.parametres_label)

        self.settings_tab.setLayout(layout)

    def open_parametres_modal(self):
        self.parametres_modal = ParametresModal(self)
        self.parametres_modal.exec_()
        self.init_settings_tab()  # Recharger l'onglet Paramètres après la fermeture de la modale


class ParametresModal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Paramètres")
        self.setFixedSize(500, 550)  # Taille ajustée pour un design plus large et aéré
        self.setStyleSheet("background-color: #fafafa; border-radius: 10px; padding: 20px;")  # Fond clair et arrondi

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Titre du modal
        self.title_label = QLabel("Paramètres de l'entreprise")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #4CAF50; padding-bottom: 20px;")
        self.layout.addWidget(self.title_label)

        # Formulaire des paramètres
        self.form_layout = QFormLayout()

        self.nom_entreprise_input = self.create_input_field("Nom de l'entreprise")
        self.adresse_entreprise_input = self.create_input_field("Adresse de l'entreprise")
        self.telephone_entreprise_input = self.create_input_field("Téléphone de l'entreprise")
        self.email_entreprise_input = self.create_input_field("Email de l'entreprise")

        # Logo de l'entreprise avec un bouton stylisé
        self.logo_entreprise_label = QLabel()
        self.logo_entreprise_label.setPixmap(QPixmap("logo.png").scaled(120, 120, aspectRatioMode=1))
        self.logo_entreprise_button = self.create_button("Changer Logo", self.change_logo)

        logo_group = QGroupBox("Logo de l'entreprise")
        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self.logo_entreprise_label)
        logo_layout.addWidget(self.logo_entreprise_button)
        logo_group.setLayout(logo_layout)

        self.form_layout.addRow(logo_group)

        # Modèle de message
        self.modele_message_input = QTextEdit()
        self.modele_message_input.setStyleSheet(self.get_input_field_style())
        self.form_layout.addRow("Modèle de Message:", self.modele_message_input)

        self.layout.addLayout(self.form_layout)

        # Bouton pour enregistrer les paramètres avec une animation
        self.save_button = self.create_button("Enregistrer", self.save_settings)
        self.layout.addWidget(self.save_button)

        # Charger les paramètres existants
        self.load_settings()

    def create_input_field(self, placeholder):
        """Créer un champ de saisie stylisé avec un effet ombre"""
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet(self.get_input_field_style())
        self.apply_shadow(input_field)
        return input_field

    def create_button(self, text, slot):
        """Créer un bouton avec une apparence extravagante et une interaction"""
        button = QPushButton(text)
        button.setStyleSheet("""
            background-color: #2196F3;
            color: white;
            font-size: 16px;
            padding: 12px;
            border-radius: 10px;
            border: none;
            transition: background-color 0.3s;
        """)
        button.clicked.connect(slot)
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet("""
            background-color: #2196F3;
            color: white;
            font-size: 16px;
            padding: 12px;
            border-radius: 10px;
            border: none;
            transition: background-color 0.3s;
        """)
        button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; padding: 12px; border-radius: 10px;")
        button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; padding: 12px; border-radius: 10px;")
        return button

    def get_input_field_style(self):
        """Style pour les champs de saisie avec bordures et ombres"""
        return """
            border: 1px solid #2196F3;
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
            background-color: #ffffff;
        """

    def apply_shadow(self, widget):
        """Appliquer un effet d'ombre portée sur les widgets"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(2, 2)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        widget.setGraphicsEffect(shadow)

    def change_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Changer le Logo", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.logo_entreprise_label.setPixmap(QPixmap(file_path).scaled(120, 120, aspectRatioMode=1))

    def save_settings(self):
        """Enregistrer les paramètres"""
        nom_entreprise = self.nom_entreprise_input.text()
        adresse_entreprise = self.adresse_entreprise_input.text()
        telephone_entreprise = self.telephone_entreprise_input.text()
        email_entreprise = self.email_entreprise_input.text()
        modele_message = self.modele_message_input.toPlainText()

        query = QSqlQuery()
        query.prepare("INSERT OR REPLACE INTO parametres (id, nom_entreprise, adresse_entreprise, telephone_entreprise, email_entreprise, modele_message) VALUES (1, ?, ?, ?, ?, ?)")
        query.addBindValue(nom_entreprise)
        query.addBindValue(adresse_entreprise)
        query.addBindValue(telephone_entreprise)
        query.addBindValue(email_entreprise)
        query.addBindValue(modele_message)

        if not query.exec():
            QMessageBox.critical(self, "Erreur", "Impossible d'enregistrer les paramètres")
        else:
            QMessageBox.information(self, "Succès", "Paramètres enregistrés avec succès")
            self.close()

    def load_settings(self):
        """Charger les paramètres enregistrés"""
        query = QSqlQuery("SELECT nom_entreprise, adresse_entreprise, telephone_entreprise, email_entreprise, modele_message FROM parametres WHERE id = 1")
        if query.next():
            self.nom_entreprise_input.setText(query.value(0))
            self.adresse_entreprise_input.setText(query.value(1))
            self.telephone_entreprise_input.setText(query.value(2))
            self.email_entreprise_input.setText(query.value(3))
            self.modele_message_input.setText(query.value(4))

class ShowModeleModal(QDialog):
    def __init__(self, modele_id, parent=None):
        super().__init__(parent)
        self.modele_id = modele_id
        self.setWindowTitle("Détails du Modèle")
        self.layout = QVBoxLayout(self)

        # Champ pour afficher le nom du modèle
        self.nom_label = QLabel()
        self.layout.addWidget(QLabel("Nom du Modèle:"))
        self.layout.addWidget(self.nom_label)

        # Champ pour afficher le contenu du modèle
        self.contenu_label = QTextEdit()
        self.contenu_label.setReadOnly(True)  # Empêcher l'édition du contenu
        self.layout.addWidget(QLabel("Contenu du Modèle:"))
        self.layout.addWidget(self.contenu_label)

        # Charger les informations du modèle
        self.load_modele()

    def load_modele(self):
        query = QSqlQuery()
        query.prepare("SELECT nom, contenu FROM modeles_proforma WHERE id = ?")
        query.addBindValue(self.modele_id)
        if query.exec() and query.next():
            nom = query.value(0)
            contenu = query.value(1)

            # Afficher les informations du modèle
            self.nom_label.setText(nom)
            self.contenu_label.setText(contenu)
        else:
            QMessageBox.critical(self, "Erreur", "Impossible de charger les informations du modèle")

class EditProformaModal(QDialog):
    def __init__(self, proforma_id, parent=None):
        super().__init__(parent)
        self.proforma_id = proforma_id
        self.setWindowTitle("Éditer un Proforma")
        self.setStyleSheet("background-color: #f4f6f9; border-radius: 10px;")  # Style général
        self.layout = QVBoxLayout(self)

        self._apply_shadow_effect()  # Appliquer un effet d'ombre global

        # Sélection du contact
        self.contact_combo = QComboBox()
        self.parent().load_contacts_combo(self.contact_combo)
        self.layout.addWidget(QLabel("Sélectionner un contact:"))
        self.layout.addWidget(self.contact_combo)

        # Sélection du modèle de proforma
        self.modele_combo = QComboBox()
        self.parent().load_modeles_combo(self.modele_combo)
        self.layout.addWidget(QLabel("Sélectionner un modèle de proforma:"))
        self.layout.addWidget(self.modele_combo)

        # Champ pour le contenu du proforma
        self.contenu_proforma = QTextEdit()
        self.contenu_proforma.setStyleSheet("border-radius: 8px; padding: 10px; font-size: 14px;")
        self.layout.addWidget(QLabel("Contenu du Proforma:"))
        self.layout.addWidget(self.contenu_proforma)

        # Bouton pour enregistrer les modifications
        save_button = QPushButton("Enregistrer")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_button.clicked.connect(self.save_proforma)
        self.layout.addWidget(save_button)

        # Charger les informations du proforma
        self.load_proforma()

    def _apply_shadow_effect(self):
        """Applique un effet d'ombre au dialogue"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(5)
        shadow.setYOffset(5)
        shadow.setColor(Qt.black)
        self.setGraphicsEffect(shadow)

    def load_proforma(self):
        """Charge les informations du proforma dans les champs"""
        query = QSqlQuery()
        query.prepare("SELECT contact_id, modele_id, contenu FROM proformas WHERE id = ?")
        query.addBindValue(self.proforma_id)
        if query.exec() and query.next():
            contact_id = query.value(0)
            modele_id = query.value(1)
            contenu = query.value(2)

            # Sélectionner le contact et le modèle dans les combobox
            self.contact_combo.setCurrentIndex(self.contact_combo.findData(contact_id))
            self.modele_combo.setCurrentIndex(self.modele_combo.findData(modele_id))
            self.contenu_proforma.setText(contenu)

    def save_proforma(self):
        """Enregistre les modifications du proforma"""
        contact_id = self.contact_combo.currentData()
        modele_id = self.modele_combo.currentData()
        contenu = self.contenu_proforma.toPlainText()

        if not contact_id or not modele_id or not contenu:
            self._show_error_message("Veuillez remplir tous les champs.")
            return

        query = QSqlQuery()
        query.prepare("UPDATE proformas SET contact_id = ?, modele_id = ?, contenu = ? WHERE id = ?")
        query.addBindValue(contact_id)
        query.addBindValue(modele_id)
        query.addBindValue(contenu)
        query.addBindValue(self.proforma_id)
        if not query.exec():
            self._show_error_message("Impossible de mettre à jour le proforma.")
        else:
            self.parent().load_proformas()
            self._show_success_message("Proforma mis à jour avec succès.")
            self.close()

    def _show_error_message(self, message):
        """Affiche un message d'erreur personnalisé"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle("Erreur")
        msg_box.setStyleSheet("background-color: #f8d7da; color: #721c24; font-size: 14px;")
        msg_box.exec_()

    def _show_success_message(self, message):
        """Affiche un message de succès personnalisé"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Succès")
        msg_box.setStyleSheet("background-color: #d4edda; color: #155724; font-size: 14px;")
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


