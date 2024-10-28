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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kcxOhXQwmoH5W+GGdMqc=
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion

rem Dossier contenant les sous-dossiers robotx
set dossier_parent=C:\bon

rem Dossier parent pour les fichiers data.json dans AI-FB-Robot (chemin dynamique vers le dossier Téléchargements)
set dossier_texte=%USERPROFILE%\Downloads\AI-FB-Robot\text

rem Fichier de log sur le bureau
set LOGFILE=%USERPROFILE%\Desktop\journalinstallation.txt

rem Compter le nombre de sous-dossiers textx dans le dossier_texte
set /a x=0
for /d %%t in ("%dossier_texte%\text*") do (
    set /a x+=1
)

echo Nombre de dossiers textx trouvés: !x!
echo Dossier texte parent : %dossier_texte%
echo Dossier robot parent : %dossier_parent%

rem Boucle sur tous les dossiers textx et robotx
for /l %%i in (1,1,!x!) do (
    rem Chemin vers le fichier data.json dans le dossier robotx
    set fichier_data_robot=%dossier_parent%\robot%%i%\data.json
    set fichier_data_texte=%dossier_texte%\text%%i%\data.json

    echo Traitement du dossier robot%%i%
    echo Chemin data.json dans robot : !fichier_data_robot!
    echo Chemin data.json dans texte : !fichier_data_texte!

    rem Vérification que les fichiers data.json existent dans robotx et textx
    if exist "!fichier_data_robot!" (
        if exist "!fichier_data_texte!" (
            echo Copie de !fichier_data_texte! vers !fichier_data_robot!
            copy /y "!fichier_data_texte!" "!fichier_data_robot!" >nul
            echo Mise à jour réussie du fichier !fichier_data_robot!
        ) else (
            echo [ERREUR] - Le fichier !fichier_data_texte! n'existe pas.
        )
    ) else (
        echo [ERREUR] - Le fichier !fichier_data_robot! n'existe pas.
    )
)

echo Toutes les mises à jour sont terminées. >> "%LOGFILE%"

