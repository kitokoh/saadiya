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
call git clone https://github.com/iamtalhaasghar/alright whatsready1
cd /d D:\bons\Thefbkgrupshare\whatsready1
call python -m venv whatsready1Env
cd /d D:\bons\Thefbkgrupshare\whatsready1\whatsready1Env\Scripts
call activate

cd /d D:\bons\Thefbkgrupshare\whatsready1


call python setup.py install 

call copy d:\bons\Thefbkgrupshare\shareFarmoos\.env d:\bons\Thefbkgrupshare\whatsready1\.env
call copy d:\bons\Thefbkgrupshare\shareFarmoos\data.json d:\bons\Thefbkgrupshare\whatsready1\data.json

call copy d:\bons\gESpROJET\bots\marketingBot\doorShareBot.bat d:\bons\gESpROJET\bots\marketingBot\whatsready1Share.bat
call copy d:\bons\gESpROJET\bots\saveGroup\doorShareBot.bat d:\bons\gESpROJET\bots\saveGroup\whatsready1Grp.bat

cd /d D:\bons\fbkGrupimages
call mkdir whatsready1


cd /d D:\bons\Thefbkgrupshare\whatsready1\whatsready1Env\Scripts
call activate
cd /d D:\bons\Thefbkgrupshare\whatsready1
 python example.py
pause
@echo off    
:: cmd /k "cd /d C:\Users\ibrahim\Downloads\system\botfork"



 :: #         f   f
:: cmd /k "cd /d D:\FFmpeg"
timeout 10




PAUSE
