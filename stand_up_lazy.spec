# -*- mode: python ; coding: utf-8 -*-

import platform

hiddenimports = []
icon = ""
if platform.system() == "Linux":
    hiddenimports = ["plyer.platforms.linux.notification"]
    icon = "./icons/stand_up_lazy.png"
elif platform.system() == "Windows":
    hiddenimports = ["plyer.platforms.win.notification"]
    icon = "./icons/stand_up_lazy.ico"
elif platform.system() == "Darwin":
    hiddenimports = ['plyer.platforms.macosx.notification']
    icon = "./icons/stand_up_lazy.icns"
a = Analysis(
    ["stand_up_lazy.py"],
    pathex=[],
    binaries=[],
    datas=[(icon, ".")],
    hiddenimports=hiddenimports,
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
    name='stand_up_lazy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[icon],
)
app = BUNDLE(
    exe,
    name='Stand Up, Lazy!.app',
    icon=icon,
    bundle_identifier=None,
)
