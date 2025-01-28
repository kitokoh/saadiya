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
ECHO Demande Prix 
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

    
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=1765244048
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://pro.fiverr.com/business/team_members?source=admin
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.freelancer.com/post-project
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.toptal.com/hire
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.upwork.com/nx/search/talent

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.europages.com.tr/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.amazon.com.tr/s?me=A368G57G993ZXD&marketplaceID=A33AVAJ2PDY3EV
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://mfgmatch.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.go4worldbusiness.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://sourcing.hktdc.com/en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://importer.ec21.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" Manufacturer.com 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" GlobalTrade.net
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.tradekey.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.globalspec.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.indiamart.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.made-in-china.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.tradeindia.com/ 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.mfg.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.thomasnet.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" http://www.manufacturerusa.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://b2brazil.com.br/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://phantombuster.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.goafricaonline.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://docs.google.com/spreadsheets/d/1TajXf58mLNsBixl6tCXRhSPixIzLsSf4HTiu6qxrbcg/edit#gid=700780096
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://ases.kitokoh.com/#/
   
  GOTO CASE_2
:CASE_2
 :: Section :Nour actu .
    pause
    ECHO Nour actu

        start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=1765244048
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://pro.fiverr.com/business/team_members?source=admin
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.freelancer.com/post-project
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.toptal.com/hire
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.upwork.com/nx/search/talent
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://phantombuster.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.europages.com.tr/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.amazon.com.tr/s?me=A368G57G993ZXD&marketplaceID=A33AVAJ2PDY3EV
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://mfgmatch.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.go4worldbusiness.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://sourcing.hktdc.com/en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://importer.ec21.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" Manufacturer.com 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" GlobalTrade.net
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.tradekey.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.globalspec.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.indiamart.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.made-in-china.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.tradeindia.com/ 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.mfg.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.thomasnet.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" http://www.manufacturerusa.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://b2brazil.com.br/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.goafricaonline.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://docs.google.com/spreadsheets/d/1TajXf58mLNsBixl6tCXRhSPixIzLsSf4HTiu6qxrbcg/edit#gid=700780096
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://ases.kitokoh.com/#/
    

   
    GOTO CASE_3
:CASE_3
 :: Section : kitokoh .
    pause
    ECHO Kitokoh

       start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=1765244048
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://pro.fiverr.com/business/team_members?source=admin
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.freelancer.com/post-project
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.toptal.com/hire
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.upwork.com/nx/search/talent
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://phantombuster.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.europages.com.tr/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.amazon.com.tr/s?me=A368G57G993ZXD&marketplaceID=A33AVAJ2PDY3EV
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://mfgmatch.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.go4worldbusiness.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://sourcing.hktdc.com/en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://importer.ec21.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" Manufacturer.com 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" GlobalTrade.net
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.tradekey.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.globalspec.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.indiamart.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.made-in-china.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.tradeindia.com/ 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.mfg.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.thomasnet.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" http://www.manufacturerusa.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://b2brazil.com.br/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.goafricaonline.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://docs.google.com/spreadsheets/d/1TajXf58mLNsBixl6tCXRhSPixIzLsSf4HTiu6qxrbcg/edit#gid=700780096
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://ases.kitokoh.com/#/
     
  COLOR 0F
  GOTO CASE_4
:CASE_4
 :: Section 3: Farmoos
    pause
    ECHO Farmoos
        start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=1765244048
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://pro.fiverr.com/business/team_members?source=admin
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.freelancer.com/post-project
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.toptal.com/hire
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.upwork.com/nx/search/talent
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://phantombuster.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.europages.com.tr/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.amazon.com.tr/s?me=A368G57G993ZXD&marketplaceID=A33AVAJ2PDY3EV
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://mfgmatch.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.go4worldbusiness.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://sourcing.hktdc.com/en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://importer.ec21.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" Manufacturer.com 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" GlobalTrade.net
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.tradekey.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.globalspec.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.indiamart.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.made-in-china.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.tradeindia.com/ 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.mfg.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.thomasnet.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" http://www.manufacturerusa.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://b2brazil.com.br/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.goafricaonline.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://docs.google.com/spreadsheets/d/1TajXf58mLNsBixl6tCXRhSPixIzLsSf4HTiu6qxrbcg/edit#gid=700780096
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://ases.kitokoh.com/#/
    
   
  GOTO CASE_5
:CASE_5
 :: Section : okps door
    pause
    ECHO door

        start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" e\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://pro.fiverr.com/business/team_members?source=admin
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.freelancer.com/post-project
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Pr--profile-directory="Profile 5" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=1765244048
    start "Chrome" "C:\Program Files\Googlofile 5" https://www.toptal.com/hire
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.upwork.com/nx/search/talent
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://phantombuster.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.europages.com.tr/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.amazon.com.tr/s?me=A368G57G993ZXD&marketplaceID=A33AVAJ2PDY3EV
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://mfgmatch.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.go4worldbusiness.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://sourcing.hktdc.com/en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://importer.ec21.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" Manufacturer.com 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" GlobalTrade.net
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.tradekey.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.globalspec.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.indiamart.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.made-in-china.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.tradeindia.com/ 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.mfg.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.thomasnet.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" http://www.manufacturerusa.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://b2brazil.com.br/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.goafricaonline.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://docs.google.com/spreadsheets/d/1TajXf58mLNsBixl6tCXRhSPixIzLsSf4HTiu6qxrbcg/edit#gid=700780096
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://ases.kitokoh.com/#/
    
    
    GOTO CASE_6
:CASE_6
:: Section : Tamam -
    pause
    ECHO Tamamam
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=1765244048
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://pro.fiverr.com/business/team_members?source=admin
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.freelancer.com/post-project
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.toptal.com/hire
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.upwork.com/nx/search/talent
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://phantombuster.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.europages.com.tr/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.amazon.com.tr/s?me=A368G57G993ZXD&marketplaceID=A33AVAJ2PDY3EV
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://mfgmatch.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.go4worldbusiness.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://sourcing.hktdc.com/en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://importer.ec21.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" Manufacturer.com 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" GlobalTrade.net
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.tradekey.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.globalspec.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.indiamart.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.made-in-china.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.tradeindia.com/ 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.mfg.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.thomasnet.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" http://www.manufacturerusa.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://b2brazil.com.br/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.goafricaonline.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://docs.google.com/spreadsheets/d/1TajXf58mLNsBixl6tCXRhSPixIzLsSf4HTiu6qxrbcg/edit#gid=700780096
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://ases.kitokoh.com/#/
   
  GOTO CASE_7
:CASE_7
 :: Section : kit sphop
    pause
    ECHO Kit sphop 

        start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=1765244048
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://pro.fiverr.com/business/team_members?source=admin
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.freelancer.com/post-project
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.toptal.com/hire
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.upwork.com/nx/search/talent
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://phantombuster.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.europages.com.tr/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.amazon.com.tr/s?me=A368G57G993ZXD&marketplaceID=A33AVAJ2PDY3EV
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://mfgmatch.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.go4worldbusiness.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://sourcing.hktdc.com/en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://importer.ec21.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" Manufacturer.com 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" GlobalTrade.net
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.tradekey.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.globalspec.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.indiamart.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.made-in-china.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.tradeindia.com/ 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.mfg.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.thomasnet.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" http://www.manufacturerusa.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://b2brazil.com.br/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.goafricaonline.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://docs.google.com/spreadsheets/d/1TajXf58mLNsBixl6tCXRhSPixIzLsSf4HTiu6qxrbcg/edit#gid=700780096
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://ases.kitokoh.com/#/
    
  GOTO CASE_8
:CASE_8
:: Section : Turk novatech
    pause

    ECHO Turknvoatech visites

        start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=1765244048
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://pro.fiverr.com/business/team_members?source=admin
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.freelancer.com/post-project
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.toptal.com/hire
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.upwork.com/nx/search/talent
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://phantombuster.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.europages.com.tr/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.amazon.com.tr/s?me=A368G57G993ZXD&marketplaceID=A33AVAJ2PDY3EV
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://mfgmatch.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.go4worldbusiness.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://sourcing.hktdc.com/en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://importer.ec21.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" Manufacturer.com 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" GlobalTrade.net
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.tradekey.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.globalspec.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.indiamart.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.made-in-china.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.tradeindia.com/ 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.mfg.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.thomasnet.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" http://www.manufacturerusa.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://b2brazil.com.br/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.goafricaonline.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://docs.google.com/spreadsheets/d/1TajXf58mLNsBixl6tCXRhSPixIzLsSf4HTiu6qxrbcg/edit#gid=700780096
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://ases.kitokoh.com/#/
   :CASE_9
 :: Section : kps otomotiv.
    pause
    ECHO kps

       start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=1765244048
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://pro.fiverr.com/business/team_members?source=admin
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.freelancer.com/post-project
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.toptal.com/hire
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.upwork.com/nx/search/talent
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://phantombuster.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.europages.com.tr/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.amazon.com.tr/s?me=A368G57G993ZXD&marketplaceID=A33AVAJ2PDY3EV
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://mfgmatch.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.go4worldbusiness.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://sourcing.hktdc.com/en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://importer.ec21.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" Manufacturer.com 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" GlobalTrade.net
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.tradekey.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.globalspec.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.indiamart.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.made-in-china.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.tradeindia.com/ 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.mfg.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.thomasnet.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" http://www.manufacturerusa.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://b2brazil.com.br/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.goafricaonline.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://docs.google.com/spreadsheets/d/1TajXf58mLNsBixl6tCXRhSPixIzLsSf4HTiu6qxrbcg/edit#gid=700780096
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://ases.kitokoh.com/#/
    
    GOTO CASE_10
:CASE_10
 :: Section : africa novatech
    pause
    ECHO ant visites

       start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=1765244048
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://pro.fiverr.com/business/team_members?source=admin
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.freelancer.com/post-project
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.toptal.com/hire
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.upwork.com/nx/search/talent
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://phantombuster.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.europages.com.tr/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.amazon.com.tr/s?me=A368G57G993ZXD&marketplaceID=A33AVAJ2PDY3EV
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://mfgmatch.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.go4worldbusiness.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://sourcing.hktdc.com/en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://importer.ec21.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" Manufacturer.com 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" GlobalTrade.net
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.tradekey.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.globalspec.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.indiamart.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.made-in-china.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.tradeindia.com/ 
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.mfg.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.thomasnet.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" http://www.manufacturerusa.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://b2brazil.com.br/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.goafricaonline.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://docs.google.com/spreadsheets/d/1TajXf58mLNsBixl6tCXRhSPixIzLsSf4HTiu6qxrbcg/edit#gid=700780096
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://ases.kitokoh.com/#/
    
  pause
    GOTO END_CASE
:DEFAULT_CASE
  ECHO Unknown color "%COLOR%"
  GOTO END_CASE
:END_CASE
  VER > NUL # reset ERRORLEVEL
  GOTO :EOF # return from CALL
    












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
ECHO Demande Prix 
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
  COLOR CF
  pause
  GOTO CASE_2
:CASE_2
    GOTO CASE_3
:CASE_3
  COLOR 0F
  GOTO CASE_4
:CASE_4
  COLOR CF
  pause
  GOTO CASE_5
:CASE_5
    GOTO CASE_6
:CASE_6
  COLOR 0F
  GOTO CASE_7
:CASE_7
  COLOR CF
  pause
  GOTO CASE_8
:CASE_8
    GOTO CASE_9
:CASE_9
  COLOR 0F
  GOTO CASE_10
:CASE_10
  COLOR 0F
  GOTO END_CASE
:DEFAULT_CASE
  ECHO Unknown color "%COLOR%"
  GOTO END_CASE
:END_CASE
  VER > NUL # reset ERRORLEVEL
  GOTO :EOF # return from CALL