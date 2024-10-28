git rm -r --cached .
git add .
git commit -m "Nettoyage du cache"



project/
│
├── main.py              # Point d'entrée principal de l'application
├── media_manager.py      # Gestion des médias (classes et fonctions relatives aux médias)
├── group_manager.py      # Gestion des groupes (classes et fonctions relatives aux groupes)
├── update_media_dialog.py # Fenêtre de modification des médias
├── utils.py              # Fonctions utilitaires (chargement de fichiers, JSON)
├── resources/            # Ressources supplémentaires (icônes, images, etc.)
└── README.md             # Fichier d'instructions pour l'installation et l'utilisation


project_root/
│
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py             # Configuration de la base de données
│   │   ├── user.py             # Modèle User
│   │   ├── instance.py         # Modèle Instance
│   │   ├── license.py          # Modèle License
│   │   ├── media.py            # Modèle Media
│   │   ├── group.py            # Modèle Group
│   │   ├── facebook_user.py     # Modèle FacebookUser
│   │   ├── alert.py            # Modèle Alert
│   │   ├── audit_log.py        # Modèle AuditLog
│   │   ├── quota.py            # Modèle Quota
│   │   ├── backup_log.py       # Modèle BackupLog
│   │   ├── user_role.py        # Modèle UserRole
│   │   ├── email_session.py     # Modèle EmailSession
│   │   ├── user_session.py      # Modèle UserSession
│   │   ├── contact.py          # Modèle Contact
│   │   ├── instance_user.py     # Modèle InstanceUser
│   │   └── group_user.py        # Modèle GroupUser
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── user_controller.py   # Contrôleur pour User
│   │   ├── instance_controller.py # Contrôleur pour Instance
│   │   ├── license_controller.py # Contrôleur pour License
│   │   ├── media_controller.py   # Contrôleur pour Media
│   │   ├── group_controller.py   # Contrôleur pour Group
│   │   ├── facebook_user_controller.py # Contrôleur pour FacebookUser
│   │   ├── alert_controller.py   # Contrôleur pour Alert
│   │   ├── audit_log_controller.py # Contrôleur pour AuditLog
│   │   ├── quota_controller.py   # Contrôleur pour Quota
│   │   ├── backup_log_controller.py # Contrôleur pour BackupLog
│   │   ├── user_role_controller.py # Contrôleur pour UserRole
│   │   ├── email_session_controller.py # Contrôleur pour EmailSession
│   │   ├── user_session_controller.py # Contrôleur pour UserSession
│   │   ├── contact_controller.py  # Contrôleur pour Contact
│   │   ├── instance_user_controller.py # Contrôleur pour InstanceUser
│   │   └── group_user_controller.py # Contrôleur pour GroupUser
│   │
│   ├── views/
│   │   ├── __init__.py
│   │   ├── user_view.py          # Vue pour User
│   │   ├── instance_view.py      # Vue pour Instance
│   │   ├── license_view.py       # Vue pour License
│   │   ├── media_view.py         # Vue pour Media
│   │   ├── group_view.py         # Vue pour Group
│   │   ├── facebook_user_view.py  # Vue pour FacebookUser
│   │   ├── alert_view.py         # Vue pour Alert
│   │   ├── audit_log_view.py     # Vue pour AuditLog
│   │   ├── quota_view.py         # Vue pour Quota
│   │   ├── backup_log_view.py    # Vue pour BackupLog
│   │   ├── user_role_view.py     # Vue pour UserRole
│   │   ├── email_session_view.py  # Vue pour EmailSession
│   │   ├── user_session_view.py   # Vue pour UserSession
│   │   ├── contact_view.py       # Vue pour Contact
│   │   ├── instance_user_view.py  # Vue pour InstanceUser
│   │   └── group_user_view.py     # Vue pour GroupUser
│   │
│   ├── templates/
│   │   ├── user_template.html      # Modèle HTML pour User
│   │   ├── instance_template.html   # Modèle HTML pour Instance
│   │   ├── license_template.html    # Modèle HTML pour License
│   │   ├── media_template.html      # Modèle HTML pour Media
│   │   ├── group_template.html      # Modèle HTML pour Group
│   │   ├── facebook_user_template.html # Modèle HTML pour FacebookUser
│   │   ├── alert_template.html      # Modèle HTML pour Alert
│   │   ├── audit_log_template.html  # Modèle HTML pour AuditLog
│   │   ├── quota_template.html      # Modèle HTML pour Quota
│   │   ├── backup_log_template.html # Modèle HTML pour BackupLog
│   │   ├── user_role_template.html  # Modèle HTML pour UserRole
│   │   ├── email_session_template.html # Modèle HTML pour EmailSession
│   │   ├── user_session_template.html # Modèle HTML pour UserSession
│   │   ├── contact_template.html    # Modèle HTML pour Contact
│   │   ├── instance_user_template.html # Modèle HTML pour InstanceUser
│   │   └── group_user_template.html  # Modèle HTML pour GroupUser
│   │
│   ├── config.py                  # Configuration de l'application
│   └── main.py                    # Point d'entrée de l'application
│
└── requirements.txt               # Dépendances de l'application




pyinstaller --onefile --windowed --noconsole --icon=resources/icons/robot-512.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" main.py
conda install lzma

conda install bzip2
conda install openssl
pyinstaller --noconsole main.spec


 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/diving-png-4436-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/system.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/Creative-Freedom-Shimmer-Folder-New.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/createFolder.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/Creative-Freedom-Shimmer-Folder-New.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/dossiers.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/instagram-icon-956-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/copieMediaDemo.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/instagram-icon-956-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/majenv.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/robot-icons-30504-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/geninfo.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/house-key-icon-41543-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/generedemolicence.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/house-key-icon-41543-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/updatejson.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/information-icon-6055-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/Visibleinstance.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/information-icon-6055-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/verificateur.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/facebook-icon-png-770-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/cletobureau.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/facebook-icon-png-770-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin"  installFBrobotPy/demarrageAuto.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/pink-message-icon-12045-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/sendlog.py

 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/android-icon-3083-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/invisibleinstance.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/android-icon-3083-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/affiheMessage.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/android-icon-3083-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/mailSucces.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/android-icon-3083-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/invisibleinstance.py
 pyinstaller --onefile --windowed --noconsole --icon=resources/icons/android-icon-3083-Windows.ico --add-data "resources/*;resources" --paths "C:\Users\ibrahim\anaconda3\Library\bin" installFBrobotPy/secureChrome.py

Translate module Fbk robot
Translate to Tr 
 
genere files ts for ui forler 

pylupdate5  ui/carousel.py  -ts lang/tr_TR/ui/carousel.ts
pylupdate5 ui/feature_buttons.py  -ts lang/tr_TR/ui/feature_buttons.ts
pylupdate5 ui/footer.py  -ts lang/tr_TR/ui/footer.ts
pylupdate5 ui/header.py -ts lang/tr_TR/ui/header.ts
pylupdate5 ui/login.py  -ts lang/tr_TR/ui/login.ts
pylupdate5 ui/register.py -ts lang/tr_TR/ui/register.ts
pylupdate5 ui/secondry_menu.py -ts lang/tr_TR/ui/secondry_menu.ts
pylupdate5 ui/side_menu.py -ts lang/tr_TR/ui/side_menu.ts
pylupdate5 ui/toggle_menu.py -ts lang/tr_TR/ui/toggle_menu.ts



generer qm for ui 

lrelease lang/tr_TR/ui/carousel.ts
lrelease lang/tr_TR/ui/feature_buttons.ts
lrelease lang/tr_TR/ui/footer.ts
lrelease lang/tr_TR/ui/header.ts
lrelease lang/tr_TR/ui/login.ts
lrelease lang/tr_TR/ui/register.ts
lrelease lang/tr_TR/ui/secondry_menu.ts
lrelease lang/tr_TR/ui/side_menu.ts
lrelease lang/tr_TR/ui/toggle_menu.ts

generate ts for Modules  

pylupdate5 main.py -ts lang/tr_TR/modules/main.ts
pylupdate5 main_fb_robot.py -ts lang/tr_TR/modules/main_fb_robot.ts
pylupdate5 instances_table.py -ts lang/tr_TR/modules/instances_tables.ts
pylupdate5 home.py -ts lang/tr_TR/modules/home.ts
pylupdate5 group_manager.py -ts lang/tr_TR/modules/group_manager.ts
pylupdate5 media_manager.py -ts lang/tr_TR/modules/media_manager.ts
pylupdate5 utils.py -ts lang/tr_TR/modules/utils.ts
pylupdate5 fb_robot_install.py -ts lang/tr_TR/modules/fb_robot_install.ts

generete qm for modules 

lrelease lang/tr_TR/modules/main.ts
lrelease lang/tr_TR/modules/main_fb_robot.ts
lrelease lang/tr_TR/modules/instances_tables.ts
lrelease lang/tr_TR/modules/home.ts
lrelease lang/tr_TR/modules/group_manager.ts
lrelease lang/tr_TR/modules/media_manager.ts
lrelease lang/tr_TR/modules/utils.ts
lrelease lang/tr_TR/modules/fb_robot_install.ts


translate to En 


Translate to Ar 

pylupdate5 main.py -ts lang/tr_TRanslations_fr.ts


setx PATH "%PATH%;C:\Users\ibrahim\anaconda3\Lib\site-packages\PyQt5\Qt5\bin" /M

OpenSSH\;C:\Program Files\Microsoft SQL Server\150\Tools\Binn\;C:\Program Files\Git\cmd;C:\Program Files (x86)\Incredibuild;C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;C:\Program Files\NVIDIA Corporation\NVIDIA NvDLISR;C:\Program Files\Docker\Docker\resources\bin;C:\Users\ibrahim\anaconda3\Scripts\;C:\Users\ibrahim\anaconda3\;D:\xampp\php;C:\ProgramData\ComposerSetup\bin;C:\Program Files\dotnet\;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Windows\System32\OpenSSH\;C:\Program Files\Microsoft SQL Server\150\Tools\Binn\;C:\Program Files\Git\cmd;C:\Program Files (x86)\Incredibuild;C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;C:\Program Files\NVIDIA Corporation\NVIDIA NvDLISR;C:\Program Files\Docker\Docker\resources\bin;C:\Users\ibrahim\anaconda3\Scripts\;C:\Users\ibrahim\anaconda3\;D:\xampp\php;C:\ProgramData\ComposerSetup\bin;C:\Program Files\dotnet\;C:\Users\ibrahim\AppData\Local\Programs\Python\Python313\Scripts\;C:\Users\ibrahim\AppData\Local\Programs\Python\Python313\;C:\Users\ibrahim\AppData\Local\Microsoft\WindowsApps;;C:\Program Files\JetBrains\PyCharm 2023.3.3\bin;;C:\Users\ibrahim\AppData\Local\Programs\Microsoft VS Code\bin;C:\Users\ibrahim\AppData\Local\Microsoft\WinGet\Packages\Schniz.fnm_Microsoft.Winget.Source_8wekyb3d8bbwe;C:\Users\ibrahim\AppData\Roaming\Composer\vendor\bin;C:\Users\ibrahim\.dotnet\tools;C:\Users\ibrahi



database 
factory 
 python -m models.factory.factoryfbrobot   
 python models/database/databasefbrobot.py 

 python models/database/databasefbrobot.py 


