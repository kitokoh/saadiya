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
IF %hour%==21 ( SET MENU=2) ELSE  ( SET /P MENU="Choose opption (type 1, 2 ,3 ,4,5,6 ,7,8,9,10): ")

1>NUL CALL :CASE_%MENU% # jump to :CASE_1, :CASE_2, etc.
IF ERRORLEVEL 1 CALL :DEFAULT_CASE # If label doesn't exist

ECHO Done.
EXIT /B

:CASE_1
:: START https://support.microsoft.com/en-us/windows/windows-10-system-requirements-6d4e9a79-66bf-7950-467c-795cf0386715
    :: Section : Ibrahim personnell ajouter un les opportunute universite et autre 
    ECHO Ibrahim Personnell
    ECHO clic to continue .........

    
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=1765244048
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://pro.fiverr.com/business/team_members?source=admin
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.google.com/maps/contrib/1

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.ib.turknovatech.com/wp-admin
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.tiktok.com/@ibrahimalimahadi
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.facebook.com/smartprimes/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.instagram.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.linkedin.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://bio.link/borgo
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.ib.turknovatech.com/shop/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.europages.com.tr/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://tr.pinterest.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.ib.turknovatech.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://nextdoor.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://tr.pinterest.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://workplace.clickworker.com/en/workplace/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://business.tiktok.com/manage/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.tiktok.com/messages?lang=en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://twitter.com/messages
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://business.facebook.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://business.facebook.com/latest/inbox/all/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.reddit.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.quora.com/profile/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.youtube.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://vimeo.com/home?signup=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.goafricaonline.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://search.google.com/search-console

    :: Section :Nour actu .
    pause
    GOTO CASE_2
  :: bot
:CASE_2
ECHO Nour actu

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=1169353092
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.fiverr.com/nouractu?up_rollout=true
     start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.google.com/maps/contrib/1
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.nouractu.com
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.nouractu.com/wp-admin


     start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.europages.co.uk/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://business.facebook.com/latest/home?business_id=3026753937582709&asset_id=604175819994562

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox



    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.reddit.com/user/nouractu/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.quora.com/profile/Nour-Actu
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://studio.youtube.com/channel/UCB-bf-9wYePpDNZ4vSfv2GQ/videos
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://vimeo.com/user218410891

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.facebook.com/groups/joins/?nav_source=tab&ordering=viewer_added

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.tiktok.com/@nouractu
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://business.tiktok.com/manage/overview/?org_id=7368758065719722001&show-adv-guide=yes&overviewfrom=bc_registration
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.tiktok.com/messages?lang=en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.facebook.com/nouractu.td
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.instagram.com/nouractu/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.linkedin.com/company/102158404/admin/feed/posts/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://linktr.ee/nouractu
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://linktr.ee/admin?welcome=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.pinterest.fr/nouractu/?actingBusinessId=938297041023494469


    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.pinterest.fr/nouractu/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.youtube.com/channel/UCB-bf-9wYePpDNZ4vSfv2GQ
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.quora.com/profile/Nour-Actu
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://studio.youtube.com/channel/UCB-bf-9wYePpDNZ4vSfv2GQ/videos
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://vimeo.com/user218410891
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://twitter.com/messages
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://search.google.com/search-console


    GOTO CASE_3,
 :: travail
:CASE_3

    :: Section : kitokoh .
    pause
    ECHO Kitokoh

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://docs.google.com/spreadsheets/u/0/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit?pli=1#gid=105532318
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.fiverr.com/kitokohluxe?up_rollout=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3"  https://www.tchop.nouractu.com
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3"  https://www.tchop.nouractu.com/wp-admin
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.google.com/maps/contrib/1

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.kitokoh.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3"  https://www.kitokoh.com/tokoadmin/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.europages.com
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://tr.pinterest.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://business.tiktok.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3"  https://www.tiktok.com/messages?lang=en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://twitter.com/messages
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://business.facebook.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://business.facebook.com/latest/inbox/all/?asset_id=269643532888278&mailbox_id=269643532888278&selected_item_id=61556910585889&thread_type=FB_MESSAGE

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://Nova360.io/crm/conversation
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://web.whatsapp.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://brandregistry.amazon.com.tr/brand/enrollment/manage/applications
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://sellercentral.amazon.com.tr/home
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.reddit.com/user/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://linktr.ee/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.quora.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.youtube.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://vimeo.com/home?signup=true

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://search.google.com/search-console


    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.facebook.com/groups/joins/?nav_source=tab&ordering=viewer_added
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.goafricaonline.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
    GOTO CASE_4
:: finance admin
:CASE_4
 :: Section 3: Farmoos
    pause
    ECHO Farmoos
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit?pli=1#gid=0
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.farmoos.com
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.farmoos.com/wp-admin/edit.php?post_type=shop_order
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.europages.co.uk/account/company-profile/cover
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.google.com/maps/contrib/1

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://tr.pinterest.com/farmoos/farmoos1/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://business.tiktok.com/manage/overview?org_id=7354726627907141633&select_track=1
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.tiktok.com/messages?lang=en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://twitter.com/messages
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://business.facebook.com/latest/leads_center?asset_id=269643532888278&nav_id=1406782370
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://business.facebook.com/latest/inbox/all/?asset_id=269643532888278&mailbox_id=269643532888278&selected_item_id=61556910585889&thread_type=FB_MESSAGE

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://Nova360.io/crm/conversation
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://web.whatsapp.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://brandregistry.amazon.com.tr/brand/enrollment/manage/applications
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://sellercentral.amazon.com.tr/home
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.reddit.com/user/farmoos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://linktr.ee/farmoos
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.quora.com/profile/Milkin-Farming-FarmoosTM

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.youtube.com/@framoostr
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://vimeo.com/home?signup=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://partner.trendyol.com/account/info?tab=contractAndDocuments&openApproveModal=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://search.google.com/search-console


    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://gsp.aliexpress.com/apps/onboarding/audit_ae_tr
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.deepl.com/en/translator/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.facebook.com/groups/joins/?nav_source=tab&ordering=viewer_added
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://auth.turkishexporter.com.tr/mypage/tr/boughtleads/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.goafricaonline.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/

    GOTO CASE_5
:: ref stat
:CASE_5
 :: Section : okps door
    pause
    ECHO door

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" http://www.okpsplastik.com.tr
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.kitokoh.com/custumers
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.kitokoh.com/faq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.kitokoh.com/invest/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.google.com/maps/contrib/1

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.okpsdoor.com/tokoadmin
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.europages.co.uk/account/company-profile/cover

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://tr.pinterest.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://business.tiktok.com/manage/overview?org_id=7354726627907141633&select_track=1
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.tiktok.com/messages?lang=en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://twitter.com/messages
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://business.facebook.com/latest/leads_center?asset_id=269643532888278&nav_id=1406782370
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://business.facebook.com/latest/inbox/all/?asset_id=269643532888278&mailbox_id=269643532888278&selected_item_id=61556910585889&thread_type=FB_MESSAGE

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://brandregistry.amazon.com.tr/brand/enrollment/manage/applications
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://sellercentral.amazon.com.tr/home
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.reddit.com/user/kitokoh/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://linktr.ee/kitokoh
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.quora.com/profile/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.youtube.com/@kitokoh
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://vimeo.com/home?signup=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://partner.trendyol.com/account/info?tab=contractAndDocuments&openApproveModal=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://search.google.com/search-console



    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://gsp.aliexpress.com/apps/onboarding/audit_ae_tr
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.deepl.com/en/translator/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.facebook.com/groups/joins/?nav_source=tab&ordering=viewer_added
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://auth.turkishexporter.com.tr/mypage/tr/boughtleads/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.goafricaonline.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/

   GOTO CASE_6
 :: conception
:CASE_6
  :: Section : Tamam -
    pause
    ECHO Tamamam

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=1038622607
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.fiverr.com/ecommereai?up_rollout=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.google.com/maps/contrib/1

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.services.kitokoh.com/wp-admin/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6"https://www.host.services.kitokoh.com.com
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6"  https://www.africanovatech.com/wp-admin/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.kitokoh.com/tamam
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.kitokoh.com/tamam/wp-admin/edit.php?post_type=shop_order
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.europages.co.uk/account/company-profile/cover
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://tr.pinterest.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://business.tiktok.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6"  https://www.tiktok.com/messages?lang=en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://twitter.com/messages
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://business.facebook.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://business.facebook.com/latest/inbox/all/?asset_id=269643532888278&mailbox_id=269643532888278&selected_item_id=61556910585889&thread_type=FB_MESSAGE

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://Nova360.io/crm/conversation
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://web.whatsapp.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://brandregistry.amazon.com.tr/brand/enrollment/manage/applications
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://sellercentral.amazon.com.tr/home
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.reddit.com/user/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://linktr.ee/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.quora.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.youtube.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://vimeo.com/home?signup=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://search.google.com/search-console



    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.facebook.com/groups/joins/?nav_source=tab&ordering=viewer_added
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.goafricaonline.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
     GOTO CASE_7
:CASE_7
:: Section : kit sphop
    pause
    ECHO Kit sphop 

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=1051512183
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.fiverr.com/fakiabrahim?up_rollout=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7"  https://www.kit-sphop.com
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7"  https://www.kit-sphop.com/wp-admin/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.kit-sphop.com/wp-admin/edit.php?post_type=shop_order
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.europages.co.uk/account/company-profile/cover
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://tr.pinterest.com/
     start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.google.com/maps/contrib/1

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://business.tiktok.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7"  https://www.tiktok.com/messages?lang=en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://twitter.com/messages
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://business.facebook.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://business.facebook.com/latest/inbox/all/?asset_id=269643532888278&mailbox_id=269643532888278&selected_item_id=61556910585889&thread_type=FB_MESSAGE

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://web.whatsapp.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://brandregistry.amazon.com.tr/brand/enrollment/manage/applications
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://sellercentral.amazon.com.tr/home
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.reddit.com/user/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://linktr.ee/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.quora.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.youtube.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://vimeo.com/home?signup=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://search.google.com/search-console



    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.facebook.com/groups/joins/?nav_source=tab&ordering=viewer_added
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.goafricaonline.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
    GOTO CASE_8
:CASE_8
 :: Section : Turk novatech
    pause

    ECHO Turknvoatech visites

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=1034336491
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.fiverr.com/users/turknovatech/seller_dashboard

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8"  https://www.turknovatech.com/wp-admin/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.turknvoatech.com/wp-admin/edit.php?post_type=shop_order
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.europages.co.uk/account/company-profile/cover
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://tr.pinterest.com/
     start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.google.com/maps/contrib/1

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://business.tiktok.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8"  https://www.tiktok.com/messages?lang=en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://twitter.com/messages
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://business.facebook.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://business.facebook.com/latest/inbox/all/?asset_id=269643532888278&mailbox_id=269643532888278&selected_item_id=61556910585889&thread_type=FB_MESSAGE

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.linkedin.com/feed/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://web.whatsapp.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://brandregistry.amazon.com.tr/brand/enrollment/manage/applications
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://sellercentral.amazon.com.tr/home
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.reddit.com/user/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://linktr.ee/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.quora.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.youtube.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://vimeo.com/home?signup=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://search.google.com/search-console



    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.facebook.com/groups/joins/?nav_source=tab&ordering=viewer_added
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.goafricaonline.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
    GOTO CASE_9
:CASE_9
 :: Section : kps otomotiv.
    pause
    ECHO kps

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=891400134
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.fiverr.com/ibo_nova360?up_rollout=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://www.europages.co.uk/account/company-profile/cover
     start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.google.com/maps/contrib/1

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://tr.pinterest.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://business.tiktok.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://www.tiktok.com/messages?lang=en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://twitter.com/messages
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://business.facebook.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://business.facebook.com/latest/inbox/all/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://Nova360.io/crm/conversation
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://web.whatsapp.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://brandregistry.amazon.com.tr/brand/enrollment/manage/applications
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://sellercentral.amazon.com.tr/home
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://www.reddit.com/user/farmoos/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://linktr.ee/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://www.quora.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://www.youtube.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://vimeo.com/home?signup=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://partner.trendyol.com/account/info?tab=contractAndDocuments&openApproveModal=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://search.google.com/search-console



    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://gsp.aliexpress.com/apps/onboarding/audit_ae_tr
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://www.deepl.com/en/translator/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://www.facebook.com/groups/joins/?nav_source=tab&ordering=viewer_added
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://auth.turkishexporter.com.tr/mypage/tr/boughtleads/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://www.goafricaonline.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9"  https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
     GOTO CASE_10
:CASE_10
 :: Section : africa novatech
    pause
    ECHO ant visites

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://docs.google.com/spreadsheets/d/1fZ4FgloW6B6CArPRpjqbyjUHMMEdTy7zoGSj4OWTBX4/edit#gid=2031157750
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://fr.fiverr.com/novatecha?up_rollout=true
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.ai.africanovatech.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://search.google.com/search-console/index?resource_id=https%3A%2F%2Fafricanovatech.com%2F
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.ai.africanovatech.com/wp-admim
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.host.africanovatech.com/wp-admin/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default"https://www.host.africanovatech.com
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default"  https://www.africanovatech.com/wp-admin/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.africanoatech.com/wp-admin/edit.php?post_type=shop_order
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.europages.co.uk/account/company-profile/cover
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://tr.pinterest.com/
     start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.google.com/maps/contrib/1

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://business.tiktok.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default"  https://www.tiktok.com/messages?lang=en
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://twitter.com/messages
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://business.facebook.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://business.facebook.com/latest/inbox/all/?asset_id=269643532888278&mailbox_id=269643532888278&selected_item_id=61556910585889&thread_type=FB_MESSAGE

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://web.whatsapp.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://brandregistry.amazon.com.tr/brand/enrollment/manage/applications
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://sellercentral.amazon.com.tr/home
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.reddit.com/user/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://linktr.ee/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.quora.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.youtube.com/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://vimeo.com/home?signup=true



    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.facebook.com/groups/joins/?nav_source=tab&ordering=viewer_added
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.turkishexporter.com.tr/fr/rfq/
    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.goafricaonline.com/

    start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://musaviredanisin.ticaret.gov.tr/giris/?next=/anasayfa/
          GOTO END_CASE
:DEFAULT_CASE
  ECHO Unknown color "%MENU%"
  GOTO END_CASE
:END_CASE
  VER > NUL # reset ERRORLEVEL
  GOTO :EOF # return from CALL

    
    