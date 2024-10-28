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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kdxy4eg44pSNklCm3OMWTp0LtS0q14U4+EmtyiC3VlC5b
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
set tmpFile=tmp.txt
set logFile=%USERPROFILE%\Desktop\journalInstallation.txt
set errorFlag=0

:: Journalisation dans journalInstallation.txt
echo [INFO] - Script démarré le %date% à %time% >> "%logFile%"

:: Vérification et création du dossier s'il n'existe pas
echo [INFO] - Vérification du dossier %licenceFolder%.
if not exist "%licenceFolder%" (
    echo [INFO] - Création du dossier %licenceFolder%.
    mkdir "%licenceFolder%" || (
        echo [ERROR] - Échec de la création du dossier %licenceFolder%. >> "%logFile%"
        set errorFlag=1
        goto :end
    )
    echo [INFO] - Le dossier %licenceFolder% a été créé avec succès. >> "%logFile%"
) else (
    echo [INFO] - Le dossier %licenceFolder% existe déjà. >> "%logFile%"
)

:: Suppression de l'ancien fichier tmp.txt s'il existe
if exist "%licenceFolder%\%tmpFile%" (
    del "%licenceFolder%\%tmpFile%" || (
        echo [ERROR] - Échec de la suppression de %tmpFile%. >> "%logFile%"
        set errorFlag=1
        goto :end
    )
    echo [INFO] - Le fichier %tmpFile% a été supprimé avec succès. >> "%logFile%"
)

:: Récupération du numéro de série
for /f "tokens=2 delims==" %%A in ('wmic bios get serialnumber /value') do set serial=%%A
if not defined serial (
    echo [ERROR] - Impossible de récupérer le numéro de série. >> "%logFile%"
    set errorFlag=1
    goto :end
)
echo [INFO] - Numéro de série récupéré : %serial%. >> "%logFile%"

:: Définition de l'adresse MAC fixe
set "mac=E4-42-A6-3A-AC"
echo [INFO] - Adresse MAC fixe : %mac%. >> "%logFile%"

:: Récupération de la date et de l'heure
for /f "tokens=1" %%A in ('wmic os get localdatetime ^| find "."') do set datetime=%%A

:: Formatage de la date pour être en dd/mm/yyyy HH:MM
set year=!datetime:~0,4!
set month=!datetime:~4,2!
set day=!datetime:~6,2!
set hour=!datetime:~8,2!
set minute=!datetime:~10,2!

:: Formater l'heure pour l'afficher en 2 chiffres
if !hour! lss 10 set hour=0!hour!
if !minute! lss 10 set minute=0!minute!

set formattedDate=!day!/!month!/!year! !hour!:!minute!
echo [INFO] - Date et heure formatées : %formattedDate%. >> "%logFile%"

:: Récupération du nom de l'utilisateur
set username=%USERNAME%
echo [INFO] - Nom d'utilisateur : %username%. >> "%logFile%"

:: Génération d'une chaîne aléatoire de 500 caractères
set "chars=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
set "randStr="
for /l %%A in (1,1,1000) do (
    set /a "randIndex=!random! %% 70"
    for %%B in (!randIndex!) do set "randStr=!randStr!!chars:~%%B,1!"
)
if not defined randStr (
    echo [ERROR] - La chaîne aléatoire n'a pas été générée correctement. >> "%logFile%"
    set errorFlag=1
    goto :end
)
echo [INFO] - Chaîne aléatoire générée avec succès. >> "%logFile%"

:: Stockage des informations dans tmp.txt
echo [INFO] - Stockage des informations dans %tmpFile%.
echo serial=%serial% > "%licenceFolder%\%tmpFile%"
echo mac=%mac% >> "%licenceFolder%\%tmpFile%"
echo datetime=%formattedDate% >> "%licenceFolder%\%tmpFile%"
echo username=%username% >> "%licenceFolder%\%tmpFile%"
echo randStr=%randStr% >> "%licenceFolder%\%tmpFile%"
echo [INFO] - Informations stockées dans %tmpFile%. >> "%logFile%"

:: Rendre tmp.txt caché et système
attrib +h +s "%licenceFolder%\%tmpFile%"
echo [INFO] - %tmpFile% est maintenant caché et marqué comme fichier système. >> "%logFile%"

:end
:: Enregistrer la fin de l'exécution du script dans le journal
if %errorFlag%==0 (
    echo [INFO] - Script terminé avec succès le %date% à %time%. >> "%logFile%"
) else (
    echo [ERROR] - Le script s'est terminé avec des erreurs le %date% à %time%. >> "%logFile%"
)

