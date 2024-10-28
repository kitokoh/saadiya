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
set languages=tr_TR ar_SA en_US pt_BR
set ui_subdirs=ui modules

REM Boucle sur les langues pour créer les répertoires
for %%L in (%languages%) do (
    for %%S in (%ui_subdirs%) do (
        if not exist "%%L\%%S" (
            echo Création du dossier %%L\%%S...
            mkdir resources\lang\%%L\%%S
        )
    )
)

REM -------------------------------------------------------
REM Générer les fichiers .ts pour chaque langue
REM Boucle pour chaque fichier source à traduire
set ui_files=carousel feature_buttons footer header login register secondry_menu side_menu toggle_menu
set module_files=main main_fb_robot instances_table home group_manager media_manager utils fb_robot_install

echo Génération des fichiers .ts pour l'UI...
for %%L in (%languages%) do (
    for %%F in (%ui_files%) do (
        pylupdate5 ui/%%F.py -ts resources/lang/%%L/ui/%%F.ts
    )
)

echo Génération des fichiers .ts pour les modules...
for %%L in (%languages%) do (
    for %%F in (%module_files%) do (
        pylupdate5 %%F.py -ts resources/lang/%%L/modules/%%F.ts
    )
)

REM -------------------------------------------------------
REM Traduire les fichiers .ts avec le script Python
REM Boucle pour chaque fichier généré
echo Traduction des fichiers .ts avec Google Translate...

for %%L in (%languages%) do (
    for %%F in (%ui_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/lang/%%L/ui/%%F.ts lang/%%L/ui/%%F_translated.ts %%L
    )
    for %%F in (%module_files%) do (
        python SUPERADMİN/traductionApp/traducteur.py resources/lang/%%L/modules/%%F.ts lang/%%L/modules/%%F_translated.ts %%L
    )
)
rem python traducteur.py lang/ar_SA/ui/carousel_translated.ts lang/ar_SA/ui/carousel_translated_translated.ts ar

REM -------------------------------------------------------
REM Générer les fichiers .qm à partir des fichiers traduits
echo Génération des fichiers .qm...

for %%L in (%languages%) do (
    for %%F in (%ui_files%) do (
        lrelease resources/lang/%%L/ui/%%F_translated.ts
    )
    for %%F in (%module_files%) do (
        lrelease resources/lang/%%L/modules/%%F_translated.ts
    )
)

echo Toutes les traductions sont terminées avec succès!
pause
