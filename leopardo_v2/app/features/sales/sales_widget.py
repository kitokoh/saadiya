import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QToolBar
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize

class RibbonButton(QPushButton):
    def __init__(self, text="", icon_path=None, parent=None):
        super().__init__(text, parent)
        if icon_path:
            self.setIcon(QIcon(icon_path))
        self.setCheckable(True)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:checked {
                background-color: #e0e0e0;
            }
        """)

class SalesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.ribbon = QToolBar("Ribbon")
        self.ribbon.setIconSize(QSize(20, 20))
        main_layout.addWidget(self.ribbon)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        self.add_ribbon_button("Documents", "", self.show_documents_page)
        self.add_ribbon_button("Link Manager", "", self.show_link_manager_page)

        # Set the first page as default
        self.show_documents_page()

    def add_ribbon_button(self, text, icon_path, function):
        button = RibbonButton(text, icon_path)
        button.clicked.connect(function)
        self.ribbon.addWidget(button)
        return button

    def show_documents_page(self):
        # Placeholder for now
        self.stacked_widget.setCurrentWidget(QLabel("Documents Page Placeholder"))

    def show_link_manager_page(self):
        # Placeholder for now
        self.stacked_widget.setCurrentWidget(QLabel("Link Manager Page Placeholder"))

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QMainWindow
    app = QApplication(sys.argv)
    window = QMainWindow()
    widget = SalesWidget()
    window.setCentralWidget(widget)
    window.show()
    sys.exit(app.exec_())
