# import sys
# import os
# import subprocess
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QLabel, QMessageBox
# )
# from PyQt5.QtCore import QTimer

# class PythonScriptRunnerApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#         self.run_script()  # Exécute le script au démarrage

#     def initUI(self):
#         self.setWindowTitle("Exécuter le Script Python")
#         self.setGeometry(100, 100, 300, 100)  # Dimension de la fenêtre

#         self.label = QLabel("Exécution du script en cours...", self)
#         self.label.setGeometry(10, 10, 280, 30)  # Positionnement de l'étiquette

#     def run_script(self):
#         # Chemins pour l'environnement virtuel et le script Python
#         env_path = r"C:\bon\robot1\env1\Scripts\activate"
#         script_path = r"C:\bon\robot1\mailapresinstall.py"

#         try:
#             # Commande pour exécuter le script dans l'environnement virtuel
#             command = f'cmd /c "{env_path} && python {script_path}"'
#             result = subprocess.run(command, shell=True, capture_output=True, text=True)

#             # Affiche le résultat de l'exécution du script
#             if result.returncode == 0:
#                # QMessageBox.information(self, "Succès", "Le script a été exécuté avec succès !")
#                 print(result.stdout)  # Affiche la sortie standard
#             else:
#                 QMessageBox.critical(self, "Erreur", "Une erreur est survenue lors de l'exécution du script.")
#                 print(result.stderr)  # Affiche l'erreur si elle existe

#         except Exception as e:
#             QMessageBox.critical(self, "Erreur", f"Une erreur inattendue est survenue : {str(e)}")

#         # Ferme l'application après 1 seconde
#         QTimer.singleShot(0, self.close)




# def main():
#     app = QApplication(sys.argv)

#     # Création et affichage de l'application
#     ex = PythonScriptRunnerApp()
#     ex.show()

#     sys.exit(app.exec_())
    
# if __name__ == "__main__":
#     main()  # Appelle la fonction main si le script est exécuté directement

import os
import subprocess

def run_script(env_path, script_path):
    try:
        # Commande pour exécuter le script dans l'environnement virtuel
        command = f'cmd /c "{env_path} && python {script_path}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Affiche le résultat de l'exécution du script
        if result.returncode == 0:
            print("Le script a été exécuté avec succès !")
            print(result.stdout)  # Affiche la sortie standard
        else:
            print("Une erreur est survenue lors de l'exécution du script.")
            print(result.stderr)  # Affiche l'erreur si elle existe

    except Exception as e:
        print(f"Une erreur inattendue est survenue : {str(e)}")

def main():
    # Chemins pour l'environnement virtuel et le script Python
    env_path = r"C:\bon\robot1\env1\Scripts\activate"
    script_path = r"C:\bon\robot1\mailapresinstall.py"

    # Exécuter le script
    run_script(env_path, script_path)

if __name__ == "__main__":
    main()  # Appelle la fonction main si le script est exécuté directement
