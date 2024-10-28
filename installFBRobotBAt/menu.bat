::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC6PawM1qnxN+02BevSIsh31B2WM6F5+EmZ75w==
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kcxele0ExsWsi
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
title FB Robot Pro Kurulum Menüsü
color 0A
cls

:menu
echo ==================================================================
echo                      FB Robot Pro Kurulum Menüsü
echo ==================================================================
echo.
echo [1] FB Robot Pro'yu Yükle
echo [2] Lisans İste
echo [3] FB Robot Pro'yu Kaldır
echo [4] Çıkış
echo.
echo ==================================================================
echo Lütfen bir seçenek seçiniz (1-4):
set /p secim=

if "%secim%"=="1" goto install
if "%secim%"=="2" goto license
if "%secim%"=="3" goto uninstall
if "%secim%"=="4" goto exit
echo Geçersiz bir seçim yaptınız. Lütfen tekrar deneyin.
pause
cls
goto menu

:install
cls
echo ==================================================================
echo                        FB Robot Pro'yu Yükleme
echo ==================================================================
echo FB Robot Pro yükleme başlatılıyor...
rem Burada kurulum komutlarınızı ekleyin
echo Kurulum tamamlandı!
pause
cls
goto menu

:license
cls
echo ==================================================================
echo                        Lisans İste
echo ==================================================================
echo Lisans almak için lütfen şu adrese başvurun: support@fbrobotpro.com
rem Buraya lisans isteme işlemleri eklenebilir
echo Lisans talebi gönderildi!
pause
cls
goto menu

:uninstall
cls
echo ==================================================================
echo                    FB Robot Pro'yu Kaldırma
echo ==================================================================
echo FB Robot Pro kaldırılıyor...
rem Buraya kaldırma komutlarınızı ekleyin
echo FB Robot Pro başarıyla kaldırıldı!
pause
cls
goto menu

:exit
cls
echo Çıkış yapılıyor...
pause
exit
