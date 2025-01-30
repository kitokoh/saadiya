import sys
import time
import random
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen, QProgressBar, QMessageBox
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtMultimedia import QSoundEffect

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mon Application PyQt")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        # Ajoutez ici le code pour initialiser votre interface utilisateur
        # Exemple simple : un label ou autre widget
        label = QLabel("Bienvenue dans l'application !", self)
        label.setGeometry(300, 250, 200, 40)
        label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")

def load_random_splash_image():
    splash_images = [
        "chemin/vers/image1.png",  # Remplacez par vos images locales
        "chemin/vers/image2.png",
        "chemin/vers/image3.png",
        "chemin/vers/image4.png"
    ]
    return random.choice(splash_images)

def load_application(splash, progress_bar):
    try:
        splash.showMessage("Chargement des modules...", Qt.AlignBottom | Qt.AlignCenter, Qt.white)
        time.sleep(1)
        progress_bar.setValue(30)

        splash.showMessage("Initialisation des données...", Qt.AlignBottom | Qt.AlignCenter, Qt.white)
        time.sleep(1)
        progress_bar.setValue(60)

        splash.showMessage("Préparation de l'interface...", Qt.AlignBottom | Qt.AlignCenter, Qt.white)
        time.sleep(1)
        progress_bar.setValue(100)
    except Exception as e:
        splash.close()
        QMessageBox.critical(None, "Erreur", f"Une erreur est survenue : {str(e)}")
        sys.exit(1)

def play_loading_sound():
    sound = QSoundEffect()
    sound.setSource(QUrl.fromLocalFile("chemin/vers/son_loading.wav"))  # Remplacez par votre fichier son
    sound.setLoopCount(QSoundEffect.Infinite)
    sound.setVolume(0.5)
    sound.play()

def main():
    app = QApplication(sys.argv)

    # Charger une image aléatoire pour le splash screen
    splash_image_path = load_random_splash_image()
    splash_pix = QPixmap(splash_image_path)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)

    # Ajouter une barre de progression
    progress_bar = QProgressBar(splash)
    progress_bar.setGeometry(10, splash_pix.height() - 30, splash_pix.width() - 20, 20)
    progress_bar.setMaximum(100)
    progress_bar.setTextVisible(False)

    # Afficher le splash screen
    splash.show()

    # Démarrer le son de chargement
    play_loading_sound()

    # Démarrer le chargement dans un thread séparé
    loading_thread = threading.Thread(target=load_application, args=(splash, progress_bar))
    loading_thread.start()

    # Créer et afficher la fenêtre principale après le chargement
    main_window = MainWindow()
    main_window.show()

    # Ajouter une animation de fondu sur le splash screen
    fade_animation = QPropertyAnimation(splash, b"windowOpacity")
    fade_animation.setDuration(1000)
    fade_animation.setStartValue(1.0)
    fade_animation.setEndValue(0.0)
    fade_animation.setEasingCurve(QEasingCurve.OutQuad)
    fade_animation.start()

    # Fermer le splash screen après l'animation
    QTimer.singleShot(1000, splash.close)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
