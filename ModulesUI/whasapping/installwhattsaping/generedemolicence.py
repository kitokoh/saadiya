import os
import sys
import datetime
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

class LicenceGenerator:
    def __init__(self):
        # Initialisation des variables
        self.licence_folder = 'C:\\wabon'
        self.tmp_folder = 'C:\\wabon'
        self.tmp_file = os.path.join(self.tmp_folder, 'tmp.txt')
        self.licence_file = os.path.join(self.licence_folder, 'python.txt')
        self.log_file = os.path.join(user_data_dir, 'resources', 'journalInstallation.txt')
        self.error_flag = False

        # Démarrer immédiatement la génération de licence
        self.generate_licence()

    def log(self, message):
        with open(self.log_file, 'a') as log:
            log.write(f"[{datetime.datetime.now()}] - {message}\n")

    def generate_licence(self):
        # Vérification de l'existence de python.txt
        if os.path.exists(self.licence_file):
            self.log(f"[INFO] - Le fichier {self.licence_file} existe déjà. Aucune nouvelle licence générée.")
            print(f"Licence non générée : le fichier {self.licence_file} existe déjà.")
            return

        self.log('Démarrage de la génération de licence.')

        # Vérification de l'existence du fichier tmp.txt
        if not os.path.exists(self.tmp_file):
            self.log(f"[ERROR] - Le fichier {self.tmp_file} n'a pas été trouvé.")
            print('Erreur : tmp.txt introuvable.')
            return
        else:
            self.log(f"[INFO] - Le fichier {self.tmp_file} a été trouvé.")

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
        licence = f"A1a9003{info['serial']}:{info['mac'].replace(' ', '')}{datetime_final}{info['username'].replace(' ', '')}"

        # Enregistrement de la licence
        self.log(f"[INFO] - Enregistrement de la licence dans {self.licence_file}.")
        try:
            with open(self.licence_file, 'w') as f:
                f.write(licence + '\n')
                #f.write(info['randStr'] + '\n')
            
            self.log(f"[INFO] - Fichier {self.licence_file} créé avec succès.")
            os.system(f'attrib +h +s "{self.licence_file}"')  # Rendre le fichier caché et système
        except Exception as e:
            self.log(f"[ERROR] - Échec de l'enregistrement dans le fichier {self.licence_file}. {str(e)}")
            print(f'Erreur : Échec de l\'enregistrement de la licence. Détails : {str(e)}')
            return

        # Suppression du fichier tmp.txt après génération de la licence
        if os.path.exists(self.tmp_file):
            try:
                os.remove(self.tmp_file)
                self.log(f"[INFO] - Le fichier {self.tmp_file} a été supprimé avec succès après la génération de la licence.")
            except Exception as e:
                self.log(f"[ERROR] - Échec de la suppression du fichier {self.tmp_file}. {str(e)}")
        else:
            self.log(f"[ERROR] - Le fichier {self.tmp_file} n'a pas été trouvé lors de la tentative de suppression.")

        print('Licence générée avec succès.')
        self.log('[FIN] - Fin du processus de génération de licence.')

def main():
    generator = LicenceGenerator()

if __name__ == "__main__":
    main()
