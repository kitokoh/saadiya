

   @ECHO OFF

:: This CMD script provides you with your operating system, hardware and network information.

TITLE My System Info

ECHO Please wait... Gathering system information.

ECHO =========================

ECHO OPERATING SYSTEM

systeminfo | findstr /c:"OS Name"

systeminfo | findstr /c:"OS Version"

ECHO =========================

ECHO BIOS

systeminfo | findstr /c:"System Type"

ECHO =========================

ECHO MEMORY

systeminfo | findstr /c:"Total Physical Memory"

ECHO =========================

ECHO CPU

wmic cpu get name

ECHO =========================

ECHO NETWORK ADDRESS

ipconfig | findstr IPv4

ipconfig | findstr IPv6    
@ECHO OFF
ECHO ==========================
ECHO Lancer sream  
ECHO 1. Ibrahim    2. Nouractu
ECHO 3. Kitokoh    4. farmoos
ECHO 5. door    6. tamam
ECHO 7. Kit       8. tnt
ECHO 9. kps    10. ant

@echo Started: %date% %time%
ECHO ============================
    :: SET /P MENU = 1
    :: tester si nous sommes a 9 heurs et autres heures
@echo off
set hour=%time:~0,2%

IF %hour%==16 ( SET MENU=1) 
IF %hour%==10 ( SET MENU=2) 
IF %hour%==11 ( SET MENU=3) 
IF %hour%==15 ( SET MENU=4) 
IF %hour%==15 ( SET MENU=5) 
IF %hour%==14 ( SET MENU=6) 
IF %hour%==21 ( SET MENU=2) ELSE  ( SET /P MENU="Choose opption (type 1, 2 ,3 ,4,5,6 ,7,8,9,10): ")

1>NUL CALL :CASE_%MENU% # jump to :CASE_1, :CASE_2, etc.
IF ERRORLEVEL 1 CALL :DEFAULT_CASE # If label doesn't exist

ECHO Done.
EXIT /B

:CASE_1
:: source de contenu stream 


:: Pour publier stream 

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.facebook.com/live/producer 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://dashboard.twitch.tv/u/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://kick.com/dashboard/settings/stream




@echo off
cd /d "C:\Program Files\obs-studio\bin\64bit"
start obs64.exe
pause
exit

:: Pour le partages et developpement


  pause
  GOTO CASE_2
:CASE_2
:: source de contenu stream 


:: Pour publier stream 

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.facebook.com/live/producer 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://dashboard.twitch.tv/u/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://kick.com/dashboard/settings/stream




@echo off
cd /d "C:\Program Files\obs-studio\bin\64bit"
start obs64.exe
pause
exit

:: Pour le partages et developpement


    GOTO CASE_3
:CASE_3
:: source de contenu stream 


:: Pour publier stream 

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.facebook.com/live/producer 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://dashboard.twitch.tv/u/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://kick.com/dashboard/settings/stream




@echo off
cd /d "C:\Program Files\obs-studio\bin\64bit"
start obs64.exe
pause
exit

:: Pour le partages et developpement

  GOTO CASE_4
:CASE_4
:: source de contenu stream 


:: Pour publier stream 

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.facebook.com/live/producer 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://dashboard.twitch.tv/u/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://kick.com/dashboard/settings/stream




@echo off
cd /d "C:\Program Files\obs-studio\bin\64bit"
start obs64.exe
pause
exit

:: Pour le partages et developpement

  pause
  GOTO CASE_5
:CASE_5
:: source de contenu stream 


:: Pour publier stream 

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.facebook.com/live/producer 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://dashboard.twitch.tv/u/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://kick.com/dashboard/settings/stream




@echo off
cd /d "C:\Program Files\obs-studio\bin\64bit"
start obs64.exe
pause
exit

:: Pour le partages et developpement


    GOTO CASE_6
:CASE_6
:: source de contenu stream 


:: Pour publier stream 

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.facebook.com/live/producer 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://dashboard.twitch.tv/u/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://kick.com/dashboard/settings/stream




@echo off
cd /d "C:\Program Files\obs-studio\bin\64bit"
start obs64.exe
pause
exit

:: Pour le partages et developpement

  GOTO CASE_7
:CASE_7
:: source de contenu stream 


:: Pour publier stream 

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.facebook.com/live/producer 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://dashboard.twitch.tv/u/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://kick.com/dashboard/settings/stream




@echo off
cd /d "C:\Program Files\obs-studio\bin\64bit"
start obs64.exe
pause
exit

:: Pour le partages et developpement

  pause
  GOTO CASE_8
:CASE_8
:: source de contenu stream 


:: Pour publier stream 

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.facebook.com/live/producer 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://dashboard.twitch.tv/u/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://kick.com/dashboard/settings/stream




@echo off
cd /d "C:\Program Files\obs-studio\bin\64bit"
start obs64.exe
pause
exit

:: Pour le partages et developpement


    GOTO CASE_9
:CASE_9
:: source de contenu stream 


:: Pour publier stream 

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.facebook.com/live/producer 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://dashboard.twitch.tv/u/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://kick.com/dashboard/settings/stream




@echo off
cd /d "C:\Program Files\obs-studio\bin\64bit"
start obs64.exe
pause
exit

:: Pour le partages et developpement

  GOTO CASE_10
:CASE_10
:: source de contenu stream 


:: Pour publier stream 

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.facebook.com/live/producer 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://dashboard.twitch.tv/u/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://kick.com/dashboard/settings/stream




@echo off
cd /d "C:\Program Files\obs-studio\bin\64bit"
start obs64.exe
pause
exit

:: Pour le partages et developpement

  GOTO END_CASE
:DEFAULT_CASE
  ECHO Unknown color "%COLOR%"
  GOTO END_CASE
:END_CASE
  VER > NUL # reset ERRORLEVEL
  GOTO :EOF # return from CALL