import os
from pathlib import Path

# Configuration
LANGUAGES = ["tr_TR", "ar_SA", "en_US", "pt_BR", "fr_Fr"]
ROOT_DIR = Path(__file__).parent  # Racine du projet
IGNORE_DIRS = {".venv", "__pycache__", "resources"}  # Dossiers à ignorer

def scan_py_files(root):
    """Retourne un dictionnaire {dossier_relatif: [fichiers.py]}"""
    py_files = {}
    for dirpath, _, filenames in os.walk(root):
        dir_rel = str(Path(dirpath).relative_to(root))
        
        # Ignore certains dossiers
        if any(ignore in dir_rel for ignore in IGNORE_DIRS):
            continue
        
        # Filtre les .py
        files = [f.replace(".py", "") for f in filenames if f.endswith(".py")]
        if files:
            py_files[dir_rel.replace("\\", "/")] = files
    return py_files

def generate_translation_commands(py_files):
    """Génère les commandes de traduction pour le .bat"""
    bat_lines = [
        "@echo off",
        "REM ===== Script généré automatiquement =====",
        f"set languages={' '.join(LANGUAGES)}",
        ""
    ]
    
    # 1. Création des dossiers langues
    for lang in LANGUAGES:
        bat_lines.append(f"\nREM Création structure pour {lang}")
        for rel_dir in py_files:
            bat_lines.append(f'mkdir "resources\\lang\\{lang}\\{rel_dir}" 2>nul')
            bat_lines.append(f'mkdir "resources\\langts\\{lang}\\{rel_dir}" 2>nul')
    
    # 2. Commandes pylupdate5
    bat_lines.append("\nREM Génération des fichiers .ts")
    for lang in LANGUAGES:
        for rel_dir, files in py_files.items():
            for file in files:
                src_path = f"{rel_dir}/{file}.py".replace("/", "\\")
                ts_path = f"resources\\langts\\{lang}\\{rel_dir}\\{file}.ts".replace("/", "\\")
                bat_lines.append(f'pylupdate5 "{src_path}" -ts "{ts_path}"')
    
    # 3. Commandes lrelease
    bat_lines.append("\nREM Compilation des .qm")
    for lang in LANGUAGES:
        for rel_dir in py_files:
            ts_dir = f"resources\\langts\\{lang}\\{rel_dir}".replace("/", "\\")
            qm_dir = f"resources\\lang\\{lang}\\{rel_dir}".replace("/", "\\")
            bat_lines.append(f'for %%F in ("{ts_dir}\\*.ts") do lrelease "%%F" -qm "{qm_dir}\\%%~nF.qm"')
    
    bat_lines.append("\necho Traduction terminée !")
    bat_lines.append("pause")
    
    return "\n".join(bat_lines)

if __name__ == "__main__":
    print("Analyse de la structure du projet...")
    py_files = scan_py_files(ROOT_DIR)
    
    print("Génération du script batch...")
    bat_content = generate_translation_commands(py_files)
    
    with open("auto_translate.bat", "w", encoding="utf-8") as f:
        f.write(bat_content)
    
    print("Fichier 'auto_translate.bat' créé avec succès !")
    print(f"Structure détectée : {list(py_files.keys())}")