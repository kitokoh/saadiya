::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC6IexwgpmMPn2eKOYq4thzoTUbE1lk1D3FtykzWiiI4ZZ461+4GwDO/+0iynqkC1Hn7R+QcEGLlj6VrN6k=
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kfxStZww8rENHpXeEMMLSthfkKg==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
:: Définir la taille de la fenêtre CMD
mode con: cols=70 lines=20
title AI FB Robot Pro - Kurulum Basarili

:: Calculer la position pour centrer la fenêtre CMD (pour une résolution de 1920x1080)
:: Largeur de la fenêtre = 560 pixels, Hauteur de la fenêtre = 300 pixels
:: Position horizontale (X) = (1920 - 560) / 2 = 680
:: Position verticale (Y) = (1080 - 300) / 2 = 390
powershell -command "&{$cmd = (New-Object -ComObject Shell.Application).Windows() | ? { $_.LocationName -eq 'AI FB Robot Pro - Kurulum Basarili'}; if ($cmd) { $cmd.Left = 680; $cmd.Top = 390;}}"

:: Couleur de fond bleu foncé et texte blanc brillant
color 17
cls

:: Effet de logo avec des étoiles en ASCII
echo.
echo   **********************************************
echo   *                                            *
echo   *    AI FB Robot Pro - Basariyla Kuruldu     *
echo   *                                            *
echo   **********************************************
echo.

:: Affichage d'une barre de chargement simulée pour rendre l'attente plus dynamique
echo.
set /p =Lisans anahtariniz hazirlaniyor: <nul
for /l %%A in (1,1,30) do (
    set /p =. <nul
    ping -n 1 -w 100 127.0.0.1 >nul
)
echo.

:: Animation supplémentaire pour simuler l'envoi de l'e-mail
echo.
set /p =E-posta sunucusu ile baglanti kuruluyor: <nul
for /l %%A in (1,1,20) do (
    set /p =* <nul
    ping -n 1 -w 100 127.0.0.1 >nul
)
echo.
ping -n 1 -w 1000 127.0.0.1 >nul

:: Félicitations finales
cls
echo.
echo   **********************************************
echo   *    Tebrikler! AI FB Robot Pro kurulumunuz   *
echo   *             basariyla tamamlandi!           *
echo   **********************************************
echo.
echo.
echo  Lisans anahtariniz yakinda kayitli e-posta adresinize gonderilecektir.
echo  Lutfen sabirli olunuz ve e-postanizi kontrol ediniz.
echo.
ping -n 5 127.0.0.1 >nul

:: Message de fin avec pause avant la fermeture
echo.
echo   Tesekkürler ve AI FB Robot Pro'yu kullanmaya hazirsiniz!

timeout /t 3 /nobreak > nul

rem pause >nul
exit
