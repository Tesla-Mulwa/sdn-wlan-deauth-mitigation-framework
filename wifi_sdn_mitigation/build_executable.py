#!/usr/bin/env python3
"""
Build script for WiFi SDN Mitigation Simulation Executable
Creates a single GUI executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil

def check_dependencies():
    """Check if required packages are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        'pyinstaller',
        'pandas',
        'matplotlib',
        'seaborn',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} - MISSING")
    
    if missing_packages:
        print(f"\nInstalling missing packages: {', '.join(missing_packages)}")
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✓ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"✗ Failed to install {package}")
                return False
    
    return True

def create_spec_file():
    """Create PyInstaller spec file"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.py', '.'),
        ('simulator.py', '.'),
        ('controller.py', '.'),
        ('network.py', '.'),
        ('metrics.py', '.'),
        ('visualization.py', '.'),
        ('requirements.txt', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'pandas',
        'matplotlib',
        'seaborn',
        'numpy',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.pyplot',
        'seaborn',
        'threading',
        'time',
        'random',
        'os',
        'sys',
        'csv',
        'datetime',
        'math',
        'argparse'
    ],
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
    a.zipfiles,
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
    icon=None,
    version='file_version_info.txt',
)
'''
    
    with open('wifi_sdn_simulation.spec', 'w') as f:
        f.write(spec_content)
    
    print("✓ Created PyInstaller spec file")

def create_version_info():
    """Create version info file"""
    version_info = '''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x40004,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'WiFi SDN Research'),
        StringStruct(u'FileDescription', u'WiFi SDN Mitigation Simulation'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'wifi_sdn_simulation'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2024'),
        StringStruct(u'OriginalFilename', u'WiFi_SDN_Simulation.exe'),
        StringStruct(u'ProductName', u'WiFi SDN Mitigation Simulation'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
    
    with open('file_version_info.txt', 'w') as f:
        f.write(version_info)
    
    print("✓ Created version info file")

def build_executable():
    """Build the executable"""
    print("\nBuilding executable...")
    
    try:
        # Run PyInstaller
        cmd = [
            'pyinstaller',
            '--onefile',
            '--windowed',
            '--name=WiFi_SDN_Simulation',
            '--add-data=config.py;.',
            '--add-data=simulator.py;.',
            '--add-data=controller.py;.',
            '--add-data=network.py;.',
            '--add-data=metrics.py;.',
            '--add-data=visualization.py;.',
            '--hidden-import=pandas',
            '--hidden-import=matplotlib',
            '--hidden-import=seaborn',
            '--hidden-import=numpy',
            '--hidden-import=tkinter',
            '--hidden-import=tkinter.ttk',
            '--hidden-import=tkinter.messagebox',
            '--hidden-import=tkinter.filedialog',
            '--hidden-import=matplotlib.backends.backend_tkagg',
            '--hidden-import=matplotlib.pyplot',
            '--hidden-import=seaborn',
            '--hidden-import=threading',
            '--hidden-import=time',
            '--hidden-import=random',
            '--hidden-import=os',
            '--hidden-import=sys',
            '--hidden-import=csv',
            '--hidden-import=datetime',
            '--hidden-import=math',
            '--hidden-import=argparse',
            'gui.py'
        ]
        
        subprocess.check_call(cmd)
        print("✓ Executable built successfully!")
        
        # Check if executable was created
        exe_path = os.path.join('dist', 'WiFi_SDN_Simulation.exe')
        if os.path.exists(exe_path):
            print(f"✓ Executable created: {exe_path}")
            print(f"  Size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
            return True
        else:
            print("✗ Executable not found")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Build error: {e}")
        return False

def create_launcher_script():
    """Create a simple launcher script"""
    launcher_content = '''@echo off
echo Starting WiFi SDN Mitigation Simulation...
echo.
echo If the GUI doesn't start, please ensure you have:
echo - Windows 10 or later
echo - Visual C++ Redistributable installed
echo.
pause
'''
    
    with open('launch_simulation.bat', 'w') as f:
        f.write(launcher_content)
    
    print("✓ Created launcher script")

def main():
    """Main build function"""
    print("WiFi SDN Mitigation Simulation - Executable Builder")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('gui.py'):
        print("✗ Error: gui.py not found. Please run this script from the project directory.")
        return False
    
    # Check dependencies
    if not check_dependencies():
        print("✗ Failed to install required dependencies")
        return False
    
    # Create version info
    create_version_info()
    
    # Build executable
    if build_executable():
        print("\n🎉 BUILD SUCCESSFUL!")
        print("\nExecutable created in 'dist' folder:")
        print("  - WiFi_SDN_Simulation.exe")
        print("\nTo run the simulation:")
        print("  1. Navigate to the 'dist' folder")
        print("  2. Double-click 'WiFi_SDN_Simulation.exe'")
        print("  3. Or run from command line: WiFi_SDN_Simulation.exe")
        
        # Create launcher script
        create_launcher_script()
        
        print("\n📋 Notes:")
        print("  - The executable is self-contained (no Python installation needed)")
        print("  - All dependencies are included")
        print("  - Results will be saved in 'data' and 'plots' folders")
        print("  - The GUI will create these folders automatically")
        
        return True
    else:
        print("\n❌ BUILD FAILED!")
        print("Please check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 