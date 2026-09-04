@echo off
title Galactic Markdown Editor - Context Menu Uninstaller
color 0E
chcp 65001 >nul 2>&1

echo ================================================================
echo    [-] GALACTIC MARKDOWN EDITOR - CONTEXT MENU UNINSTALLER
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
python "%~dp0setup_context_menu.py" --uninstall

echo.
echo ================================================================
echo Press any key to exit this uninstaller...
pause >nul
