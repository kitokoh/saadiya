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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kchuoawE3rEpHu2usOdGVpQbyQ0qF4wU1A2AU
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
set "file_path=C:\bon\python.txt"

echo Vérification de l'existence du fichier : %file_path%
REM Vérifie si le fichier existe
if exist "%file_path%" (
    echo Le fichier python.txt existe. Modification des attributs...
    
    REM Affichage des attributs actuels du fichier avant modification
    attrib "%file_path%"
    
    REM Essaye de rendre le fichier caché et système
    attrib +h +s "%file_path%"
    
    REM Affichage des attributs après modification pour vérifier le changement
    attrib "%file_path%"
    
    if %errorlevel%==0 (
        echo [OK] Le fichier python.txt est maintenant invisible.
    ) else (
        echo [ERREUR] Échec lors de la modification des attributs.
    )
) else (
    echo [HATA] Le fichier python.txt n'existe pas dans C:\bon!
)

pause
