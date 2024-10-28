import os
import re

def add_self_tr_to_strings(file_path):
    """Lit le contenu d'un fichier Python, ajoute self.tr() aux chaînes simples dans les composants PyQt5 et enregistre les modifications."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex pour détecter les chaînes de caractères simples dans les appels des méthodes PyQt5
    pyqt_methods = [
        r'setWindowTitle\((["\'])(.*?)(\1)\)',         # setWindowTitle("...")
        r'QLabel\((["\'])(.*?)(\1)\)',                # QLabel("...")
        r'QPushButton\((["\'])(.*?)(\1)\)',           # QPushButton("...")
        r'setToolTip\((["\'])(.*?)(\1)\)',            # setToolTip("...")
        r'QMessageBox\.(information|warning|critical|question)\(([^,]+),\s*(["\'])(.*?)(\3)\)'  # QMessageBox...
    ]

    def replace_string(match):
        full_match = match.group(0)  # Expression complète
        quote = match.group(1)       # Le type de guillemet utilisé (simple ou double)
        text = match.group(2)        # Le texte à traduire

        # Vérifie si self.tr() est déjà là
        if 'self.tr(' not in full_match:
            # Ajoute self.tr() autour de la chaîne
            return full_match.replace(f'{quote}{text}{quote}', f'self.tr({quote}{text}{quote})')
        return full_match

    # Applique la regex sur le contenu pour chaque méthode PyQt5 à modifier
    for method in pyqt_methods:
        content = re.sub(method, replace_string, content)

    # Gérer les QMessageBox avec plusieurs chaînes
    content = re.sub(
        r'QMessageBox\.(information|warning|critical|question)\(([^,]+),\s*(["\'])(.*?)(\3)(,)?(.*)?\)', 
        lambda m: f'QMessageBox.{m.group(1)}({m.group(2)}, self.tr({m.group(3)}{m.group(4)}{m.group(5)}), {m.group(7) if m.group(7) else ""})', 
        content
    )

    # Écrire le contenu modifié dans le fichier
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def modify_python_files_in_directory(directory):
    """Parcourt tous les fichiers .py d'un répertoire et applique la modification aux chaînes de caractères dans les composants PyQt5."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f'Modification du fichier : {file_path}')
                add_self_tr_to_strings(file_path)

if __name__ == "__main__":
    # Remplacez 'chemin_du_dossier' par le chemin du dossier contenant les fichiers .py
    directory = "../TEST"  # Changez ce chemin selon vos besoins
    modify_python_files_in_directory(directory)
