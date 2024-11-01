import os
import re
import datetime
import subprocess

class LicenseChecker:
    def __init__(self, license_dir="C:\\bon"):
        self.license_dir = license_dir
        self.license_file = os.path.join(self.license_dir, 'python.txt')
        self.fixed_mac_address = "E4-42-A6-3A-AC"  # MAC fixe à vérifier

    def get_license_file(self):
        """Vérifie si le fichier de licence est présent dans le répertoire spécifié."""
        if os.path.exists(self.license_file):
            print(f"Fichier de licence trouvé : {self.license_file}")
            return self.license_file
        return None

    def parse_license(self, license_str):
        """Extrait les informations clés de la licence et les valide."""
        print(f"Tentative d'analyse de la licence : {license_str}")
        match = re.match(r'^(A1a9)(\d{3})([A-Za-z0-9 ]+|To be filled by O\.E\.M\.):([A-F0-9-]{14})(\d{12})(\w+)$', license_str)
        
        if match:
            validity_days = int(match.group(2))
            serial_number = match.group(3).strip()
            mac_address = match.group(4)
            date_str = match.group(5)

            # Conversion de la date
            try:
                hours = int(date_str[:2])
                minutes = int(date_str[2:4])
                day = int(date_str[4:6])
                month = int(date_str[6:8])
                year = int(date_str[8:12])
                license_date = datetime.datetime(year, month, day, hours, minutes)
            except ValueError:
                print("Erreur lors de la conversion de la date")
                return None, None, None, None

            return validity_days, serial_number, mac_address, license_date
        print("Erreur : format de licence non valide.")
        return None, None, None, None

    def get_serial_number(self):
        """Récupère le numéro de série de la machine avec plusieurs tentatives."""
        try:
            serial_number = os.popen("wmic bios get serialnumber").read().strip().split("\n")[1].strip()
            print(f"Numéro de série obtenu via WMIC : {serial_number}")
            if serial_number and "To be filled by O.E.M." not in serial_number:
                return serial_number
        except IndexError:
            print("Erreur : IndexError lors de la récupération du numéro de série via WMIC.")

        # Essayez avec PowerShell si WMIC ne retourne rien
        try:
            serial_number = subprocess.check_output(
                ["powershell", "(Get-WmiObject win32_bios).SerialNumber"],
                universal_newlines=True
            ).strip()
            print(f"Numéro de série obtenu via PowerShell : {serial_number}")
        except subprocess.CalledProcessError as e:
            print(f"Erreur : Impossible de récupérer le numéro de série avec PowerShell. Détails : {e}")

        # Vérification et retour de la valeur si elle est valide
        return serial_number if serial_number and "To be filled by O.E.M." not in serial_number else "To be filled by O.E.M."

    def check_mac_address(self, license_mac):
        """Vérifie si l'adresse MAC correspond à celle définie dans la licence."""
        return license_mac == self.fixed_mac_address

    def is_license_valid(self):
        """Vérifie si la licence est valide et retourne la date d'expiration formatée, ou 'Invalid' si elle est invalide."""
        license_file = self.get_license_file()
        if not license_file:
            return "Invalid"

        try:
            with open(license_file, 'r') as f:
                license_content = f.read().strip()
                print("Contenu du fichier de licence lu avec succès.")
        except IOError:
            return "Invalid"

        validity_days, license_serial, license_mac, license_date = self.parse_license(license_content)
        if validity_days is None or license_mac is None or license_date is None:
            return "Invalid"

        # Vérification du numéro de série et de l'adresse MAC
        actual_serial_number = self.get_serial_number()
        print(f"Numéro de série dans la licence : {license_serial}, Numéro de série actuel : {actual_serial_number}")
        if actual_serial_number != license_serial or not self.check_mac_address(license_mac):
            print("Erreur : Le numéro de série ou l'adresse MAC ne correspond pas.")
            return "Invalid"

        # Calcul de la date d'expiration
        current_time = datetime.datetime.now()
        expiration_date = license_date + datetime.timedelta(days=validity_days)

        if current_time > expiration_date:
            print(f"Erreur : La licence a expiré le {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}.")
            return "Invalid"

        # Si la licence est valide, retourner la date d'expiration formatée
        print(f"Licence valide jusqu'au {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}.")
        return expiration_date.strftime('%A %d %B %Y')

# Exemple d'utilisation
#license_checker = LicenseChecker(license_dir="C:\\bon")
#print(license_checker.is_license_valid())
