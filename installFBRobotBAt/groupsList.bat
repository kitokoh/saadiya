::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAnk
::fBw5plQjdG8=
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9keQCkex8nhWdRoiqAL8L8
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
:: Configuration des couleurs de fond et de texte (Texte blanc sur fond bleu)
color 1F

:: Désactiver l'affichage des commandes
echo.

:: Création d'une bordure visuelle
echo ====================================================================
echo =                        Scraping Aracı                           =
echo ====================================================================

:: Ajout d'un message d'accueil stylisé
echo.
echo Scraping Aracına Hoş Geldiniz!
echo Bu program çevrimiçi veri toplamanıza yardımcı olacak.
echo.

:: Demande du mot-clé à l'utilisateur avec une instruction claire
set /p keyword=>> Lütfen kazımak istediğiniz anahtar kelimeyi girin : 
echo.

:: Confirmation de l'entrée utilisateur
echo Seçtiğiniz anahtar kelime : "%keyword%"
echo.

:: Exécution du script Python avec le mot-clé saisi
echo Kazıma başlatılıyor...
python scraper_script.py %keyword%

:: Vérification de la sortie et pause pour garder la fenêtre ouverte
echo.
echo ====================================================================
echo =                        Kazıma Tamamlandı!                       =
echo ====================================================================
pause
