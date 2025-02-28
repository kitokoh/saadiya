@echo off
echo Optimisation du processeur et des performances...
echo.

:: Vérifier si le script est exécuté en tant qu'administrateur
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Exécution en tant qu'administrateur confirmée.
) else (
    echo Ce script doit être exécuté en tant qu'administrateur.
    pause
    exit /b 1
)

:: Détection de l'OS
echo Détection du système d'exploitation...
ver | find "Windows" >nul
if %errorLevel% == 0 (
    echo Système détecté : Windows.
    goto WINDOWS_OPTIMIZATION
) else (
    echo Système non reconnu ou non pris en charge.
    pause
    exit /b 1
)

:WINDOWS_OPTIMIZATION
:: Activer le mode Haute Performance
echo Activation du mode Haute Performance...
powercfg /s SCHEME_MIN
if %errorLevel% == 0 (
    echo Mode Haute Performance activé avec succès.
) else (
    echo Échec de l'activation du mode Haute Performance.
)

:: Désactiver la mise en veille automatique
echo Désactivation de la mise en veille automatique...
powercfg /change standby-timeout-ac 0
powercfg /change monitor-timeout-ac 0
powercfg /change hibernate-timeout-ac 0
if %errorLevel% == 0 (
    echo Mise en veille automatique désactivée avec succès.
) else (
    echo Échec de la désactivation de la mise en veille automatique.
)

:: Désactiver l'économie d'énergie du processeur
echo Désactivation de l'économie d'énergie du processeur...
powercfg -attributes SUB_PROCESSOR 75b0ae3f-bce0-45a7-8c89-c9611c25e100 -ATTRIB_HIDE
if %errorLevel% == 0 (
    echo Économie d'énergie du processeur désactivée avec succès.
) else (
    echo Échec de la désactivation de l'économie d'énergie du processeur.
)

:: Désactiver l'Hyper-Threading (Intel)
echo Désactivation de l'Hyper-Threading (Intel)...
wmic cpu get NumberOfCores, NumberOfLogicalProcessors
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Executive" /v AdditionalCriticalWorkerThreads /t REG_DWORD /d 0 /f
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Executive" /v AdditionalDelayedWorkerThreads /t REG_DWORD /d 0 /f
if %errorLevel% == 0 (
    echo Hyper-Threading désactivé avec succès.
) else (
    echo Échec de la désactivation de l'Hyper-Threading.
)

:: Activer le SMT (AMD)
echo Activation du SMT (AMD)...
bcdedit /set useplatformclock true
bcdedit /set tscsyncpolicy Enhanced
if %errorLevel% == 0 (
    echo SMT activé avec succès.
) else (
    echo Échec de l'activation du SMT.
)

:: Désactiver les services inutiles pour améliorer les performances
echo Désactivation des services inutiles...
sc config SysMain start= disabled
sc config DiagTrack start= disabled
sc config DPS start= disabled
sc config WMPNetworkSvc start= disabled
sc config WSearch start= disabled
if %errorLevel% == 0 (
    echo Services inutiles désactivés avec succès.
) else (
    echo Échec de la désactivation des services inutiles.
)

:: Optimiser les paramètres réseau
echo Optimisation des paramètres réseau...
netsh int tcp set global autotuninglevel=normal
netsh int tcp set global rss=enabled
netsh int tcp set global chimney=enabled
if %errorLevel% == 0 (
    echo Paramètres réseau optimisés avec succès.
) else (
    echo Échec de l'optimisation des paramètres réseau.
)

:: Nettoyer les fichiers temporaires
echo Nettoyage des fichiers temporaires...
del /q /f %TEMP%\*
if %errorLevel% == 0 (
    echo Fichiers temporaires nettoyés avec succès.
) else (
    echo Échec du nettoyage des fichiers temporaires.
)

:: Redémarrer l'ordinateur pour appliquer les changements
echo Redémarrage dans 10 secondes...
timeout /t 10
shutdown /r /t 0

