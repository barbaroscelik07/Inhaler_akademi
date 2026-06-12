# -*- mode: python ; coding: utf-8 -*-
"""
İnhaler APSD Akademi — PyInstaller spec.

Komut satırı --icon bayrağı --onefile modunda Windows runner'da exe kabuk
ikonunu bazen gömmediği için ikon burada açıkça tanımlanır. Bu, exe dosya
ikonunun (masaüstü / dosya gezgini) güvenilir biçimde gömülmesini sağlar.
"""

block_cipher = None

import os
SPEC_DIR = os.path.dirname(os.path.abspath(SPEC))
ICON_PATH = os.path.join(SPEC_DIR, 'assets', 'icon.ico')
# Build sırasında ikon bulunamazsa logda açıkça görünsün
if not os.path.exists(ICON_PATH):
    raise SystemExit(f"HATA: ikon bulunamadi -> {ICON_PATH}")

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],
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

# matplotlib ve scipy alt modüllerini güvenilir biçimde topla
from PyInstaller.utils.hooks import collect_submodules
a.hiddenimports += collect_submodules('matplotlib')
a.hiddenimports += collect_submodules('scipy.special')
a.hiddenimports += collect_submodules('scipy.stats')

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='InhalerAPSD-Akademi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=ICON_PATH,
)
