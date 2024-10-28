::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6UnkwLVeszeY3X3/mbMOQS/kD3OMN8hDRTm8Rs
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
::YxY4rhs+aU+IeA==
::cxY6rQJ7JhzQF1fEqQJhZkoaHmQ=
::ZQ05rAF9IBncCkqN+0xwdVsFAlXMbgs=
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kcxOhZBw7pyBHrmHl
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion

rem Répertoire contenant les sous-dossiers textx
set dossier_texte=%USERPROFILE%\Downloads\AI-FB-Robot\text

rem Chemin du fichier data.json à copier (situé dans le répertoire courant du script)
set fichier_source=%CD%\data.json

rem Fichier de log sur le bureau
set LOGFILE=%USERPROFILE%\Desktop\journalinstallation.txt

rem Vérification que le fichier source existe
if not exist "%fichier_source%" (
    echo [ERREUR] - Le fichier source data.json n'existe pas dans le répertoire courant.
    echo [ERREUR] - Le fichier source data.json n'existe pas dans le répertoire courant. >> "%LOGFILE%"
    pause
    exit /b
)

rem Compter le nombre de sous-dossiers textx dans le dossier_texte
set /a x=0
for /d %%t in ("%dossier_texte%\text*") do (
    set /a x+=1
)

echo Nombre de dossiers textx trouvés: !x!
echo Dossier texte parent : %dossier_texte%
echo Fichier source : %fichier_source%

rem Boucle sur tous les dossiers textx
for /l %%i in (1,1,!x!) do (
    rem Chemin vers le fichier data.json dans le dossier textx
    set fichier_data_texte=%dossier_texte%\text%%i%\data.json

    echo Traitement du dossier text%%i%
    echo Chemin du fichier data.json dans texte : !fichier_data_texte!

    rem Vérification que le fichier data.json existe dans textx
    if exist "!fichier_data_texte!" (
        echo Mise à jour de !fichier_data_texte! avec le contenu de %fichier_source%.
        copy /y "%fichier_source%" "!fichier_data_texte!" >nul
        echo Mise à jour réussie du fichier !fichier_data_texte! >> "%LOGFILE%"
    ) else (
        echo [INFO] - Le fichier data.json n'existe pas dans text%%i%, création en cours.
        copy /y "%fichier_source%" "!fichier_data_texte!" >nul
        echo Fichier data.json créé dans text%%i% >> "%LOGFILE%"
    )
)

echo Toutes les mises à jour sont terminées. >> "%LOGFILE%"

