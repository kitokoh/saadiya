@echo off
setlocal enabledelayedexpansion

echo ================================
echo PUSHING TO GITHUB, GITLAB, BITBUCKET
echo ================================

:: Définir les variables
set EXE_FILE=Nova360.exe
set ZIP_FILE=release.zip
set TAG_NAME=v%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%

:: Ajouter les fichiers volumineux à Git LFS
git lfs track "*.exe"
git add .gitattributes

:: Ajouter les modifications
git add -A
git commit -m "Update code and release %TAG_NAME%"

:: Pousser les modifications sur les trois remotes
git push origin master
git push gitlab master
git push bitbucket master

:: Créer une archive ZIP pour le fichier EXE
echo Compressing %EXE_FILE% to %ZIP_FILE%
powershell Compress-Archive -Path %EXE_FILE% -DestinationPath %ZIP_FILE%

:: Créer un tag et pousser
git tag %TAG_NAME%
git push origin %TAG_NAME%
git push gitlab %TAG_NAME%
git push bitbucket %TAG_NAME%

:: Publier la release sur GitHub
echo Publishing release on GitHub...
curl -X POST -H "Authorization: token GITHUB_TOKEN" ^
    -H "Content-Type: application/json" ^
    -d "{\"tag_name\": \"%TAG_NAME%\", \"name\": \"%TAG_NAME%\", \"body\": \"Release %TAG_NAME%\"}" ^
    https://api.github.com/repos/username/repo/releases

curl -X POST -H "Authorization: token GITHUB_TOKEN" ^
    -H "Content-Type: application/octet-stream" ^
    --upload-file %ZIP_FILE% ^
    https://uploads.github.com/repos/username/repo/releases/assets?name=%ZIP_FILE%

:: Publier la release sur GitLab
echo Publishing release on GitLab...
curl --header "PRIVATE-TOKEN: GITLAB_TOKEN" --upload-file %ZIP_FILE% ^
    "https://gitlab.com/api/v4/projects/username%%2Frepo/releases/%TAG_NAME%/assets/links"

:: Publier la release sur Bitbucket
echo Publishing release on Bitbucket...
curl -X POST -u username:BITBUCKET_APP_PASSWORD ^
    --form files=@%ZIP_FILE% ^
    https://api.bitbucket.org/2.0/repositories/username/repo/downloads

echo ================================
echo PUSH COMPLETE
echo ================================

:: Nettoyage
del %ZIP_FILE%
pause
