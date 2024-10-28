::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC65YQ07vSNLtWuLJIrP41qxGwW+70U0FHJnyWrTg0s=
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
::ZQ05rAF9IAHYFVzEqQITOh5VWAHCGmS2ArAOiA==
::eg0/rx1wNQPfEVWB+kM9LVsJDCeQOWquA/U65+T/6vjn
::fBEirQZwNQPfEVWB+kM9LVsJDCeQOWquA/U65+T/6vjn
::cRolqwZ3JBvQF1fEqQITOh5VWAHCGmS2ArAOiA==
::dhA7uBVwLU+EWG2R5klwBhRCTRCHP2Pa
::YQ03rBFzNR3SWATE2k0mKUgCHGQ=
::dhAmsQZ3MwfNWATEphJifXs=
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRmn5kcxPB4UaguOOG6oZg==
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9keh24fQYxu30Ms3yAVw==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion

rem Définir le chemin du dossier Téléchargements de l'utilisateur
set "downloadDir=%USERPROFILE%\Downloads\AI-FB-Robot"

rem Créer le dossier AI-FB-Robot dans Téléchargements
if not exist "%downloadDir%" (
    mkdir "%downloadDir%"
    echo Dossier AI-FB-Robot créé dans Téléchargements.
)

rem Créer les sous-dossiers media et text
if not exist "%downloadDir%\media" mkdir "%downloadDir%\media"
if not exist "%downloadDir%\text" mkdir "%downloadDir%\text"

rem Initialiser le compteur pour les dossiers roboti
set /a robotCount=0
set "singleRobotDir="

rem Compter les dossiers roboti, y compris cachés
for /f "delims=" %%d in ('dir /b /ad /s C:\bon\robot* 2^>nul') do (
    if exist "%%d" (
        set /a robotCount+=1
        set "singleRobotDir=%%d"
    )
)

rem Vérifier le nombre de dossiers trouvés
if %robotCount% leq 0 (
    echo Aucun dossier roboti trouvé dans C:\bon.
    pause
    exit /b
)

echo Nombre de dossiers roboti trouvés : %robotCount%.

rem Si un seul dossier robot est trouvé, créer directement les fichiers dans text et media
if %robotCount% equ 1 (
    echo {} > "%downloadDir%\text\data.json"
    echo Log du dossier %singleRobotDir% > "%downloadDir%\text\log.txt"
    echo Fichier média associé > "%downloadDir%\media\media.txt"  rem Exemple de fichier média
) else (
    rem Créer les sous-dossiers et les fichiers pour plusieurs dossiers
    for /l %%i in (1,1,%robotCount%) do (
        mkdir "%downloadDir%\media\media%%i"
        mkdir "%downloadDir%\text\text%%i"
        echo {} > "%downloadDir%\text\text%%i\data.json"
        echo Log de text%%i > "%downloadDir%\text\text%%i\text%%i.log"
    )
)

echo Création terminée avec %robotCount% dossiers traités.

exit /b
