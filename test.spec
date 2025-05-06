# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

# Collecte automatique des fichiers de traduction QtWebEngine
qtwebengine_locales = collect_data_files('PyQt5', subdir='Qt5/translations/qtwebengine_locales', include_py_files=False)

a = Analysis(
    ['main.py'],
    pathex=['.'],  # Répertoire local
    binaries=[],  # Aucun DLL manuel
    datas=[
        ('resources/icons/*.ico', 'resources/icons'),
        ('resources/icons/*.png', 'resources/icons'),
        ('resources/data/*.json', 'resources/data'),
        ('resources/images/*', 'resources/images'),
        ('resources/videos/*', 'resources/videos'),
        ('resources/sounds/*', 'resources/sounds'),
        ('resources/gifs/*', 'resources/gifs'),
        ('resources/lang/*', 'resources/lang'),
    ] + qtwebengine_locales,  # Ajout Qt locales
    hiddenimports=[
        'sip',
        'PyQt5.QtWebEngineWidgets',
        'ssl',
        'pymysql',
        'psycopg2',
        'email.mime.multipart',
        'email.mime.text',
        'email.mime.base',
        'email.encoders'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Supprime les symboles de debug pour alléger
    upx=True,    # Compression UPX
    upx_exclude=[],
    console=False,  # Fenêtre GUI uniquement
    icon='resources/icons/robot-icons-30504-Windows.ico',
    distpath='dist',    # Dossier de sortie
    workpath='build',   # Dossier temporaire
    onefile=True        # Tout dans un seul .exe
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
