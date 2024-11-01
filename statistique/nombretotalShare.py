import requests
import os

class LogLineCounter:
    def __init__(self, url):
        self.url = url

    def download_log_file(self):
        """Télécharge le fichier log.txt depuis l'URL fournie."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Vérifie si la requête a réussi
            
            # Enregistre le contenu dans log.txt
            with open('log.txt', 'w') as log_file:
                log_file.write(response.text)

            return 'log.txt téléchargé avec succès.'
        except requests.exceptions.RequestException as e:
            return f"Erreur lors du téléchargement : {str(e)}"

    def count_lines_in_log(self):
        """Compte le nombre de lignes dans log.txt."""
        if not os.path.exists('log.txt'):
            return "Le fichier log.txt n'existe pas. Veuillez le télécharger d'abord."

        with open('log.txt', 'r') as log_file:
            lines = log_file.readlines()
            return len(lines)

    def process_log(self):
        """Télécharge le fichier log et compte les lignes."""
        download_message = self.download_log_file()
        print(download_message)

        line_count = self.count_lines_in_log()
        return f"Nombre de lignes dans log.txt : {line_count}"


def main():
    url = input("Entrez le lien vers log.txt : ")
    log_counter = LogLineCounter(url)
    result = log_counter.process_log()
    print(result)


if __name__ == "__main__":
    main()
