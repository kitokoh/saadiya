@echo off
setlocal enabledelayedexpansion

:: Chemin vers le fichier JSON
set "jsonPath=C:\bon\robot1\data.json"

:: Lire le fichier JSON avec PowerShell et extraire les liens
for /f "delims=" %%i in ('powershell -Command "Get-Content -Raw -Path '%jsonPath%' | ConvertFrom-Json | Select-Object -ExpandProperty groups"') do (
    set "links=%%i"
)

:: Convertir les liens en tableau
set "linksArray=!links: =!"

:: Ouvrir les liens par groupes de 10
set /a groupSize=10
set /a totalLinks=0
for %%l in (!linksArray!) do (
    set /a totalLinks+=1
)

set /a numGroups=(totalLinks + groupSize - 1) / groupSize

for /L %%g in (0,1,%numGroups%) do (
    set /a startIdx=%%g*groupSize
    set /a endIdx=startIdx+groupSize-1
    echo Opening group %%g...
    for /L %%i in (!startIdx!,1,!endIdx!) do (
        if !%%i! lss !totalLinks! (
            for /F "tokens=1,* delims= " %%a in ("!linksArray!") do (
                if !%%i! equ 0 (
                    start "" "%%b"
                    set /a startIdx+=1
                ) else (
                    set /a startIdx-=1
                    start "" "%%b"
                )
            )
        )
    )
    :: Mettre en pause le script
    echo Press any key to continue...
    pause >nul
)

echo All links have been opened.
pause
