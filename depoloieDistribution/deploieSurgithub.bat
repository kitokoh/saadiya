

@echo off
setlocal

rem Variables (à ajuster)
set "REPO_OWNER=nova360-ai"
set "REPO_NAME=nova360"
set "TOKEN=VotreToken"
set "FILE_PATH=D:\Installations\Nova360"
set "TAG_NAME=v1.0.0"
set "RELEASE_NAME=FbRobotModules"
set "RELEASE_BODY=Cette release contient la dernière version de l'exécutable."

rem Obtenir l'ID de la release (ou en créer une si elle n'existe pas)
set "RELEASE_ID="
for /f "tokens=*" %%A in ('curl -s -H "Authorization: token %TOKEN%" ^
    https://api.github.com/repos/%REPO_OWNER%/%REPO_NAME%/releases/tags/%TAG_NAME% ^
    ^| findstr /C:"\"id\":"') do (
    for /f "tokens=2 delims=: " %%B in ("%%A") do set "RELEASE_ID=%%B"
)

if not defined RELEASE_ID (
    echo Release non trouvée, création d'une nouvelle release...
    for /f "tokens=*" %%A in ('curl -s -X POST -H "Authorization: token %TOKEN%" ^
        -H "Content-Type: application/json" ^
        -d "{\"tag_name\":\"%TAG_NAME%\",\"name\":\"%RELEASE_NAME%\",\"body\":\"%RELEASE_BODY%\"}" ^
        https://api.github.com/repos/%REPO_OWNER%/%REPO_NAME%/releases ^
        ^| findstr /C:"\"id\":"') do (
        for /f "tokens=2 delims=: " %%B in ("%%A") do set "RELEASE_ID=%%B"
    )
)

rem Vérifier si la release a bien été créée
if not defined RELEASE_ID (
    echo Erreur : Impossible de créer ou d'obtenir l'ID de la release.
    exit /b 1
)

echo Release ID : %RELEASE_ID%

rem Téléversement du fichier .exe dans la release
curl -X POST -H "Authorization: token %TOKEN%" ^
     -H "Content-Type: application/octet-stream" ^
     --data-binary @"%FILE_PATH%" ^
     https://uploads.github.com/repos/%REPO_OWNER%/%REPO_NAME%/releases/%RELEASE_ID%/assets?name=%~nxFILE_PATH%

if %ERRORLEVEL% NEQ 0 (
    echo Erreur lors du téléversement du fichier.
    exit /b 1
)

echo Téléversement réussi !
exit /b 0
