::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC6IexwgpmMPn2eKOYq4thzoTUbEwEcxD2Rnk2rTwXprLfZlm8oPnjO78kmxlqYfsQ==
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kbRelaiM7riBHrmHl
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion

:: Variables
set licenceFolder=C:\bon
set licenceFile=test.txt
set errorFlag=0

:: Créer le dossier C:\bon s'il n'existe pas
if not exist %licenceFolder% (
    mkdir %licenceFolder%
    if errorlevel 1 (
        echo [ERROR] - Impossible de créer le dossier %licenceFolder%.
        set errorFlag=1
        goto :end
    )
)

:: Supprimer test.txt s'il existe déjà
if exist %licenceFolder%\%licenceFile% (
    del %licenceFolder%\%licenceFile%
    if errorlevel 1 (
        echo [ERROR] - Impossible de supprimer l'ancien fichier %licenceFile%.
        set errorFlag=1
        goto :end
    )
)

:: Récupérer le numéro de série de l'ordinateur
for /f "tokens=2 delims==" %%A in ('wmic bios get serialnumber /value 2^>nul') do (
    set serial=%%A
)
if not defined serial (
    echo [ERROR] - Impossible de récupérer le numéro de série de l'ordinateur.
    set errorFlag=1
    goto :end
)

:: Récupérer l'adresse MAC au format "E4-42-A6-3A-AC" (première interface active)
for /f "tokens=1 delims=," %%A in ('getmac /fo csv /nh 2^>nul') do (
    if not "%%A"=="N/A" (
        set mac=%%A
        goto :mac_found
    )
)
if not defined mac (
    echo [ERROR] - Impossible de récupérer l'adresse MAC valide.
    set errorFlag=1
    goto :end
)

:mac_found

:: Récupérer la date et l'heure actuelles au format JJMMAAAAHHMM
for /f "tokens=1-4 delims=/ " %%A in ('date /t') do (set currentdate=%%C%%A%%B)
for /f "tokens=1-2 delims=: " %%A in ('time /t') do set currenttime=%%A%%B
set datetime=%currentdate%%currenttime%

:: Récupérer le nom de l'utilisateur actuel
set username=%USERNAME%

:: Générer une chaîne aléatoire de 500 caractères
set "chars=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
set "randStr="
for /l %%A in (1,1,500) do (
    set /a "randIndex=!random! %% 36"
    set "randStr=!randStr!!chars:~!randIndex!,1!"
)

:: Composer la licence : 001[Numéro de série]:[Adresse MAC][DateHeure][NomUtilisateur][500 caractères aléatoires]
set licence=001%serial%:%mac%%datetime%%username%%randStr%

:: Enregistrer la licence dans test.txt
echo %licence% > "%licenceFolder%\%licenceFile%"
if errorlevel 1 (
    echo [ERROR] - Impossible d'écrire dans %licenceFile%.
    set errorFlag=1
    goto :end
)

:: Message de succès
echo [SUCCES] - La licence a été générée et enregistrée dans %licenceFolder%\%licenceFile%.

:end
if %errorFlag%==1 (
    echo [ECHEC] - Une erreur s'est produite pendant l'exécution du script.
) else (
    echo [FIN] - Script exécuté avec succès.
)
pause
