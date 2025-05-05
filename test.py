import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout, QComboBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

class CurrencyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Suivi des Devises en Temps Réel")
        self.setStyleSheet("background-color: #222; color: white;")
        self.setFixedSize(500, 400)

        # Devises à surveiller
        self.coins = {
            'bitcoin': 'BTC',
            'ethereum': 'ETH',
            'usd': 'USD',
            'eur': 'EUR',
            'try': 'TRY',
            'gbp': 'GBP',
            'jpy': 'JPY',
            'cny': 'CNY',
        }

        self.currencies = list(self.coins.keys())  # noms API
        self.display_labels = {}  # Pour afficher les taux

        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_rates)
        self.timer.start(10000)  # 10 secondes
        self.update_rates()

    def initUI(self):
        layout = QVBoxLayout()

        self.selector = QComboBox()
        self.selector.addItems(self.currencies)
        self.selector.setStyleSheet("background-color: #444; color: white;")
        self.selector.currentTextChanged.connect(self.update_rates)
        layout.addWidget(QLabel("Choisissez la devise de base :"))
        layout.addWidget(self.selector)

        self.grid = QGridLayout()
        for i, coin in enumerate(self.currencies):
            if coin != self.selector.currentText():
                label = QLabel(f"{self.coins[coin]}")
                label.setFont(QFont("Arial", 12, QFont.Bold))
                value = QLabel("...")
                value.setFont(QFont("Arial", 12))
                value.setAlignment(Qt.AlignCenter)
                self.grid.addWidget(label, i, 0)
                self.grid.addWidget(value, i, 1)
                self.display_labels[coin] = value

        layout.addLayout(self.grid)
        self.setLayout(layout)

    def update_rates(self):
        base = self.selector.currentText()
        try:
            to_display = [coin for coin in self.currencies if coin != base]
            coins_param = ','.join(to_display)
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coins_param}&vs_currencies={base}"
            response = requests.get(url)
            data = response.json()

            for coin in to_display:
                if coin in data and base in data[coin]:
                    rate = data[coin][base]
                    self.display_labels[coin].setText(str(rate))
                else:
                    self.display_labels[coin].setText("N/A")
        except Exception as e:
            for label in self.display_labels.values():
                label.setText("Erreur")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CurrencyApp()
    win.show()
    sys.exit(app.exec_())
