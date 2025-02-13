::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFDpQQQ2MNXiuFLQI5/rH/OuGpkQEVd4zfZz41rGdDu8F6xayJaok1XVUi/cFDxRWcRSudgoIr29Bs2aKOMzRugzuRAWZ6Ex9TDIkylTZgi80d8Amk8AMsw==
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
::Zh4grVQjdCyDJGyX8VAjFDpQQQ2MNXiuFLQI5/rH/OuGpkQEVd4zfZz41rGdDu8F6xayJaok1XVUi/cFDxRWcRSudgoIr2x9pGuHONPI/Qr5Tyg=
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@ECHO OFF
chcp 65001 > nul

:: Définir les couleurs : texte blanc sur fond bleu
COLOR 1F

:: Définir le titre de la fenêtre CMD et réduire sa taille
TITLE AI FB ROBOT PRO - Robot 4
MODE con: cols=60 lines=15

:: Effacer l'écran
CLS

:: Afficher la bannière
ECHO ==============================================================================
ECHO                              AI FB ROBOT PRO                                  
ECHO ==============================================================================
ECHO                  Démarrage de Robot 4 en cours...                    
ECHO ==============================================================================
ECHO.

:: Vérifier si le répertoire de Robot 4 existe
IF NOT EXIST "C:\bon\robot4" (
    ECHO Le répertoire de Robot 4 est introuvable !
    ECHO ==============================================================================
    PAUSE
    EXIT /B
)

:: Activer l'environnement virtuel de Robot 4
ECHO ==============================================================================
ECHO Activation de l'environnement pour Robot 4...
ECHO ==============================================================================
cd /d C:\bon\robot4\env1\Scripts
call activate

:: Naviguer vers le répertoire de Robot 4
ECHO ==============================================================================
ECHO Navigation vers le répertoire de Robot 4...
ECHO ==============================================================================
cd /d C:\bon\robot4

:: Exécuter le script Python de Robot 4
ECHO ==============================================================================
ECHO Exécution du script de Robot 4...
ECHO ==============================================================================
python __post_in_groups__.py

:: Afficher un message de fin
ECHO ==============================================================================
ECHO Le processus de Robot 4 est terminé.
ECHO ==============================================================================
PAUSE