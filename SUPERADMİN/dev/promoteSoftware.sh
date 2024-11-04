#!/bin/bash

# File details
SOFTWARE_NAME="Saadiya"
VERSION="1.0"
FILE_PATH="/path/to/yourfile.exe"
DESCRIPTION="Saadiya is a powerful marketing automation tool."
DEVELOPER_NAME="Your Company"
WEBSITE_URL="https://yourwebsite.com"
EMAIL="support@yourwebsite.com"

# Example submission to a fictional API
submit_to_site() {
    echo "Submitting to $1"
    curl -X POST "$2" \
        -F "software_name=$SOFTWARE_NAME" \
        -F "version=$VERSION" \
        -F "file=@$FILE_PATH" \
        -F "description=$DESCRIPTION" \
        -F "developer_name=$DEVELOPER_NAME" \
        -F "website_url=$WEBSITE_URL" \
        -F "email=$EMAIL" || echo "Failed to submit to $1"
}

# Example API endpoints - replace with actual URLs if available
submit_to_site "FileHippo" "https://api.filehippo.com/v1/submit"
submit_to_site "Softpedia" "https://api.softpedia.com/v1/submit"
submit_to_site "Download.com" "https://api.download.com/v1/submit"
submit_to_site "AlternativeTo" "https://api.alternativeto.net/submit"

echo "Submission complete for APIs."


or 

#!/bin/bash

# Chemin vers le fichier .exe
EXE_PATH="/path/to/your/software.exe"

# Détails du logiciel
SOFTWARE_NAME="Saadiya AI"
SOFTWARE_VERSION="1.0"
SOFTWARE_DESCRIPTION="Saadiya AI is a cutting-edge automation tool for social media and marketing."
SOFTWARE_WEBSITE="https://www.saadiya.ai"
DEVELOPER_EMAIL="contact@saadiya.ai"

# Chemin vers le WebDriver
CHROME_DRIVER_PATH="/path/to/chromedriver"

# Fonction pour soumettre à Softpedia
submit_softpedia() {
    python3 <<EOF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration de Chrome WebDriver
driver = webdriver.Chrome(service=Service("${CHROME_DRIVER_PATH}"))

try:
    driver.get("https://www.softpedia.com/submit/")

    # Remplir le formulaire (Exemple d'interaction)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "software_name"))).send_keys("${SOFTWARE_NAME}")
    driver.find_element(By.NAME, "version").send_keys("${SOFTWARE_VERSION}")
    driver.find_element(By.NAME, "description").send_keys("${SOFTWARE_DESCRIPTION}")
    driver.find_element(By.NAME, "website").send_keys("${SOFTWARE_WEBSITE}")
    driver.find_element(By.NAME, "email").send_keys("${DEVELOPER_EMAIL}")
    # Upload .exe file
    driver.find_element(By.NAME, "file").send_keys("${EXE_PATH}")

    # Soumettre le formulaire
    driver.find_element(By.NAME, "submit_button").click()
    
    print("Submission to Softpedia completed.")
finally:
    driver.quit()
EOF
}

# Fonction pour soumettre à FileHippo (à adapter selon la structure du site)
submit_filehippo() {
    python3 <<EOF
# Code similaire à submit_softpedia, adapté aux champs spécifiques de FileHippo
EOF
}

# Fonction pour soumettre à CNET Download (à adapter selon la structure du site)
submit_cnet() {
    python3 <<EOF
# Code similaire à submit_softpedia, adapté aux champs spécifiques de CNET Download
EOF
}

# Appels de fonctions pour chaque site
submit_softpedia
submit_filehippo
submit_cnet

echo "Automated submission script completed."



or from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configuration
file_path = "/path/to/yourfile.exe"
software_name = "Saadiya"
version = "1.0"
description = "Saadiya is a powerful marketing automation tool."
developer_name = "Your Company"
website_url = "https://yourwebsite.com"
email = "support@yourwebsite.com"

# Launch browser
driver = webdriver.Chrome()  # Or use webdriver.Firefox(), etc.
driver.get("https://softpedia.com/submit")  # Replace with actual submission page

# Example form-filling, adjust selectors as per the actual webpage structure
try:
    # Software name
    driver.find_element(By.ID, "software_name").send_keys(software_name)

    # Version
    driver.find_element(By.ID, "version").send_keys(version)

    # Upload file
    driver.find_element(By.ID, "file_upload").send_keys(file_path)

    # Description
    driver.find_element(By.ID, "description").send_keys(description)

    # Developer name
    driver.find_element(By.ID, "developer_name").send_keys(developer_name)

    # Website URL
    driver.find_element(By.ID, "website_url").send_keys(website_url)

    # Email
    driver.find_element(By.ID, "email").send_keys(email)

    # Submit the form
    driver.find_element(By.ID, "submit_button").click()

    print("Submission to Softpedia successful.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    time.sleep(5)  # Wait for submission to complete, if necessary
    driver.quit()
