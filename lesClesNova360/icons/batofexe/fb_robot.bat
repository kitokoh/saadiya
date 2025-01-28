::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCuDJFeL4kNjfktoZQqRKGq2CrQI4ef1/NaLp14+WOcsVoDN2+fYcNwa6UrqZqok1XVUl80JFB5keBOoaw07pmUPv2eKOYqMvQisHR/Zq3w5FWF7kHCehSg0AA==
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
::Zh4grVQjdCuDJFeL4kNjfktoZQqRKGq2CrQI4ef1/NaLp14+WOcsVoDN2+fYcNwa6UrqZqok1XVUl80JFB5keBCUfAA2pnoMs3yAVw==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion

REM Chemin du fichier à modifier
set "fichier=C:\bon\python.txt"
echo [INFO] Chemin du fichier à modifier : %fichier%

REM Vérifier si le fichier existe
echo [INFO] Vérification de l'existence du fichier...
if not exist "%fichier%" (
    echo [ERREUR] Le fichier %fichier% n'existe pas.
    goto :end
)
echo [INFO] Fichier trouvé.

REM Lire la première ligne du fichier
set "premiere_ligne="
echo [INFO] Lecture de la première ligne du fichier...
for /f "usebackq delims=" %%A in ("%fichier%") do (
    set "premiere_ligne=%%A"
    echo [INFO] Première ligne lue : !premiere_ligne!
    goto :check_conditions
)

:check_conditions
REM Vérifie si la première ligne commence par A1a9003 et se termine par 212
echo [INFO] Vérification des conditions (début par 'A1a9003' et fin par '212')...
if "!premiere_ligne:~0,7!"=="A1a9003" if "!premiere_ligne:~-3!"=="212" (
    echo [INFO] Conditions remplies. Préparation de la modification...
    
    REM Modifier A1a9003 par A1a9333
    set "nouvelle_ligne=!premiere_ligne:A1a9003=A1a9333!"
    echo [INFO] Nouvelle ligne après modification : !nouvelle_ligne!

    REM Créer un fichier temporaire avec la modification
    echo [INFO] Création d'un fichier temporaire pour appliquer les modifications...
    > "%fichier%.tmp" (
        echo !nouvelle_ligne!
        more +1 "%fichier%" >> "%fichier%.tmp"
    )
    
    REM Remplacer le fichier original par le fichier temporaire
    echo [INFO] Remplacement du fichier original par le fichier temporaire...
    move /y "%fichier%.tmp" "%fichier%" >nul
    echo [SUCCES] Modification réussie : 'A1xxx' a été remplacé par 'A1ayyyyy' dans %fichier%.
) else (
    echo [INFO] Conditions non remplies. Aucune modification n'a été effectuée.
)

:end
echo [INFO] Fin du script.
pause
endlocal
