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

set langtstranslatedtoHuman=tr_TR ar_SA en_US pt_BR fr_Fr
set ui_subdirststranslated=ui modules adsPro blogpro brandingpro chatBotpro emailingpro instagrampro linkedingpro pinterestpro redditpro snapchatpro tiktokpro twitterpro whatssappro youtubepro


REM Boucle sur les langues pour créer les répertoires
for %%L in (%langtstranslatedtoHuman%) do (
    for %%S in (%ui_subdirststranslated%) do (
        if not exist "%%L\%%S" (
            echo Création du dossier %%L\%%S...
            mkdir resources\langtstranslatedtoHuman\%%L\%%S
        )
    )
)




REM -------------------------------------------------------update_media_dialog demarrageAuto main_x_robot 
REM Générer les fichiers .ts pour chaque langue
REM Boucle pour chaque fichier source à traduire
set ui_files=carousel feature_buttons footer header login register secondry_menu side_menu toggle_menu
set module_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto
set fbkrobot_files=demarrageAuto setup sendatajson sendatajson2 sendatajson3 supprimBon supprimeDossierİnstall uninstallQT updatejson

set whatssap_files=main main_wp_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 supprimBon supprimeDossierİnstall uninstallQT updatejson 
set instagram_files=main main_insta_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 supprimBon supprimeDossierİnstall uninstallQT updatejson
set linkeding_files=main main_linkeding_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 supprimBon supprimeDossierİnstall uninstallQT updatejson
set blog_files=main main_blog_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 supprimBon supprimeDossierİnstall uninstallQT updatejson
set adspro_files=main main_ads_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 supprimBon supprimeDossierİnstall uninstallQT updatejson
set branding_files=main main_brand_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 supprimBon supprimeDossierİnstall uninstallQT updatejson
set chatBot_files=main main_chatbot_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 supprimBon supprimeDossierİnstall uninstallQT updatejson
set emailing_files=main main_mail_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 supprimBon supprimeDossierİnstall uninstallQT updatejson
set pinterest_files=main main_pin_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 supprimBon supprimeDossierİnstall uninstallQT updatejson
set reddit_files=main main_reddit_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 supprimBon supprimeDossierİnstall uninstallQT updatejson
set snapchat_files=main main_snap_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 supprimBon supprimeDossierİnstall uninstallQT updatejson
set tiktok_files=main main_tok_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 supprimBon supprimeDossierİnstall uninstallQT updatejson
set twitter_files=main main_x_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 supprimBon supprimeDossierİnstall uninstallQT updatejson
set youtube_files=main main_ytb_robot instances_table home group_manager media_manager utils fb_robot_install demarrageAuto setup sendatajson sendatajson2 supprimBon supprimeDossierİnstall uninstallQT updatejson













REM -------------------------------------------------------
REM Générer les fichiers .qm à partir des fichiers traduits
echo Génération des fichiers .qm...

for %%L in (%languages%) do (
    for %%F in (%ui_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/ui/%%F_translated.ts -qm resources/lang/%%L/ui/%%F_translated.qm
    )
    for %%F in (%module_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/modules/%%F_translated.ts -qm resources/lang/%%L/modules/%%F_translated.qm
    )
    for %%F in (%adspro_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/adspro/%%F_translated.ts -qm resources/lang/%%L/adspro/%%F_translated.qm
    )
    for %%F in (%blog_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/blogpro/%%F_translated.ts -qm resources/lang/%%L/blogpro/%%F_translated.qm
    )
    for %%F in (%branding_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/branding_files/%%F_translated.ts -qm resources/lang/%%L/branding_files/%%F_translated.qm
    )
    for %%F in (%chatBot_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/chatBotpro/%%F_translated.ts -qm resources/lang/%%L/chatBotpro/%%F_translated.qm
    )
    for %%F in (%emailing_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/emailingpro/%%F_translated.ts -qm resources/lang/%%L/emailingpro/%%F_translated.qm
    )
    for %%F in (%instagram_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/instagrampro/%%F_translated.ts -qm resources/lang/%%L/instagrampro/%%F_translated.qm
    )
    for %%F in (%linkeding_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/linkedingpro/%%F_translated.ts -qm resources/lang/%%L/linkedingpro/%%F_translated.qm
    )
    for %%F in (%pinterest_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/pinterestpro/%%F_translated.ts -qm resources/lang/%%L/pinterestpro/%%F_translated.qm
    )
    for %%F in (%reddit_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/redditpro/%%F_translated.ts -qm resources/lang/%%L/redditpro/%%F_translated.qm
    )
    for %%F in (%snapchat_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/snapchatpro/%%F_translated.ts -qm resources/lang/%%L/snapchatpro/%%F_translated.qm
    )
    for %%F in (%tiktok_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/tiktokpro/%%F_translated.ts -qm resources/lang/%%L/tiktokpro/%%F_translated.qm
    )
    for %%F in (%twitter_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/twitterpro/%%F_translated.ts -qm resources/lang/%%L/twitterpro/%%F_translated.qm
    )
    for %%F in (%whatssap_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/whatssappro/%%F_translated.ts -qm resources/lang/%%L/whatssappro/%%F_translated.qm
    )
    for %%F in (%youtube_files%) do (
        lrelease resources/langtstranslatedtoHuman/%%L/youtubepro/%%F_translated.ts -qm resources/lang/%%L/youtubepro/%%F_translated.qm
    )
)

echo Toutes les traductions sont terminées avec succès!
pause
