::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC6qeA49pW9AumHIIteYshvkWQXctxl+EmZ75w==
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kdxy4eg44pSNklCm3OMWTp0LtS0q160o6HmtiyWbIiUs=
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion

REM Chemin du dossier contenant les dossiers robotX
set baseDir=C:/bon
set logFile=%UserProfile%/Desktop/journalinstallation.txt

REM Initialiser le fichier log une seule fois
if exist "%logFile%" (
    echo. >> "%logFile%"
    echo =========================================== >> "%logFile%"
    echo Mise à jour des fichiers .env recommencée le %date% à %time% >> "%logFile%"
) else (
    echo Mise à jour des fichiers .env commencée le %date% à %time% > "%logFile%"
)

REM Utiliser PowerShell pour lister tous les dossiers une seule fois
set count=0
for /f "tokens=*" %%i in ('powershell -Command "Get-ChildItem -Path %baseDir% -Directory -Force | Where-Object { $_.Name -like 'robot*' } | Select-Object -ExpandProperty Name"') do (
    set /a count+=1
    set folder[!count!]=%%i
)

REM Vérification du nombre de dossiers à traiter
if !count! equ 0 (
    echo Aucun dossier robot trouvé dans %baseDir%. >> "%logFile%"
    echo Aucun dossier robot trouvé.
    pause
    exit /b
)

echo !count! dossiers trouvés dans %baseDir%. >> "%logFile%"

REM Stocker les résultats du log dans une variable
set logContent=

REM Boucle pour mettre à jour chaque dossier robotX
for /l %%i in (1,1,!count!) do (
    REM Chemin du fichier .env
    set folderName=!folder[%%i]!
    set envFile=%baseDir%\!folderName!\.env

    REM Vérifier si le fichier .env existe
    if exist "!envFile!" (
        (
         echo CHROME_FOLDER ="C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome\\User Data\\Profil %%i"
           echo #for macOS
            echo #CHROME_FOLDER = /Users/your_username/Library/Application Support/Google/Chrome
            echo WAIT_MIN = 5
            echo PROFILE = Default #your profile name into the chrome folder
            echo #based on localization you've to change these values
            echo PUBLISH_LABEL = Post
            echo VISIT_LABEL = Visit
        ) > "!envFile!"

        REM Ajouter au contenu du log
        set logContent=!logContent!Fichier .env mis à jour pour !folderName! à %time%.\n
    ) else (
        set logContent=!logContent!ERREUR : Le fichier .env pour !folderName! n'a pas été trouvé.\n
    )
)

REM Écrire tout le contenu du log en une seule fois
echo !logContent! >> "%logFile%"
echo Mise à jour terminée à %time%. >> "%logFile%"
echo Toutes les mises à jour sont terminées.

exit /b
