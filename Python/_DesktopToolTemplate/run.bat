@echo off
title Desktop Tool Template - Launcher
color 0B
chcp 65001 >nul 2>&1

:: [Template Tier: Tier 1 (Mandatory - Core Essentials)]
:: Smart launcher: prioritizes standalone executable -> pythonw -> python -> py

:: 1. Prefer standalone compiled executable if it exists
if exist "%~dp0desktop_tool.exe" (
    start "" "%~dp0desktop_tool.exe" %*
    exit /b 0
)
if exist "%~dp0dist\desktop_tool.exe" (
    start "" "%~dp0dist\desktop_tool.exe" %*
    exit /b 0
)

:: 2. Run with pythonw for silent windowless launch
where pythonw >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    start "" pythonw "%~dp0app.py" %*
    exit /b 0
)

:: 3. Fall back to standard python
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    python "%~dp0app.py" %*
    exit /b 0
)

:: 4. Fall back to Windows py launcher
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    py "%~dp0app.py" %*
    exit /b 0
)

color 0C
echo [!] Error: Python was not found in your system PATH.
echo     Please install Python 3.8+ or add Python to your PATH.
echo.
pause
exit /b 1
