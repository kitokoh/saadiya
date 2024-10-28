::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAnk
::fBw5plQjdG8=
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSDk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion

:: Définir le numéro de profil à surveiller (i=1 par défaut)
set i=1

:: Chemin du profil utilisateur et du fichier de cookies pour le profil spécifique (Profil 1, Default)
set profilePath=C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Profil %i%\Default
set logFile=C:\bon\check_facebook_login_log.txt

:: Chemin de l'exécutable robot.exe
set robotPath=C:\chemin\vers\robot.exe

:: Initialiser le fichier log
echo [INFO] Vérification de la connexion Facebook pour le profil "Profil %i%" - %date% %time% > "%logFile%"

:: Lancer Google Chrome avec le profil spécifié
echo [INFO] Démarrage de Google Chrome pour le profil "Profil %i%" - %date% %time% >> "%logFile%"
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Profil %i%\Default" https://www.facebook.com
echo [INFO] Google Chrome démarré avec le profil "Profil %i%" - %date% %time% >> "%logFile%"

:: Attendre la création du cookie Facebook
set cookieFound=0
set attempts=0
echo [INFO] En attente de la création du cookie Facebook pour le profil "Profil %i%"... >> "%logFile%"

:waitForCookie
if exist "%profilePath%\Cookies" (
    echo [INFO] Cookie Facebook détecté pour le profil "Profil %i%" - %date% %time% >> "%logFile%"
    echo Cookie Facebook détecté !
    set cookieFound=1
) else (
    set /a attempts+=1
    if %attempts% geq 60 (
        echo [ERREUR] Temps d'attente expiré. Le cookie n'a pas été trouvé pour le profil "Profil %i%" - %date% %time% >> "%logFile%"
        echo Temps d'attente expiré. Le cookie n'a pas été trouvé.
        exit /b
    )
    timeout /t 1 >nul
    goto waitForCookie
)

:: Fermer Google Chrome après la détection du cookie
if %cookieFound%==1 (
    echo [INFO] Fermeture de Google Chrome pour le profil "Profil %i%" - %date% %time% >> "%logFile%"
    echo Fermeture de Google Chrome...
    taskkill /IM chrome.exe /F
)

:: Lancer robot.exe après avoir détecté le cookie
echo [INFO] Lancement de robot.exe après connexion à Facebook pour le profil "Profil %i%" - %date% %time% >> "%logFile%"
echo Lancement de robot.exe...
start "" "%robotPath%"

echo [INFO] Script terminé - %date% %time% >> "%logFile%"
exit /b
