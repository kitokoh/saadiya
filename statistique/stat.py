from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTabWidget, QPushButton, QFrame, QGridLayout
)
from PyQt5.QtChart import (
    QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis,
    QPieSeries, QLineSeries
)
from PyQt5.QtGui import QFont, QColor, QPainter
from PyQt5.QtCore import Qt
from ui.header import HeaderSection  # Import du header

from ui.footer import FooterSection  # Import du footer
from ui.secondry_menu import SecondaryMenu  # Assurez-vous d'importer votre nouvelle classe
class Dashboard(QMainWindow):
    def __init__(self, title="SAADIYA.AI", subtitle="Analytics Overview"):
        super().__init__()
        
        self.setWindowTitle(title)
        self.setGeometry(100, 210, 900, 600)
        self.setStyleSheet("background-color: #f5f5f5;")

        main_layout = QVBoxLayout()

# Ajouter le header
        header = HeaderSection(self, title=subtitle, app_name=title, slogan="AI Marketing Automation Solution")
        main_layout.addWidget(header)

        # Title Section
        title_label = QLabel("Dashboard")
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setStyleSheet("color: #3f51b5; padding: 1px; text-align: left;")
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Arial", 12, QFont.StyleItalic))
        subtitle_label.setStyleSheet("color: #777; padding: 5px; text-align: left;")
        
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        #main_layout.addWidget(subtitle_label, alignment=Qt.AlignCenter)

        # Tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabBar::tab { 
                background: #3f51b5; 
                color: white; 
                padding: 15px 25px; 
                font-weight: bold; 
                border-radius: 5px; 
                margin: 5px; 
                min-width: 100px; 
                border: 2px solid transparent; /* Ajout d'une bordure transparente pour une belle transition */
            }
            
            QTabBar::tab:selected { 
                background: #1e88e5; 
                border: 2px solid #ffeb3b; /* Bordure jaune lorsque sélectionné */
            }
            
            QTabBar::tab:hover { 
                background: #5f79e8; 
                border: 2px solid #ffeb3b; /* Bordure jaune lors du survol */
            }

            /* Styles pour les flèches */
            QTabBar::tab::before {
                content: "▶"; /* Flèche droite avant le texte */
                color: #ffffff;
                padding-right: 8px; /* Espacement entre la flèche et le texte */
            }

            QTabBar::tab:selected::before {
                content: "▼"; /* Flèche vers le bas pour l'onglet sélectionné */
            }
        """)



        self.tab_general = QWidget()
        self.tab_influence_rate = QWidget()
        self.tab_other_solutions = QWidget()

        self.tab_widget.addTab(self.tab_general, self.tr("General"))
        self.tab_widget.addTab(self.tab_influence_rate, self.tr(" Rate"))
        self.tab_widget.addTab(self.tab_other_solutions, self.tr("Modules"))
        
        main_layout.addWidget(self.tab_widget)
        self.setup_general_tab()
        self.setup_influence_rate_tab()
        self.setup_other_solutions_tab()
        
        # Footer
        footer = QLabel("© 2024 Marketing Automation. All rights reserved.")
        footer.setFont(QFont("Arial", 10))
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #999; padding: 20px;")
        main_layout.addWidget(footer)
        footer2 = FooterSection(self)
        main_layout.addWidget(footer2)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def setup_general_tab(self):
        layout = QVBoxLayout()
        
        # Stat Buttons Row
        stats_layout = QHBoxLayout()
        stats_buttons = [
            (self.tr("License Validity"), "Valid"),
            (self.tr("Next Post Time"), "12:00 PM"),
            (self.tr("Active Groups"), "152"),
            (self.tr("Total Shares"), "5280"),
            (self.tr("Custom Stat"), "Surprise!")
        ]
        
        for title, stat in stats_buttons:
            button = QPushButton(f"{title}\n{stat}")
            button.setFont(QFont("Arial", 14, QFont.Bold))
            button.setStyleSheet("""
                background-color: #4caf50; color: white; padding: 20px; 
                border-radius: 12px; transition: background-color 0.3s;
            """)
            button.setCursor(Qt.PointingHandCursor)
            button.setStyleSheet("""
                background-color: #4caf50; color: white; padding: 20px; 
                border-radius: 12px; transition: background-color 0.3s;
            """)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.get_button_color()}; 
                    color: white; padding: 15px; border-radius: 12px; font-size: 12pt;
                }}
                QPushButton:hover {{
                    background-color: {self.get_hover_color()};
                }}
            """)
            stats_layout.addWidget(button)
        
        layout.addLayout(stats_layout)
        
        # Charts Row
        chart_layout = QHBoxLayout()
        chart_layout.addWidget(self.create_bar_chart())
        chart_layout.addWidget(self.create_line_chart())
        layout.addLayout(chart_layout)

        self.tab_general.setLayout(layout)

    def setup_influence_rate_tab(self):
        layout = QVBoxLayout()
        
        # Title Section
        title = QLabel(self.tr("Influence Rate Analysis"))
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title, alignment=Qt.AlignCenter)

        subtitle = QLabel(self.tr("Detailed insights on marketing impact"))
        subtitle.setFont(QFont("Arial", 16, QFont.StyleItalic))
        layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        # Chart Rows
        for _ in range(2):
            chart_row = QHBoxLayout()
            chart_row.addWidget(self.create_line_chart())
            chart_row.addWidget(self.create_pie_chart())
            layout.addLayout(chart_row)
        
        # Bottom Row
        bottom_layout = QHBoxLayout()
        for _ in range(3):
            label = QLabel("Custom Content")
            label.setFont(QFont("Arial", 12))
            label.setAlignment(Qt.AlignCenter)
            bottom_layout.addWidget(label)
        layout.addLayout(bottom_layout)

        self.tab_influence_rate.setLayout(layout)

    def setup_other_solutions_tab(self):
        layout = QVBoxLayout()

        # Header Section
        title = QLabel(self.tr("Facebook Automation Solutions"))
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title, alignment=Qt.AlignCenter)
        
        subtitle = QLabel(self.tr("Enhance your automation with powerful tools"))
        subtitle.setFont(QFont("Arial", 16, QFont.StyleItalic))
        layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        # Icon Buttons Section
        grid_layout = QGridLayout()
        icons = [
            (self.tr("Auto Comment"), "#ff6f61"),
            (self.tr("Messenger Pro"), "#ffa500"),
            (self.tr("Facebook API"), "#42a5f5"),
            (self.tr("Page Share"), "#7e57c2"),
            (self.tr("Data Scraping"), "#66bb6a"),
            (self.tr("Scheduler"), "#ef5350"),
            (self.tr("Analytics"), "#26a69a"),
            (self.tr("Other Tools"), "#d4e157")
        ]
        
        for i, (name, color) in enumerate(icons):
            button = QPushButton(name)
            button.setFont(QFont("Arial", 12, QFont.Bold))
            button.setStyleSheet(f"""
                background-color: {color}; color: white; padding: 15px; 
                border-radius: 12px; transition: background-color 0.3s;
            """)
            button.setCursor(Qt.PointingHandCursor)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color}; 
                    color: white; padding: 15px; border-radius: 12px; font-size: 12pt;
                }}
                QPushButton:hover {{
                    background-color: {self.get_hover_color()};
                }}
            """)
            grid_layout.addWidget(button, i // 4, i % 4)
        
        layout.addLayout(grid_layout)
        self.tab_other_solutions.setLayout(layout)

    def create_bar_chart(self):
        series = QBarSeries()
        set0 = QBarSet(self.tr("Posts"))
        set0 << 15 << 30 << 20 << 10 << 25 << 18 << 22
        series.append(set0)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(self.tr("Daily Posts"))
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axisX = QBarCategoryAxis()
        axisX.append(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setRange(0, 40)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        return chart_view

    def create_line_chart(self):
        series = QLineSeries()
        series.append(0, 6)
        series.append(1, 4)
        series.append(2, 8)
        series.append(3, 5)
        series.append(4, 10)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(self.tr("Growth Over Time"))
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        axisX = QValueAxis()
        axisX.setRange(0, 4)
        axisX.setTitleText(self.tr("Time"))
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setRange(0, 12)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        return chart_view

    def create_pie_chart(self):
        series = QPieSeries()
        series.append(self.tr("Completed"), 60)
        series.append(self.tr("Pending"), 30)
        series.append(self.tr("Failed"), 10)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(self.tr("Status Distribution"))

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        return chart_view

    def get_hover_color(self):
        return "#3e8e41"  # Couleur au survol des boutons

    def get_button_color(self):
        return "#4caf50"  # Couleur des boutons

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())
