# import sys
# import time
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar
# )
# from PyQt5.QtCore import Qt, QTimer
# from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor

# class InstallationWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("AI FB Robot Pro - Installation Réussie")
#         self.setGeometry(680, 390, 560, 300)  # Centrer la fenêtre

#         # Mise en page principale
#         self.layout = QVBoxLayout()

#         # Définir la couleur d'arrière-plan
#         palette = QPalette()
#         palette.setColor(QPalette.Background, QColor(30, 30, 30))  # Couleur foncée
#         self.setAutoFillBackground(True)
#         self.setPalette(palette)

#         # Ajout d'un logo (vous pouvez remplacer "your_logo.png" par votre image)
#         self.logo_label = QLabel(self)
#         self.logo_pixmap = QPixmap("your_logo.png").scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
#         self.logo_label.setPixmap(self.logo_pixmap)
#         self.logo_label.setAlignment(Qt.AlignCenter)
#         self.layout.addWidget(self.logo_label)

#         # Message de succès
#         self.success_label = QLabel("Félicitations !\nL'instance a été installée avec succès !", self)
#         self.success_label.setAlignment(Qt.AlignCenter)
#         self.success_label.setFont(QFont("Arial", 16, QFont.Bold))
#         self.success_label.setStyleSheet("color: #00FF00;")  # Texte vert
#         self.layout.addWidget(self.success_label)

#         # Barre de progression pour simuler le chargement
#         self.progress_bar = QProgressBar(self)
#         self.progress_bar.setRange(0, 100)
#         self.layout.addWidget(self.progress_bar)

#         # Appliquer la mise en page
#         self.setLayout(self.layout)

#         # Démarrer le processus d'installation
#         self.start_installation()

#     def start_installation(self):
#         # Simule le chargement
#         self.simulate_loading(100)

#     def simulate_loading(self, max_value):
#         # Simulation de la progression
#         self.progress_bar.setValue(0)
#         for i in range(max_value + 1):
#             QTimer.singleShot(i * 30, lambda value=i: self.progress_bar.setValue(value))  # Incrémente progressivement
#         QTimer.singleShot((max_value + 1) * 30, self.close_window)

#     def close_window(self):
#         # Fermer la fenêtre après quelques secondes
#         QTimer.singleShot(30000, self.close)  # Fermer après 3 secondes

# def main():
#     app = QApplication(sys.argv)

#     # Créer et afficher la fenêtre
#     window = InstallationWindow()
#     window.show()

#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()
import time

def simulate_loading(max_value):
    """Simule le processus de chargement avec une barre de progression dans la console."""
    print("Installation en cours...")
    
    # Barre de progression simulée
    for i in range(max_value + 1):
        progress = int((i / max_value) * 100)
        bar = "[" + "#" * (progress // 10) + " " * (10 - (progress // 10)) + "]"
        print(f"\r{bar} {progress}%", end="")
        time.sleep(0.03)  # Simule l'attente pour chaque incrément

    print("\nFélicitations ! L'instance a été installée avec succès !")

def main():
    """Point d'entrée principal du script."""
    simulate_loading(100)  # Simule un chargement jusqu'à 100%

if __name__ == "__main__":
    main()
