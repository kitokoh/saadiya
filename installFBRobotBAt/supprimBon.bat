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
set "folder_path=C:\bon"

echo Tentative de fermeture des processus utilisant le dossier C:\bon...
REM Utilise handle.exe pour identifier les processus verrouillant le dossier (si handle est installé)
for /f "tokens=2 delims= " %%a in ('handle C:\bon 2^>nul ^| findstr C:\bon') do (
    echo Fermeture du processus PID %%a qui utilise C:\bon...
    taskkill /PID %%a /F
)

REM Pause pour permettre aux processus de se fermer
timeout /t 3 > nul

REM Vérifie si le dossier existe toujours
if exist "%folder_path%" (
    echo Le dossier C:\bon existe, il sera supprimé...
    
    REM Supprimer le dossier et tout son contenu (/s pour tout supprimer, /q pour ne pas demander confirmation)
    rmdir /s /q "%folder_path%"
    
    if exist "%folder_path%" (
        echo [ERREUR] La suppression du dossier C:\bon a échoué!
    ) else (
        echo [OK] Le dossier C:\bon a été supprimé avec succès.
    )
) else (
    echo [ERREUR] Le dossier C:\bon n'existe pas!
)

pause
