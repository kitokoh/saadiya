import sqlite3
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum, auto
from datetime import datetime, timedelta
import hashlib
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QComboBox, QLineEdit, QTableWidget,
                             QTableWidgetItem, QTabWidget, QStackedWidget, QFormLayout,
                             QDoubleSpinBox, QSpinBox, QCheckBox, QTextEdit, QGroupBox,
                             QScrollArea, QFrame, QSizePolicy, QSplitter)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Configuration du style
plt.style.use('dark_background')
COLORS = {
    'primary': '#6e44ff',
    'secondary': '#b892ff',
    'accent': '#ff7d00',
    'background': '#0a0a12',
    'text': '#f8f1ff',
    'success': '#00ff9d',
    'danger': '#ff6482',
    'warning': '#ffcc00'
}

## Database Manager (Enhanced)
class DatabaseManager:
    def __init__(self, db_name='finance.db'):
        self.conn = sqlite3.connect(db_name)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()

        # Mining Strategies
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS mining_strategies (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            algorithm TEXT NOT NULL,
            hardware_config TEXT,
            profit_threshold REAL,
            energy_cost REAL,
            created_at TEXT,
            updated_at TEXT,
            parameters TEXT,
            is_active INTEGER DEFAULT 0
        )
        ''')

        # Trading Strategies
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trading_strategies (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            base_currency TEXT,
            quote_currency TEXT,
            indicators TEXT,
            entry_rules TEXT,
            exit_rules TEXT,
            risk_per_trade REAL,
            created_at TEXT,
            updated_at TEXT,
            backtest_results TEXT,
            is_active INTEGER DEFAULT 0
        )
        ''')

        # Execution Logs
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS execution_logs (
            id TEXT PRIMARY KEY,
            strategy_type TEXT,
            strategy_id TEXT,
            timestamp TEXT,
            result REAL,
            parameters TEXT,
            execution_time REAL,
            details TEXT
        )
        ''')

        # Market Data Cache
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS market_data (
            symbol TEXT,
            timestamp TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL,
            PRIMARY KEY (symbol, timestamp)
        )
        ''')

        self.conn.commit()

    def save_mining_strategy(self, strategy):
        """Save or update a mining strategy"""
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO mining_strategies
        (id, name, algorithm, hardware_config, profit_threshold, energy_cost,
         created_at, updated_at, parameters, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            strategy.id,
            strategy.name,
            strategy.algorithm.name,
            json.dumps([hw.__dict__ for hw in strategy.hardware]),
            strategy.profit_threshold,
            strategy.electricity_cost,
            datetime.now().isoformat(),
            datetime.now().isoformat(),
            json.dumps(strategy.__dict__),
            strategy.is_active
        ))
        self.conn.commit()

    def get_active_mining_strategies(self):
        """Get all active mining strategies"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM mining_strategies WHERE is_active = 1')
        return cursor.fetchall()

    # Additional CRUD methods for trading strategies, logs, etc.

## Data Models
class MiningAlgorithm(Enum):
    SHA256 = auto()
    Ethash = auto()
    RandomX = auto()
    Equihash = auto()
    Blake2b = auto()

@dataclass
class MiningHardware:
    gpu_model: str
    hashrate: float
    power_consumption: float
    cost: float
    count: int = 1

@dataclass
class MiningStrategy:
    id: str
    name: str
    algorithm: MiningAlgorithm
    hardware: List[MiningHardware]
    electricity_cost: float
    profit_threshold: float = 0.1
    coin: Optional[str] = None
    is_active: bool = False

    def calculate_profitability(self, network_data: Dict) -> Dict:
        """Enhanced profitability calculation"""
        total_hashrate = sum(hw.hashrate * hw.count for hw in self.hardware)
        total_power = sum(hw.power_consumption * hw.count for hw in self.hardware) / 1000

        # Calculate daily reward
        daily_reward = (total_hashrate / network_data['difficulty']) * \
                       network_data['block_reward'] * network_data['price'] * 24 * 3600
        daily_cost = total_power * 24 * self.electricity_cost
        daily_profit = daily_reward - daily_cost

        roi_days = sum(hw.cost * hw.count for hw in self.hardware) / daily_profit if daily_profit > 0 else float('inf')

        return {
            'daily_reward': daily_reward,
            'daily_cost': daily_cost,
            'daily_profit': daily_profit,
            'roi_days': roi_days,
            'profitability': daily_profit > self.profit_threshold,
            'hashrate': total_hashrate,
            'power_consumption': total_power
        }

class TradingIndicator(Enum):
    SMA = auto()
    EMA = auto()
    RSI = auto()
    MACD = auto()
    BollingerBands = auto()
    OBV = auto()
    Stochastic = auto()

@dataclass
class TradingRule:
    indicator: TradingIndicator
    condition: str
    value: float
    lookback_period: int = 14
    weight: float = 1.0

@dataclass
class TradingStrategy:
    id: str
    name: str
    entry_rules: List[TradingRule]
    exit_rules: List[TradingRule]
    risk_per_trade: float = 0.01
    base_currency: str = 'BTC'
    quote_currency: str = 'USDT'
    is_active: bool = False
    take_profit: Optional[float] = None
    stop_loss: Optional[float] = None

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'entry_rules': [rule.__dict__ for rule in self.entry_rules],
            'exit_rules': [rule.__dict__ for rule in self.exit_rules],
            'risk_per_trade': self.risk_per_trade,
            'base_currency': self.base_currency,
            'quote_currency': self.quote_currency,
            'is_active': self.is_active,
            'take_profit': self.take_profit,
            'stop_loss': self.stop_loss
        }

## Custom Qt Widgets
class MplCanvas(FigureCanvas):
    """Matplotlib canvas for embedding plots"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor=COLORS['background'])
        fig.patch.set_alpha(0.0)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        self.setStyleSheet("background-color: transparent;")

class StrategyCard(QFrame):
    """Reusable card widget for strategy display"""
    def __init__(self, title, description, parent=None):
        super().__init__(parent)
        self.setObjectName("StrategyCard")
        self.setStyleSheet(f"""
            #StrategyCard {{
                background-color: {COLORS['background']};
                border: 1px solid {COLORS['primary']};
                border-radius: 8px;
                padding: 12px;
            }}
            QLabel {{
                color: {COLORS['text']};
            }}
        """)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(self.title_label)

        self.desc_label = QLabel(description)
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)

        self.status_label = QLabel("Inactive")
        self.status_label.setStyleSheet(f"color: {COLORS['danger']};")
        layout.addWidget(self.status_label)

        self.toggle_btn = QPushButton("Activate")
        self.toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                padding: 5px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['secondary']};
            }}
        """)
        layout.addWidget(self.toggle_btn)

class DashboardHeader(QWidget):
    """Dashboard header with title and stats - CORRIGÉ"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.title_label = QLabel("Crypto Strategy Assistant")
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setStyleSheet(f"color: {COLORS['primary']};")
        layout.addWidget(self.title_label, stretch=1)  # Utilisation de stretch

        # Conteneur pour les stats
        stats_container = QWidget()
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setContentsMargins(0, 0, 0, 0)

        self.mining_stat = QLabel("Mining: 0 active")
        self.trading_stat = QLabel("Trading: 0 active")
        self.profit_stat = QLabel("Daily Profit: $0.00")

        for stat in [self.mining_stat, self.trading_stat, self.profit_stat]:
            stat.setStyleSheet(f"color: {COLORS['text']}; padding: 0 10px;")
            stats_layout.addWidget(stat)

        # Ajout du conteneur au layout principal
        layout.addWidget(stats_container)
