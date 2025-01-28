

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
ECHO Publier des contenues 
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

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.canva.com/
:: Pour publier simple  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://publish.buffer.com/calendar/week
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://vimeo.com/upload/videos
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://t.me/nouractu
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.farmoos.com/wp-admin/edit.php

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://news.google.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://nouractu.com/wp-admin/post-new.php
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://nouractu.com/wp-admin/admin.php?page=blog2social-post
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.linkedin.com/company/102158404/admin/feed/posts/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.pinterest.fr/pin-creation-tool/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.dailymotion.com/partner/x2nsxek/media/video
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.tumblr.com/new/photo
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://twitter.com/home
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://business.facebook.com/latest/
:: Pour publier Pub  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://ads.google.com/aw/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://ads.pinterest.com/advertiser/549767728207/?attributionWindow=30%2F30%2F30&conversionReportDate=AD_EVENT
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://ads.tiktok.com/i18n/fast_creation/ad-mode?aadvid=7368756014373470209
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://ads.twitter.com/onboarding/18ce55p4wjg/welcome
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://business.facebook.com/latest/home?business_id=3026753937582709&asset_id=604175819994562
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://adsmanager.facebook.com/adsmanager/manage/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.linkedin.com/campaignmanager/new-advertiser
:: Pour publier Job  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.linkedin.com/my-items/posted-jobs/
:: Pour publier product  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://merchants.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.google.com/retail/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://manufacturers.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.farmoos.com/wp-admin/edit.php?post_type=product
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://sellercentral.amazon.com.tr/inventory/
:: Pour publier Review   
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://www.google.com/maps/contrib/1
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1" https://business.trustpilot.com/





:: Pour le partages et developpement 
  pause
  GOTO CASE_2
:CASE_2
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.canva.com/
:: Pour publier simple  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://publish.buffer.com/calendar/week
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://vimeo.com/upload/videos
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://t.me/nouractu
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.farmoos.com/wp-admin/edit.php

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://news.google.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://nouractu.com/wp-admin/post-new.php
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://nouractu.com/wp-admin/admin.php?page=blog2social-post
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.linkedin.com/company/102158404/admin/feed/posts/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.pinterest.fr/pin-creation-tool/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.dailymotion.com/partner/x2nsxek/media/video
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.tumblr.com/new/photo
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://twitter.com/home
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://business.facebook.com/latest/
:: Pour publier Pub  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://ads.google.com/aw/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://ads.pinterest.com/advertiser/549767728207/?attributionWindow=30%2F30%2F30&conversionReportDate=AD_EVENT
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://ads.tiktok.com/i18n/fast_creation/ad-mode?aadvid=7368756014373470209
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://ads.twitter.com/onboarding/18ce55p4wjg/welcome
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://business.facebook.com/latest/home?business_id=3026753937582709&asset_id=604175819994562
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://adsmanager.facebook.com/adsmanager/manage/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.linkedin.com/campaignmanager/new-advertiser
:: Pour publier Job  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.linkedin.com/my-items/posted-jobs/
:: Pour publier product  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://merchants.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.google.com/retail/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://manufacturers.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.farmoos.com/wp-admin/edit.php?post_type=product
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://sellercentral.amazon.com.tr/inventory/
:: Pour publier Review   
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://www.google.com/maps/contrib/1
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 2" https://business.trustpilot.com/


    GOTO CASE_3
:CASE_3

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.canva.com/
:: Pour publier simple  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://publish.buffer.com/calendar/week
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://vimeo.com/upload/videos
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://t.me/nouractu
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.farmoos.com/wp-admin/edit.php

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://news.google.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://nouractu.com/wp-admin/post-new.php
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://nouractu.com/wp-admin/admin.php?page=blog2social-post
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.linkedin.com/company/102158404/admin/feed/posts/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.pinterest.fr/pin-creation-tool/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.dailymotion.com/partner/x2nsxek/media/video
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.tumblr.com/new/photo
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://twitter.com/home
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://business.facebook.com/latest/
:: Pour publier Pub  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://ads.google.com/aw/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://ads.pinterest.com/advertiser/549767728207/?attributionWindow=30%2F30%2F30&conversionReportDate=AD_EVENT
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://ads.tiktok.com/i18n/fast_creation/ad-mode?aadvid=7368756014373470209
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://ads.twitter.com/onboarding/18ce55p4wjg/welcome
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://business.facebook.com/latest/home?business_id=3026753937582709&asset_id=604175819994562
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://adsmanager.facebook.com/adsmanager/manage/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.linkedin.com/campaignmanager/new-advertiser
:: Pour publier Job  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.linkedin.com/my-items/posted-jobs/
:: Pour publier product  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://merchants.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.google.com/retail/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://manufacturers.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.farmoos.com/wp-admin/edit.php?post_type=product
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://sellercentral.amazon.com.tr/inventory/
:: Pour publier Review   
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://www.google.com/maps/contrib/1
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 3" https://business.trustpilot.com/





:: Pour le partages et developpement 
  GOTO CASE_4
:CASE_4

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.canva.com/
:: Pour publier simple  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://publish.buffer.com/calendar/week
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://vimeo.com/upload/videos
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://t.me/nouractu
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.farmoos.com/wp-admin/edit.php

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://news.google.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://nouractu.com/wp-admin/post-new.php
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://nouractu.com/wp-admin/admin.php?page=blog2social-post
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.linkedin.com/company/102158404/admin/feed/posts/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.pinterest.fr/pin-creation-tool/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.dailymotion.com/partner/x2nsxek/media/video
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.tumblr.com/new/photo
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://twitter.com/home
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://business.facebook.com/latest/
:: Pour publier Pub  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://ads.google.com/aw/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://ads.pinterest.com/advertiser/549767728207/?attributionWindow=30%2F30%2F30&conversionReportDate=AD_EVENT
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://ads.tiktok.com/i18n/fast_creation/ad-mode?aadvid=7368756014373470209
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://ads.twitter.com/onboarding/18ce55p4wjg/welcome
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://business.facebook.com/latest/home?business_id=3026753937582709&asset_id=604175819994562
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://adsmanager.facebook.com/adsmanager/manage/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.linkedin.com/campaignmanager/new-advertiser
:: Pour publier Job  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.linkedin.com/my-items/posted-jobs/
:: Pour publier product  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://merchants.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.google.com/retail/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://manufacturers.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.farmoos.com/wp-admin/edit.php?post_type=product
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://sellercentral.amazon.com.tr/inventory/
:: Pour publier Review   
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://www.google.com/maps/contrib/1
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 10" https://business.trustpilot.com/





:: Pour le partages et developpement 
  pause
  GOTO CASE_5
:CASE_5

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.canva.com/
:: Pour publier simple  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://publish.buffer.com/calendar/week
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://vimeo.com/upload/videos
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://t.me/nouractu
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.farmoos.com/wp-admin/edit.php

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://news.google.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://nouractu.com/wp-admin/post-new.php
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://nouractu.com/wp-admin/admin.php?page=blog2social-post
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.linkedin.com/company/102158404/admin/feed/posts/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.pinterest.fr/pin-creation-tool/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.dailymotion.com/partner/x2nsxek/media/video
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.tumblr.com/new/photo
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://twitter.com/home
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://business.facebook.com/latest/
:: Pour publier Pub  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://ads.google.com/aw/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://ads.pinterest.com/advertiser/549767728207/?attributionWindow=30%2F30%2F30&conversionReportDate=AD_EVENT
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://ads.tiktok.com/i18n/fast_creation/ad-mode?aadvid=7368756014373470209
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://ads.twitter.com/onboarding/18ce55p4wjg/welcome
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://business.facebook.com/latest/home?business_id=3026753937582709&asset_id=604175819994562
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://adsmanager.facebook.com/adsmanager/manage/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.linkedin.com/campaignmanager/new-advertiser
:: Pour publier Job  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.linkedin.com/my-items/posted-jobs/
:: Pour publier product  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://merchants.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.google.com/retail/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://manufacturers.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.farmoos.com/wp-admin/edit.php?post_type=product
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://sellercentral.amazon.com.tr/inventory/
:: Pour publier Review   
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://www.google.com/maps/contrib/1
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 5" https://business.trustpilot.com/





:: Pour le partages et developpement 
    GOTO CASE_6
:CASE_6

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.canva.com/
:: Pour publier simple  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://publish.buffer.com/calendar/week
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://vimeo.com/upload/videos
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://t.me/nouractu
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.farmoos.com/wp-admin/edit.php

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://news.google.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://nouractu.com/wp-admin/post-new.php
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://nouractu.com/wp-admin/admin.php?page=blog2social-post
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.linkedin.com/company/102158404/admin/feed/posts/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.pinterest.fr/pin-creation-tool/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.dailymotion.com/partner/x2nsxek/media/video
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.tumblr.com/new/photo
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://twitter.com/home
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://business.facebook.com/latest/
:: Pour publier Pub  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://ads.google.com/aw/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://ads.pinterest.com/advertiser/549767728207/?attributionWindow=30%2F30%2F30&conversionReportDate=AD_EVENT
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://ads.tiktok.com/i18n/fast_creation/ad-mode?aadvid=7368756014373470209
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://ads.twitter.com/onboarding/18ce55p4wjg/welcome
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://business.facebook.com/latest/home?business_id=3026753937582709&asset_id=604175819994562
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://adsmanager.facebook.com/adsmanager/manage/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.linkedin.com/campaignmanager/new-advertiser
:: Pour publier Job  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.linkedin.com/my-items/posted-jobs/
:: Pour publier product  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://merchants.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.google.com/retail/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://manufacturers.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.farmoos.com/wp-admin/edit.php?post_type=product
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://sellercentral.amazon.com.tr/inventory/
:: Pour publier Review   
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://www.google.com/maps/contrib/1
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 6" https://business.trustpilot.com/





:: Pour le partages et developpement 
  GOTO CASE_7
:CASE_7

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.canva.com/
:: Pour publier simple  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://publish.buffer.com/calendar/week
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://vimeo.com/upload/videos
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://t.me/nouractu
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.farmoos.com/wp-admin/edit.php

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://news.google.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://nouractu.com/wp-admin/post-new.php
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://nouractu.com/wp-admin/admin.php?page=blog2social-post
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.linkedin.com/company/102158404/admin/feed/posts/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.pinterest.fr/pin-creation-tool/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.dailymotion.com/partner/x2nsxek/media/video
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.tumblr.com/new/photo
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://twitter.com/home
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://business.facebook.com/latest/
:: Pour publier Pub  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://ads.google.com/aw/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://ads.pinterest.com/advertiser/549767728207/?attributionWindow=30%2F30%2F30&conversionReportDate=AD_EVENT
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://ads.tiktok.com/i18n/fast_creation/ad-mode?aadvid=7368756014373470209
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://ads.twitter.com/onboarding/18ce55p4wjg/welcome
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://business.facebook.com/latest/home?business_id=3026753937582709&asset_id=604175819994562
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://adsmanager.facebook.com/adsmanager/manage/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.linkedin.com/campaignmanager/new-advertiser
:: Pour publier Job  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.linkedin.com/my-items/posted-jobs/
:: Pour publier product  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://merchants.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.google.com/retail/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://manufacturers.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.farmoos.com/wp-admin/edit.php?post_type=product
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://sellercentral.amazon.com.tr/inventory/
:: Pour publier Review   
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://www.google.com/maps/contrib/1
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 7" https://business.trustpilot.com/





:: Pour le partages et developpement 
  pause
  GOTO CASE_8
:CASE_8

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.canva.com/
:: Pour publier simple  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://publish.buffer.com/calendar/week
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://vimeo.com/upload/videos
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://t.me/nouractu
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.farmoos.com/wp-admin/edit.php

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://news.google.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://nouractu.com/wp-admin/post-new.php
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://nouractu.com/wp-admin/admin.php?page=blog2social-post
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.linkedin.com/company/102158404/admin/feed/posts/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.pinterest.fr/pin-creation-tool/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.dailymotion.com/partner/x2nsxek/media/video
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.tumblr.com/new/photo
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://twitter.com/home
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://business.facebook.com/latest/
:: Pour publier Pub  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://ads.google.com/aw/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://ads.pinterest.com/advertiser/549767728207/?attributionWindow=30%2F30%2F30&conversionReportDate=AD_EVENT
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://ads.tiktok.com/i18n/fast_creation/ad-mode?aadvid=7368756014373470209
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://ads.twitter.com/onboarding/18ce55p4wjg/welcome
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://business.facebook.com/latest/home?business_id=3026753937582709&asset_id=604175819994562
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://adsmanager.facebook.com/adsmanager/manage/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.linkedin.com/campaignmanager/new-advertiser
:: Pour publier Job  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.linkedin.com/my-items/posted-jobs/
:: Pour publier product  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://merchants.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.google.com/retail/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://manufacturers.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.farmoos.com/wp-admin/edit.php?post_type=product
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://sellercentral.amazon.com.tr/inventory/
:: Pour publier Review   
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://www.google.com/maps/contrib/1
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 8" https://business.trustpilot.com/





:: Pour le partages et developpement 
    GOTO CASE_9
:CASE_9

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.canva.com/
:: Pour publier simple  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://publish.buffer.com/calendar/week
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://vimeo.com/upload/videos
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://t.me/nouractu
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.farmoos.com/wp-admin/edit.php

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://news.google.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://nouractu.com/wp-admin/post-new.php
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://nouractu.com/wp-admin/admin.php?page=blog2social-post
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.linkedin.com/company/102158404/admin/feed/posts/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.pinterest.fr/pin-creation-tool/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.dailymotion.com/partner/x2nsxek/media/video
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.tumblr.com/new/photo
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://twitter.com/home
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://business.facebook.com/latest/
:: Pour publier Pub  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://ads.google.com/aw/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://ads.pinterest.com/advertiser/549767728207/?attributionWindow=30%2F30%2F30&conversionReportDate=AD_EVENT
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://ads.tiktok.com/i18n/fast_creation/ad-mode?aadvid=7368756014373470209
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://ads.twitter.com/onboarding/18ce55p4wjg/welcome
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://business.facebook.com/latest/home?business_id=3026753937582709&asset_id=604175819994562
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://adsmanager.facebook.com/adsmanager/manage/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.linkedin.com/campaignmanager/new-advertiser
:: Pour publier Job  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.linkedin.com/my-items/posted-jobs/
:: Pour publier product  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://merchants.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.google.com/retail/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://manufacturers.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.farmoos.com/wp-admin/edit.php?post_type=product
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://sellercentral.amazon.com.tr/inventory/
:: Pour publier Review   
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://www.google.com/maps/contrib/1
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 9" https://business.trustpilot.com/





:: Pour le partages et developpement 
  GOTO CASE_10
:CASE_10
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.canva.com/
:: Pour publier simple  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://publish.buffer.com/calendar/week
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.instagram.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.tiktok.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://studio.youtube.com/channel/  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://vimeo.com/upload/videos
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://t.me/nouractu
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.farmoos.com/wp-admin/edit.php

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://news.google.com/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://nouractu.com/wp-admin/post-new.php
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://nouractu.com/wp-admin/admin.php?page=blog2social-post
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.linkedin.com/company/102158404/admin/feed/posts/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.pinterest.fr/pin-creation-tool/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.dailymotion.com/partner/x2nsxek/media/video
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.tumblr.com/new/photo
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://twitter.com/home
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://business.facebook.com/latest/
:: Pour publier Pub  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://ads.google.com/aw/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://ads.pinterest.com/advertiser/549767728207/?attributionWindow=30%2F30%2F30&conversionReportDate=AD_EVENT
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://ads.tiktok.com/i18n/fast_creation/ad-mode?aadvid=7368756014373470209
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://ads.twitter.com/onboarding/18ce55p4wjg/welcome
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://business.facebook.com/latest/home?business_id=3026753937582709&asset_id=604175819994562
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://adsmanager.facebook.com/adsmanager/manage/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.linkedin.com/campaignmanager/new-advertiser
:: Pour publier Job  

start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.linkedin.com/my-items/posted-jobs/
:: Pour publier product  
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://merchants.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.google.com/retail/
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://manufacturers.google.com/mc
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.farmoos.com/wp-admin/edit.php?post_type=product
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://sellercentral.amazon.com.tr/inventory/
:: Pour publier Review   
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://www.google.com/maps/contrib/1
start "Chrome" "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" https://business.trustpilot.com/

  GOTO END_CASE
:DEFAULT_CASE
  ECHO Unknown color "%COLOR%"
  GOTO END_CASE
:END_CASE
  VER > NUL # reset ERRORLEVEL
  GOTO :EOF # return from CALL