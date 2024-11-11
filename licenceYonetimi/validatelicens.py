import os
import json
import random
import string
import re
from datetime import datetime

class LicenseValidator:
    def __init__(self):
        self.session_file = os.path.join('resources', 'data', 'session.json')
        self.users_file = os.path.join('resources', 'data', 'users.json')
        self.dossiers = {
            "01": "bon", "02": "wabon", "03": "inbon", "04": "instabon", "05": "ytbon",
            "06": "xbon", "07": "grambon", "08": "redditbon", "09": "brandbon",
            "10": "pinbon", "11": "snapbon", "12": "blogbon", "13": "mailbon", "14": "tokbok"
        }
        self.instance_types = ["A", "B", "C"]

    def log(self, message):
        print(f"[LOG] {message}")

    def get_username_initials(self):
        self.log("Reading username initials from session file.")
        with open(self.session_file, "r") as session_file:
            session_data = json.load(session_file)
        username = session_data.get("username", "")[:2]
        self.log(f"Username initials obtained: {username}")
        return username

    def get_email_initials(self):
        self.log("Fetching email initials from users file.")
        with open(self.users_file, "r") as users_file:
            users_data = json.load(users_file)
        
        username = self.get_username_initials()
        user = next((user for user in users_data if user["username"].startswith(username)), None)
        
        if user:
            email = user.get("email", "")
            initials = email[:3]
            self.log(f"Email initials obtained: {initials}")
            return initials
        self.log("No matching user found.")
        return ""

    def generate_random_string(self, length):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        self.log(f"Generated random string of length {length}: {random_string}")
        return random_string

    def get_windows_username_initials(self):
        username = os.getlogin()[:3]
        random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=2))
        windows_initial_block = f"{username}{random_chars}"
        self.log(f"Generated Windows username initials block: {windows_initial_block}")
        return windows_initial_block

    def generate_license_key(self):
        self.log("Generating license key.")
        
        bloc1 = f"{self.get_username_initials()}{self.get_email_initials()}"
        bloc2 = self.generate_random_string(5)
        bloc3 = self.generate_random_string(5)
        bloc4 = self.generate_random_string(5)

        month = f"{datetime.now().month:02d}"
        instance_type = random.choice(self.instance_types)
        dossier_number = f"{random.randint(1, 14):02d}"
        bloc5 = f"{month}{instance_type}{dossier_number}"

        #instance_number = str(random.randint(1, 9))  # Removing leading zero if present
        instance_number = str(random.randint(1, 9)).zfill(2)

        random_suffix = self.generate_random_string(2)
        bloc6 = f"{instance_number}{random_suffix}"

        bloc7 = self.get_windows_username_initials()

        license_key = f"{bloc1}-{bloc2}-{bloc3}-{bloc4}-{bloc5}-{bloc6}-{bloc7}"
        self.log(f"License key generated: {license_key}")
        return license_key

    def validate_license(self, license_key):
        self.log(f"Validating license key: {license_key}")
        
        pattern = r"^[A-Za-z]{2}[A-Za-z0-9]{3}-[A-Za-z0-9]{5}-[A-Za-z0-9]{5}-[A-Za-z0-9]{5}-\d{2}[A-C]\d{2}-\d{1}[A-Za-z0-9]{3}-[A-Za-z]{3}[A-Za-z0-9]{2}$"
        if not re.match(pattern, license_key):
            self.log("License key validation failed due to regex mismatch.")
            return False
        
        month = int(license_key.split("-")[4][:2])
        current_month = datetime.now().month
        is_valid = month == current_month
        self.log(f"License key validation status: {is_valid}")
        return is_valid

    def get_instance_path(self, license_key):
        self.log(f"Constructing instance path for license key: {license_key}")
        
        match = re.search(r"(\d{2}[A-C]\d{2})", license_key.split("-")[4])
        if not match:
            error_message = "Invalid license format"
            self.log(error_message)
            raise ValueError(error_message)

        dossier_number = match.group(0)[-2:]
        instance_number = str(int(license_key.split('-')[5][:2]))  # Removing leading zero if present
        instance_folder = f"robot{instance_number}"

        dossier_name = self.dossiers.get(dossier_number, "bon")
        path = os.path.join(f"C:\\{dossier_name}", instance_folder, "python.txt")
        self.log(f"Instance path constructed: {path}")
        return path
    def get_dossier_path(self, license_key):
        self.log(f"Constructing instance path for license key: {license_key}")
        
        match = re.search(r"(\d{2}[A-C]\d{2})", license_key.split("-")[4])
        if not match:
            error_message = "Invalid license format"
            self.log(error_message)
            raise ValueError(error_message)

        dossier_number = match.group(0)[-2:]
        instance_number = str(int(license_key.split('-')[5][:2]))  # Removing leading zero if present
        instance_folder = f"robot{instance_number}"

        dossier_name = self.dossiers.get(dossier_number, "bon")
        path = os.path.join(f"C:\\{dossier_name}","python.txt")
        self.log(f"Instance path constructed: {path}")
        return path

    def update_python_file(self, license_key):
        if not self.validate_license(license_key):
            error_message = "License validation failed"
            self.log(error_message)
            raise ValueError(error_message)

        path = self.get_instance_path(license_key)
        dossier = self.get_dossier_path(license_key)

        if not os.path.exists(dossier):
            error_message = f"File not found: {path}"
            self.log(error_message)
            raise FileNotFoundError(error_message)

        self.log(f"Updating file at path: {path}")
        with open(dossier, "r", encoding="utf-8") as file:
            content = file.read()

        prefix = content[:7]
        remaining_content = content[7:]
        current_value = int(prefix[4:])
        
        instance_type = license_key.split("-")[4][2]
        # addition_value = {"A": 30, "B": 330, "C": 900}.get(instance_type, 0)
        
        # new_value = current_value + addition_value
        addition_value = {"A": 30, "B": 360, "C": 996}.get(instance_type, 0)
        
        # Calcul du nouveau résultat
        new_value = current_value + addition_value
        
        # Si le type est "A", ajouter un zéro devant si new_value est inférieur à 100
        if instance_type == "A" and new_value < 100:
            new_value = f"0{new_value}"

        new_prefix = prefix[:4] + str(new_value)
        new_content = new_prefix + remaining_content + f"\n{license_key}"

        with open(path, "w", encoding="utf-8") as file:
            file.write(new_content)
        
        self.log("File successfully updated.")

# # Usage example
# validator = LicenseValidator()
# license_key = validator.generate_license_key()
# #license_key = "haafr-3FVZM-jnTFh-lT9rK-11C01-01BS-ibryV"
# try:
#     validator.update_python_file(license_key)
# except Exception as e:
#     print(f"Error: {e}") 
