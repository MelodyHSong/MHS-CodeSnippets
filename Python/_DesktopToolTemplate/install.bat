@echo off
title Desktop Tool Template - Windows Integration Installer
color 0E
chcp 65001 >nul 2>&1

echo ================================================================
echo    [+] DESKTOP TOOL TEMPLATE - INTEGRATION INSTALLER
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

:: Run the installer in auto mode (prefers compiled .exe if present, falls back to pythonw)
python "%~dp0setup_integration.py" --install --mode auto

echo.
echo ================================================================
echo Press any key to exit this installer...
pause >nul
