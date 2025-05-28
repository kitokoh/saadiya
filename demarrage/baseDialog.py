
from typing import List, Dict, Optional, Tuple, Callable
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QVBoxLayout, 
                            QLabel, QPushButton, QCheckBox, QLineEdit, 
                            QMessageBox, QWidget)
class BaseDialog(QDialog):
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)
        self.setModal(True)
        self.init_ui()
        
    def init_ui(self):
        raise NotImplementedError("Subclasses must implement init_ui")
    
    def get_results(self) -> Dict:
        return {}
