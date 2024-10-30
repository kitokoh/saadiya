import os
import json
import mysql.connector
from mysql.connector import Error

def fetch_media_data():
    """Récupère les descriptions et les chemins des médias à partir de la base de données."""
    try:
        # Connexion à la base de données MySQL
        connection = mysql.connector.connect(
            host='localhost',       # Adresse du serveur MySQL
            database='nom_de_base',  # Nom de la base de données
            user='root',            # Utilisateur MySQL
            password='mot_de_passe'  # Mot de passe MySQL
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            # Sélection des champs description et chemin (path) des médias
            query = "SELECT description, path FROM medias"
            cursor.execute(query)
            result = cursor.fetchall()

            # Si des résultats sont trouvés
            if result:
                return result
            else:
                print("Aucune donnée trouvée dans la table 'medias'.")
                return None

    except Error as e:
        print(f"Erreur lors de la connexion à MySQL : {str(e)}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def save_to_json(data, destination_path):
    """Enregistre les données dans un fichier JSON."""
    try:
        # Vérification de l'existence du dossier textx et création si nécessaire
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        # Enregistrement des données dans le fichier data.json
        with open(destination_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Données enregistrées dans {destination_path}")

    except Exception as e:
        print(f"Erreur lors de l'enregistrement du fichier JSON : {str(e)}")


if __name__ == "__main__":
    # Récupérer les données des médias depuis la base de données
    media_data = fetch_media_data()

    if media_data:
        # Chemin vers le fichier data.json dans Téléchargements
        user_downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads", "fbkrobot", "text1", "data.json")

        # Enregistrer les données dans le fichier data.json
        save_to_json(media_data, user_downloads_dir)
