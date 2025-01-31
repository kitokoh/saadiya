import sys
import random
import time
import asyncio
import aiohttp
import socks
import socket
import logging
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QProgressBar, QTabWidget, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import QThread, pyqtSignal
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import stem.process
from stem import Signal
from stem.control import Controller

# Configuration des logs
logging.basicConfig(filename='proxy_scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Liste de proxys (exemple, remplacez par vos propres proxys)
PROXIES = [
    "http://user:pass@proxy1:port",
    "socks5://user:pass@proxy2:port",
    "http://user:pass@proxy3:port"
]

# Liste de user-agents aléatoires
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

# Configuration de Tor
TOR_PROXY = "socks5://127.0.0.1:9050"

class ProxyScraperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.session = aiohttp.ClientSession()  # Session asynchrone pour les requêtes
        self.tor_process = None  # Processus Tor

    def initUI(self):
        self.setWindowTitle("Proxy Scraper avec Rotation Avancée")
        self.setGeometry(100, 100, 1000, 800)

        # Layout principal
        main_layout = QVBoxLayout()

        # Onglets
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_scraping_tab(), "Scraping")
        self.tabs.addTab(self.create_proxy_manager_tab(), "Gestion des Proxys")
        self.tabs.addTab(self.create_user_agent_manager_tab(), "Gestion des User-Agents")
        main_layout.addWidget(self.tabs)

        # Barre de progression
        self.progress_bar = QProgressBar(self)
        main_layout.addWidget(self.progress_bar)

        self.setLayout(main_layout)

    def create_scraping_tab(self):
        """Crée l'onglet de scraping"""
        tab = QWidget()
        layout = QVBoxLayout()

        self.url_label = QLabel("URL cible :", self)
        layout.addWidget(self.url_label)

        self.url_input = QLineEdit(self)
        self.url_input.setText("https://httpbin.org/ip")  # Test sur httpbin pour voir l'IP
        layout.addWidget(self.url_input)

        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.use_tor_checkbox = QPushButton("Utiliser Tor", self)
        self.use_tor_checkbox.setCheckable(True)
        layout.addWidget(self.use_tor_checkbox)

        self.start_button = QPushButton("Lancer la requête", self)
        self.start_button.clicked.connect(self.start_scraping)
        layout.addWidget(self.start_button)

        tab.setLayout(layout)
        return tab

    def create_proxy_manager_tab(self):
        """Crée l'onglet de gestion des proxys"""
        tab = QWidget()
        layout = QVBoxLayout()

        self.proxy_table = QTableWidget(self)
        self.proxy_table.setColumnCount(1)
        self.proxy_table.setHorizontalHeaderLabels(["Proxys"])
        self.update_proxy_table()
        layout.addWidget(self.proxy_table)

        tab.setLayout(layout)
        return tab

    def create_user_agent_manager_tab(self):
        """Crée l'onglet de gestion des user-agents"""
        tab = QWidget()
        layout = QVBoxLayout()

        self.user_agent_table = QTableWidget(self)
        self.user_agent_table.setColumnCount(1)
        self.user_agent_table.setHorizontalHeaderLabels(["User-Agents"])
        self.update_user_agent_table()
        layout.addWidget(self.user_agent_table)

        tab.setLayout(layout)
        return tab

    def update_proxy_table(self):
        """Met à jour la table des proxys"""
        self.proxy_table.setRowCount(len(PROXIES))
        for i, proxy in enumerate(PROXIES):
            self.proxy_table.setItem(i, 0, QTableWidgetItem(proxy))

    def update_user_agent_table(self):
        """Met à jour la table des user-agents"""
        self.user_agent_table.setRowCount(len(USER_AGENTS))
        for i, user_agent in enumerate(USER_AGENTS):
            self.user_agent_table.setItem(i, 0, QTableWidgetItem(user_agent))

    def start_scraping(self):
        url = self.url_input.text()
        if not url:
            self.log_output.append("❌ Veuillez entrer une URL.")
            return

        self.start_button.setEnabled(False)
        self.progress_bar.setValue(0)

        # Lancer la tâche asynchrone
        self.scraping_thread = ScrapingThread(url, self.use_tor_checkbox.isChecked())
        self.scraping_thread.update_signal.connect(self.update_log)
        self.scraping_thread.progress_signal.connect(self.update_progress)
        self.scraping_thread.finished_signal.connect(self.on_finished)
        self.scraping_thread.start()

    def update_log(self, message):
        self.log_output.append(message)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def on_finished(self):
        self.start_button.setEnabled(True)
        self.progress_bar.setValue(100)

    def closeEvent(self, event):
        """Arrête Tor lors de la fermeture de l'application"""
        if self.tor_process:
            self.tor_process.terminate()
        event.accept()

class ScrapingThread(QThread):
    update_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()

    def __init__(self, url, use_tor=False):
        super().__init__()
        self.url = url
        self.use_tor = use_tor

    def run(self):
        asyncio.run(self.async_scraping())

    async def async_scraping(self):
        proxy = self.get_working_proxy()
        if not proxy:
            self.update_signal.emit("❌ Aucun proxy valide disponible.")
            return

        user_agent = random.choice(USER_AGENTS)
        headers = {"User-Agent": user_agent}

        delay = random.uniform(3, 10)  # Simule un comportement humain
        self.update_signal.emit(f"🕒 Attente de {delay:.2f} sec avant la requête...")
        await asyncio.sleep(delay)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=headers, proxy=proxy, timeout=10) as response:
                    if response.status == 200:
                        content = await response.text()
                        self.update_signal.emit(f"✅ Succès ! Réponse : {content}")
                        self.progress_signal.emit(50)

                        # Scraping avec BeautifulSoup
                        soup = BeautifulSoup(content, 'html.parser')
                        self.update_signal.emit(f"🔍 Données extraites : {soup.title.string}")
                        self.progress_signal.emit(100)
                    else:
                        self.update_signal.emit(f"⚠️ Erreur {response.status} : {response.reason}")
        except Exception as e:
            self.update_signal.emit(f"❌ Erreur : {e}")
        finally:
            self.finished_signal.emit()

    def get_working_proxy(self):
        """Vérifie la validité des proxys et retourne un proxy fonctionnel"""
        if self.use_tor:
            return TOR_PROXY

        for proxy in PROXIES:
            try:
                if proxy.startswith("socks5"):
                    socks.set_default_proxy(socks.SOCKS5, proxy.split("://")[1].split("@")[1].split(":")[0], int(proxy.split(":")[-1]))
                    socket.socket = socks.socksocket
                else:
                    test_proxy = {"http": proxy, "https": proxy}

                response = requests.get("https://httpbin.org/ip", proxies=test_proxy if not proxy.startswith("socks5") else None, timeout=5)
                if response.status_code == 200:
                    self.update_signal.emit(f"✅ Proxy valide trouvé : {proxy}")
                    return proxy
            except Exception as e:
                self.update_signal.emit(f"❌ Proxy mort : {proxy} - {e}")
        return None

def start_tor():
    """Démarre le service Tor"""
    tor_process = stem.process.launch_tor_with_config(
        config={
            'SocksPort': '9050',
            'ControlPort': '9051',
        }
    )
    return tor_process

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProxyScraperApp()
    window.show()
    sys.exit(app.exec_())













    import unittest
from unittest.mock import patch, MagicMock
from your_script import ScrapingThread, PROXIES, USER_AGENTS

class TestScrapingThread(unittest.TestCase):
    @patch('aiohttp.ClientSession.get')
    async def test_async_scraping(self, mock_get):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.text.return_value = "<html><title>Test</title></html>"
        mock_get.return_value.__aenter__.return_value = mock_response

        thread = ScrapingThread("https://httpbin.org/ip")
        await thread.async_scraping()

        self.assertEqual(mock_get.call_count, 1)

    def test_get_working_proxy(self):
        thread = ScrapingThread("https://httpbin.org/ip")
        proxy = thread.get_working_proxy()
        self.assertIn(proxy, PROXIES + [TOR_PROXY])

if __name__ == '__main__':
    unittest.main()