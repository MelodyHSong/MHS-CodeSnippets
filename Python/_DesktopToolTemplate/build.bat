@echo off
title Desktop Tool Template - PyInstaller Executable Builder
color 0E
chcp 65001 >nul 2>&1

echo ================================================================
echo    [+] DESKTOP TOOL TEMPLATE - BUILD STANDALONE EXECUTABLE
echo ================================================================
echo.

:: Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo [!] Error: Python was not found in your system PATH.
    echo.
    pause
    exit /b 1
)

:: Ensure dependencies are present
echo [i] Checking and installing requirements...
python -m pip install -r "%~dp0requirements.txt"
echo.

:: Ensure icon asset is present
if not exist "%~dp0assets\app_icon.ico" (
    echo [i] Generating application icon...
    python "%~dp0generate_icon.py"
    echo.
)

:: Run PyInstaller build via setup script
python "%~dp0setup_integration.py" --build

echo.
echo ================================================================
echo Build complete. Executable is located in dist\desktop_tool.exe
echo ================================================================
pause
