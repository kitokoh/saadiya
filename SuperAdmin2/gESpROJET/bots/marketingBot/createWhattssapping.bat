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
cd /d D:\bons\Thefbkgrupshare
call git clone https://github.com/SaeidJavadi/Advanced-WhatsApp-Sender whattsBot
cd /d D:\bons\Thefbkgrupshare\whattsBot
call python -m venv whattsBotEnv
cd /d D:\bons\Thefbkgrupshare\whattsBot\whattsBotEnv\Scripts
call activate

cd /d D:\bons\Thefbkgrupshare\whattsBot


call python -m pip install -r requirements.txt 

call copy d:\bons\Thefbkgrupshare\shareFarmoos\.env d:\bons\Thefbkgrupshare\whattsBot\.env
call copy d:\bons\Thefbkgrupshare\shareFarmoos\data.json d:\bons\Thefbkgrupshare\whattsBot\data.json

call copy d:\bons\gESpROJET\bots\marketingBot\doorShareBot.bat d:\bons\gESpROJET\bots\marketingBot\whattsBotShare.bat
call copy d:\bons\gESpROJET\bots\saveGroup\doorShareBot.bat d:\bons\gESpROJET\bots\saveGroup\whattsBotGrp.bat

cd /d D:\bons\fbkGrupimages
call mkdir whattsBot


cd /d D:\bons\Thefbkgrupshare\whattsBot\Scripts
call activate
cd /d D:\bons\Thefbkgrupshare\whattsBot
 python __save_groups__.py
pause
@echo off    
:: cmd /k "cd /d C:\Users\ibrahim\Downloads\system\botfork"



 :: #         f   f
:: cmd /k "cd /d D:\FFmpeg"
timeout 10




PAUSE
