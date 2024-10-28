::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC65YQ07vSNLtWuLJIrP41u4HQW+70U0FHJnyWrTg0s=
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kah2kYhwIv2dRv2aJMuOToBzoT1rH41M1ew==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion

REM Vérification des droits d'administrateur
openfiles >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Ce script doit être exécuté en tant qu'administrateur.
    pause
    exit /b
)

REM Variables pour la journalisation
set LOGFILE=%USERPROFILE%\Desktop\journalInstallation.txt

REM Création du fichier de log s'il n'existe pas
if not exist "%LOGFILE%" (
    echo -- Journalisation du processus de rendu visible démarrée -- >> "%LOGFILE%"
    echo %date% %time% : Processus démarré >> "%LOGFILE%"
)

REM Variables de couleur et design de la console
color 1F
mode con: cols=80 lines=30
title FacebookRobotPro - Rendre les instances visibles

REM Affichage d'introduction
cls
echo ================================================================================ 
echo                  FACEBOOK ROBOT PRO - RENDRE LES INSTANCES VISIBLES               
echo ================================================================================ 
echo.

REM Demander le nombre d'instances à rendre visibles (par défaut 1)
set /p instance_count="Combien d'instances voulez-vous rendre visibles (par défaut = 1) ? : "
if "%instance_count%"=="" set instance_count=1

REM Boucle pour rendre plusieurs instances visibles
for /l %%i in (1,1,%instance_count%) do (
    echo.
    echo ================================================================================ 
    echo                      RENDRE VISIBLE INSTANCE %%i / %instance_count%                     
    echo ================================================================================

    REM Vérifier si le dossier d'instance %%i existe
    if exist "C:\bon\robot%%i" (
        echo Rendre visible l'instance robot%%i...
        attrib -h -s "C:\bon\robot%%i"
        echo %date% %time% : Instance robot%%i est maintenant visible >> "%LOGFILE%"
    ) else (
        echo L'instance robot%%i n'existe pas.
        echo %date% %time% : Instance robot%%i n'existe pas >> "%LOGFILE%"
    )
)

echo ================================================================================ 
echo                 LES DOSSIERS D'INSTANCES SONT MAINTENANT VISIBLES                
echo ================================================================================ 
echo %date% %time% : Processus terminé avec succès >> "%LOGFILE%"
rem pause

REM Fin du script
exit /b
