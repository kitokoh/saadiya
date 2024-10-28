::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC6qeA49pW9AumHIIteYshvkWQXctxl+EmZ75w==
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kah2kYhwIvH5Gt3CAecKEtm8=
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion

REM Vérification des droits d'administrateur
openfiles >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Bu komut dosyası yönetici olarak çalıştırılmalıdır.
    pause
    exit /b
)

REM Variables pour la journalisation
set LOGFILE=%USERPROFILE%\Masaüstü\journalInstallation.txt

REM Création du fichier de log s'il n'existe pas
if not exist "%LOGFILE%" (
    echo -- Güncelleme Günlüğü Başlatılıyor -- >> "%LOGFILE%"
    echo %date% %time% : Güncelleme işlemi başladı >> "%LOGFILE%"
)

REM Variables de couleur et design de la console
color 2F
mode con: cols=80 lines=30
title FacebookRobotPro - Tüm Instansları Güncelleme

REM Affichage d'introduction
cls
echo ================================================================================
echo                     FACEBOOK ROBOT PRO INSTANSLARINI GÜNCELLEMEYE HOS GELDINIZ                  
echo ================================================================================

REM Demande de confirmation
set /p confirmation="Tüm instance'ları güncellemek istiyor musunuz? (E/H) : "
if /I not "%confirmation%"=="E" (
    echo Güncelleme işlemi iptal edildi.
    echo %date% %time% : Güncelleme işlemi iptal edildi >> "%LOGFILE%"
    pause
    exit /b
)

REM Boucle pour mettre à jour les instances
set /a instance_index=1

:LOOP
REM Vérifier si l'instance %instance_index% existe
set foldername=C:\bon\robot%instance_index%
if exist "%foldername%" (
    REM Accéder au répertoire de l'instance
    cd /d "%foldername%"
    
    REM Mettre à jour le dépôt GitHub
    echo robot%instance_index% güncelleniyor...
    git pull origin main
    if %ERRORLEVEL% neq 0 (
        echo Git güncellemesi başarısız oldu: robot%instance_index% >> "%LOGFILE%"
    ) else (
        echo %date% %time% : robot%instance_index% başarıyla güncellendi >> "%LOGFILE%"
    )

    REM Réactiver l'environnement virtuel et mettre à jour les dépendances
    if exist "env%instance_index%\Scripts\activate" (
        call "env%instance_index%\Scripts\activate"
        pip install --upgrade -r requirements.txt
        if %ERRORLEVEL% neq 0 (
            echo %date% %time% : robot%instance_index% için bağımlılık güncellemesi başarısız oldu >> "%LOGFILE%"
        ) else (
            echo %date% %time% : robot%instance_index% için bağımlılıklar güncellendi >> "%LOGFILE%"
        )
    )

    REM Passer à l'instance suivante
    set /a instance_index+=1
    goto :LOOP
) else (
    REM Si aucune instance suivante n'existe
    echo Tüm instance'lar başarıyla güncellendi.
    echo %date% %time% : Tüm instance'lar başarıyla güncellendi >> "%LOGFILE%"
    pause
    exit /b
)

REM Fin du script
exit /b
