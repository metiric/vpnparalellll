# NetGuard remote installer
# Usage from cmd:
#   powershell -ExecutionPolicy Bypass -Command "iwr -useb https://raw.githubusercontent.com/metiric/netguard/main/bootstrap.ps1 | iex"

$ErrorActionPreference = "Stop"

# !!! Замени на свой GitHub username/repo перед пушем !!!
$RepoBase    = "https://raw.githubusercontent.com/metiric/netguard/main"
$InstallDir  = Join-Path $env:APPDATA "NetGuard"
$StartupDir  = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Startup"
$ShortcutLnk = Join-Path $StartupDir "NetGuard.lnk"

$Files = @("netguard_service.py", "netguard_admin.py", "uninstall.bat")

Write-Host "[NetGuard] Checking Python..."
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python not found. Install from https://python.org (check 'Add to PATH')."
    return
}

Write-Host "[NetGuard] Preparing install dir: $InstallDir"
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null

foreach ($f in $Files) {
    Write-Host "[NetGuard] Downloading $f..."
    Invoke-WebRequest -UseBasicParsing -Uri "$RepoBase/$f" -OutFile (Join-Path $InstallDir $f)
}

Write-Host "[NetGuard] Installing dependencies..."
& python -m pip install --quiet --disable-pip-version-check psutil

Write-Host "[NetGuard] Creating autostart shortcut..."
$shell = New-Object -ComObject WScript.Shell
$sc = $shell.CreateShortcut($ShortcutLnk)
$sc.TargetPath       = "pythonw.exe"
$sc.Arguments        = "`"$InstallDir\netguard_service.py`""
$sc.WorkingDirectory = $InstallDir
$sc.WindowStyle      = 7
$sc.Save()

Write-Host "[NetGuard] Starting service..."
Start-Process -WindowStyle Hidden -FilePath "pythonw.exe" -ArgumentList "`"$InstallDir\netguard_service.py`""

Write-Host "[NetGuard] Done."
