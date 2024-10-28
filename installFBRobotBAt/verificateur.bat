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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kdxy4eg44pSNklCm3OMWTp0LtS0q18E4iEmN9hGLEiT4pLtZwn6M=
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion

:: Chemins des répertoires
set bonDir=C:\bon
set aiFbRobotDir=%USERPROFILE%\Downloads\AI-FB-Robot
set logFile=%UserProfile%\Desktop\journalinstallation.txt

:: Création du fichier log s'il n'existe pas (ajout à la suite sinon)
if not exist "%logFile%" (
    echo =============================== >> "%logFile%"
    echo Rapport d'installation >> "%logFile%"
    echo =============================== >> "%logFile%"
    echo. >> "%logFile%"
)

:: Démarrage du rapport pour 'bonDir'
echo Démarrage du rapport pour le répertoire %bonDir% >> "%logFile%"
if exist "%bonDir%" (
    set folderCount=0
    for /d %%D in ("%bonDir%\*") do (
        set /a folderCount+=1
        echo Sous-dossier trouvé : %%~nxD >> "%logFile%"
    )
    if !folderCount! gtr 0 (
        echo Total des sous-dossiers trouvés dans %bonDir% : !folderCount! >> "%logFile%"
    ) else (
        echo Aucun sous-dossier trouvé dans %bonDir% >> "%logFile%"
    )
) else (
    echo Le répertoire %bonDir% n'existe pas ! >> "%logFile%"
)
echo. >> "%logFile%"

:: Démarrage du rapport pour 'aiFbRobotDir'
echo Démarrage du rapport pour le répertoire %aiFbRobotDir% >> "%logFile%"
if exist "%aiFbRobotDir%" (
    set itemCount=0
    for /r "%aiFbRobotDir%" %%F in (*) do (
        set /a itemCount+=1
        if "%%~aF" lss "d" (
            echo Fichier trouvé : %%~nxF >> "%logFile%"
        ) else (
            echo Dossier trouvé : %%~nxF >> "%logFile%"
        )
    )
    if !itemCount! gtr 0 (
        echo Total des éléments trouvés dans %aiFbRobotDir% : !itemCount! >> "%logFile%"
    ) else (
        echo Aucun élément trouvé dans %aiFbRobotDir% >> "%logFile%"
    )
) else (
    echo Le répertoire %aiFbRobotDir% n'existe pas ! >> "%logFile%"
)
echo. >> "%logFile%"

:: Fin du script
echo Script terminé. Les informations ont été enregistrées dans "%logFile%". >> "%logFile%"

