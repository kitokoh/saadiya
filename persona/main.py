import sys
from PyQt6.QtWidgets import QApplication
from views import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Style application
    app.setStyle("Fusion")
    
    # Création et affichage de la fenêtre principale
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()