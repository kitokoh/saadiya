::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC6obwIxu28Pv2eKOYrJ6kLWQ0aN6VwjVWx3iAM=
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kdxy4eg44pSNklCm3OMWTp0LtS0q181s0GnFxjXDfgmU+eNYI
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off



:: Configuration des couleurs : fond bleu (1) et texte blanc (F)
color 1F


:: Vérifier si le dossier robot1 est caché, et le rendre visible si nécessaire
if exist "C:\bon\robot1" (
    echo Vérification si le dossier robot1 est caché...
    attrib -h -s "C:\bon\robot1"
    echo Dossier robot1 accessible.
) else (
    echo [ERREUR] Le dossier C:\bon\robot1 n'existe pas!
    pause
    exit /b
)

:: Afficher un message d'information
echo Mise à jour du fichier data.json avec le nom d'utilisateur courant...

:: Vérifier si le dossier Scripts existe
if exist "C:\bon\robot1\env1\Scripts" (
    echo Accès au dossier Scripts...
    
    :: Activer l'environnement virtuel et exécuter le script Python
    cd /d C:\bon\robot1\env1\Scripts
    call activate
    cd /d C:\bon\robot1\
    echo Exécution du script Python update_json.py...
    cd /d C:\bon\robot1\

    python update_json.py
) else (
    echo [ERREUR] Le dossier Scripts n'existe pas dans C:\bon\robot1!
    pause
    exit /b
)

:: Pause pour afficher le résultat avant de fermer la fenêtre

