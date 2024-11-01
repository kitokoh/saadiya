# import os
# import subprocess
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
# from PyQt5.QtCore import QTimer

# class ChromeLauncher(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#         self.launch_chrome()  # Lancer automatiquement Chrome au démarrage

#     def initUI(self):
#         self.setWindowTitle('Lanceur Chrome avec Profils')
#         self.setGeometry(300, 300, 400, 200)

#         # Ajouter un label pour les messages
#         self.label = QLabel('Démarrage en cours...', self)
#         self.label.move(50, 50)

#     def launch_chrome(self):
#         robot_folder = r'C:\bon'
#         chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

#         # Vérifier si Google Chrome est installé
#         if not os.path.exists(chrome_path):
#             QMessageBox.critical(self, 'Erreur', 'Google Chrome n\'est pas installé à l\'emplacement prévu.')
#             self.close_after_delay()
#             return

#         # Calculer le nombre de dossiers robotX
#         count = 0
#         for folder in os.listdir(robot_folder):
#             if folder.startswith('robot') and os.path.isdir(os.path.join(robot_folder, folder)):
#                 count += 1

#         # Si aucun dossier robotX n'est trouvé
#         if count == 0:
#             QMessageBox.warning(self, 'Avertissement', f'Aucun dossier robot n\'a été trouvé dans {robot_folder}.')
#             self.close_after_delay()
#             return

#         # Afficher le nombre de dossiers trouvés
#         self.label.setText(f'{count} dossiers robot trouvés dans {robot_folder}.')

#         # Boucle pour ouvrir plusieurs instances de Google Chrome avec des profils différents
#         for i in range(1, count + 1):
#             profile_path = os.path.join(os.getenv('USERPROFILE'), f'AppData\\Local\\Google\\Chrome\\User Data\\Profil {i}')
#             url = 'https://www.facebook.com/login'
#             try:
#                 subprocess.Popen([chrome_path, f'--profile-directory=Default', f'--user-data-dir={profile_path}', url])
#                 self.label.setText(f'Google Chrome ouvert avec succès avec le profil {i}.')
#             except Exception as e:
#                 QMessageBox.critical(self, 'Erreur', f'Une erreur est survenue lors de l\'ouverture de Google Chrome avec le profil {i}.')
#                 self.close_after_delay()
#                 return

#         # Fermer l'application après 2 secondes
#         self.close_after_delay()

#     def close_after_delay(self):
#         QTimer.singleShot(000, self.close)  # Ferme la fenêtre après 2 secondes



# def main():
#     app = QApplication(sys.argv)
#     window = ChromeLauncher()
#     window.show()

#     # Démarrer l'application sans attendre d'interaction utilisateur
#     QTimer.singleShot(0, window.launch_chrome)
#     sys.exit(app.exec_())
    
# if __name__ == "__main__":
#     main()  # Appelle la fonction main si le script est exécuté directement



import os
import subprocess
import sys
import time

def launch_chrome():
    robot_folder = r'C:\wabon'
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    # Vérifier si Google Chrome est installé
    if not os.path.exists(chrome_path):
        print("Erreur : Google Chrome n'est pas installé à l'emplacement prévu.")
        return

    # Calculer le nombre de dossiers robotX
    count = 0
    for folder in os.listdir(robot_folder):
        if folder.startswith('robot') and os.path.isdir(os.path.join(robot_folder, folder)):
            count += 1

    # Si aucun dossier robotX n'est trouvé
    if count == 0:
        print(f"Avertissement : Aucun dossier robot n'a été trouvé dans {robot_folder}.")
        return

    # Afficher le nombre de dossiers trouvés
    print(f"{count} dossiers robot trouvés dans {robot_folder}.")

    # Boucle pour ouvrir plusieurs instances de Google Chrome avec des profils différents
    for i in range(1, count + 1):
        profile_path = os.path.join(os.getenv('USERPROFILE'), f'AppData\\Local\\Google\\Chrome\\User Data\\Profil {i}')
        url = 'https://www.wa.com'
        try:
            subprocess.Popen([chrome_path, f'--profile-directory=Default', f'--user-data-dir={profile_path}', url])
            print(f"Google Chrome ouvert avec succès avec le profil {i}.")
        except Exception as e:
            print(f"Erreur lors de l'ouverture de Google Chrome avec le profil {i} : {str(e)}")
            return

    # Fermer l'application après un délai
    print("Lancement terminé. La fenêtre se fermera dans 2 secondes...")
    time.sleep(2)

def main():
    launch_chrome()

if __name__ == "__main__":
    main()  # Appelle la fonction main si le script est exécuté directement
