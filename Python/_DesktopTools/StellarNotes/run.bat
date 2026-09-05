@echo off
title StellarNotes - Launcher
color 0B
chcp 65001 >nul 2>&1

:: Prefer standalone compiled executable if it exists
if exist "%~dp0dist\stellar_notes.exe" (
    start "" "%~dp0dist\stellar_notes.exe" %*
    exit /b 0
)

:: Run with pythonw for silent windowless launch
where pythonw >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    start "" pythonw "%~dp0stellar_notes.py" %*
    exit /b 0
)

:: Fall back to standard python
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    python "%~dp0stellar_notes.py" %*
    exit /b 0
)

color 0C
echo [!] Error: Python was not found in your system PATH.
echo     Please install Python 3.8+ or add Python to your PATH.
echo.
pause
exit /b 1
