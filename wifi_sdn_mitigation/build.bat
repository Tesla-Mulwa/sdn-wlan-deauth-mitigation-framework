@echo off
echo WiFi SDN Mitigation Simulation - Executable Builder
echo ================================================
echo.

echo Installing PyInstaller if not already installed...
pip install pyinstaller

echo.
echo Building executable...
python build_executable.py

echo.
echo Build process completed!
echo Check the 'dist' folder for your executable.
pause 