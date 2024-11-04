import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authentification Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
client = gspread.authorize(creds)

# Mise à jour des données dans le sheet
sheet = client.open("Performance Report").sheet1
sheet.update_cell(2, 1, "Downloads")  # Titre
sheet.update_cell(2, 2, 1200)  # Valeur
