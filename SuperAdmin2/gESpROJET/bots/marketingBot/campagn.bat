@ECHO OFF 

:: This batch file details Windows 10, hardware, and networking configuration.

TITLE My System Info

ECHO Please wait... Checking system information.

:: Section 1: Windows 10 information

ECHO ==========================

ECHO WINDOWS INFO

ECHO ============================

systeminfo | findstr /c:"OS Name"

systeminfo | findstr /c:"OS Version"

systeminfo | findstr /c:"System Type"

:: Section 2: Hardware information.

ECHO ============================

ECHO Je vais ouvir les pages 

ECHO ============================

ECHO ============================

ECHO HARDWARE INFO

ECHO ============================

systeminfo | findstr /c:"Total Physical Memory"

wmic cpu get name

wmic diskdrive get name,model,size

wmic path win32_videocontroller get name

wmic path win32_VideoController get CurrentHorizontalResolution,CurrentVerticalResolution

:: Section 3: Networking information.

ECHO ============================

ECHO NETWORK INFO

ECHO ============================

ipconfig | findstr IPv4ipconfig | findstr IPv6
:: taskkill /F /IM chrome.exe /T > nul


@ECHO OFF
ECHO ==========================

ECHO 1. Share face grp    2. bot
ECHO 3. Travail    4. Finance admin
ECHO 5. Contenue    6. Conception
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
IF %hour%==21 ( SET MENU=2) ELSE  ( SET /P MENU="Choose opption (type 1, 2 ,3 ,4,5,6): ")

1>NUL CALL :CASE_%MENU% # jump to :CASE_1, :CASE_2, etc.
IF ERRORLEVEL 1 CALL :DEFAULT_CASE # If label doesn't exist

ECHO Done.
EXIT /B
    :: visite
    
:CASE_1
 ::start cmd.exe /C FarmoossharefbkGp.bat    
  start cmd.exe /C "C:\Users\ibrahim\Desktop\Nouractu      Ibrahim3.bat"    
  timeout 30

 start cmd.exe /C "C:\Users\ibrahim\Desktop\Ibrahim 1 Ant  (Tnt).bat"  
   timeout 30
   
 start cmd.exe /C "C:\Users\ibrahim\Desktop\tamam  ibrahim2.bat"    
   timeout 30
 
 start cmd.exe /C "C:\Users\ibrahim\Desktop\doorika1 account.bat"
   timeout 30

 start cmd.exe /C "C:\Users\ibrahim\Desktop\kitokoh   Fatiha.bat"
   timeout 30

 start cmd.exe /C "C:\Users\ibrahim\Desktop\Farmoos  fatma.bat"
   timeout 30

 start cmd.exe /C "C:\Users\ibrahim\Desktop\tamam Ahmat (kitsphop).bat"
   timeout 30

 start cmd.exe /C "C:\Users\ibrahim\Desktop\kitokoh sissoko (profilX).bat"  
   timeout 30
   
 ::start cmd.exe /C ANTECHshareBot.bat     
 ::start cmd.exe /C kitokohsharebot.bat     
 ::start cmd.exe /C kitsphopShareBot.bat     
 ::start cmd.exe /C TntechShareBot.bat     
  ::start cmd.exe /C profilXSharebot.bat   
  ::start cmd.exe /C sharefbbot.bat   
::start cmd.exe /C ..\botfreqtrade.bat   

  start cmd.exe /C jobot.bat   


  GOTO END_CASE
  :: bot
:CASE_2
    start cmd.exe /C job.cmd     

    GOTO END_CASE,
 :: travail
:CASE_3
    start cmd.exe /C sharefbbot.bat     
  GOTO END_CASE
:: finance admin
:CASE_4
    start cmd.exe /C doorShareBot.bat     
  GOTO END_CASE
:: ref stat
:CASE_5
  COLOR 0F
  GOTO END_CASE
 :: conception
:CASE_6
  COLOR 0F
  GOTO END_CASE
:DEFAULT_CASE
  ECHO Unknown color "%MENU%"
  GOTO END_CASE
:END_CASE
  VER > NUL # reset ERRORLEVEL
  GOTO :EOF # return from CALL



SET /P COLOR="Choose a background color (type red, blue or black): "

2>NUL CALL :CASE_%COLOR% # jump to :CASE_red, :CASE_blue, etc.
IF ERRORLEVEL 1 CALL :DEFAULT_CASE # If label doesn't exist

ECHO Done.
EXIT /B



:CASE_red
  COLOR CF
  pause
  GOTO END_CASE
:CASE_blue
    GOTO END_CASE
:CASE_black
  COLOR 0F
  GOTO END_CASE
:DEFAULT_CASE
  ECHO Unknown color "%COLOR%"
  GOTO END_CASE
:END_CASE
  VER > NUL # reset ERRORLEVEL
  GOTO :EOF # return from CALL

:: START https://support.microsoft.com/en-us/windows/windows-10-system-requirements-6d4e9a79-66bf-7950-467c-795cf0386715
:: Section : Ibrahim personnell



setlocal enableDelayedExpansion 

set loopcount=5
:loop
echo Hello Ibrahim!
set /a loopcount=loopcount-1
if %loopcount%==0 goto exitloop
goto loop
:exitloop

PAUSE