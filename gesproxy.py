import sys
import random
import time
import requests
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

# Liste de proxys tournants (exemple, remplacez par vos propres proxys)
PROXIES = [
    "http://user:pass@proxy1:port",
    "http://user:pass@proxy2:port",
    "http://user:pass@proxy3:port"
]

# Liste de user-agents aléatoires
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

class ProxyScraperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.session = requests.Session()  # Garde les cookies pour éviter d'être détecté comme bot

    def initUI(self):
        self.setWindowTitle("Proxy Scraper avec Rotation Avancée")
        self.setGeometry(100, 100, 600, 450)

        layout = QVBoxLayout()

        self.url_label = QLabel("URL cible :", self)
        layout.addWidget(self.url_label)

        self.url_input = QLineEdit(self)
        self.url_input.setText("https://httpbin.org/ip")  # Test sur httpbin pour voir l'IP
        layout.addWidget(self.url_input)

        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.start_button = QPushButton("Lancer la requête", self)
        self.start_button.clicked.connect(self.start_scraping_thread)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def start_scraping_thread(self):
        thread = threading.Thread(target=self.start_scraping)
        thread.start()

    def start_scraping(self):
        url = self.url_input.text()
        if not url:
            self.log_output.append("❌ Veuillez entrer une URL.")
            return

        proxy = self.get_working_proxy()
        if not proxy:
            self.log_output.append("❌ Aucun proxy valide disponible.")
            return

        user_agent = random.choice(USER_AGENTS)
        headers = {"User-Agent": user_agent}
        proxies = {"http": proxy, "https": proxy}

        delay = random.uniform(3, 10)  # Simule un comportement humain
        self.log_output.append(f"🕒 Attente de {delay:.2f} sec avant la requête...")
        QApplication.processEvents()
        time.sleep(delay)

        try:
            response = self.session.get(url, headers=headers, proxies=proxies, timeout=10)
            if response.status_code == 200:
                self.log_output.append(f"✅ Succès ! Réponse : {response.text}")
            else:
                self.log_output.append(f"⚠️ Erreur {response.status_code} : {response.reason}")
        except requests.exceptions.RequestException as e:
            self.log_output.append(f"❌ Erreur : {e}")

    def get_working_proxy(self):
        """ Vérifie la validité des proxys et retourne un proxy fonctionnel """
        for proxy in PROXIES:
            try:
                test_proxy = {"http": proxy, "https": proxy}
                response = requests.get("https://httpbin.org/ip", proxies=test_proxy, timeout=5)
                if response.status_code == 200:
                    self.log_output.append(f"✅ Proxy valide trouvé : {proxy}")
                    return proxy
            except requests.exceptions.RequestException:
                self.log_output.append(f"❌ Proxy mort : {proxy}")
        return None

def start_selenium_proxy(url):
    """ Utilisation de Selenium avec undetected_chromedriver pour contourner les protections avancées """
    options = uc.ChromeOptions()
    options.add_argument("--headless")  # Exécute le navigateur sans interface graphique
    options.add_argument(f"--proxy-server={random.choice(PROXIES)}")
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Évite d’être détecté comme bot

    driver = uc.Chrome(options=options)
    driver.get(url)

    time.sleep(random.uniform(3, 7))  # Pause aléatoire pour simuler un humain
    page_source = driver.page_source
    driver.quit()

    return page_source

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProxyScraperApp()
    window.show()
    sys.exit(app.exec_())
# 🛠️ Améliorations détaillées
# 1️⃣ Détection automatique des proxys morts

# Avant d'envoyer une requête, le programme teste tous les proxys.
# Si un proxy ne fonctionne pas, il passe au suivant.
# 2️⃣ Ajout de Selenium et undetected_chromedriver

# Permet de contourner des protections avancées comme Cloudflare.
# Simule un vrai navigateur avec fingerprint modifié.
# 3️⃣ Rotation des User-Agents et des empreintes digitales

# Change le User-Agent pour éviter de se faire bloquer.
# Désactive certaines fonctionnalités détectables (AutomationControlled).
# 4️⃣ Multi-threading pour ne pas bloquer l’interface

# Lancement de la requête dans un thread pour que l'UI reste réactive.
# 5️⃣ Délai aléatoire amélioré

# Simule un comportement humain en intégrant un temps d’attente aléatoire avant chaque requête.
# 🔧 Possibles améliorations futures
# Support des proxys SOCKS5 pour plus d’anonymat.
# Scraping avancé avec BeautifulSoup pour extraire des données des pages web.
# Ajout de Tor pour encore plus d’anonymat.
