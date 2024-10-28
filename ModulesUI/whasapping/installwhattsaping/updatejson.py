import os
import json
import getpass

# Chemin du répertoire à parcourir
base_path = "C:\\Bon"

# Obtenir le nom de l'utilisateur courant
current_user = getpass.getuser()

# Parcourir tous les dossiers dans le répertoire de base
for root, dirs, files in os.walk(base_path):
    for dir_name in dirs:
        if dir_name.startswith("robot"):
            # Chemin complet vers le dossier robotx
            robot_folder_path = os.path.join(root, dir_name)
            # Chemin du fichier JSON (ajustez le nom du fichier si nécessaire)
            json_file_path = os.path.join(robot_folder_path, "data.json")  # Remplacez 'data.json' par le nom de votre fichier JSON

            # Vérifier si le fichier JSON existe
            if os.path.isfile(json_file_path):
                try:
                    # Lire le fichier JSON
                    with open(json_file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                    # Vérifier et mettre à jour le contenu de chaque "image" dans les "posts"
                    for post in data.get("posts", []):
                        if 'abdul' in post.get("image", ""):  # Vérifier si le chemin de l'image contient "abdul"
                            print(f"Avant mise à jour : {post['image']}")  # Affichage avant la mise à jour
                            post["image"] = post["image"].replace("abdul", current_user)  # Remplacer "abdul" par le nom d'utilisateur
                            print(f"Après mise à jour : {post['image']}")  # Affichage après la mise à jour

                    # Écrire les données mises à jour dans le fichier JSON
                    with open(json_file_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)

                    print(f"Mis à jour : {json_file_path}")

                except Exception as e:
                    print(f"Erreur lors de la lecture ou de l'écriture de {json_file_path} : {e}")
            else:
                print(f"Fichier JSON non trouvé : {json_file_path}")
