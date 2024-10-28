::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC6sYQAzpWsPtWyXOMqZ/gbiRUbEtRpiSyhDjm3UgzwoLtprlaM=
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
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kdxy4eg44pSNklCm3OMWTp0LtS0q19U4zDndxpGvCgyY+LtZwn6M=
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion

:: Chemin du dossier où se trouvent les dossiers robotX
set robotFolder=C:\bon

:: Vérifier si Google Chrome est installé
if not exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo Google Chrome n'est pas installé à l'emplacement prévu.
    exit /b
)

:: Calculer le nombre de dossiers robotX, y compris les dossiers cachés
set count=0
for /f "delims=" %%d in ('dir /ad /b /a:h "%robotFolder%\robot*" 2^>nul') do (
    set /a count+=1
)

:: Vérification si aucun dossier robot n'a été trouvé
if %count%==0 (
    echo Aucun dossier robot n'a été trouvé dans le dossier %robotFolder%.
    exit /b
)

echo %count% dossiers robot trouvés dans le dossier %robotFolder%.

:: Boucle pour ouvrir plusieurs instances de Google Chrome avec des profils différents
for /l %%i in (1,1,%count%) do (
    echo Ouverture de Google Chrome avec le profil %%i...

    :: Ouvrir Google Chrome avec le profil %%i et rediriger vers la page de connexion Facebook
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" --user-data-dir="C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Profil %%i" "https://www.facebook.com/login"
    
    :: Vérifier s'il y a une erreur lors de l'ouverture de Google Chrome
    if errorlevel 1 (
        echo Une erreur est survenue lors de l'ouverture de Google Chrome avec le profil %%i.
        exit /b
    ) else (
        echo Google Chrome ouvert avec succès avec le profil %%i.
    )

    timeout /t 2 >nul
)

echo Toutes les instances de Google Chrome ont été ouvertes avec succès.

exit /b

