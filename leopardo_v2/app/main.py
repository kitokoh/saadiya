import sys
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
from PyQt5.QtWidgets import QApplication
from .ui.splash_screen import SplashScreen
from .ui.main_window import MainWindow

def main():
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()

    def show_main_window():
        window = MainWindow()
        window.show()
        splash.finish(window)

    QTimer.singleShot(3000, show_main_window)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
