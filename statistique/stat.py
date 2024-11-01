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
from PyQt5.QtCore import QPropertyAnimation, QRect, Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import subprocess
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QGridLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from ui.header import HeaderSection  # Import du header

from ui.footer import FooterSection  # Import du footer
from ui.secondry_menu import SecondaryMenu  # Assurez-vous d'importer votre nouvelle classe
from statistique.activiteprogramme import Activite
class Dashboard(QMainWindow):
    def __init__(self, title="SAADIYA.AI", subtitle="Analytics Overview", validiter=None, var2=None, var3=None, var4=None, var5=None,
        var6=None, var7=None, var8=None, var9=None, var10=None):
        super().__init__()
        
        self.setWindowTitle(title)
        self.setGeometry(100, 210, 900, 600)
        self.setStyleSheet("background-color: #f5f5f5;")

        # Attribuer les variables pour utilisation dans la classe
        self.validiter = validiter
        self.var2 = var2
        self.var3 = var3
        self.var4 = var4
        self.var5 = var5
        self.var6 = var6
        self.var7 = var7
        self.var8 = var8
        self.var9 = var9
        self.var10 = var10

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
        self.programmer_solutions = QWidget()

        self.tab_widget.addTab(self.tab_general, self.tr("General"))
        self.tab_widget.addTab(self.tab_influence_rate, self.tr(" Rate"))
        self.tab_widget.addTab(self.tab_other_solutions, self.tr("Modules"))
        self.tab_widget.addTab(self.programmer_solutions, self.tr("Programmer"))

        main_layout.addWidget(self.tab_widget)
        self.setup_general_tab()
        self.setup_influence_rate_tab()
        self.setup_other_solutions_tab()
        self.programmer_solutions_tab()
        
        # Footer
        footer = QLabel(self.tr("© 2024 Marketing Automation. Next update: November 15, 2024."))
        footer.setFont(QFont("Arial", 10))
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #999; padding: 20px;")
        main_layout.addWidget(footer)
        footer2 = FooterSection(self)
        main_layout.addWidget(footer2)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
    def programmer_solutions_tab(self):
        layout = QVBoxLayout()
               # Title Section
        title = QLabel(self.tr("Influence Rate Analysis"))
        title.setFont(QFont("Arial", 24, QFont.Bold))
       # layout.addWidget(title, alignment=Qt.AlignCenter)

        subtitle = QLabel(self.tr("Detailed insights on marketing impact"))
        subtitle.setFont(QFont("Arial", 16, QFont.StyleItalic))
        #layout.addWidget(subtitle, alignment=Qt.AlignCenter)
        tableau =QHBoxLayout()
        #root = tk.Tk()
        activite = Activite()
        #root.mainloop()
        #activite = Activite(root)
        tableau.addWidget(activite)
        layout.addLayout(tableau)

        self.programmer_solutions.setLayout(layout)


        pass
    def setup_general_tab(self):
        layout = QVBoxLayout()

        # Stat Buttons Row
        stats_layout = QHBoxLayout()
        stats_buttons = [
            (self.tr("License Valid Until"), self.validiter),
            (self.tr("Next Post Time"), "12:00 PM"),
            (self.tr("Active Groups"), "152"),
            (self.tr("Total Shares"), "5280"),
            (self.tr("Custom Stat"), "Surprise!")
        ]

        for i, (title, stat) in enumerate(stats_buttons):
            button = QPushButton(f"{title}\n{stat}")
            button.setFont(QFont("Arial", 12, QFont.Bold))
            button.setFixedSize(280, 70)  # Taille uniforme
            color = self.get_button_color(i)  # Couleur spécifique par bouton
            hover_color = self.get_hover_color(i)

            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color}; color: white;
                    padding: 10px; border-radius: 12px; 
                    font-size: 12pt; border: 2px solid #333;
                    transition: background-color 0.3s;
                }}
                QPushButton:hover {{
                    background-color: {hover_color};
                }}
            """)
            button.setCursor(Qt.PointingHandCursor)

            # Ajouter effet de clignotement pour le bouton de validité
            if title == self.tr("License Valid Until"):
                self.add_blinking_effect(button)

            stats_layout.addWidget(button)

        layout.addLayout(stats_layout)

        # Charts Row
        chart_layout = QHBoxLayout()
        chart_layout.addWidget(self.create_bar_chart())
        chart_layout.addWidget(self.create_line_chart())
        layout.addLayout(chart_layout)

        self.tab_general.setLayout(layout)

    def get_button_color(self, index):
        colors = ["#4caf50", "#2196f3", "#ff5722", "#9c27b0", "#ffeb3b"]
        return colors[index % len(colors)]

    def get_hover_color(self, index):
        hover_colors = ["#66bb6a", "#42a5f5", "#ff7043", "#ab47bc", "#fff176"]
        return hover_colors[index % len(hover_colors)]

    def add_blinking_effect(self, button):
        self.anim = QPropertyAnimation(button, b"geometry")
        self.anim.setDuration(800)
        self.anim.setLoopCount(-1)  # Animation infinie
        initial_geometry = button.geometry()
        self.anim.setStartValue(QRect(initial_geometry))
        self.anim.setKeyValueAt(0.5, QRect(initial_geometry.adjusted(5, 5, -5, -5)))
        self.anim.setEndValue(QRect(initial_geometry))
        self.anim.start()
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

    # def get_hover_color(self):
    #     return "#3e8e41"  # Couleur au survol des boutons

    # def get_button_color(self):
    #     return "#4caf50"  # Couleur des boutons

#     from PyQt5.QtWidgets import QLabel, QVBoxLayout, QGridLayout, QPushButton, QSizePolicy
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QFont, QColor

    def setup_other_solutions_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Adding margins around the layout

        # Header Section
        title = QLabel(self.tr("Facebook Automation Solutions"))
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #333; margin-bottom: 5px;")  # Darker color for header
        layout.addWidget(title, alignment=Qt.AlignCenter)
        
        subtitle = QLabel(self.tr("Enhance your automation with powerful tools"))
        subtitle.setFont(QFont("Arial", 12, QFont.StyleItalic))
        subtitle.setStyleSheet("color: #555; margin-bottom: 15px;")  # Subtle subtitle color
        layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        # Icon Buttons Section
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(15)  # Horizontal space between buttons
        grid_layout.setVerticalSpacing(15)  # Vertical space between buttons
        
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
            button.setFont(QFont("Arial", 11, QFont.Bold))
            button.setCursor(Qt.PointingHandCursor)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            
            # Enhanced stylesheet for the buttons
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color}; 
                    color: white; 
                    padding: 15px; 
                    border-radius: 12px;
                    font-size: 11pt;
                    font-weight: bold;
                    box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
                    transition: all 0.3s ease;
                }}
                QPushButton:hover {{
                    background-color: {self.get_hover_color(color)}; 
                    box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.35);
                }}
                QPushButton:pressed {{
                    background-color: {self.get_darker_color(color)}; 
                    box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.2);
                }}
            """)
            
            grid_layout.addWidget(button, i // 4, i % 4)
        
        layout.addLayout(grid_layout)
        self.tab_other_solutions.setLayout(layout)

    # Fonction pour obtenir une couleur plus foncée lors du survol
    def get_hover_color(self, color):
        col = QColor(color)
        col = col.darker(110)  # Make it slightly darker for hover effect
        return col.name()

    # Fonction pour une couleur plus sombre lors du clic
    def get_darker_color(self, color):
        col = QColor(color)
        col = col.darker(130)  # Darker color for pressed effect
        return col.name()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())
