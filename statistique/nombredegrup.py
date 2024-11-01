import json

class GroupCounter:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        """Charge le contenu du fichier JSON et renvoie les données."""
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Le fichier spécifié est introuvable.")
            return None
        except json.JSONDecodeError:
            print("Erreur lors de la lecture du fichier JSON.")
            return None
        except Exception as e:
            print(f"Une erreur est survenue : {str(e)}")
            return None

    def count_groups(self):
        """Compte le nombre de groupes dans le fichier JSON."""
        data = self.load_data()
        if data and "groups" in data:
            number_of_groups = len(data["groups"])
            return number_of_groups
        elif data:
            print("Aucune clé 'groups' trouvée dans le fichier JSON.")
            return 0
        return 0

def main():
    file_path = 'data.json'  # Spécifiez le chemin vers votre fichier data.json
    group_counter = GroupCounter(file_path)
    number_of_groups = group_counter.count_groups()

    # Affichez le résultat
    print(f"Nombre de groupes : {number_of_groups}")

if __name__ == "__main__":
    main()
