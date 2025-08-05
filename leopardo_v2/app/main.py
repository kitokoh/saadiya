import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget

class RefactoredApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Leopardo V2")
        self.setGeometry(100, 100, 1200, 800)

        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # Tab widget for features
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        # Add the refactored Home widget
        from features.home.home_widget import HomeWidget
        self.home_widget = HomeWidget()
        self.add_feature_tab(self.home_widget, "Accueil")

    def add_feature_tab(self, widget, title):
        """Adds a widget as a new tab."""
        self.tab_widget.addTab(widget, title)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RefactoredApp()
    window.show()
    sys.exit(app.exec_())
