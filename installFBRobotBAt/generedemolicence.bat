::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC6jYRonrCNJs33IPsSTvUK1Gx3dtQYHEmtwiHTDwiI4b7M=
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kdxy4eg44pSNklCm3OMWTp0LtS0q14U4+Hnd1k2bUiSY0bNprn80A1m675Eif
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion
:: Configuration des couleurs : fond bleu (1) et texte blanc (F)
color 1F
:: Variables
set licenceFolder=C:\bon
set tmpFile=%licenceFolder%\tmp.txt
set licenceFile=%licenceFolder%\python.txt
set logFile=%USERPROFILE%\Desktop\journalInstallation.txt
set errorFlag=0

:: Vérification de l'existence du fichier tmp.txt
echo [INFO] - Vérification de l'existence du fichier %tmpFile%.
if not exist "%tmpFile%" (
    echo [ERROR] - Le fichier tmp.txt n'a pas été trouvé dans %licenceFolder%. >> "%logFile%"
    echo [ERROR] - Le fichier tmp.txt est introuvable, script annulé.
    pause
    goto :end
)

:: Lecture des informations depuis tmp.txt
echo [INFO] - Lecture des informations depuis tmp.txt.
for /f "tokens=1,* delims==" %%A in (%tmpFile%) do (
    set %%A=%%B
)

:: Debug : Affichage des valeurs lues
echo [DEBUG] - Numéro de série lu : %serial%
echo [DEBUG] - Adresse MAC lue : %mac%
echo [DEBUG] - Date et heure lues : %datetime%
echo [DEBUG] - Nom d'utilisateur lu : %username%
echo [DEBUG] - Chaîne aléatoire lue : %randStr%

:: Vérification des valeurs récupérées
if not defined serial (
    echo [ERROR] - Le numéro de série n'a pas été récupéré correctement. >> "%logFile%"
    set errorFlag=1
)
if not defined mac (
    echo [ERROR] - L'adresse MAC n'a pas été récupérée correctement. >> "%logFile%"
    set errorFlag=1
)
if not defined datetime (
    echo [ERROR] - La date et l'heure n'ont pas été récupérées correctement. >> "%logFile%"
    set errorFlag=1
)
if not defined username (
    echo [ERROR] - Le nom d'utilisateur n'a pas été récupéré correctement. >> "%logFile%"
    set errorFlag=1
)
if not defined randStr (
    echo [ERROR] - La chaîne aléatoire n'a pas été récupérée correctement. >> "%logFile%"
    set errorFlag=1
)

:: Si une erreur est détectée, fin du script
if %errorFlag%==1 (
    echo [ERROR] - Une ou plusieurs erreurs ont été détectées. Le script va se terminer.
    pause
    goto :end
)

:: Traitement de la date et de l'heure pour la mise au format souhaité
for /f "tokens=2 delims==" %%A in ('wmic os get localdatetime /value') do set ldt=%%A

:: Extraction des heures, minutes, jour, mois, année à partir de ldt : format YYYYMMDDHHMMSS
set yyyy=!ldt:~0,4!
set mois=!ldt:~4,2!
set jour=!ldt:~6,2!
set heure=!ldt:~8,2!
set minute=!ldt:~10,2!

:: Construction du format souhaité : HHMMJJMMYYYY
set datetimeFinal=!heure!!minute!!jour!!mois!!yyyy!

:: Debug : Affichage du format de date final
echo [DEBUG] - Date au format final : !datetimeFinal!

:: Suppression des espaces des variables
set mac=!mac: =!
set username=!username: =!
set randStr=!randStr: =!

:: Construction de la licence au format désiré
set licence=003%serial%:%mac%!datetimeFinal!%username%

:: Suppression des espaces dans la licence finale
set licence=!licence: =!

:: Debug : Vérification de la licence générée
echo [DEBUG] - Licence générée : !licence!

:: Vérification de l'existence du fichier lissance.txt
if exist "%licenceFile%" (
    echo [INFO] - Le fichier %licenceFile% existe déjà, aucune action nécessaire. >> "%logFile%"
) else (
    :: Enregistrement de la licence dans lissance.txt
    echo [INFO] - Enregistrement de la licence dans %licenceFile%. >> "%logFile%"
    (
        echo !licence!
        echo !randStr!
    ) > "%licenceFile%" 2>> "%logFile%" || (
        echo [ERROR] - Échec de l'enregistrement dans le fichier %licenceFile%. >> "%logFile%"
        pause
        goto :end
    )

    :: Vérification de l'existence du fichier après écriture
    if exist "%licenceFile%" (
        echo [INFO] - Fichier %licenceFile% créé avec succès. >> "%logFile%"
    ) else (
        echo [ERROR] - Le fichier %licenceFile% n'a pas été trouvé après l'écriture. >> "%logFile%"
        pause
    )

    :: Rendre lissance.txt caché et système
    attrib +h +s "%licenceFile%"
)

:: Suppression du fichier tmp.txt
if exist "%tmpFile%" (
    del "%tmpFile%"
    echo [INFO] - Le fichier tmp.txt a été supprimé avec succès. >> "%logFile%"
) else (
    echo [ERROR] - Le fichier tmp.txt n'a pas été trouvé lors de la suppression. >> "%logFile%"
)

:end
echo [FIN] - Fin du script.

