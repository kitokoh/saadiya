# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['telecommande.py'],  # Remplacez par le nom de votre fichier principal
    pathex=['C:\\Users\\cheic\\anaconda3\\Library\\bin', 'D:\\nova360\\lang\\telecommade'],
    binaries=[
        ('C:\\Users\\cheic\\anaconda3\\Library\\bin\\liblzma.dll', '.'),
        ('C:\\Users\\cheic\\anaconda3\\Library\\bin\\LIBBZ2.dll', '.'),
        ('C:/Users/cheic/anaconda3/Lib/site-packages/PyQt5/Qt5/bin/*.dll', '.'),
    ],
    datas=[
        ('resources/icons/*', 'resources/icons'),  # Ajoutez vos ressources ici (par ex. icônes, gifs)
                ('resources/images/*', 'resources/images'),  # Ajoutez vos ressources ici (par ex. icônes, gifs)
        ('resources/gifs/*', 'resources/gifs'),  # Ajoutez vos ressources ici (par ex. icônes, gifs)

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
    a.binaries,
    a.datas,
    [],
    name='remote',
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
    icon='../resources/icons/robot-icons-30504-Windows.ico',  # Vérifiez le chemin d'accès à l'icône
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
    upx_exclude=[],
    name='Telecommande',
)
