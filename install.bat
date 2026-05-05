@echo off
setlocal

set "INSTALL_DIR=%APPDATA%\NetGuard"
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT=%STARTUP_DIR%\NetGuard.lnk"

echo [NetGuard] Installing network monitor...

where python >nul 2>nul
if errorlevel 1 (
    echo Python not found. Install Python 3 from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

copy /Y "%~dp0netguard_service.py" "%INSTALL_DIR%\" >nul
copy /Y "%~dp0netguard_admin.py"   "%INSTALL_DIR%\" >nul
copy /Y "%~dp0uninstall.bat"       "%INSTALL_DIR%\" >nul

echo [NetGuard] Installing dependencies...
python -m pip install --quiet --disable-pip-version-check psutil

echo [NetGuard] Registering autostart...
powershell -NoProfile -Command ^
  "$s = (New-Object -ComObject WScript.Shell).CreateShortcut('%SHORTCUT%');" ^
  "$s.TargetPath = 'pythonw.exe';" ^
  "$s.Arguments  = '\"%INSTALL_DIR%\netguard_service.py\"';" ^
  "$s.WorkingDirectory = '%INSTALL_DIR%';" ^
  "$s.WindowStyle = 7;" ^
  "$s.Save()"

echo [NetGuard] Starting service...
start "" pythonw.exe "%INSTALL_DIR%\netguard_service.py"

echo [NetGuard] Done.
endlocal
