import glob
import os
import shutil

# Chemins sources à scanner pour les .dll
dll_paths = [
    r"C:\Users\cheic\anaconda3\Library\bin\*.dll",
    r"C:\Users\cheic\anaconda3\Lib\site-packages\PyQt5\Qt5\bin\*.dll"
]

# Dossier cible
output_dir = "dlls"
os.makedirs(output_dir, exist_ok=True)

copied = []

# Copie les fichiers .dll
for pattern in dll_paths:
    for filepath in glob.glob(pattern):
        filename = os.path.basename(filepath)
        dest = os.path.join(output_dir, filename)
        shutil.copy2(filepath, dest)
        copied.append((f'dlls/{filename}', '.'))

# Affiche ce que tu dois coller dans ton .spec :
print("\n📦 A coller dans ton fichier .spec > binaries=\n")
print("binaries = [")
for item in copied:
    print(f"    {item},")
print("]")
