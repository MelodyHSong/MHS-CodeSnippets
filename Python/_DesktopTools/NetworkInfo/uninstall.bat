@echo off
title NetworkVisor - Desktop Shortcut Uninstaller
color 0C
chcp 65001 >nul 2>&1

echo ================================================================
echo    [-] NETWORK VISOR - DESKTOP SHORTCUT UNINSTALLER
echo ================================================================
echo.

:: Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo [!] Error: Python was not found in your system PATH.
    echo     Please ensure Python is installed and added to PATH.
    echo.
    pause
    exit /b 1
)

:: Run the uninstaller
python "%~dp0setup_desktop.py" --uninstall

echo.
echo ================================================================
echo Press any key to exit this uninstaller...
pause >nul
