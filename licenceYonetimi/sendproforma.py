import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys

# Définition des répertoires
user_data_dir1 = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

#user_data_dir1 = os.path.dirname(_current_folder)
user_data_dir = os.path.join(user_data_dir1, 'resources', 'data')
#key_data_dir = os.path.join(user_data_dir1, 'resources')


#current_folder = os.getcwd()
data_dir = os.path.join(user_data_dir1, 'resources', 'data')
settings_dir = os.path.join(user_data_dir1, 'resources')
lang_file = os.path.join(settings_dir, 'lang.json')

class ProformaGenerator:
    def __init__(self, license_type):
        self.license_type = license_type
        self.user_info = self.load_user_info()
        self.language = self.load_language()
        self.translations = self.load_translations()
        self.today = datetime.today().strftime("%d-%m-%Y")

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

            if not user_info:
                raise ValueError("Utilisateur non trouvé dans users.json.")
                
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
        # Définir les prix pour chaque type de licence
        prices = {
            "mensuelle": "50 USD",
            "annuelle": "200 USD",
            "lifetime": "500 USD"
        }
        return prices.get(self.license_type.lower(), "N/A")

    def generate_proforma_pdf(self):
        if not self.user_info:
            return

        #pdf_path = os.path.join(settings_dir, f"proforma_{self.user_info['username']}.pdf")
        pdf_path = os.path.join(settings_dir, f"proforma.pdf")

        c = canvas.Canvas(pdf_path, pagesize=A4)
        c.setTitle(self.translate("proforma_invoice"))

        # En-tête
        c.setFillColor(colors.darkblue)
        c.rect(0, 800, 600, 50, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 815, self.translate("proforma_invoice"))

        c.setFont("Helvetica", 10)
        c.drawString(450, 815, self.translate("issue_date") + " " + self.today)

        # Informations utilisateur
        margin_left = 50
        c.setFillColor(colors.black)
        c.drawString(margin_left, 740, self.translate("username") + " " + self.user_info['username'])
        c.drawString(margin_left, 720, self.translate("name") + " " + self.user_info.get('name', 'N/A'))
        c.drawString(margin_left, 700, self.translate("email") + " " + self.user_info.get('email', 'N/A'))

        # Détails de la licence
        license_price = self.get_license_price()
        license_details = [
            [self.translate("description"), self.translate("Marketing Automation License")],
            [self.translate("license_type"), self.license_type.capitalize()],
            [self.translate("start_date"), self.today],
            [self.translate("price"), license_price]
        ]

        # Tableau des détails de la licence
        table = Table(license_details, colWidths=[200, 300])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        table.wrapOn(c, 50, 500)
        table.drawOn(c, 50, 600)

        # Footer
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.gray)
        c.drawString(margin_left, 50, self.translate("contact_us"))
        c.drawString(margin_left, 40, self.translate("footer_email"))
        c.drawString(margin_left, 30, self.translate("footer_phone"))

        c.showPage()
        c.save()
        
       # QMessageBox.information(None, self.translate("success"), f"{self.translate('proforma_generated')} {pdf_path}")

# # Exécution de l'application
# app = QApplication(sys.argv)
# proforma = ProformaGenerator("annuelle")
# proforma.generate_proforma_pdf()
# sys.exit(app.exec_())
