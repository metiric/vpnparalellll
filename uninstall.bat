@echo off
setlocal

set "INSTALL_DIR=%APPDATA%\NetGuard"
set "SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\NetGuard.lnk"

echo [NetGuard] Sending shutdown signal...
python "%INSTALL_DIR%\netguard_admin.py" 2>nul

timeout /t 2 /nobreak >nul

echo [NetGuard] Removing autostart entry...
if exist "%SHORTCUT%" del /f /q "%SHORTCUT%"

taskkill /F /IM pythonw.exe >nul 2>nul

echo [NetGuard] Cleaning up...
endlocal
(goto) 2>nul & rmdir /s /q "%APPDATA%\NetGuard"
