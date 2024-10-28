from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(self.tr("Application Example"))

        layout = QVBoxLayout()

        self.label = QLabel(self.tr("Welcome to the app!"))
        layout.addWidget(self.label)

        self.button = QPushButton(self.tr("Click me"))
        self.button.setToolTip(self.tr("This is a clickable button"))
        self.button.clicked.connect(self.show_message)
        layout.addWidget(self.button)

        self.error_button = QPushButton(self.tr("Show Error"))
        self.error_button.setToolTip(self.tr("Click to show an error message"))
        self.error_button.clicked.connect(self.show_error)
        layout.addWidget(self.error_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_message(self):
        QMessageBox.information(self, self.tr("Information"),  "Button clicked successfully!")

    def show_error(self):
        QMessageBox.warning(self, self.tr("Error"),  "An unexpected error occurred.")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
