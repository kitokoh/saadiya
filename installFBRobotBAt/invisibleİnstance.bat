::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC65YQ07vSNLtWuLJIrP41qxGwW+70U0FHJnyWrTg0s=
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kdxy4eg44pSNklCm3OMWTp0LtS0q170UmEnZ9hW/VpSUodNJmmcZN1ji7nA==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion

REM Yönetici haklarının kontrol edilmesi
openfiles >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Bu script yönetici olarak çalıştırılmalıdır.
    pause
    exit /b
)

REM Günlük kaydı için değişkenler
set LOGFILE=%USERPROFILE%\Masaüstü\journalInstallation.txt

REM Günlük dosyasının oluşturulması (mevcut değilse)
if not exist "%LOGFILE%" (
    echo -- Gizleme işlemi günlüğü başlatıldı -- >> "%LOGFILE%"
    echo %date% %time% : İşlem başlatıldı >> "%LOGFILE%"
)

REM Konsol renk ve tasarım değişkenleri
color 1F
mode con: cols=80 lines=30
title FacebookRobotPro - Bir oturumu gizle

REM Giriş ekranı
cls
echo ================================================================================ 
echo                         FACEBOOK ROBOT PRO - BİR OTURUMU GİZLE                        
echo ================================================================================ 
echo.

REM Kullanıcıdan gizlenecek oturum numarası istenir
set /p instance_number="Gizlenecek oturum numarasını girin (Varsayılan: 1) : "

REM Varsayılan değer belirlenmesi (eğer boş bırakılırsa)
if "%instance_number%"=="" (
    set instance_number=1
)

REM Oturum klasörünün var olup olmadığını kontrol et
if exist "C:\bon\robot%instance_number%" (
    echo robot%instance_number% oturumu gizleniyor...
    attrib +h +s "C:\bon\robot%instance_number%"
    echo %date% %time% : robot%instance_number% oturumu gizlendi >> "%LOGFILE%"
) else (
    echo robot%instance_number% oturumu mevcut değil.
    echo %date% %time% : robot%instance_number% oturumu mevcut değil >> "%LOGFILE%"
)

echo ================================================================================ 
echo                     %instance_number% NUMARALI OTURUM ŞİMDİ GİZLİ                     
echo ================================================================================ 
echo %date% %time% : İşlem başarıyla tamamlandı >> "%LOGFILE%"


REM Scriptin sonu
exit /b
