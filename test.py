import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys

current_folder = os.getcwd()
data_dir = os.path.join(os.path.dirname(current_folder), 'lang', 'resources', 'data')
settings_dir = os.path.join(os.path.dirname(current_folder), 'lang', 'resources')
lang_file = os.path.join(settings_dir, 'lang.json')

class ProformaGenerator:
    def __init__(self, license_type):
        self.license_type = license_type
        self.user_info = self.load_user_info()
        self.language = self.load_language()
        self.translations = self.load_translations()
        self.today = datetime.today().strftime("%d-%m-%Y")
        self.invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def load_user_info(self):
        try:
            session_path = os.path.join(data_dir, 'session.json')
            with open(session_path, 'r') as session_file:
                session_data = json.load(session_file)
                username = session_data.get("username")

            user_file_path = os.path.join(data_dir, 'users.json')
            with open(user_file_path, 'r') as user_file:
                users_data = json.load(user_file)
                user_info = next((user for user in users_data if user['username'] == username), None)

            return user_info
        except Exception as e:
            QMessageBox.warning(None, "Erreur", f"Erreur lors du chargement des informations : {e}")
            return None

    def load_language(self):
        settings_path = os.path.join(settings_dir, 'settings.json')
        try:
            with open(settings_path, 'r') as settings_file:
                settings_data = json.load(settings_file)
                return settings_data.get("language", "en")
        except Exception as e:
            QMessageBox.warning(None, "Erreur", f"Erreur lors du chargement des paramètres : {e}")
            return "en"

    def load_translations(self):
        try:
            with open(lang_file, 'r') as lang_file_data:
                return json.load(lang_file_data).get(self.language, {})
        except Exception as e:
            QMessageBox.warning(None, "Erreur", f"Erreur lors du chargement des traductions : {e}")
            return {}

    def translate(self, key):
        return self.translations.get(key, key)

    def get_license_price(self):
        prices = {
            "mensuelle": "50 USD",
            "annuelle": "200 USD",
            "lifetime": "500 USD"
        }
        return prices.get(self.license_type.lower(), "N/A")

    def generate_proforma_pdf(self):
        if not self.user_info:
            return

        pdf_path = os.path.join(settings_dir, "proforma.pdf")
        c = canvas.Canvas(pdf_path, pagesize=A4)
        c.setTitle(self.translate("proforma_invoice"))

        # En-tête
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 800, "INVOICE")
        c.drawString(400, 800, "Nova360.ai")

        c.setFont("Helvetica", 10)
        c.drawString(50, 780, f"Invoice Number: {self.invoice_number}")
        c.drawString(50, 760, f"Username: {self.user_info['username']}")
        c.drawString(50, 740, f"Name: {self.user_info.get('name', 'N/A')}")
        c.drawString(50, 720, f"Email: {self.user_info.get('email', 'N/A')}")

        # Adresse
        c.drawString(50, 700, "Nova360.ai, 799 Market St, Floor 8, San Francisco, California 94103")
        c.drawString(300, 700, "Bill To:")
        c.drawString(300, 680, f"{self.user_info.get('name', 'N/A')}")
        c.drawString(300, 660, f"{self.user_info.get('email', 'N/A')}")

        # Informations supplémentaires
        c.drawString(50, 640, "Amount paid on September 17, 2024")
        c.drawString(50, 620, "If you have questions about your invoice, visit https://nova360.ai/invoices-and-receipts-overview")

        # Tableau
        license_price = self.get_license_price()
        license_details = [
            ["Description", "License Type", "Unit Price", "Amount"],
            ["Marketing Digital License", self.license_type.capitalize(), license_price, license_price]
        ]

        table = Table(license_details, colWidths=[150, 150, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        table.wrapOn(c, 50, 500)
        table.drawOn(c, 50, 500)

        # Total
        c.drawString(300, 480, "Subtotal: " + license_price)
        c.drawString(300, 460, "Total: " + license_price)
        c.drawString(300, 440, "Applied Balance: 0 USD")

        # Pied de page
        c.drawString(50, 50, f"Invoice Number: {self.invoice_number}")
        c.drawString(400, 50, f"Date: {self.today}")
        c.drawString(400, 30, "Page 1/1")

        c.showPage()
        c.save()

# Exécution
# app = QApplication(sys.argv)
# proforma = ProformaGenerator("annuelle")
# proforma.generate_proforma_pdf()
# sys.exit(app.exec_())
