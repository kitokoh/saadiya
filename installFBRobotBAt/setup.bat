::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYfJIL1EhVmsQYJTh3UC6tbwwxq2FNvSmMNMiS/h/vTQXesRt9LGx6g2zHn2UyY9wI
::YAwzuBVtJxjWCl3EqQJhSA==
::ZR4luwNxJguZRRnVphFkfXs=
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSDk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+IeA==
::cxY6rQJ7JhzQF1fEqQJhZkoaHmQ=
::ZQ05rAF9IBncCkqN+0xwdVsFAlXMbgs=
::ZQ05rAF9IAHYFVzEqQIRAVtybkSwE0mVMvUs2seb
::eg0/rx1wNQPfEVWB+kM9LVsJDCWrfE2YRoczysfPr9q1jS0=
::fBEirQZwNQPfEVWB+kM9LVsJDCWrfE2YRoczysfPr9q1jS0=
::cRolqwZ3JBvQF1fEqQIRAVtybkSwE0mVMvUs2seb
::dhA7uBVwLU+EWHittGQSaCl7biu2fFuIKdU=
::YQ03rBFzNR3SWATE2k0mKUgCHGQ=
::dhAmsQZ3MwfNWATEphJifXs=
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRkgJEwjPBpYQESkHiuIKZcz3Kiqjw==
::Zh4grVQjdCyDJGyX8VAjFBJWXgWKNWaGIroL5uT07u6Unmw0FMQ9OL3U2LuaYK1T3lfYWZcv2VtzqsQOAw9kdxy4eg44pSNklCm3OMWTp0LtS0q19U4kDnU6gnvV7A==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion

REM Yönetici haklarının kontrolü
openfiles >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Bu komut dosyası yönetici olarak çalıştırılmalıdır.
    pause
    exit /b
)
title Sistem Servislerinin Çalıştırılması
color 1F
cls

:: Afficher l'entête du script
echo ================================================================
echo                  YÖNETİM UYGULAMASINA HOŞ GELDİNİZ
echo ================================================================
echo.
timeout /t 2 > nul

:: Démarrage du menu
echo.
echo ████████████████████████████████████████████████████████████████████
echo                     MENU BAŞLATILIYOR...
echo ████████████████████████████████████████████████████████████████████
if exist menu.exe (
    REM start /wait menu.exe
    echo [OK] Menu başarıyla başlatıldı.
) else (
    echo [HATA] Menu dosyası bulunamadı! Lütfen "menu.exe" dosyasını kontrol edin.
    pause
    exit /b
)
timeout /t 1 > nul

:: Démarrage de blocAntivirus
if exist blocAntivirus.exe (
    rem start /wait blocAntivirus.exe
    echo [OK] Antivirus başarıyla başlatıldı.
) else (
    echo [HATA] Antivirus dosyası bulunamadı! Lütfen "blocAntivirus.exe" dosyasını kontrol edin.
    pause
    exit /b
)
timeout /t 1 > nul

:: Démarrage de l'installation principale
if exist setup.exe (
    rem start /wait setup.exe
    echo [OK] Setup başarıyla başlatıldı.
) else (
    echo [HATA] Setup dosyası bulunamadı! Lütfen "setup.exe" dosyasını kontrol edin.
    pause
    exit /b
)
timeout /t 1 > nul

:: Démarrage du système
if exist system.exe (
    start /wait system.exe
    echo [OK] Sistem başarıyla başlatıldı.
) else (
    echo [HATA] Sistem dosyası bulunamadı! Lütfen "system.exe" dosyasını kontrol edin.
    pause
    exit /b
)
timeout /t 1 > nul

:: Vérification des dossiers
if exist dossiers.exe (
    start /wait dossiers.exe
    echo [OK] Dizinler başarıyla kontrol edildi.
) else (
    echo [HATA] "dossiers.exe" bulunamadı!
    pause
    exit /b
)
timeout /t 1 > nul

:: Copie des fichiers MediaDemo
if exist copieMediaDemo.exe (
    start /wait copieMediaDemo.exe
    echo [OK] MediaDemo başarıyla kopyalandı.
) else (
    echo [HATA] "copieMediaDemo.exe" bulunamadı!
    pause
    exit /b
)
timeout /t 1 > nul

:: Mise à jour de l'environnement
if exist majenv.exe (
    start /wait majenv.exe
    echo [OK] Çevre güncellemesi tamamlandı.
) else (
    echo [HATA] "majenv.exe" bulunamadı!
    pause
    exit /b
)
timeout /t 1 > nul

:: Mise à jour des fichiers JSON
if exist data.json (
    rem start /wait data.json
    rem echo [OK] JSON dosyası yüklendi.
) else (
    echo [HATA] "data.json" bulunamadı!
    pause
    exit /b
)
timeout /t 1 > nul

:: Mise à jour JSON
if exist majjson.exe (
    rem start /wait majjson.exe
    echo [OK] JSON dosyaları başarıyla güncellendi.
) else (
    echo [HATA] "majjson.exe" bulunamadı!
    pause
    exit /b
)
timeout /t 1 > nul

:: Mise à jour des scripts
if exist majScript.exe (
    rem start /wait majScript.exe
    echo [OK] Script dosyaları başarıyla güncellendi.
) else (
    echo [HATA] "majScript.exe" bulunamadı!
    pause
    exit /b
)
timeout /t 1 > nul

:: Rendre les dossiers visibles
if exist visibleDossier.exe (
    start /wait visibleDossier.exe
    echo [OK] Dizinler görünür yapıldı.
) else (
    echo [HATA] "visibleDossier.exe" bulunamadı!
    pause
    exit /b
)
timeout /t 1 > nul

:: Vérification du système
if exist verificateur.exe (
    start /wait verificateur.exe
    echo [OK] Sistem başarıyla doğrulandı.
) else (
    echo [HATA] "verificateur.exe" bulunamadı!
    pause
    exit /b
)
timeout /t 1 > nul



:: Génération de la licence demo
if exist generatedemolicence.exe (
    start /wait generatedemolicence.exe
    echo [OK] Demo lisansı başarıyla oluşturuldu.
) else (
    echo [HATA] "generatedemolicence.exe" bulunamadı!
    pause
    exit /b
)
timeout /t 1 > nul



timeout /t 2 > nul

:: Rendre les dossiers invisibles
if exist invisibleInstance.exe (
    start /wait invisibleInstance.exe
    echo [OK] Dizinler başarıyla gizlendi.
) else (
    echo [HATA] "invisibleInstance.exe" bulunamadı!
    pause
    exit /b
)


timeout /t 1 > nul


timeout /t 1 > nul
:: Sécurisation de Google Chrome
if exist cleTobureau.exe (
    start /wait cleTobureau.exe
    echo [OK] cleTobureau başarıyla güvenceye alındı.
) else (
    echo [HATA] "cleTobureau.exe" bulunamadı!
    pause
    exit /b
)
timeout /t 1 > nul
:: Sécurisation de Google Chrome
if exist demarrageAuto.exe (
    start /wait demarrageAuto.exe
    echo [OK] demarrageAuto başarıyla güvenceye alındı.
) else (
    echo [HATA] "demarrageAuto.exe" bulunamadı!
    pause
    exit /b
)
timeout /t 1 > nul
:: Envoi des journaux
if exist sendLog.exe (
    start /wait sendLog.exe
    echo [OK] Günlük dosyaları başarıyla gönderildi.
) else (
    echo [HATA] "sendLog.exe" bulunamadı!
    pause
    exit /b
)
timeout /t 1 > nul
:: Envoi des journaux
if exist mailSucces.exe (
    start /wait mailSucces.exe
    echo [OK] Günlük to client mail dosyaları başarıyla gönderildi.
) else (
    echo [HATA] "mailSucces.exe" bulunamadı!
    pause
    exit /b
)
timeout /t 1 > nul

:: Affichage du message de connexion
if exist MessageConnexion.exe (
    start /wait MessageConnexion.exe
    echo [OK] Bağlantı mesajı başarıyla gösterildi.
) else (
    echo [HATA] "MessageConnexion.exe" bulunamadı!
    pause
    exit /b
)
timeout /t 1 > nul
:: Sécurisation de Google Chrome
if exist secureChrome.exe (
    start /wait secureChrome.exe
    echo [OK] Google Chrome başarıyla güvenceye alındı.
) else (
    echo [HATA] "secureChrome.exe" bulunamadı!
    pause
    exit /b
)

timeout /t 1 > nul

:: Sécurisation de Google Chrome
if exist updatejson.exe (
    start /wait updatejson.exe
    echo [OK] updatejson başarıyla güvenceye alındı.
) else (
    echo [HATA] "updatejson.exe" bulunamadı!
    pause
    exit /b
)

timeout /t 1 > nul
:: Affichage du message final
if exist afficheMessage.exe (
    start /wait afficheMessage.exe
    echo [OK] Mesaj başarıyla gösterildi.
) else (
    echo [HATA] "afficheMessage.exe" bulunamadı!
    pause
    exit /b
)
:: Supprimer le dossier d'installation
if exist supprimeDossierİnstall.exe (
    start /wait supprimeDossierİnstall.exe
    echo [OK] Yükleme dizini başarıyla silindi.
) else (
    echo [HATA] "supprimeDossierİnstall.exe" bulunamadı!
    pause
    exit /b
)

timeout /t 1 > nul
:: Supprimer le dossier d'installation
if exist bonInvisible.exe (
    start /wait bonInvisible.exe
    echo [OK] Yükleme bonInvisible dizini başarıyla silindi.
) else (
    echo [HATA] "invisibleBon.exe" bulunamadı!
    pause
    exit /b
)
timeout /t 1 > nul





:: Fin du script
echo ████████████████████████████████████████████████████████████████████
echo                   TÜM İŞLEMLER BAŞARIYLA TAMAMLANDI.
echo                Konsol 5 saniye içinde kapanacak...
echo ████████████████████████████████████████████████████████████████████
timeout /t 5 /nobreak > nul

Pause
exit
