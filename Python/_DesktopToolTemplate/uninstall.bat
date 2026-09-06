@echo off
title Desktop Tool Template - Windows Integration Uninstaller
color 0C
chcp 65001 >nul 2>&1

:: [Template Tier: Tier 2 (Optional - Windows Shell Integration)]
:: Safe to delete if: This tool does not integrate with Windows Explorer context menus or shortcuts.

echo ================================================================
echo    [-] DESKTOP TOOL TEMPLATE - INTEGRATION UNINSTALLER
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

:: Run the uninstaller
if exist "%~dp0setup_integration.py" (
    %PYTHON_CMD% "%~dp0setup_integration.py" --uninstall
) else if exist "%~dp0setup_context_menu.py" (
    %PYTHON_CMD% "%~dp0setup_context_menu.py" --uninstall
) else (
    color 0C
    echo [!] Error: Neither setup_integration.py nor setup_context_menu.py was found.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo Press any key to exit this uninstaller...
pause >nul
