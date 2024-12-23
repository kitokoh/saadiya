# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['telecommande.py'],  # Remplacez par le nom de votre fichier principal
    pathex=['.'],  # Chemin vers votre script
    binaries=[],
    datas=[
        ('icons/*', 'icons'),  # Ajoutez vos ressources ici (par ex. icônes, gifs)
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Telecommande',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Changez à True pour garder la console (mode débogage)
    icon='../resources/icons/robot-icons-30497-Windows.ico',  # Remplacez par le chemin vers votre icône
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Telecommande',
)
