import os

class RobotFolderCounter:
    def __init__(self, directory):
        self.directory = directory

    def count_robot_folders(self):
        count = 0
        for folder_name in os.listdir(self.directory):
            # Vérifier si le dossier commence par 'robot' et se termine par un chiffre
            if folder_name.startswith("robot") and folder_name[5:].isdigit():
                count += 1
        return count

# Utilisation de la classe
if __name__ == "__main__":
    # Remplacez par le chemin vers votre répertoire
    path_to_directory = "C:/chemin/vers/votre/répertoire"
    
    # Création d'une instance de la classe
    robot_counter = RobotFolderCounter(path_to_directory)
    
    # Compter les dossiers
    instances_count = robot_counter.count_robot_folders()
    
    # Afficher le nombre d'instances
    print(f"Nombre d'instances : {instances_count}")
