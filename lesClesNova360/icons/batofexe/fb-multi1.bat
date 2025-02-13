@ECHO OFF
chcp 65001 > nul

:: Définir les couleurs : texte blanc sur fond bleu
COLOR 1F

:: Définir le titre de la fenêtre CMD et réduire sa taille
TITLE AI FB ROBOT PRO - Robot 1
MODE con: cols=60 lines=15

:: Effacer l'écran
CLS

:: Afficher la bannière
ECHO ==============================================================================
ECHO                              AI FB ROBOT PRO                                  
ECHO ==============================================================================
ECHO                  Démarrage de Robot 1 en cours...                    
ECHO ==============================================================================
ECHO.

:: Vérifier si le répertoire de Robot 1 existe
IF NOT EXIST "C:\bon\robot1" (
    ECHO Le répertoire de Robot 1 est introuvable !
    ECHO ==============================================================================
    PAUSE
    EXIT /B
)

:: Activer l'environnement virtuel de Robot 1
ECHO ==============================================================================
ECHO Activation de l'environnement pour Robot 1...
ECHO ==============================================================================
cd /d C:\bon\robot1\env1\Scripts
call activate

:: Naviguer vers le répertoire de Robot 1
ECHO ==============================================================================
ECHO Navigation vers le répertoire de Robot 1...
ECHO ==============================================================================
cd /d C:\bon\robot1

:: Exécuter le script Python de Robot 1
ECHO ==============================================================================
ECHO Exécution du script de Robot 1...
ECHO ==============================================================================
    python __post_in_groupsx__.py

:: Afficher un message de fin
ECHO ==============================================================================
ECHO Le processus de Robot 1 est terminé.
ECHO ==============================================================================
PAUSE

