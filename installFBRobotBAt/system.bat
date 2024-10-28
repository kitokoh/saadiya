::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC6tfB8mpiN3pmCEI8LSugzuKg==
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnVphFkfXs=
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unl4ER/Y6dcHewrHu
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
set LOGFILE=%USERPROFILE%\Desktop\journalInstallation.txt

REM Création du fichier de log s'il n'existe pas
if not exist "%LOGFILE%" (
    echo -- Kurulum Günlüğü Başlatılıyor -- >> "%LOGFILE%"
    echo %date% %time% : Kurulum başladı >> "%LOGFILE%"
)

REM Variables de couleur et design de la console
color 1F
mode con: cols=80 lines=30
title FacebookRobotPro - Otomatik Kurulum

REM Affichage d'introduction
cls
echo ================================================================================ 
echo                     FACEBOOK ROBOT PRO KURULUMUNA HOS GELDINIZ                  
echo ================================================================================ 
echo.

REM Vérification de la connexion Internet
echo Internet baglantisi kontrol ediliyor...
ping google.com -n 1 >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Internet baglantisi bulunamadi. Lutfen baglantinizi kontrol edin.
    echo %date% %time% : Internet baglantisi bulunamadi >> "%LOGFILE%"
    exit /b
) else (
    echo Internet baglantisi bulundu.
    echo %date% %time% : Internet baglantisi bulundu >> "%LOGFILE%"
)

REM Vérification de l'installation de Git
git --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Git yüklü degil. Yukleniyor...
    if exist "Git-2.42.0-64-bit.exe" (
        start /wait "" "Git-2.42.0-64-bit.exe" /SILENT /VERYSILENT /NORESTART
        echo %date% %time% : Git yuklendi >> "%LOGFILE%"
    ) else (
        echo Git yükleyici bulunamadi, lutfen yükleyiciyi kontrol edin.
        exit /b
    )
) else (
    for /f "tokens=3" %%v in ('git --version') do set gitversion=%%v
    echo Yüklü sürümü: %gitversion%
    echo %date% %time% : Yüklü  sürümü %gitversion% >> "%LOGFILE%"
)

REM Vérification de l'installation de Python
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python yüklü degil. Yukleniyor...
    if exist "python-3.11.5-amd64.exe" (
        start /wait "" "python-3.11.5-amd64.exe" /quiet InstallAllUsers=1 PrependPath=1
        echo %date% %time% : Python yuklendi >> "%LOGFILE%"
    ) else (
        echo Python yükleyici bulunamadi, lutfen yükleyiciyi kontrol edin.
        exit /b
    )
) else (
    for /f "tokens=2" %%v in ('python --version') do set pyversion=%%v
    echo Yüklü sürümü: %pyversion%
    echo %date% %time% : Yüklü sürümü %pyversion% >> "%LOGFILE%"
)

REM Vérifier si le dossier C:\bon existe
if not exist "C:\bon" (
    echo Dossier C:\bon bulunamadi, 1 instance yuklenecek.
    set instance_count=1
) else (
    REM Demander le nombre d'instances à installer (par défaut 1)
    set /p instance_count="Kac instance yüklemek istiyorsunuz (varsayilan = 1) ? : "
    if "%instance_count%"=="" set instance_count=1
)

REM Boucle pour installer plusieurs instances
for /l %%i in (1,1,%instance_count%) do (
    echo.
    echo ================================================================================ 
    echo                         INSTANS %%i / %instance_count% YÜKLENIYOR                         
    echo ================================================================================ 

    REM Définir le chemin d'installation
    set foldername=C:\bon\robot%%i

    REM Vérifier si l'instance %%i est déjà installée
    if exist "C:\bon\robot%%i" (
        echo Robot%%i zaten yüklenmiş. Bu instance atlanıyor.
        echo %date% %time% : Robot%%i zaten yüklü >> "%LOGFILE%"
    ) else (
        echo Instance %%i yükleniyor...

        REM Créer le dossier d'installation
        cd /d C:\bon
        REM mkdir robot%%i
        echo %date% %time% : robot%%i dizini oluşturuldu >> "%LOGFILE%"

        REM Cloner le dépôt GitHub
        cd /d C:\bon

        git clone https://github.com/kitokoh/facebook-group-bot robot%%i
        echo %date% %time% : GitHub deposu robot%%i için klonlandı >> "%LOGFILE%"

        REM Créer l'environnement virtuel
        cd /d C:\bon\robot%%i

        python -m venv env%%i
        echo %date% %time% : env%%i sanal ortami olusturuldu >> "%LOGFILE%"

        REM Activer l'environnement virtuel
        cd /d C:\bon\robot%%i\env%%i\Scripts
        call activate
        echo %date% %time% : env%%i sanal ortami aktif edildi >> "%LOGFILE%"

        REM Installer les dépendances
        cd /d C:\bon\robot%%i

        pip install -r requirements.txt
        echo %date% %time% : Gereksinimler yüklendi >> "%LOGFILE%"

        REM Installer Selenium
        cd /d C:\bon\robot%%i\env%%i\Scripts
        call activate 
        pip install selenium

        echo %date% %time% : Selenium yüklendi >> "%LOGFILE%"

        REM Rendre le dossier d'installation invisible
        cd /d C:\bon
        attrib +h +s robot%%i
        echo %date% %time% : robot%%i dizini gizlendi >> "%LOGFILE%"
    )
)


pause
REM Fin du script
exit /b