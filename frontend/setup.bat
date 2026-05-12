@echo off
REM Jarvis Ayurveda Frontend - Setup Script for Windows

echo.
echo ================================
echo Jarvis Ayurveda Frontend Setup
echo ================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Node.js is not installed. Please install Node.js 16+ from https://nodejs.org/
    pause
    exit /b 1
)

echo Node.js version:
node --version
echo npm version:
npm --version
echo.

REM Check if we're in the frontend directory
if not exist "package.json" (
    echo Error: package.json not found. Please run this script from the frontend directory.
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
call npm install

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo .env file created. Please update it with your configuration.
)

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo To start the development server, run:
echo   npm run dev
echo.
echo To build for production, run:
echo   npm run build
echo.
echo Open http://localhost:3000 in your browser when the server is running.
echo.
pause
