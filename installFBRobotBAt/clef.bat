::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC6tbwwxq2FNvSmMNMiS/h/vTQXesRt9LGx6g2zHn2UyY9wI
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kdxy4eg44pSNklCm3OMWTp0LtS0q15Uc1VWBsggM=
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@ECHO OFF
chcp 65001 > nul

:: Ce script CMD fournit des informations système et exécute des scripts de robots en parallèle.

:: Définir les couleurs : texte blanc sur fond bleu
COLOR 1F

:: Définir le titre de la fenêtre
TITLE AI FB ROBOT PRO - Sistem Bilgisi ve Robot Yürütme

:: Effacer l'écran avant d'afficher le contenu
CLS

:: Affichage de la bannière
ECHO ==============================================================================
ECHO                            AI FB ROBOT PRO                          
ECHO ==============================================================================
ECHO                       Sistem bilgileri toplanıyor...                     
ECHO ==============================================================================
ECHO.
ECHO Lütfen bekleyin...
ECHO.

:: Initialiser le compteur de robots
SET robot_sayisi=0

:: Rechercher uniquement les dossiers cachés dans C:\bon qui commencent par "robot"
FOR /F "tokens=*" %%D IN ('DIR /A:DH /B C:\bon\robot*') DO (
    SET /A robot_sayisi+=1
)

:: Affichage du nombre de dossiers de robots trouvés
ECHO ==============================================================================
ECHO %robot_sayisi% gizli robot dizini bulundu.
ECHO ==============================================================================

:: Si aucun dossier robot n'a été trouvé, arrêter le script
IF %robot_sayisi%==0 (
    ECHO Hiç gizli robot dizini bulunamadı! Çıkılıyor...
    ECHO ==============================================================================
    PAUSE
    EXIT /B
)

:: Afficher le message de démarrage des robots
ECHO.
ECHO ==============================================================================
ECHO Robotlar başlatılıyor...
ECHO ==============================================================================

:: Boucle pour exécuter chaque robot dans un CMD séparé
FOR /L %%i IN (1,1,%robot_sayisi%) DO (
    ECHO ==============================================================================
    ECHO Robot %%i için yeni CMD penceresi açılıyor...
    ECHO ==============================================================================

    :: Ouvrir une nouvelle fenêtre CMD avec un titre personnalisé pour chaque robot en simultané
    start "Robot %%i" cmd /c "
    TITLE Robot %%i - AI FB ROBOT PRO
    COLOR 1F
    ECHO ==============================================================================
    ECHO Robot %%i için ortam etkinleştiriliyor...
    ECHO ==============================================================================
    cd /d C:\bon\robot%%i\env%%i\Scripts
    call activate
    
    ECHO ==============================================================================
    ECHO Robot %%i dizinine geçiliyor...
    ECHO ==============================================================================
    cd /d C:\bon\robot%%i
    
    ECHO ==============================================================================
    ECHO Robot %%i scripti çalıştırılıyor...
    ECHO ==============================================================================
    python __post_in_groups__.py
    
    ECHO ==============================================================================
    ECHO Robot %%i tamamlandı.
    ECHO ==============================================================================
    PAUSE
    "
)

ECHO ==============================================================================
ECHO Tüm robotlar farklı CMD pencerelerinde eş zamanlı olarak başlatıldı.
ECHO ==============================================================================
PAUSE
