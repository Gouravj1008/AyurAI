@echo off
REM Jarvis Ayurvedic Chatbot - Windows Launcher
REM Activates virtual environment and launches the application

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo  ^>^> JARVIS AYURVEDIC HEALTH ASSISTANT
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        echo Make sure Python 3.9+ is installed and in PATH
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if dependencies are installed
pip show transformers >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing dependencies (this may take a few minutes)...
    pip install --upgrade pip
    pip install -r requirements_complete.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        echo Check your internet connection and try again
        pause
        exit /b 1
    )
)

REM Run validation
echo.
echo Running system validation...
python validate_system.py
if errorlevel 1 (
    echo.
    echo Validation failed. Please fix issues before launching.
    pause
    exit /b 1
)

REM Launch application
echo.
echo Launching Jarvis...
echo.
python run_jarvis_improved.py

if errorlevel 1 (
    echo.
    echo Application failed to start
    echo Check jarvis.log for details
    pause
)

REM Cleanup
deactivate

pause
