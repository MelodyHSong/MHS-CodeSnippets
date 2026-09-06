@echo off
title Desktop Tool Template - Windows Integration Installer
color 0E
chcp 65001 >nul 2>&1

:: [Template Tier: Tier 2 (Optional - Windows Shell Integration)]
:: Safe to delete if: This tool does not integrate with Windows Explorer context menus or shortcuts.

echo ================================================================
echo    [+] DESKTOP TOOL TEMPLATE - INTEGRATION INSTALLER
echo ================================================================
echo.

:: Check if Python or py launcher is installed
set PYTHON_CMD=
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 set PYTHON_CMD=python
if not defined PYTHON_CMD (
    where py >nul 2>&1
    if %ERRORLEVEL% EQU 0 set PYTHON_CMD=py
)
if not defined PYTHON_CMD (
    color 0C
    echo [!] Error: Python was not found in your system PATH.
    echo     Please ensure Python 3.8+ is installed and added to PATH.
    echo.
    pause
    exit /b 1
)

:: Run installer in auto mode (prefers compiled .exe if present, falls back to pythonw)
if exist "%~dp0setup_integration.py" (
    %PYTHON_CMD% "%~dp0setup_integration.py" --install --mode auto
) else if exist "%~dp0setup_context_menu.py" (
    %PYTHON_CMD% "%~dp0setup_context_menu.py" --install --mode auto
) else (
    color 0C
    echo [!] Error: Neither setup_integration.py nor setup_context_menu.py was found.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo Press any key to exit this installer...
pause >nul
