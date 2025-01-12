# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

# Collect qtwebengine locale files
qtwebengine_locales = collect_data_files(
    'PyQt5',
    subdir='Qt5/translations/qtwebengine_locales',
    include_py_files=False
)
a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\cheic\\anaconda3\\Library\\bin', 'D:\\nova360\\lang'],
    
    binaries=[
        ('C:\\Users\\cheic\\anaconda3\\Library\\bin\\liblzma.dll', '.'),
        ('C:\\Users\\cheic\\anaconda3\\Library\\bin\\LIBBZ2.dll', '.'),
        ('C:\\Users\\cheic\\anaconda3\\Library\\bin\\libssl-3-x64.dll', '.'),
        ('C:/Users/cheic/anaconda3/Lib/site-packages/PyQt5/Qt5/bin/*.dll', '.'),
        ('C:\\Users\\cheic\\anaconda3\\Library\\bin\\libcrypto-3-x64.dll', '.')
    ],
    datas=[
        ('resources/icons/*.ico', 'resources/icons'),
        ('resources/icons/*.png', 'resources/icons'),
        ('resources/data/*.json', 'resources/data'),
        ('resources/images/*', 'resources/images'),
        ('resources/videos/*', 'resources/videos'),
        ('D:\\nova360\\Installations\\lesClesNova360\\icons\\exeCle\\*', 'resources/tools'),
        ('resources/sounds/*', 'resources/sounds'),
        ('resources/gifs/*', 'resources/gifs'),

         ('resources/*.key', 'resources'),

         ('resources/lang/*', 'resources/lang')

    ],

    hiddenimports=['sip', 
    'pymysql',  # Add pymysql if you're using it
    'pysqlite2',  # Add if you're using pysqlite2
    'MySQLdb',    # Add if you're using MySQLdb
    'psycopg2',   # Add if you're using psycopg2
    'ssl','PyQt5.QtWebEngineWidgets', 'cryptography', 'smtplib', 'email.mime.multipart', 'email.mime.text', 'email.mime.base', 'email.encoders'],


    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # False si vous ne voulez pas de console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icons/robot-icons-30504-Windows.ico',  # Vérifiez le chemin d'accès à l'icône
    distpath='D:/Installations/Nova360',  # Dossier de sortie
    workpath='D:/Installations/Nova360/build',  # Dossier de travail
    onefile=True  # Active l'option --onefile

)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='collect'
)
