import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QComboBox, QLineEdit, QTableWidget,
                             QTableWidgetItem, QTabWidget, QStackedWidget, QFormLayout,
                             QDoubleSpinBox, QSpinBox, QCheckBox, QTextEdit, QGroupBox,
                             QScrollArea, QFrame, QSizePolicy, QSplitter, QDialog)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import hashlib

from app.components.widgets.finance_helpers import (DatabaseManager, MplCanvas, StrategyCard, DashboardHeader,
                                                  MiningAlgorithm, MiningHardware, MiningStrategy,
                                                  TradingIndicator, TradingRule, TradingStrategy, COLORS)

class FinanceWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.current_theme = 'dark'
        self.init_ui()
        self.load_sample_data()

    def init_ui(self):
        """Initialize the main UI components"""
        main_layout = QVBoxLayout(self)
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
            # btn.setIcon(QIcon(icon))
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

        # Trading performance chart
        trading_chart_widget = QWidget()
        trading_chart_layout = QVBoxLayout(trading_chart_widget)
        trading_chart_layout.addWidget(QLabel("Trading Performance"))
        self.trading_canvas = MplCanvas()
        trading_chart_layout.addWidget(self.trading_canvas)

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
        # add_btn.setIcon(QIcon("icons/add.png"))
        toolbar.addWidget(add_btn)
        layout.addLayout(toolbar)

        # Strategies list
        self.mining_table = QTableWidget()
        self.mining_table.setColumnCount(6)
        self.mining_table.setHorizontalHeaderLabels(["Name", "Algorithm", "Hardware", "Profit", "Status", "Actions"])
        self.mining_table.horizontalHeader().setStretchLastSection(True)
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
        # add_btn.setIcon(QIcon("icons/add.png"))
        toolbar.addWidget(add_btn)
        layout.addLayout(toolbar)

        # Strategies list
        self.trading_table = QTableWidget()
        self.trading_table.setColumnCount(6)
        self.trading_table.setHorizontalHeaderLabels(["Name", "Pair", "Indicators", "Risk", "Status", "Actions"])
        self.trading_table.horizontalHeader().setStretchLastSection(True)
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
        layout.addWidget(self.analytics_canvas)

        return page

    def apply_styles(self):
        """Apply application-wide styles"""
        self.setStyleSheet(f"""
            QWidget {{
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

    def update_mining_chart(self, data=None):
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

    def update_trading_chart(self, data=None):
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

    def update_analytics_chart(self, data=None):
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

    def update_mining_table(self, data=None):
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

    def update_trading_table(self, data=None):
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

    def load_sample_data(self):
        """Load sample data for demonstration"""
        self.update_mining_chart()
        self.update_trading_chart()
        self.update_analytics_chart()
        self.update_mining_table()
        self.update_trading_table()

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
