@echo off
:: Désactiver l'affichage des commandes

:: Chemin vers le fichier start2.bat
set "start2Path=C:\cpu_monero\start2.bat"

:: Vérifier si xmrig.exe est en cours d'exécution
tasklist /FI "IMAGENAME eq xmrig.exe" 2>nul | find /i "xmrig.exe" >nul
if %errorLevel% == 0 (
    echo xmrig.exe est en cours d'exécution.
    echo Fermeture de xmrig.exe...
    taskkill /IM xmrig.exe /F >nul
    timeout /t 2 /nobreak >nul
) else (
    echo xmrig.exe n'est pas en cours d'exécution.
    echo Démarrage de start2.bat en arrière-plan...
    start "" /B "%start2Path%"
)

:: Fin du script
echo Opération terminée.
