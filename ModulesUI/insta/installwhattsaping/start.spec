# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['start.py'],
    pathex=[],
    binaries=[],
    datas=[
        (r'C:\\Users\\ibrahim\\Downloads\Robot_Labo_Pro\\lang\\resources\\icons\\facebook-icon-png-770-Windows.ico', 'resources/icons')  # Assurez-vous que le chemin est correct
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=True,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='start',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Changez à True si vous voulez voir la console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[r'C:\\Users\\ibrahim\\Downloads\\Robot_Labo_Pro\\lang\\resources\\icons\\facebook-icon-png-770-Windows.ico'],  # Assurez-vous que le chemin est correct
)
