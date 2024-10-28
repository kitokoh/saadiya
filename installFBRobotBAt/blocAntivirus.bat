::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC6qYBs9v2dQo3fIPsSTvUKzHhnctwYHEmtwiHTDwiI4b7M=
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kdxy4eg44pSNklCm3OMWTp0LtS0q15Ec/GER6k2rGhTkuc51tgsZj
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
:: Vérifier si le script est exécuté en tant qu'administrateur
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] - Ce script doit être exécuté en tant qu'administrateur.
    pause
    exit /b
)

:: Désactivation temporaire de la protection en temps réel de Windows Defender
echo [INFO] - Désactivation de la protection en temps réel de Windows Defender...
powershell -Command "Start-Process powershell -ArgumentList 'Set-MpPreference -DisableRealtimeMonitoring $true' -Verb RunAs"

:: Vérifier si la désactivation a réussi
if %errorLevel% neq 0 (
    echo [ERROR] - Impossible de désactiver Windows Defender. Vérifiez vos privilèges et réessayez.
    pause
    exit /b
)

:: Attendre 30 minutes (1800 secondes)
echo [INFO] - Attente de 30 minutes...
timeout /t 1800 /nobreak >nul

:: Réactiver la protection en temps réel après 30 minutes
echo [INFO] - Réactivation de la protection en temps réel de Windows Defender...
powershell -Command "Start-Process powershell -ArgumentList 'Set-MpPreference -DisableRealtimeMonitoring $false' -Verb RunAs"

echo [INFO] - Windows Defender est à nouveau activé.
pause
exit
