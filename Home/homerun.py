import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, 
                            QStackedWidget, QToolBar, QStatusBar, QPushButton, 
                            QFrame, QHBoxLayout, QSizePolicy)
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QSize, QTranslator

class RibbonButton(QPushButton):
    def __init__(self, text="", icon=None, parent=None):
        super().__init__(parent)
        self.setText(self.tr(text))
        if icon:
            self.setIcon(QIcon(icon))
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 6px 12px;
                background: transparent;
                color: #333;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #e6e6e6;
                border-radius: 4px;
            }
            QPushButton:pressed {
                background: #d0d0d0;
                border-radius: 4px;
            }
            QPushButton:checked {
                background: #d0d0d0;
                border-radius: 4px;
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Professional Application"))
        self.setGeometry(100, 100, 1200, 800)
        self.setup_ui()
        
        # Setup translator
        self.translator = QTranslator()
        
        # Modern style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QToolBar {
                background: white;
                border-bottom: 1px solid #d0d0d0;
                padding: 4px;
                spacing: 4px;
            }
            QStatusBar {
                background: white;
                border-top: 1px solid #d0d0d0;
            }
        """)

    def setup_ui(self):
        self.create_ribbon()
        self.create_status_bar()
        self.create_main_content()

    def create_ribbon(self):
        # Main ribbon toolbar
        self.ribbon = QToolBar("Ribbon")
        self.ribbon.setIconSize(QSize(20, 20))
        self.addToolBar(self.ribbon)

        # Start tab
        self.start_btn = RibbonButton(self.tr("Start"))
        self.start_btn.setChecked(True)
        self.start_btn.clicked.connect(lambda: self.show_page("start"))
        self.ribbon.addWidget(self.start_btn)

        # Open tab
        self.open_btn = RibbonButton(self.tr("Open"))
        self.open_btn.clicked.connect(lambda: self.show_page("open"))
        self.ribbon.addWidget(self.open_btn)

        # Stat tab
        self.stat_btn = RibbonButton(self.tr("Stat"))
        self.stat_btn.clicked.connect(lambda: self.show_page("stat"))
        self.ribbon.addWidget(self.stat_btn)

        # Separator
        self.ribbon.addSeparator()

        # Clipboard group
        clipboard_group = QFrame()
        clipboard_layout = QHBoxLayout(clipboard_group)
        clipboard_layout.setContentsMargins(0, 0, 0, 0)
        clipboard_layout.setSpacing(2)

        cut_btn = RibbonButton(icon="icons/cut.png")
        cut_btn.setToolTip(self.tr("Cut"))
        copy_btn = RibbonButton(icon="icons/copy.png")
        copy_btn.setToolTip(self.tr("Copy"))
        paste_btn = RibbonButton(icon="icons/paste.png")
        paste_btn.setToolTip(self.tr("Paste"))

        clipboard_layout.addWidget(cut_btn)
        clipboard_layout.addWidget(copy_btn)
        clipboard_layout.addWidget(paste_btn)
        self.ribbon.addWidget(clipboard_group)

    def create_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # Message area
        self.status_label = QLabel(self.tr("Ready"))
        status_bar.addWidget(self.status_label, 1)

        # Status widgets
        zoom_label = QLabel("100%")
        status_bar.addPermanentWidget(zoom_label)

    def create_main_content(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Content area
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Create only the start page initially
        self.pages = {
            "start": self.create_start_page(),
            "open": None,  # Will be created on first access
            "stat": None   # Will be created on first access
        }

        self.stacked_widget.addWidget(self.pages["start"])
        self.show_page("start")

    def create_open_page(self):
        """Create the Open page only when needed"""
        # from page_classes import OpenPage
        page = OpenPage()
        self.pages["open"] = page
        self.stacked_widget.addWidget(page)
        return page

    def create_stat_page(self):
        """Create the Stat page only when needed"""
        # from page_classes import StatPage
        page = StatPage()
        self.pages["stat"] = page
        self.stacked_widget.addWidget(page)
        return page

    def show_page(self, page_name):
        if page_name in self.pages:
            # Create page if it doesn't exist yet
            if self.pages[page_name] is None:
                if page_name == "open":
                    self.create_open_page()
                elif page_name == "stat":
                    self.create_stat_page()

            self.stacked_widget.setCurrentWidget(self.pages[page_name])
            self.update_button_states(page_name)
            self.status_label.setText(self.tr(f"Showing {page_name} page"))

    def update_button_states(self, active_page):
        self.start_btn.setChecked(active_page == "start")
        self.open_btn.setChecked(active_page == "open")
        self.stat_btn.setChecked(active_page == "stat")

    def tr(self, text):
        """Translation method - would connect to actual translation system"""
        return text

    def create_start_page(self):
        # Créer un conteneur pour la page start
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        from manuelleRobot.open import DescriptionManager
        # Créer une instance de l'installateur
        installer = DescriptionManager(parent=page)
        
        # Ajouter l'installateur à la page
        layout.addWidget(installer)
        
        return page

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Modern Fusion style
    app.setStyle("Fusion")
    
    # Light color palette
    palette = app.palette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, Qt.white)
    palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class OpenPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Open Page - Content Manager")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title, 0, Qt.AlignCenter)

        subtitle = QLabel("This is where you would manage your content")
        subtitle.setFont(QFont("Arial", 12))
        layout.addWidget(subtitle, 0, Qt.AlignCenter)

        # Add your specific Open page widgets here
        # Example: content browser, file manager, etc.

class StatPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Stat Page - Analytics Dashboard")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title, 0, Qt.AlignCenter)

        subtitle = QLabel("This is where you would view statistics and analytics")
        subtitle.setFont(QFont("Arial", 12))
        layout.addWidget(subtitle, 0, Qt.AlignCenter)

        # Add your specific Stat page widgets here
        # Example: charts, graphs, metrics, etc.