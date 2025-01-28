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
ECHO Visite visite visite 
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
::IF %hour%==21 ( SET MENU=2) ELSE  ( SET /P MENU="Choose opption (type 1, 2 ,3 ,4,5,6 ,7,8,9,10): ")
IF %hour%==21 ( SET MENU=2) ELSE  ( SET  MENU=4)

1>NUL CALL :CASE_%MENU% # jump to :CASE_1, :CASE_2, etc.
IF ERRORLEVEL 1 CALL :DEFAULT_CASE # If label doesn't exist

ECHO Done.
EXIT /B


:CASE_1
:: START https://support.microsoft.com/en-us/windows/windows-10-system-requirements-6d4e9a79-66bf-7950-467c-795cf0386715
    :: Section : Ibrahim personnell ajouter un les opportunute universite et autre 
    ECHO Ibrahim Personnell
    ECHO clic to continue .........

  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://runwayml.com/
 
    :: Section :Nour actu .
    pause
    GOTO CASE_2
  :: bot
:CASE_2
ECHO Nour actu
  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://runwayml.com/
 
    GOTO CASE_3
 :: travail
:CASE_3

    :: Section : kitokoh .
    pause
    ECHO Kitokoh
  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://runwayml.com/
   GOTO CASE_4
:: finance admin
:CASE_4
 :: Section 3: Farmoos
    pause
    ECHO Farmoos
  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://runwayml.com/
 GOTO CASE_5
:: ref stat
:CASE_5
 :: Section : okps door
    pause
    ECHO door

  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://runwayml.com/
 GOTO CASE_6
 :: conception
:CASE_6
  :: Section : Tamam -
    pause
    ECHO Tamamam

  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://runwayml.com/
 GOTO CASE_7
:CASE_7
:: Section : kit sphop
    pause
    ECHO Kit sphop 
  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://runwayml.com/
   GOTO CASE_8
:CASE_8
:: Section : Turk novatech
    pause

    ECHO Turknovatech visites
  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://runwayml.com/
   GOTO CASE_9
:CASE_9
:: Section : Nouveau Case
    pause

    ECHO Nouveau Case visites

    
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://runwayml.com/
 :CASE_10
:: Section : Africa Novatech
    pause

    ECHO Africa Novatech visites

   
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.craiyon.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://runwayml.com/
 GOTO END_CASE
:DEFAULT_CASE
  ECHO Unknown color "%MENU%"
  GOTO END_CASE
:END_CASE
  VER > NUL # reset ERRORLEVEL
  GOTO :EOF # return from CALL


    pause
   
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.craiyon.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://runwayml.com/
 
    pause


 start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://runwayml.com/
 
    pause

   
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://runwayml.com/
 
    pause

  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://runwayml.com/

    pause

  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://runwayml.com/
  
    pause

    
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://runwayml.com/
 
    pause

   
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://runwayml.com/
    pause
 

 start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://runwayml.com/
  
    pause

   
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://runwayml.com/

    pause


     
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://easy-peasy.ai/fr/templates/chatgpt-prompt-generator
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://prompthero.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.copy.ai/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://chatgpt.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.bing.com/chat

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://app.leonardo.ai/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://creator.nightcafe.studio/explore
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://generated.photos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.bing.com/images/create
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.craiyon.com/

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://stablediffusionweb.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.artbreeder.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://deepdreamgenerator.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.imagine.art/dashboard/videos

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://studio.invideo.io/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://lumalabs.ai/dream-machine/creations 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://pictory.ai/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://app.synthesia.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://animoto.com/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.veed.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.veed.io/tools/ai-video/ai-video-generator 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.deepbrain.io/ 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://lumen5.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://runwayml.com/
  
    pause
