@echo off

:: Chemin de l'environnement virtuel
set VENV_PATH=C:\Users\ibrahim\Downloads\Robot_Labo_Pro\lang\env\Scripts\activate
:: Chemin du répertoire à utiliser pour exécuter les commandes
set WORK_DIR=C:\Users\ibrahim\Downloads\Robot_Labo_Pro\lang

:: Activer l'environnement virtuel et exécuter PyInstaller dans des fenêtres séparées
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/diving-png-4436-Windows.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/system.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/Creative-Freedom-Shimmer-Folder-New.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/createFolder.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/Creative-Freedom-Shimmer-Folder-New.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/dossiers.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/instagram-icon-956-Windows.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/copieMediaDemo.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/instagram-icon-956-Windows.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/majenv.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/robot-icons-30504-Windows.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/geninfo.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/house-key-icon-41543-Windows.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/generedemolicence.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/house-key-icon-41543-Windows.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/updatejson.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/information-icon-6055-Windows.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/Visibleinstance.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/information-icon-6055-Windows.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/verificateur.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/facebook-icon-png-770-Windows.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/cletobureau.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/facebook-icon-png-770-Windows.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/demarrageAuto.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/pink-message-icon-12045-Windows.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/sendlog.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/android-icon-3083-Windows.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/invisibleinstance.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/android-icon-3083-Windows.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/affiheMessage.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/android-icon-3083-Windows.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/mailSucces.py"
start cmd /k "call %VENV_PATH% && cd %WORK_DIR% && pyinstaller --onefile --windowed --noconsole --icon=../resources/icons/android-icon-3083-Windows.ico  --paths 'C:\Users\ibrahim\anaconda3\Library\bin'  installFBrobotPy/secureChrome.py"
