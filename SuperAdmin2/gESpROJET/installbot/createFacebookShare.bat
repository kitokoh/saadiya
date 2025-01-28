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

@echo off
cd /d C:\bons\Thefbkgrupshare
call git clone https://github.com/darideveloper/facebook-groups-post-bot antBot
cd /d C:\bons\Thefbkgrupshare\antBot
call python -m pip install -r requirements.txt 
call python -m venv antBotEnv
call copy C:\bons\Thefbkgrupshare\antbot\sample.env C:\bons\Thefbkgrupshare\antBot\.env
call copy C:\bons\Thefbkgrupshare\antbot\data-python.json C:\bons\Thefbkgrupshare\antBot\data.json

::call copy C:\bons\gESpROJET\bots\marketingBot\doorShareBot.bat C:\bons\gESpROJET\bots\marketingBot\antBotShare.bat
::call copy C:\bons\gESpROJET\bots\saveGroup\doorShareBot.bat C:\bons\gESpROJET\bots\saveGroup\antBotGrp.bat

cd /d C:\bons\fbkGrupimages
call mkdir antBot


cd /d C:\bons\Thefbkgrupshare\antBot\Scripts
call activate
cd /d C:\bons\Thefbkgrupshare\antBot
 python __save_groups__.py
pause
@echo off    
:: cmd /k "cd /d C:\Users\ibrahim\Downloads\system\botfork"



 :: #         f   f
:: cmd /k "cd /d C:\FFmpeg"
timeout 10




PAUSE
