# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

qtwebengine_locales = collect_data_files(
    'PyQt5',
    subdir='Qt5/translations/qtwebengine_locales',
    include_py_files=False
)

a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\ibrahim\\anaconda3\\Library\\bin', 'C:\\Users\\ibrahim\\Downloads\\Robot_Labo_Pro\\lang'],
    binaries=[],
    datas=[
        ('resources/icons/*.png', 'resources/icons'),
        ('resources/data/*.json', 'resources/data'),
        ('resources/lang/*', 'resources/lang'),
    ],
    hiddenimports=['sip', 'ssl', 'PyQt5.QtWebEngineWidgets', 'cryptography'],
    hookspath=[],
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
    strip=False,
    upx=True,
    console=False,
    icon='resources/appico/512.icns',  # Icône macOS


    distpath='D:/Installations/Nova360',  # Dossier de sortie
    workpath='D:/Installations/Nova360/build',  # Dossier de travail
    onefile=True  # Active l'option --onefile
)

