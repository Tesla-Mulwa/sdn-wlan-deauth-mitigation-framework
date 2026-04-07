# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[('config.py', '.'), ('simulator.py', '.'), ('controller.py', '.'), ('network.py', '.'), ('metrics.py', '.'), ('visualization.py', '.')],
    hiddenimports=['pandas', 'matplotlib', 'seaborn', 'numpy', 'tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'tkinter.filedialog', 'matplotlib.backends.backend_tkagg', 'matplotlib.pyplot', 'seaborn', 'threading', 'time', 'random', 'os', 'sys', 'csv', 'datetime', 'math', 'argparse'],
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
    name='WiFi_SDN_Simulation',
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
)
