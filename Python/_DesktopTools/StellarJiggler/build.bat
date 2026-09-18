@echo off
title StellarJiggler - PyInstaller Executable Builder
color 0E
chcp 65001 >nul 2>&1

echo ================================================================
echo    [+] STELLARJIGGLER - BUILD STANDALONE EXECUTABLE
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
    echo     Please install Python 3.8+ or add Python to your PATH.
    echo.
    pause
    exit /b 1
)

:: Ensure dependencies are present
echo [i] Checking and installing requirements...
%PYTHON_CMD% -m pip install -r "%~dp0requirements.txt"
echo.

:: Ensure icon asset is present if generator exists
if not exist "%~dp0assets\app_icon.ico" (
    if exist "%~dp0generate_icon.py" (
        echo [i] Generating application icon...
        %PYTHON_CMD% "%~dp0generate_icon.py"
        echo.
    )
)

:: Prefer full package_release pipeline if present, else fallback to direct PyInstaller
if exist "%~dp0package_release.py" (
    echo [i] Executing full release packaging sequence...
    %PYTHON_CMD% "%~dp0package_release.py"
) else (
    echo [i] Compiling standalone executable via PyInstaller...
    %PYTHON_CMD% -m PyInstaller --noconfirm "%~dp0stellar_jiggler.spec"
)

echo.
echo ================================================================
echo Build complete. Executable / release files are in dist\
echo ================================================================
pause
