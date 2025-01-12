import pygount
from pathlib import Path

def count_lines(directory):
    total_lines = 0
    total_files = 0

    for file_path in Path(directory).rglob("*.py"):  # Parcourir tous les fichiers .py
        analysis = pygount.source_analysis(file_path, "pygount")
        total_lines += analysis.code
        total_files += 1

    return total_files, total_lines

if __name__ == "__main__":
    project_directory = "."  # Remplacez par le chemin de votre projet
    files, lines = count_lines(project_directory)
    print(f"Nombre de fichiers : {files}")
    print(f"Nombre total de lignes de code : {lines}")