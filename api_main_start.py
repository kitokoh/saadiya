# main.py
from imports import *
# Démarrer le serveur FastAPI
def start_api():
    process = subprocess.Popen([sys.executable, "api.py"])
    time.sleep(2)  # Laisser le temps au serveur FastAPI de démarrer
    return process

# Lancer l'interface PyQt
def start_pyqt():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    api_process = start_api()  # Démarrer FastAPI
    try:
        start_pyqt()  # Démarrer PyQt
    finally:
        api_process.terminate()  # Terminer FastAPI quand l'interface se ferme
