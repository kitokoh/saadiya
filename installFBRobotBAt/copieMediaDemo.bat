::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC6tbwwxq2FNvSmMNMiS/h/vTQXesB19LGx6g2zHn2UyY9wI
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kdxy4eg44pSNklCm3OMWTp0LtS0q15UQgEmBZgmfZjQ8+bdwmn9sGsw==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
:: Configuration des couleurs : fond bleu (1) et texte blanc (F)
color 1F

set "source_folder=%cd%"  REM Définit le dossier source comme le répertoire courant
set "destination_folder=%USERPROFILE%\Downloads\AI-FB-Robot\media\media1"

REM Vérifie si le dossier de destination existe, sinon le crée
if not exist "%destination_folder%" (
    mkdir "%destination_folder%"
)

REM Boucle pour copier les fichiers
for %%i in (1.mp4 2.png 3.png 4.png 5.png 6.png 7.png) do (
    if exist "%source_folder%\%%i" (
        copy "%source_folder%\%%i" "%destination_folder%"
        echo %%i copié vers %destination_folder%
    ) else (
        echo %%i n'existe pas dans %source_folder%
    )
)

echo Opération terminée.

