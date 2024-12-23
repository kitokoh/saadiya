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
    pathex=['/Users/ibrahim/Downloads/Robot_Labo_Pro/lang'],
    binaries=[],
    datas=[
        ('resources/icons/*.png', 'resources/icons'),
        ('resources/data/*.json', 'resources/data'),
        ('resources/images/*', 'resources/images'),
        ('resources/videos/*', 'resources/videos'),
        ('resources/tools/*', 'resources/tools'),
        ('resources/sounds/*', 'resources/sounds'),
        ('resources/lang/*', 'resources/lang')
    ],
    hiddenimports=['sip', 'ssl', 'PyQt5.QtWebEngineWidgets', 'cryptography', 'smtplib'],
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
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity="Your Mac Developer ID",  # Optional: macOS code signing
    entitlements_file=None,
    icon='resources/icons/robot-icons-mac.icns',  # Use a macOS-compatible .icns file
    distpath='D:/Installations/Nova360',  # Dossier de sortie
    workpath='D:/Installations/Nova360/build',  # Dossier de travail
    onefile=True  # Active l'option --onefile
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,
    upx=True,
    name='collect'
)
