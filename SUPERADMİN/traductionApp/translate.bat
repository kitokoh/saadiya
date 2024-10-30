@echo off
REM =======================================================
REM Script pour traduire l'application en différentes langues
REM Assurez-vous que vous êtes dans le bon répertoire et que 
REM l'environnement virtuel est activé avant de continuer.
REM =======================================================

REM Définir le répertoire cible
set target_dir=C:\Users\ibrahim\Downloads\Robot_Labo_Pro\lang
cd %target_dir%

REM Activer l'environnement virtuel
call C:\Users\ibrahim\Downloads\Robot_Labo_Pro\lang\env\Scripts\activate

echo Environnement virtuel activé...
echo Démarrage de la traduction vers différentes langues...
echo.

REM -------------------------------------------------------
REM Créer un tableau avec les langues et sous-dossiers
set languages=tr_TR ar_SA en_US pt_BR fr_Fr
set ui_subdirs=ui modules adsPro blogpro brandingpro chatBotpro emailingpro instagrampro linkedingpro pinterestpro redditpro snapchatpro tiktokpro twitterpro whatssappro youtubepro

REM Boucle sur les langues pour créer les répertoires
for %%L in (%languages%) do (
    for %%S in (%ui_subdirs%) do (
        if not exist "%%L\%%S" (
            echo Création du dossier %%L\%%S...
            mkdir resources\lang\%%L\%%S
        )
    )
)


set languagests=tr_TR ar_SA en_US pt_BR fr_Fr
set ui_subdirsts=ui modules adsPro blogpro brandingpro chatBotpro emailingpro instagrampro linkedingpro pinterestpro redditpro snapchatpro tiktokpro twitterpro whatssappro youtubepro


REM Boucle sur les langues pour créer les répertoires
for %%L in (%languagests%) do (
    for %%S in (%ui_subdirsts%) do (
        if not exist "%%L\%%S" (
            echo Création du dossier %%L\%%S...
            mkdir resources\langts\%%L\%%S
        )
    )
)

set langtstranslated=tr_TR ar_SA en_US pt_BR fr_Fr
set ui_subdirststranslated=ui modules adsPro blogpro brandingpro chatBotpro emailingpro instagrampro linkedingpro pinterestpro redditpro snapchatpro tiktokpro twitterpro whatssappro youtubepro


REM Boucle sur les langues pour créer les répertoires
for %%L in (%langtstranslated%) do (
    for %%S in (%ui_subdirststranslated%) do (
        if not exist "%%L\%%S" (
            echo Création du dossier %%L\%%S...
            mkdir resources\langtstranslated\%%L\%%S
        )
    )
)




REM -------------------------------------------------------
REM Générer les fichiers .ts pour chaque langue
REM Boucle pour chaque fichier source à traduire
set ui_files=carousel feature_buttons footer header login register secondry_menu side_menu toggle_menu
set module_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install
set fbkrobot_files=demarrageAuto setup sendatajson sendatajson2 sendatajson3

set whatssap_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 sendatajson3 
set instagram_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 sendatajson3
set linkeding_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 sendatajson3
set blog_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 sendatajson3
set adspro_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 sendatajson3
set branding_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 sendatajson3
set chatBot_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 sendatajson3
set emailing_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 sendatajson3
set pinterest_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 sendatajson3
set reddit_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 sendatajson3
set snapchat_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 sendatajson3
set tiktok_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 sendatajson3
set twitter_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 sendatajson3
set youtube_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 sendatajson3


echo Génération des fichiers .ts pour l'UI...
for %%L in (%languages%) do (
    for %%F in (%ui_files%) do (
        pylupdate5 ui/%%F.py -ts resources/langts/%%L/ui/%%F.ts
    )
)

echo Génération des fichiers .ts pour les modules...
for %%L in (%languages%) do (
    for %%F in (%module_files%) do (
        pylupdate5 %%F.py -ts resources/langts/%%L/modules/%%F.ts
    )
)
echo Génération des fichiers installfbrobot .ts pour l'UI...
for %%L in (%languages%) do (
    for %%F in (%fbkrobot_files%) do (
        pylupdate5 installFBrobotPy/%%F.py -ts resources/langts/%%L/modules/%%F.ts
    )
)


echo Génération des fichiers .ts pour les modules...
for %%L in (%languages%) do (
    for %%F in (%whatssap_files%) do (
        pylupdate5 ModulesUI/whasapping/%%F.py -ts resources/langts/%%L/whatssappro/%%F.ts
    )
)

for %%L in (%languages%) do (
    for %%F in (%instagram_files%) do (
        pylupdate5 ModulesUI/insta/%%F.py -ts resources/langts/%%L/instagrampro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%linkeding_files%) do (
        pylupdate5 ModulesUI/linkeding/%%F.py -ts resources/langts/%%L/linkedingpro/%%F.ts
    )
)

for %%L in (%languages%) do (
    for %%F in (%blog_files%) do (
        pylupdate5 ModulesUI/AutoBlog/%%F.py -ts resources/langts/%%L/blogpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%adspro_files%) do (
        pylupdate5 ModulesUI/adsPro/%%F.py -ts resources/langts/%%L/adspro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%branding_files%) do (
        pylupdate5 ModulesUI/branding/%%F.py -ts resources/langts/%%L/brandingpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%chatBot_files%) do (
        pylupdate5 ModulesUI/chatBot/%%F.py -ts resources/langts/%%L/chatBotpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%emailing_files%) do (
        pylupdate5 ModulesUI/emailing/%%F.py -ts resources/langts/%%L/emailingpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%pinterest_files%) do (
        pylupdate5 ModulesUI/pinterest/%%F.py -ts resources/langts/%%L/pinterestpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%reddit_files%) do (
        pylupdate5 ModulesUI/reddit/%%F.py -ts resources/langts/%%L/redditpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%snapchat_files%) do (
        pylupdate5 ModulesUI/snapchat/%%F.py -ts resources/langts/%%L/snapchatpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%tiktok_files%) do (
        pylupdate5 ModulesUI/tiktok/%%F.py -ts resources/langts/%%L/tiktokpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%twitter_files%) do (
        pylupdate5 ModulesUI/twitter/%%F.py -ts resources/langts/%%L/twitterpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%youtube_files%) do (
        pylupdate5 ModulesUI/youtube/%%F.py -ts resources/langts/%%L/youtubepro/%%F.ts
    )
)





REM Traduire les fichiers .ts avec le script Python present dans le sos dossieer 



echo Génération des fichiers .ts pour les modules...
for %%L in (%languages%) do (
    for %%F in (%whatssap_files%) do (
        pylupdate5 ModulesUI/whasapping/%%F.py -ts resources/langts/%%L/whatssappro/%%F.ts
    )
)

for %%L in (%languages%) do (
    for %%F in (%instagram_files%) do (
        pylupdate5 ModulesUI/insta/installwhattsaping/%%F.py -ts resources/langts/%%L/instagrampro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%linkeding_files%) do (
        pylupdate5 ModulesUI/linkeding/installwhattsaping/%%F.py -ts resources/langts/%%L/linkedingpro/%%F.ts
    )
)

for %%L in (%languages%) do (
    for %%F in (%blog_files%) do (
        pylupdate5 ModulesUI/AutoBlog/installwhattsaping/%%F.py -ts resources/langts/%%L/blogpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%adspro_files%) do (
        pylupdate5 ModulesUI/adsPro/installwhattsaping/%%F.py -ts resources/langts/%%L/adspro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%branding_files%) do (
        pylupdate5 ModulesUI/branding/installwhattsaping/%%F.py -ts resources/langts/%%L/brandingpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%chatBot_files%) do (
        pylupdate5 ModulesUI/chatBot/installwhattsaping/%%F.py -ts resources/langts/%%L/chatBotpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%emailing_files%) do (
        pylupdate5 ModulesUI/emailing/installwhattsaping/%%F.py -ts resources/langts/%%L/emailingpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%pinterest_files%) do (
        pylupdate5 ModulesUI/pinterest/installwhattsaping/%%F.py -ts resources/langts/%%L/pinterestpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%reddit_files%) do (
        pylupdate5 ModulesUI/reddit/installwhattsaping/%%F.py -ts resources/langts/%%L/redditpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%snapchat_files%) do (
        pylupdate5 ModulesUI/snapchat/installwhattsaping/%%F.py -ts resources/langts/%%L/snapchatpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%tiktok_files%) do (
        pylupdate5 ModulesUI/tiktok/installwhattsaping/%%F.py -ts resources/langts/%%L/tiktokpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%twitter_files%) do (
        pylupdate5 ModulesUI/twitter/installwhattsaping/%%F.py -ts resources/langts/%%L/twitterpro/%%F.ts
    )
)
for %%L in (%languages%) do (
    for %%F in (%youtube_files%) do (
        pylupdate5 ModulesUI/youtube/installwhattsaping/%%F.py -ts resources/langts/%%L/youtubepro/%%F.ts
    )
)


REM -------------------------------------------------------
REM Traduire les fichiers .ts avec le script Python
REM Boucle pour chaque fichier généré
echo Traduction des fichiers .ts avec Google Translate...

for %%L in (%languages%) do (
    for %%F in (%ui_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/ui/%%F.ts resources/langtstranslated/%%L/ui/%%F_translated.ts %%L
    )
    for %%F in (%module_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/modules/%%F.ts resources/langtstranslated/%%L/modules/%%F_translated.ts %%L
    )
     for %%F in (%adspro_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/adspro/%%F.ts resources/langtstranslated/%%L/adspro/%%F_translated.ts %%L
    )
     for %%F in (%blog_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/blogpro/%%F.ts resources/langtstranslated/%%L/blogpro/%%F_translated.ts %%L
    )
     for %%F in (%branding_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/brandingpro/%%F.ts resources/langtstranslated/%%L/brandingpro/%%F_translated.ts %%L
    )
     for %%F in (%chatBot_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/chatBotpro/%%F.ts resources/langtstranslated/%%L/chatBotpro/%%F_translated.ts %%L
    )
     for %%F in (%emailing_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/emailingpro/%%F.ts resources/langtstranslated/%%L/emailingpro/%%F_translated.ts %%L
    )
     for %%F in (%instagram_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/instagrampro/%%F.ts resources/langtstranslated/%%L/instagrampro/%%F_translated.ts %%L
    )
     for %%F in (%linkeding_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/linkedingpro/%%F.ts resources/langtstranslated/%%L/linkedingpro/%%F_translated.ts %%L
    )
     for %%F in (%pinterest_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/pinterestpro/%%F.ts resources/langtstranslated/%%L/pinterestpro/%%F_translated.ts %%L
    )
     for %%F in (%reddit_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/redditpro/%%F.ts resources/langtstranslated/%%L/redditpro/%%F_translated.ts %%L
    )
     for %%F in (%snapchat_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/snapchatpro/%%F.ts resources/langtstranslated/%%L/snapchatpro/%%F_translated.ts %%L
    )
     for %%F in (%tiktok_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/tiktokpro/%%F.ts resources/langtstranslated/%%L/tiktokpro/%%F_translated.ts %%L
    )
     for %%F in (%twitter_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/twitterpro/%%F.ts resources/langtstranslated/%%L/twitterpro/%%F_translated.ts %%L
    )
     for %%F in (%whatssap_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/whatssappro/%%F.ts resources/langtstranslated/%%L/whatssappro/%%F_translated.ts %%L
    )
     for %%F in (%youtube_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/langts/%%L/youtubepro/%%F.ts resources/langtstranslated/%%L/youtubepro/%%F_translated.ts %%L
    )
)
rem python traducteur.py lang/ar_SA/ui/carousel_translated.ts lang/ar_SA/ui/carousel_translated_translated.ts ar

REM -------------------------------------------------------
REM Générer les fichiers .qm à partir des fichiers traduits
echo Génération des fichiers .qm...

for %%L in (%languages%) do (
    for %%F in (%ui_files%) do (
        lrelease resources/langtstranslated/%%L/ui/%%F_translated.ts -qm resources/lang/%%L/ui/%%F_translated.qm
    )
    for %%F in (%module_files%) do (
        lrelease resources/langtstranslated/%%L/modules/%%F_translated.ts -qm resources/lang/%%L/modules/%%F_translated.qm
    )
    for %%F in (%adspro_files%) do (
        lrelease resources/langtstranslated/%%L/adspro/%%F_translated.ts -qm resources/lang/%%L/adspro/%%F_translated.qm
    )
    for %%F in (%blog_files%) do (
        lrelease resources/langtstranslated/%%L/blogpro/%%F_translated.ts -qm resources/lang/%%L/blogpro/%%F_translated.qm
    )
    for %%F in (%branding_files%) do (
        lrelease resources/langtstranslated/%%L/branding_files/%%F_translated.ts -qm resources/lang/%%L/branding_files/%%F_translated.qm
    )
    for %%F in (%chatBot_files%) do (
        lrelease resources/langtstranslated/%%L/chatBotpro/%%F_translated.ts -qm resources/lang/%%L/chatBotpro/%%F_translated.qm
    )
    for %%F in (%emailing_files%) do (
        lrelease resources/langtstranslated/%%L/emailingpro/%%F_translated.ts -qm resources/lang/%%L/emailingpro/%%F_translated.qm
    )
    for %%F in (%instagram_files%) do (
        lrelease resources/langtstranslated/%%L/instagrampro/%%F_translated.ts -qm resources/lang/%%L/instagrampro/%%F_translated.qm
    )
    for %%F in (%linkeding_files%) do (
        lrelease resources/langtstranslated/%%L/linkedingpro/%%F_translated.ts -qm resources/lang/%%L/linkedingpro/%%F_translated.qm
    )
    for %%F in (%pinterest_files%) do (
        lrelease resources/langtstranslated/%%L/pinterestpro/%%F_translated.ts -qm resources/lang/%%L/pinterestpro/%%F_translated.qm
    )
    for %%F in (%reddit_files%) do (
        lrelease resources/langtstranslated/%%L/redditpro/%%F_translated.ts -qm resources/lang/%%L/redditpro/%%F_translated.qm
    )
    for %%F in (%snapchat_files%) do (
        lrelease resources/langtstranslated/%%L/snapchatpro/%%F_translated.ts -qm resources/lang/%%L/snapchatpro/%%F_translated.qm
    )
    for %%F in (%tiktok_files%) do (
        lrelease resources/langtstranslated/%%L/tiktokpro/%%F_translated.ts -qm resources/lang/%%L/tiktokpro/%%F_translated.qm
    )
    for %%F in (%twitter_files%) do (
        lrelease resources/langtstranslated/%%L/twitterpro/%%F_translated.ts -qm resources/lang/%%L/twitterpro/%%F_translated.qm
    )
    for %%F in (%whatssap_files%) do (
        lrelease resources/langtstranslated/%%L/whatssappro/%%F_translated.ts -qm resources/lang/%%L/whatssappro/%%F_translated.qm
    )
    for %%F in (%youtube_files%) do (
        lrelease resources/langtstranslated/%%L/youtubepro/%%F_translated.ts -qm resources/lang/%%L/youtubepro/%%F_translated.qm
    )
)

echo Toutes les traductions sont terminées avec succès!
pause
