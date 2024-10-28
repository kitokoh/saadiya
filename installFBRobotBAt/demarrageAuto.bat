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
::YxY4rhs+aU+IeA==
::cxY6rQJ7JhzQF1fEqQJhZkoaHmQ=
::ZQ05rAF9IBncCkqN+0xwdVsFAlXMbgs=
::ZQ05rAF9IAHYFVzEqQIDPBpGWESjKX+1Zg==
::eg0/rx1wNQPfEVWB+kM9LVsJDDeWPXmuRpQJ/Oeb
::fBEirQZwNQPfEVWB+kM9LVsJDDeWPXmuRpQJ/Oeb
::cRolqwZ3JBvQF1fEqQIDPBpGWESDKX+1Zg==
::dhA7uBVwLU+EWG2R5klwBhRCTRCHP2Pa
::YQ03rBFzNR3SWATE2k0mKUgCHGQ=
::dhAmsQZ3MwfNWATEphJifXs=
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRml3QIWCltmQwaNKCuKFLp8
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kdxy4eg44pSNklCm3OMWTp0LtS0q14k49GndmhmTVrT4vb51tgsZj
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion

REM ========== Paramètres de Couleur et Interface ==========
:: Texte blanc sur fond bleu
color 1F
:: Ajuster la taille de la fenêtre (80 colonnes, 30 lignes)
mode con: cols=80 lines=30
:: Définir le titre de la fenêtre
title AI FB ROBOT PRO - Kurulum Asistanı

cls
echo ================================================================================
echo.                                 ^| AI FB ROBOT PRO Kurulum ^|
echo ================================================================================
echo.

REM Définir le chemin du fichier de log et info.txt
set LOGFILE=%USERPROFILE%\Desktop\journalInstallation.txt
set INFOFILE=C:\bon\info.txt

REM ========== Journalisation du Processus ==========
if not exist "%LOGFILE%" (
    echo -- Kurulum Günlüğü Başlatılıyor -- >> "%LOGFILE%"
    echo %date% %time% : Kurulum başladı >> "%LOGFILE%"
)

REM ========== Demande d'Email ==========
echo Lütfen email adresinizi girin:
echo.
:: Utilisation de la couleur jaune pour les entrées utilisateur
color 1E
set /p user_email=" Email: "
color 1F
echo.
echo Email '%user_email%' kaydediliyor... >> "%LOGFILE%"
echo Email: %user_email% > "%INFOFILE%"
echo %date% %time% : Email kaydedildi: %user_email% >> "%LOGFILE%"
echo Email '%user_email%' info.txt dosyasina kaydedildi.
echo.

REM ========== Choix pour Démarrage Automatique ==========
echo Facebook Robot'un otomatik olarak başlatılmasını ister misiniz? ^(Evet/Hayır^)
echo.
color 1E
set /p auto_start=" Otomatik Başlat (Evet/Hayır): "
color 1F
echo.

if /I "%auto_start%"=="Evet" (
    echo %date% %time% : Kullanici otomatik baslatmayi secti >> "%LOGFILE%"
    echo Otomatik Baslat: Evet >> "%INFOFILE%"
    echo.

    REM ========== Choix du Type de Démarrage ==========
    echo Bilgisayar başlatıldığında mı, yoksa belirli saatlerde mi başlatılsın? ^(Başlangıç/Saatler^)
    echo.
    color 1E
    set /p start_time=" Başlangıçta mı yoksa saatlerde mi başlatılsın (Başlangıç/Saatler): "
    color 1F
    echo.

    if /I "%start_time%"=="Başlangıç" (
        echo %date% %time% : Kullanici baslangicta baslatmayi secti >> "%LOGFILE%"
        echo Baslatma Yöntemi: Bilgisayar başlatıldığında >> "%INFOFILE%"
        echo Görev başlangıçta eklenecek...
        schtasks /create /sc onlogon /tn "Facebook Robot" /tr "C:\bon\FB-Robot.exe" /rl highest
        echo %date% %time% : Facebook Robot başlangıçta başlatılacak şekilde ayarlandı >> "%LOGFILE%"
    ) else if /I "%start_time%"=="Saatler" (
        echo %date% %time% : Kullanici saatlerle baslatmayi secti >> "%LOGFILE%"
        echo Baslatma Yöntemi: Belirli Saatler >> "%INFOFILE%"
        
        REM ========== Demande de l'Heure de Démarrage ==========
        echo Lütfen başlatmak istediğiniz saatleri girin (örn. 15:00):
        echo.
        color 1E
        set /p schedule_time=" Başlatma Saati: "
        color 1F
        echo.
        echo %date% %time% : Kullanici %schedule_time% saatinde başlatmayi secti >> "%LOGFILE%"
        echo Başlatma Saati: %schedule_time% >> "%INFOFILE%"
        schtasks /create /sc daily /st %schedule_time% /tn "Facebook Robot" /tr "C:\bon\FB-Robot.exe" /rl highest
        echo %date% %time% : Facebook Robot %schedule_time% saatinde başlatılacak şekilde ayarlandı >> "%LOGFILE%"
    )
) else (
    echo %date% %time% : Kullanici otomatik baslatmayi reddetti >> "%LOGFILE%"
    echo Otomatik Baslat: Hayir >> "%INFOFILE%"
)

REM ========== Fin de l'Installation ==========
echo Kurulum tamamlandı. Tüm bilgiler kaydedildi. >> "%LOGFILE%"
echo.
color 1A
echo ================================================================================
echo.                         Kurulum tamamlandı!
echo.                  Bilgiler info.txt ve journalInstallation.txt
echo.                          dosyalarına kaydedildi.
echo ================================================================================
color 1F
echo.
pause
exit /b
