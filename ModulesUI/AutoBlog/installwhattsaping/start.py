import os
import subprocess
import threading

def run_robot_instance(instance_number):
    """Exécute une instance de robotX."""
    # Chemins d'accès
    env_script_path = f"C:\\bons\\robot{instance_number}\\env{instance_number}\\Scripts"
    robot_path = f"C:\\bons\\robot{instance_number}"

    # Commandes à exécuter
    commands = [
        f"cd /d {env_script_path}",
        "call activate",
        f"cd /d {robot_path}",
        "python __post_in_groups__.py"
    ]

    # Exécution des commandes
    try:
        # Chaque commande est exécutée dans le même shell
        process = subprocess.Popen(" && ".join(commands), shell=True)
        process.wait()  # Attendre que le processus se termine
        print(f"Instance robot{instance_number} terminée.")
    except Exception as e:
        print(f"Erreur lors de l'exécution de robot{instance_number}: {e}")

def main():
    """Main function pour parcourir les robots et les exécuter."""
    base_path = "C:\\bons"
    threads = []

    # Vérifier tous les dossiers dans le chemin spécifié
    for entry in os.scandir(base_path):
        if entry.is_dir() and entry.name.startswith("robot"):
            instance_number = entry.name.replace("robot", "")
            try:
                instance_number = int(instance_number)
                thread = threading.Thread(target=run_robot_instance, args=(instance_number,))
                threads.append(thread)
                thread.start()  # Démarrer l'exécution de chaque instance
            except ValueError:
                print(f"Nom de dossier non valide : {entry.name}")

    for thread in threads:
        thread.join()  # Attendre que toutes les threads se terminent

if __name__ == "__main__":
    main()
