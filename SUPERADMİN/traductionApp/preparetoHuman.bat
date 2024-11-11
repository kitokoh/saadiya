@echo off
set src="C:\Users\ibrahim\Downloads\Robot_Labo_Pro\lang\resources\langtstranslated"
set dest="C:\Users\ibrahim\Downloads\Robot_Labo_Pro\lang\resources\langtstranslatedtoHuman"

echo Copying files from %src% to %dest%...
xcopy %src% %dest% /E /H /C /I

echo Copy complete.
pause
