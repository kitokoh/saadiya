# import os
# import sys
# import datetime
# from PyQt5 import QtWidgets, QtGui, QtCore

# class LicenceGenerator(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()

#         # Initialisation des variables
#         self.licence_folder = 'C:\\bon'
#         self.tmp_file = os.path.join(self.licence_folder, 'tmp.txt')
#         self.licence_file = os.path.join(self.licence_folder, 'python.txt')
#         self.log_file = os.path.join(os.path.expanduser('~'), 'Desktop', 'journalInstallation.txt')
#         self.error_flag = False

#         # Configuration de l'interface utilisateur
#         self.init_ui()

#         # Démarrer immédiatement la génération de licence
#         self.generate_licence()

#     def init_ui(self):
#         # Configuration de la fenêtre
#         self.setWindowTitle('Licence Generator')
#         self.setGeometry(100, 100, 400, 100)

#         # Étiquette de statut
#         self.status_label = QtWidgets.QLabel('Génération de la licence...', self)
#         self.layout = QtWidgets.QVBoxLayout()
#         self.layout.addWidget(self.status_label)
#         self.setLayout(self.layout)

#     def log(self, message):
#         with open(self.log_file, 'a') as log:
#             log.write(f"[{datetime.datetime.now()}] - {message}\n")

#     def generate_licence(self):
#         self.log('Démarrage de la génération de licence.')

#         # Vérification de l'existence du fichier tmp.txt
#         if not os.path.exists(self.tmp_file):
#             self.log(f"[ERROR] - Le fichier {self.tmp_file} n'a pas été trouvé.")
#             self.status_label.setText('Erreur : tmp.txt introuvable.')
#             self.close_after_delay()
#             return

#         self.log('[INFO] - Lecture des informations depuis tmp.txt.')
#         with open(self.tmp_file, 'r') as f:
#             lines = f.readlines()
#             info = {}
#             for line in lines:
#                 key, value = line.strip().split('=')
#                 info[key] = value

#         # Vérification des valeurs récupérées
#         required_keys = ['serial', 'mac', 'datetime', 'username', 'randStr']
#         for key in required_keys:
#             if key not in info:
#                 self.log(f"[ERROR] - {key} n'a pas été récupéré correctement.")
#                 self.error_flag = True

#         if self.error_flag:
#             self.status_label.setText('Erreur : Valeurs manquantes.')
#             self.log('[ERROR] - Une ou plusieurs erreurs ont été détectées. Fin du processus.')
#             self.close_after_delay()
#             return

#         # Traitement de la date et formatage
#         #ldt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#        # datetime_final = ldt[8:10] + ldt[10:12] + ldt[4:6] + ldt[6:8] + ldt[:4]
#         # Traitement de la date et formatage
#         datetime_final = datetime.datetime.now().strftime("%H%M%d%m%Y")

#         # Construction de la licence
#         licence = f"003{info['serial']}:{info['mac'].replace(' ', '')}{datetime_final}{info['username'].replace(' ', '')}"

#         # Vérification de l'existence du fichier python.txt
#         if os.path.exists(self.licence_file):
#             self.log(f"[INFO] - Le fichier {self.licence_file} existe déjà, aucune action nécessaire.")
#         else:
#             # Enregistrement de la licence
#             self.log(f"[INFO] - Enregistrement de la licence dans {self.licence_file}.")
#             try:
#                 with open(self.licence_file, 'w') as f:
#                     f.write(licence + '\n')
#                     f.write(info['randStr'] + '\n')
#                 self.log(f"[INFO] - Fichier {self.licence_file} créé avec succès.")
#                 os.system(f'attrib +h +s "{self.licence_file}"')  # Rendre le fichier caché et système
#             except Exception as e:
#                 self.log(f"[ERROR] - Échec de l'enregistrement dans le fichier {self.licence_file}. {str(e)}")
#                 self.status_label.setText('Erreur : Échec de l\'enregistrement de la licence.')
#                 self.close_after_delay()
#                 return

#         # Suppression du fichier tmp.txt
#         if os.path.exists(self.tmp_file):
#             os.remove(self.tmp_file)
#             self.log(f"[INFO] - Le fichier {self.tmp_file} a été supprimé avec succès.")
#         else:
#             self.log(f"[ERROR] - Le fichier {self.tmp_file} n'a pas été trouvé lors de la suppression.")

#         self.status_label.setText('Licence générée avec succès.')
#         self.log('[FIN] - Fin du processus de génération de licence.')

#         # Fermer l'application après 2 secondes
#         self.close_after_delay()

#     def close_after_delay(self):
#         # Démarrer un timer pour fermer l'application après 2 secondes
#         QtCore.QTimer.singleShot(000, self.close)




# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     window = LicenceGenerator()
#     window.show()
#     sys.exit(app.exec_())
        
# if __name__ == "__main__":
#     main()

import os
import sys
import datetime

class LicenceGenerator:
    def __init__(self):
        # Initialisation des variables
        self.licence_folder = 'C:\\bon'
        self.tmp_file = os.path.join(self.licence_folder, 'tmp.txt')
        self.licence_file = os.path.join(self.licence_folder, 'python.txt')
        self.log_file = os.path.join(os.path.expanduser('~'), 'Desktop', 'journalInstallation.txt')
        self.error_flag = False

        # Démarrer immédiatement la génération de licence
        self.generate_licence()

    def log(self, message):
        with open(self.log_file, 'a') as log:
            log.write(f"[{datetime.datetime.now()}] - {message}\n")

    def generate_licence(self):
        self.log('Démarrage de la génération de licence.')

        # Vérification de l'existence du fichier tmp.txt
        if not os.path.exists(self.tmp_file):
            self.log(f"[ERROR] - Le fichier {self.tmp_file} n'a pas été trouvé.")
            print('Erreur : tmp.txt introuvable.')
            return

        self.log('[INFO] - Lecture des informations depuis tmp.txt.')
        with open(self.tmp_file, 'r') as f:
            lines = f.readlines()
            info = {}
            for line in lines:
                key, value = line.strip().split('=')
                info[key] = value

        # Vérification des valeurs récupérées
        required_keys = ['serial', 'mac', 'datetime', 'username', 'randStr']
        for key in required_keys:
            if key not in info:
                self.log(f"[ERROR] - {key} n'a pas été récupéré correctement.")
                self.error_flag = True

        if self.error_flag:
            print('Erreur : Valeurs manquantes.')
            self.log('[ERROR] - Une ou plusieurs erreurs ont été détectées. Fin du processus.')
            return

        # Traitement de la date et formatage
        datetime_final = datetime.datetime.now().strftime("%H%M%d%m%Y")

        # Construction de la licence
        licence = f"003{info['serial']}:{info['mac'].replace(' ', '')}{datetime_final}{info['username'].replace(' ', '')}"

        # Vérification de l'existence du fichier python.txt
        if os.path.exists(self.licence_file):
            self.log(f"[INFO] - Le fichier {self.licence_file} existe déjà, aucune action nécessaire.")
        else:
            # Enregistrement de la licence
            self.log(f"[INFO] - Enregistrement de la licence dans {self.licence_file}.")
            try:
                with open(self.licence_file, 'w') as f:
                    f.write(licence + '\n')
                    f.write(info['randStr'] + '\n')
                self.log(f"[INFO] - Fichier {self.licence_file} créé avec succès.")
                os.system(f'attrib +h +s "{self.licence_file}"')  # Rendre le fichier caché et système
            except Exception as e:
                self.log(f"[ERROR] - Échec de l'enregistrement dans le fichier {self.licence_file}. {str(e)}")
                print('Erreur : Échec de l\'enregistrement de la licence.')
                return

        # Suppression du fichier tmp.txt
        if os.path.exists(self.tmp_file):
            os.remove(self.tmp_file)
            self.log(f"[INFO] - Le fichier {self.tmp_file} a été supprimé avec succès.")
        else:
            self.log(f"[ERROR] - Le fichier {self.tmp_file} n'a pas été trouvé lors de la suppression.")

        print('Licence générée avec succès.')
        self.log('[FIN] - Fin du processus de génération de licence.')

def main():
    generator = LicenceGenerator()

if __name__ == "__main__":
    main()
