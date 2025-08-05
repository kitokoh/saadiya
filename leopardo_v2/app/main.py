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
        from .features.home.home_widget import HomeWidget
        self.home_widget = HomeWidget(self)
        self.add_feature_tab(self.home_widget, "Accueil")

        # Add the new Marketing widget
        from .features.marketing.marketing_widget import MarketingWidget
        self.marketing_widget = MarketingWidget(self)
        self.add_feature_tab(self.marketing_widget, "Marketing")

        # Add the new Sales widget
        from .features.sales.sales_widget import SalesWidget
        self.sales_widget = SalesWidget(self)
        self.add_feature_tab(self.sales_widget, "Sales")

        # Add the new Run widget
        from .features.run.run_widget import RunWidget
        self.run_widget = RunWidget(self)
        self.add_feature_tab(self.run_widget, "Run")

        # Add the new Finance widget
        from .features.finance.finance_widget import FinanceWidget
        self.finance_widget = FinanceWidget(self)
        self.add_feature_tab(self.finance_widget, "Finance")

        # Add the new Settings widget
        from .features.settings.settings_widget import SettingsWidget
        self.settings_widget = SettingsWidget(self)
        self.add_feature_tab(self.settings_widget, "Settings")

        # Add the new Tools widget
        from .features.tools.tools_widget import ToolsWidget
        self.tools_widget = ToolsWidget(self)
        self.add_feature_tab(self.tools_widget, "Tools")

    def add_feature_tab(self, widget, title):
        """Adds a widget as a new tab."""
        self.tab_widget.addTab(widget, title)

if __name__ == "__main__":
    from PyQt5.QtCore import Qt, QCoreApplication
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    window = RefactoredApp()
    window.show()
    sys.exit(app.exec_())
