# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main_fb_robot.py'],
    pathex=['C:\\Users\\ibrahim\\anaconda3\\Library\\bin'],  # inclut le chemin des DLLs manquantes
    binaries=[
        ('C:\\Users\\ibrahim\\anaconda3\\Library\\bin\\liblzma.dll', '.'),
        ('C:\\Users\\ibrahim\\anaconda3\\Library\\bin\\LIBBZ2.dll', '.'),
        ('C:\\Users\\ibrahim\\anaconda3\\Library\\bin\\libssl-3-x64.dll', '.'),
        ('C:\\Users\\ibrahim\\anaconda3\\Library\\bin\\libcrypto-3-x64.dll', '.')
    ],
    datas=[
        ('resources/icons/*.ico', 'resources/icons'),  # inclut tous les fichiers .ico
        ('resources/icons/*.png', 'resources/icons'),  # inclut tous les fichiers .png
        ('resources/data/*.json', 'resources/data'),  # inclut tous les fichiers JSON
        ('resources/images/*', 'resources/images'),  # inclut tous les fichiers dans le dossier images
        ('resources/videos/*', 'resources/videos'),  # inclut tous les fichiers dans le dossier videos
    ],
    hiddenimports=[],
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
    name='main_fb_robot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Mettre à True si tu veux voir les messages dans la console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icons/robot-512.ico',  # utilise l'icône principale par défaut
)
