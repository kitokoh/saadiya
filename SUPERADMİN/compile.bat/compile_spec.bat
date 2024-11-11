@echo off
REM Chemin de l'environnement virtuel
set VENV_PATH=C:\Users\ibrahim\Downloads\Robot_Labo_Pro\lang

REM Chemins des fichiers .spec
set SPEC_FILE1=C:\Users\ibrahim\Downloads\Robot_Labo_Pro\lang\main.spec
set SPEC_FILE2=C:\Users\ibrahim\Downloads\Robot_Labo_Pro\lang\mini-facebook.spec
set SPEC_FILE3=C:\Users\ibrahim\Downloads\Robot_Labo_Pro\lang\mini-instagram.spec
set SPEC_FILE4=C:\Users\ibrahim\Downloads\Robot_Labo_Pro\lang\mini-linkedin.spec
set SPEC_FILE5=C:\Users\ibrahim\Downloads\Robot_Labo_Pro\lang\miniw-hattssap.spec
set SPEC_FILE6=C:\Users\ibrahim\Downloads\Robot_Labo_Pro\lang\mini-youtube.spec


REM Activation de l'environnement virtuel
call "%VENV_PATH%\Scripts\activate"

REM Exécution de chaque fichier .spec en parallèle
start cmd /k pyinstaller "%SPEC_FILE1%"
start cmd /k pyinstaller "%SPEC_FILE2%"
start cmd /k pyinstaller "%SPEC_FILE3%"
start cmd /k pyinstaller "%SPEC_FILE4%"
start cmd /k pyinstaller "%SPEC_FILE5%"
start cmd /k pyinstaller "%SPEC_FILE6%"

REM Désactiver l'environnement virtuel une fois terminé (facultatif)
deactivate
