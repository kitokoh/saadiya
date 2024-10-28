::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC6IfAo1vWdUsymjJcKZtwDsB3uB70Y9Hnc5oWzciC4pLf1tjY0K0C/e
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kdxy4eg44pSNklCm3OMWTp0LtS0q15Vk1GnFSiG/UiTl1Zctt+g==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal

:: Configuration des couleurs : fond bleu (1) et texte blanc (F)
color 1F

:: Variables pour les dossiers
set "userFolder=C:\bon"
set "downloadFolder=%USERPROFILE%\Downloads\AI-FB-Robot"
set "logFile=%USERPROFILE%\Desktop\journalInstallation.txt"

:: Journalisation dans journalInstallation.txt
echo [INFO] - Script démarré le %date% à %time% >> "%logFile%"

:: Création du dossier "bon" dans le répertoire utilisateur s'il n'existe pas
if not exist "%userFolder%" (
    echo [INFO] - Création du dossier bon dans le répertoire utilisateur.
    mkdir "%userFolder%"
    echo [INFO] - Le dossier bon a été créé avec succès.
    echo [INFO] - Dossier bon créé avec succès le %date% à %time% >> "%logFile%"
) else (
    echo [INFO] - Le dossier bon existe déjà.
    echo [INFO] - Dossier bon existant vérifié le %date% à %time% >> "%logFile%"
)

:: Création du dossier "AI-FB-Robot" dans le répertoire "Downloads" s'il n'existe pas
if not exist "%downloadFolder%" (
    echo [INFO] - Création du dossier AI-FB-Robot dans le répertoire Downloads.
    mkdir "%downloadFolder%"
    echo [INFO] - Le dossier AI-FB-Robot a été créé avec succès.
    echo [INFO] - Dossier AI-FB-Robot créé avec succès le %date% à %time% >> "%logFile%"
) else (
    echo [INFO] - Le dossier AI-FB-Robot existe déjà.
    echo [INFO] - Dossier AI-FB-Robot existant vérifié le %date% à %time% >> "%logFile%"
)

:: Fin du script
echo [INFO] - Script terminé le %date% à %time% >> "%logFile%"
echo.
echo [SUCCESS] - Le script a été exécuté avec succès. Consultez le fichier de journalisation pour plus de détails.
