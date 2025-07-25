from PyQt5.QtCore import QThread, pyqtSignal
from Home.giris import SplitScreenView
from Home.login import Nova360ProApp

class LoaderThreadTelecommande(QThread):
    finished = pyqtSignal(object)  # Signal to emit the SplitScreenView instance

    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

    def run(self):
        # Instantiate SplitScreenView in the background
        telecommande_instance = SplitScreenView(main_app=self.main_app)
        self.finished.emit(telecommande_instance)  # Emit the instance once done

class LoaderThread(QThread):
    finished = pyqtSignal(object)  # Signal to emit the Nova360ProApp instance

    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

    def run(self):
        # Instantiate Nova360ProApp in the background
        app_instance = Nova360ProApp(main_app=self.main_app)
        self.finished.emit(app_instance)  # Emit the instance once done
