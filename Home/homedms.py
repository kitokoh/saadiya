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
    def __init__(self):
        super().__init__()
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

        # Home tab
        self.home_btn = RibbonButton(self.tr("Home"))
        self.home_btn.setChecked(True)
        self.home_btn.clicked.connect(lambda: self.show_page("home"))
        self.ribbon.addWidget(self.home_btn)

        # Insert tab
        self.insert_btn = RibbonButton(self.tr("Insert"))
        self.insert_btn.clicked.connect(lambda: self.show_page("insert"))
        self.ribbon.addWidget(self.insert_btn)

        # Layout tab
        self.layout_btn = RibbonButton(self.tr("Layout"))
        self.layout_btn.clicked.connect(lambda: self.show_page("layout"))
        self.ribbon.addWidget(self.layout_btn)

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

        # Create pages
        self.pages = {
            "home": self.create_home_page(),
            "insert": self.create_insert_page(),
            "layout": self.create_layout_page()
        }

        for page in self.pages.values():
            self.stacked_widget.addWidget(page)

        self.show_page("home")

    def create_home_page(self):
        # page = QWidget()
        # layout = QVBoxLayout(page)
        # layout.setAlignment(Qt.AlignCenter)

        # title = QLabel(self.tr("Welcome to the Application"))
        # title.setFont(QFont("Arial", 24, QFont.Bold))
        # layout.addWidget(title, 0, Qt.AlignCenter)

        # subtitle = QLabel(self.tr("Select a tab to begin working"))
        # subtitle.setFont(QFont("Arial", 12))
        # layout.addWidget(subtitle, 0, Qt.AlignCenter)
        from managements.specificationtech import main
            # Créer et afficher la fenêtre principale
        page = MainWindow(parent=self)
        # page.show()
        return page

    def create_insert_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel(self.tr("Insert Page"))
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title, 0, Qt.AlignCenter)

        subtitle = QLabel(self.tr("This is where you would insert elements"))
        subtitle.setFont(QFont("Arial", 12))
        layout.addWidget(subtitle, 0, Qt.AlignCenter)

        return page

    def create_layout_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel(self.tr("Layout Page"))
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title, 0, Qt.AlignCenter)

        subtitle = QLabel(self.tr("This is where you would adjust layout settings"))
        subtitle.setFont(QFont("Arial", 12))
        layout.addWidget(subtitle, 0, Qt.AlignCenter)

        return page

    def show_page(self, page_name):
        if page_name in self.pages:
            self.stacked_widget.setCurrentWidget(self.pages[page_name])
            self.update_button_states(page_name)
            self.status_label.setText(self.tr(f"Showing {page_name} page"))

    def update_button_states(self, active_page):
        self.home_btn.setChecked(active_page == "home")
        self.insert_btn.setChecked(active_page == "insert")
        self.layout_btn.setChecked(active_page == "layout")

    def tr(self, text):
        """Translation method - would connect to actual translation system"""
        return text

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