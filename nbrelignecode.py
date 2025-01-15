import pygount
from pathlib import Path

def count_lines(directory, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = []

    total_lines = 0
    total_files = 0

    for file_path in Path(directory).rglob("*.py"):  # Parcourir tous les fichiers .py
        # Vérifier si le fichier est dans un dossier exclu
        if any(str(file_path).startswith(str(Path(directory) / ex)) for ex in exclude_dirs):
            continue

        try:
            analysis = pygount.source_analysis(file_path, "pygount")
            total_lines += analysis.code
            total_files += 1
        except Exception as e:
            print(f"Erreur lors de l'analyse de {file_path}: {e}")

    return total_files, total_lines

if __name__ == "__main__":
    project_directory = "."  # Chemin de votre projet
    # Liste des répertoires à exclure
    exclude = ["venv", "__pycache__", "migrations", "build"]

    files, lines = count_lines(project_directory, exclude_dirs=exclude)
    print(f"Nombre de fichiers : {files}")
    print(f"Nombre total de lignes de code : {lines}")
