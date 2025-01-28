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
ECHO Espace de travail pour freelancer 
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
  
    :: START https://support.microsoft.com/en-us/windows/windows-10-system-requirements-6d4e9a79-66bf-7950-467c-795cf0386715
    :: Section : Ibrahim personnell
    ECHO Ibrahim Personnell
    ECHO clic to continue .........        
        
     


        :: Section 1
         ECHO Nour actu
        pause
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://pro.fiverr.com/business/team_members?source=admin
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.freelancer.com/post-project
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.toptal.com/hire
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.upwork.com/nx/search/talent
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.guru.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://istanbul.craigslist.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://1010designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.workana.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.simply.com/en/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.textbroker.fr/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://upstack.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://comeup.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.etsy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.artstation.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.designcrowd.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://soundcloud.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.cdbaby.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.tunecore.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.constant-content.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.writeraccess.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.upwork.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.youtube.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://1010designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.printful.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://printify.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://sellfy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://gumroad.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://unbabel.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://gengo.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.udemy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.coursera.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.edx.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.skillshare.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://teachable.com/


       
  pause
  GOTO CASE_2
:CASE_2
 :: Section 2
         ECHO Nour actu
        pause
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://pro.fiverr.com/business/team_members?source=admin
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.freelancer.com/post-projectstart 
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.upwork.com/nx/search/talent
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.guru.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://istanbul.craigslist.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://99designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.workana.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.simply.com/en/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.textbroker.fr/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://upstack.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://comeup.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.etsy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.artstation.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.designcrowd.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://soundcloud.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.cdbaby.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.tunecore.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.constant-content.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.writeraccess.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.upwork.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.youtube.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://99designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.printful.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://printify.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://sellfy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://gumroad.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://unbabel.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://gengo.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.udemy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.coursera.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.edx.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.skillshare.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://teachable.com/

        
    GOTO CASE_3
:CASE_3
:: Section 3
         ECHO Nour actu
        pause
        start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://pro.fiverr.com/business/team_members?source=admin
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.freelancer.com/post-project
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.toptal.com/hire
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.upwork.com/nx/search/talent
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.guru.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://istanbul.craigslist.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://99designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.workana.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.simply.com/en/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.textbroker.fr/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://upstack.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://comeup.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.etsy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.artstation.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.designcrowd.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://soundcloud.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.cdbaby.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.tunecore.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.constant-content.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.writeraccess.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.upwork.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.youtube.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://99designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.printful.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://printify.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://sellfy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://gumroad.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://unbabel.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://gengo.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.udemy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.coursera.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.edx.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.skillshare.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://teachable.com/
      
  GOTO CASE_4
:CASE_4
 
        :: Section 10
         ECHO Nour actu
        pause
                start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://pro.fiverr.com/business/team_members?source=admin
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.freelancer.com/post-project
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.toptal.com/hire
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.upwork.com/nx/search/talent
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.guru.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://istanbul.craigslist.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://1010designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.workana.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.simply.com/en/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.textbroker.fr/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://upstack.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://comeup.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.etsy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.artstation.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.designcrowd.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://soundcloud.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.cdbaby.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.tunecore.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.constant-content.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.writeraccess.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.upwork.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.youtube.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://1010designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.printful.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://printify.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://sellfy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://gumroad.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://unbabel.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://gengo.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.udemy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.coursera.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.edx.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.skillshare.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://teachable.com/

  pause
  GOTO CASE_5
:CASE_5
 :: Section 5
         ECHO Nour actu
        pause
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://pro.fiverr.com/business/team_members?source=admin
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.freelancer.com/post-project
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.toptal.com/hire
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.upwork.com/nx/search/talent
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.guru.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://istanbul.craigslist.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://99designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.workana.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.simply.com/en/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.textbroker.fr/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://upstack.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://comeup.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.etsy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.artstation.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.designcrowd.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://soundcloud.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.cdbaby.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.tunecore.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.constant-content.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.writeraccess.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.upwork.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.youtube.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://99designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.printful.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://printify.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://sellfy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://gumroad.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://unbabel.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://gengo.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.udemy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.coursera.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.edx.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.skillshare.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://teachable.com/


     
    GOTO CASE_6
:CASE_6

        :: Section 
         ECHO Nour actu
        pause
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://pro.fiverr.com/business/team_members?source=admin
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.freelancer.com/post-project
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.toptal.com/hire
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.upwork.com/nx/search/talent
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.guru.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://istanbul.craigslist.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://99designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.workana.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.simply.com/en/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.textbroker.fr/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://upstack.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://comeup.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.etsy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.artstation.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.designcrowd.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://soundcloud.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.cdbaby.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.tunecore.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.constant-content.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.writeraccess.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.upwork.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.youtube.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://99designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.printful.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://printify.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://sellfy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://gumroad.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://unbabel.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://gengo.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.udemy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.coursera.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.edx.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.skillshare.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://teachable.com/

 GOTO CASE_7
:CASE_7

        :: Section 7
         ECHO Nour actu
        pause
                start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://pro.fiverr.com/business/team_members?source=admin
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.freelancer.com/post-project
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.toptal.com/hire
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.upwork.com/nx/search/talent
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.guru.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://istanbul.craigslist.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://99designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.workana.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.simply.com/en/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.textbroker.fr/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://upstack.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://comeup.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.etsy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.artstation.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.designcrowd.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://soundcloud.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.cdbaby.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.tunecore.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.constant-content.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.writeraccess.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.upwork.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.youtube.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://99designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.printful.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://printify.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://sellfy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://gumroad.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://unbabel.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://gengo.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.udemy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.coursera.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.edx.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.skillshare.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://teachable.com/
  pause
  GOTO CASE_8
:CASE_8
        :: Section 8
         ECHO Nour actu
        pause
                start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://pro.fiverr.com/business/team_members?source=admin
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.freelancer.com/post-project
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.toptal.com/hire
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.upwork.com/nx/search/talent
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.guru.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://istanbul.craigslist.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://99designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.workana.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.simply.com/en/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.textbroker.fr/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://upstack.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://comeup.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.etsy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.artstation.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.designcrowd.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://soundcloud.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.cdbaby.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.tunecore.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.constant-content.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.writeraccess.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.upwork.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.youtube.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://99designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.printful.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://printify.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://sellfy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://gumroad.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://unbabel.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://gengo.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.udemy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.coursera.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.edx.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.skillshare.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://teachable.com/

    GOTO CASE_9
:CASE_9

        :: Section 9
         ECHO Nour actu
        pause
                start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://pro.fiverr.com/business/team_members?source=admin
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.freelancer.com/post-project
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.toptal.com/hire
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.upwork.com/nx/search/talent
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.guru.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://istanbul.craigslist.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://99designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.workana.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.simply.com/en/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.textbroker.fr/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://upstack.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://comeup.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.etsy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.artstation.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.designcrowd.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://soundcloud.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.cdbaby.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.tunecore.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.constant-content.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.writeraccess.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.upwork.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.youtube.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://99designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.printful.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://printify.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://sellfy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://gumroad.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://unbabel.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://gengo.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.udemy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.coursera.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.edx.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.skillshare.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://teachable.com/
   GOTO CASE_10
:CASE_10
   :: Section Default
             
    ECHO Nour actu
        pause
                start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://pro.fiverr.com/business/team_members?source=admin
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.freelancer.com/post-project
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.toptal.com/hire
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.upwork.com/nx/search/talent
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.guru.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.peopleperhour.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://istanbul.craigslist.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://1010designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.workana.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.simply.com/en/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.textbroker.fr/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://upstack.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://comeup.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.etsy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.artstation.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.designcrowd.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://soundcloud.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.cdbaby.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.tunecore.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.constant-content.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.writeraccess.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.upwork.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.youtube.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://1010designs.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.printful.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://printify.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://sellfy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://gumroad.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://unbabel.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://gengo.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.udemy.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.coursera.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.edx.org/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.skillshare.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://teachable.com/
  GOTO END_CASE
:DEFAULT_CASE
  ECHO Unknown color "%COLOR%"
  GOTO END_CASE
:END_CASE
  VER > NUL # reset ERRORLEVEL
  GOTO :EOF # return from CALL


   