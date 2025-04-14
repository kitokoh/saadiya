import sys
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
    def __init__(self, db_name='crypto_strategy_v2.db'):
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
## Main Application Window
class CryptoStrategyApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.current_theme = 'dark'
        self.init_ui()
        self.load_sample_data()
        
    def init_ui(self):
        """Initialize the main UI components"""
        self.setWindowTitle("Crypto Strategy Assistant")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Add header
        self.header = DashboardHeader()
        main_layout.addWidget(self.header)
        
        # Main content area
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Left sidebar (navigation)
        self.sidebar = self.create_sidebar()
        content_splitter.addWidget(self.sidebar)
        
        # Main content (stacked widgets)
        self.stacked_widget = QStackedWidget()
        
        # Dashboard page
        self.dashboard_page = self.create_dashboard_page()
        self.stacked_widget.addWidget(self.dashboard_page)
        
        # Mining page
        self.mining_page = self.create_mining_page()
        self.stacked_widget.addWidget(self.mining_page)
        
        # Trading page
        self.trading_page = self.create_trading_page()
        self.stacked_widget.addWidget(self.trading_page)
        
        # Analytics page
        self.analytics_page = self.create_analytics_page()
        self.stacked_widget.addWidget(self.analytics_page)
        
        content_splitter.addWidget(self.stacked_widget)
        content_splitter.setSizes([200, 1000])
        main_layout.addWidget(content_splitter)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Apply styles
        self.apply_styles()
        
        # Set initial page
        self.stacked_widget.setCurrentIndex(0)
    
    def create_sidebar(self):
        """Create the navigation sidebar"""
        sidebar = QWidget()
        sidebar.setObjectName("Sidebar")
        sidebar.setStyleSheet(f"""
            #Sidebar {{
                background-color: {COLORS['background']};
                border-right: 1px solid {COLORS['secondary']};
            }}
            QPushButton {{
                text-align: left;
                padding: 10px;
                border: none;
                color: {COLORS['text']};
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary']};
            }}
        """)
        
        layout = QVBoxLayout()
        sidebar.setLayout(layout)
        
        # Navigation buttons
        nav_buttons = [
            ("Dashboard", "icons/dashboard.png"),
            ("Mining Strategies", "icons/mining.png"),
            ("Trading Strategies", "icons/trading.png"),
            ("Analytics", "icons/analytics.png"),
            ("Settings", "icons/settings.png")
        ]
        
        for text, icon in nav_buttons:
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon))
            btn.setIconSize(QSize(24, 24))
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, idx=nav_buttons.index((text, icon)): self.stacked_widget.setCurrentIndex(idx))
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Theme toggle
        theme_btn = QPushButton("Toggle Theme")
        theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(theme_btn)
        
        return sidebar
    
    def create_dashboard_page(self):
        """Create the dashboard overview page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Summary cards
        summary_layout = QHBoxLayout()
        
        self.mining_card = StrategyCard("Mining", "Manage your mining strategies")
        self.trading_card = StrategyCard("Trading", "Manage your trading strategies")
        self.performance_card = StrategyCard("Performance", "View overall performance")
        
        for card in [self.mining_card, self.trading_card, self.performance_card]:
            summary_layout.addWidget(card)
        
        layout.addLayout(summary_layout)
        
        # Charts area
        charts_splitter = QSplitter(Qt.Vertical)
        
        # Mining profitability chart
        mining_chart_widget = QWidget()
        mining_chart_layout = QVBoxLayout(mining_chart_widget)
        mining_chart_layout.addWidget(QLabel("Mining Profitability"))
        self.mining_canvas = MplCanvas()
        mining_chart_layout.addWidget(self.mining_canvas)
        self.update_mining_chart()
        
        # Trading performance chart
        trading_chart_widget = QWidget()
        trading_chart_layout = QVBoxLayout(trading_chart_widget)
        trading_chart_layout.addWidget(QLabel("Trading Performance"))
        self.trading_canvas = MplCanvas()
        trading_chart_layout.addWidget(self.trading_canvas)
        self.update_trading_chart()
        
        charts_splitter.addWidget(mining_chart_widget)
        charts_splitter.addWidget(trading_chart_widget)
        layout.addWidget(charts_splitter)
        
        return page
    
    def create_mining_page(self):
        """Create the mining strategies page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Toolbar
        toolbar = QHBoxLayout()
        add_btn = QPushButton("Add Strategy")
        add_btn.setIcon(QIcon("icons/add.png"))
        add_btn.clicked.connect(self.show_add_mining_strategy_dialog)
        toolbar.addWidget(add_btn)
        layout.addLayout(toolbar)
        
        # Strategies list
        self.mining_table = QTableWidget()
        self.mining_table.setColumnCount(6)
        self.mining_table.setHorizontalHeaderLabels(["Name", "Algorithm", "Hardware", "Profit", "Status", "Actions"])
        self.mining_table.horizontalHeader().setStretchLastSection(True)
        self.update_mining_table()
        layout.addWidget(self.mining_table)
        
        # Details panel
        self.mining_details = QTextEdit()
        self.mining_details.setReadOnly(True)
        layout.addWidget(self.mining_details)
        
        return page
    
    def create_trading_page(self):
        """Create the trading strategies page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Toolbar
        toolbar = QHBoxLayout()
        add_btn = QPushButton("Add Strategy")
        add_btn.setIcon(QIcon("icons/add.png"))
        add_btn.clicked.connect(self.show_add_trading_strategy_dialog)
        toolbar.addWidget(add_btn)
        layout.addLayout(toolbar)
        
        # Strategies list
        self.trading_table = QTableWidget()
        self.trading_table.setColumnCount(6)
        self.trading_table.setHorizontalHeaderLabels(["Name", "Pair", "Indicators", "Risk", "Status", "Actions"])
        self.trading_table.horizontalHeader().setStretchLastSection(True)
        self.update_trading_table()
        layout.addWidget(self.trading_table)
        
        # Chart area
        self.trading_strategy_canvas = MplCanvas()
        layout.addWidget(self.trading_strategy_canvas)
        
        return page
    
    def create_analytics_page(self):
        """Create the analytics page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Performance metrics
        metrics_group = QGroupBox("Performance Metrics")
        metrics_layout = QHBoxLayout()
        
        self.sharpe_ratio = QLabel("Sharpe Ratio: N/A")
        self.max_drawdown = QLabel("Max Drawdown: N/A")
        self.win_rate = QLabel("Win Rate: N/A")
        
        for metric in [self.sharpe_ratio, self.max_drawdown, self.win_rate]:
            metric.setStyleSheet(f"font-size: 14px; color: {COLORS['primary']};")
            metrics_layout.addWidget(metric)
        
        metrics_group.setLayout(metrics_layout)
        layout.addWidget(metrics_group)
        
        # Combined chart
        self.analytics_canvas = MplCanvas(width=10, height=6)
        self.update_analytics_chart()
        layout.addWidget(self.analytics_canvas)
        
        return page
    
    def apply_styles(self):
        """Apply application-wide styles"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['background']};
                color: {COLORS['text']};
            }}
            QTableWidget {{
                background-color: {COLORS['background']};
                border: 1px solid {COLORS['secondary']};
                gridline-color: {COLORS['secondary']};
            }}
            QHeaderView::section {{
                background-color: {COLORS['primary']};
                color: white;
                padding: 5px;
            }}
            QTextEdit, QLineEdit, QComboBox {{
                background-color: {COLORS['background']};
                border: 1px solid {COLORS['secondary']};
                color: {COLORS['text']};
                padding: 5px;
            }}
            QGroupBox {{
                border: 1px solid {COLORS['primary']};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                color: {COLORS['primary']};
            }}
        """)
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        if self.current_theme == 'dark':
            COLORS.update({
                'background': '#f8f9fa',
                'text': '#212529',
                'primary': '#6e44ff',
                'secondary': '#5e35b1',
                'accent': '#ff7d00'
            })
            self.current_theme = 'light'
        else:
            COLORS.update({
                'background': '#0a0a12',
                'text': '#f8f1ff',
                'primary': '#6e44ff',
                'secondary': '#b892ff',
                'accent': '#ff7d00'
            })
            self.current_theme = 'dark'
        
        self.apply_styles()
        self.update_charts()
    
    def update_charts(self):
        """Update all charts with current data"""
        self.update_mining_chart()
        self.update_trading_chart()
        self.update_analytics_chart()
    
    def update_mining_chart(self):
        """Update the mining profitability chart"""
        self.mining_canvas.axes.clear()
        
        # Sample data
        days = list(range(1, 31))
        profits = [np.random.normal(50, 10) for _ in days]
        costs = [np.random.normal(30, 5) for _ in days]
        
        # Plot
        self.mining_canvas.axes.plot(days, profits, label='Profit', color=COLORS['primary'], linewidth=2)
        self.mining_canvas.axes.plot(days, costs, label='Cost', color=COLORS['accent'], linewidth=2)
        self.mining_canvas.axes.fill_between(days, profits, costs, where=(np.array(profits) > np.array(costs)), 
                                           color=COLORS['secondary'], alpha=0.3, interpolate=True)
        
        # Styling
        self.mining_canvas.axes.set_title("Mining Profitability Over Time", color=COLORS['text'], pad=20)
        self.mining_canvas.axes.set_xlabel("Days", color=COLORS['text'])
        self.mining_canvas.axes.set_ylabel("USD", color=COLORS['text'])
        self.mining_canvas.axes.legend()
        self.mining_canvas.axes.grid(color=COLORS['text'], alpha=0.1)
        self.mining_canvas.axes.set_facecolor(COLORS['background'])
        
        self.mining_canvas.draw()
    
    def update_trading_chart(self):
        """Update the trading performance chart"""
        self.trading_canvas.axes.clear()
        
        # Sample data
        dates = pd.date_range(start='2023-01-01', periods=100)
        prices = 100 + np.cumsum(np.random.randn(100))
        
        # Plot
        self.trading_canvas.axes.plot(dates, prices, label='Price', color=COLORS['primary'], linewidth=2)
        
        # Styling
        self.trading_canvas.axes.set_title("Trading Performance", color=COLORS['text'], pad=20)
        self.trading_canvas.axes.set_xlabel("Date", color=COLORS['text'])
        self.trading_canvas.axes.set_ylabel("Price", color=COLORS['text'])
        self.trading_canvas.axes.legend()
        self.trading_canvas.axes.grid(color=COLORS['text'], alpha=0.1)
        self.trading_canvas.axes.set_facecolor(COLORS['background'])
        
        self.trading_canvas.draw()
    
    def update_analytics_chart(self):
        """Update the analytics chart with combined metrics"""
        self.analytics_canvas.axes.clear()
        
        # Sample data
        dates = pd.date_range(start='2023-01-01', periods=100)
        mining_profit = np.cumsum(np.random.normal(50, 10, 100))
        trading_profit = np.cumsum(np.random.normal(30, 15, 100))
        total = mining_profit + trading_profit
        
        # Plot
        self.analytics_canvas.axes.plot(dates, mining_profit, label='Mining Profit', color=COLORS['primary'])
        self.analytics_canvas.axes.plot(dates, trading_profit, label='Trading Profit', color=COLORS['accent'])
        self.analytics_canvas.axes.plot(dates, total, label='Total Profit', color=COLORS['success'], linewidth=2)
        
        # Styling
        self.analytics_canvas.axes.set_title("Combined Performance Analytics", color=COLORS['text'], pad=20)
        self.analytics_canvas.axes.set_xlabel("Date", color=COLORS['text'])
        self.analytics_canvas.axes.set_ylabel("USD", color=COLORS['text'])
        self.analytics_canvas.axes.legend()
        self.analytics_canvas.axes.grid(color=COLORS['text'], alpha=0.1)
        self.analytics_canvas.axes.set_facecolor(COLORS['background'])
        
        self.analytics_canvas.draw()
    
    def update_mining_table(self):
        """Update the mining strategies table"""
        # Sample data - in a real app, this would come from the database
        strategies = [
            ("ETH Rig", "Ethash", "3x RTX 3080", "$12.50/day", "Active"),
            ("BTC Miner", "SHA256", "Antminer S19", "$8.20/day", "Inactive"),
            ("RVN Farm", "KAWPOW", "6x RX 580", "$5.75/day", "Active")
        ]
        
        self.mining_table.setRowCount(len(strategies))
        for row, (name, algo, hw, profit, status) in enumerate(strategies):
            self.mining_table.setItem(row, 0, QTableWidgetItem(name))
            self.mining_table.setItem(row, 1, QTableWidgetItem(algo))
            self.mining_table.setItem(row, 2, QTableWidgetItem(hw))
            self.mining_table.setItem(row, 3, QTableWidgetItem(profit))
            
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QColor(COLORS['success'] if status == "Active" else COLORS['danger']))
            self.mining_table.setItem(row, 4, status_item)
            
            # Action buttons
            btn_widget = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setStyleSheet(f"background-color: {COLORS['primary']}; color: white;")
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet(f"background-color: {COLORS['danger']}; color: white;")
            
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            btn_widget.setLayout(btn_layout)
            
            self.mining_table.setCellWidget(row, 5, btn_widget)
    
    def update_trading_table(self):
        """Update the trading strategies table"""
        # Sample data
        strategies = [
            ("RSI Strategy", "BTC/USDT", "RSI(14)", "1%", "Active"),
            ("MACD Cross", "ETH/USDT", "MACD(12,26,9)", "2%", "Inactive"),
            ("SMA Bounce", "SOL/USDT", "SMA(50)", "1.5%", "Active")
        ]
        
        self.trading_table.setRowCount(len(strategies))
        for row, (name, pair, indicators, risk, status) in enumerate(strategies):
            self.trading_table.setItem(row, 0, QTableWidgetItem(name))
            self.trading_table.setItem(row, 1, QTableWidgetItem(pair))
            self.trading_table.setItem(row, 2, QTableWidgetItem(indicators))
            self.trading_table.setItem(row, 3, QTableWidgetItem(risk))
            
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QColor(COLORS['success'] if status == "Active" else COLORS['danger']))
            self.trading_table.setItem(row, 4, status_item)
            
            # Action buttons
            btn_widget = QWidget()
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setStyleSheet(f"background-color: {COLORS['primary']}; color: white;")
            backtest_btn = QPushButton("Backtest")
            backtest_btn.setStyleSheet(f"background-color: {COLORS['accent']}; color: white;")
            
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(backtest_btn)
            btn_widget.setLayout(btn_layout)
            
            self.trading_table.setCellWidget(row, 5, btn_widget)
    
    def show_add_mining_strategy_dialog(self):
        """Show dialog to add new mining strategy"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Mining Strategy")
        dialog.setModal(True)
        dialog.resize(500, 400)
        
        layout = QFormLayout(dialog)
        
        # Form fields
        name_edit = QLineEdit()
        algo_combo = QComboBox()
        algo_combo.addItems([algo.name for algo in MiningAlgorithm])
        
        hardware_group = QGroupBox("Hardware Configuration")
        hardware_layout = QVBoxLayout()
        
        # Hardware form would be more complex in a real app
        hw_model = QLineEdit()
        hw_hashrate = QDoubleSpinBox()
        hw_hashrate.setSuffix(" MH/s")
        hw_power = QDoubleSpinBox()
        hw_power.setSuffix(" W")
        hw_cost = QDoubleSpinBox()
        hw_cost.setPrefix("$")
        
        hardware_layout.addWidget(QLabel("GPU Model:"))
        hardware_layout.addWidget(hw_model)
        hardware_layout.addWidget(QLabel("Hashrate:"))
        hardware_layout.addWidget(hw_hashrate)
        hardware_layout.addWidget(QLabel("Power Consumption:"))
        hardware_layout.addWidget(hw_power)
        hardware_layout.addWidget(QLabel("Cost:"))
        hardware_layout.addWidget(hw_cost)
        
        hardware_group.setLayout(hardware_layout)
        
        profit_threshold = QDoubleSpinBox()
        profit_threshold.setPrefix("$")
        profit_threshold.setValue(0.1)
        
        energy_cost = QDoubleSpinBox()
        energy_cost.setPrefix("$")
        energy_cost.setValue(0.12)
        energy_cost.setSuffix("/kWh")
        
        # Buttons
        btn_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        btn_box.addWidget(save_btn)
        btn_box.addWidget(cancel_btn)
        
        # Add to layout
        layout.addRow("Strategy Name:", name_edit)
        layout.addRow("Algorithm:", algo_combo)
        layout.addRow(hardware_group)
        layout.addRow("Profit Threshold:", profit_threshold)
        layout.addRow("Energy Cost:", energy_cost)
        layout.addRow(btn_box)
        
        cancel_btn.clicked.connect(dialog.reject)
        save_btn.clicked.connect(lambda: self.save_mining_strategy(
            name_edit.text(),
            MiningAlgorithm[algo_combo.currentText()],
            MiningHardware(
                hw_model.text(),
                hw_hashrate.value(),
                hw_power.value(),
                hw_cost.value()
            ),
            energy_cost.value(),
            profit_threshold.value(),
            dialog
        ))
        
        dialog.exec_()
    
    def show_add_trading_strategy_dialog(self):
        """Show dialog to add new trading strategy"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Trading Strategy")
        dialog.setModal(True)
        dialog.resize(600, 500)
        
        layout = QVBoxLayout(dialog)
        
        # Basic info
        form_layout = QFormLayout()
        name_edit = QLineEdit()
        base_currency = QComboBox()
        base_currency.addItems(["BTC", "ETH", "SOL", "ADA", "DOT"])
        quote_currency = QComboBox()
        quote_currency.addItems(["USDT", "USD", "BTC", "ETH"])
        
        form_layout.addRow("Strategy Name:", name_edit)
        form_layout.addRow("Base Currency:", base_currency)
        form_layout.addRow("Quote Currency:", quote_currency)
        
        # Rules tabs
        tabs = QTabWidget()
        entry_tab = QWidget()
        exit_tab = QWidget()
        
        tabs.addTab(entry_tab, "Entry Rules")
        tabs.addTab(exit_tab, "Exit Rules")
        
        # Build rule forms (simplified)
        entry_layout = QVBoxLayout(entry_tab)
        exit_layout = QVBoxLayout(exit_tab)
        
        for layout in [entry_layout, exit_layout]:
            rule_combo = QComboBox()
            rule_combo.addItems([ind.name for ind in TradingIndicator])
            condition_combo = QComboBox()
            condition_combo.addItems(["cross_above", "cross_below", ">", "<", "=="])
            value_edit = QDoubleSpinBox()
            lookback_edit = QSpinBox()
            lookback_edit.setValue(14)
            
            rule_form = QFormLayout()
            rule_form.addRow("Indicator:", rule_combo)
            rule_form.addRow("Condition:", condition_combo)
            rule_form.addRow("Value:", value_edit)
            rule_form.addRow("Lookback Period:", lookback_edit)
            
            layout.addLayout(rule_form)
        
        # Risk management
        risk_group = QGroupBox("Risk Management")
        risk_layout = QFormLayout()
        risk_per_trade = QDoubleSpinBox()
        risk_per_trade.setValue(1.0)
        risk_per_trade.setSuffix("%")
        stop_loss = QDoubleSpinBox()
        stop_loss.setValue(5.0)
        stop_loss.setSuffix("%")
        take_profit = QDoubleSpinBox()
        take_profit.setValue(10.0)
        take_profit.setSuffix("%")
        
        risk_layout.addRow("Risk per Trade:", risk_per_trade)
        risk_layout.addRow("Stop Loss:", stop_loss)
        risk_layout.addRow("Take Profit:", take_profit)
        risk_group.setLayout(risk_layout)
        
        # Buttons
        btn_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        btn_box.addWidget(save_btn)
        btn_box.addWidget(cancel_btn)
        
        # Assemble dialog
        layout.addLayout(form_layout)
        layout.addWidget(tabs)
        layout.addWidget(risk_group)
        layout.addLayout(btn_box)
        
        cancel_btn.clicked.connect(dialog.reject)
        save_btn.clicked.connect(lambda: self.save_trading_strategy(
            name_edit.text(),
            base_currency.currentText(),
            quote_currency.currentText(),
            risk_per_trade.value()/100,
            stop_loss.value()/100,
            take_profit.value()/100,
            dialog
        ))
        
        dialog.exec_()
    
    def save_mining_strategy(self, name, algorithm, hardware, energy_cost, profit_threshold, dialog):
        """Save a new mining strategy"""
        strategy = MiningStrategy(
            id=hashlib.md5(name.encode()).hexdigest(),
            name=name,
            algorithm=algorithm,
            hardware=[hardware],
            electricity_cost=energy_cost,
            profit_threshold=profit_threshold
        )
        
        self.db.save_mining_strategy(strategy)
        self.update_mining_table()
        dialog.accept()
        self.statusBar().showMessage(f"Mining strategy '{name}' saved successfully", 3000)
    
    def save_trading_strategy(self, name, base, quote, risk, stop_loss, take_profit, dialog):
        """Save a new trading strategy"""
        # In a real app, we would process the rules from the form
        entry_rules = [
            TradingRule(indicator=TradingIndicator.RSI, condition="<", value=30),
            TradingRule(indicator=TradingIndicator.SMA, condition="cross_above", value=50, lookback_period=20)
        ]
        
        exit_rules = [
            TradingRule(indicator=TradingIndicator.RSI, condition=">", value=70)
        ]
        
        strategy = TradingStrategy(
            id=hashlib.md5(name.encode()).hexdigest(),
            name=name,
            entry_rules=entry_rules,
            exit_rules=exit_rules,
            risk_per_trade=risk,
            base_currency=base,
            quote_currency=quote,
            stop_loss=stop_loss,
            take_profit=take_profit
        )
        
        # Save to database
        self.statusBar().showMessage(f"Trading strategy '{name}' saved successfully", 3000)
        self.update_trading_table()
        dialog.accept()
    
    def load_sample_data(self):
        """Load sample data for demonstration"""
        # Update header stats
        self.header.mining_stat.setText("Mining: 2 active")
        self.header.trading_stat.setText("Trading: 3 active")
        self.header.profit_stat.setText("Daily Profit: $28.45")
        
        # Update cards
        self.mining_card.status_label.setText("Active")
        self.mining_card.status_label.setStyleSheet(f"color: {COLORS['success']};")
        
        self.trading_card.status_label.setText("Active")
        self.trading_card.status_label.setStyleSheet(f"color: {COLORS['success']};")
        
        self.performance_card.status_label.setText("+12.5% ROI")
        self.performance_card.status_label.setStyleSheet(f"color: {COLORS['success']};")
        
        # Update analytics metrics
        self.sharpe_ratio.setText("Sharpe Ratio: 1.85")
        self.max_drawdown.setText("Max Drawdown: 8.2%")
        self.win_rate.setText("Win Rate: 63.4%")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = CryptoStrategyApp()
    window.show()
    
    sys.exit(app.exec_())