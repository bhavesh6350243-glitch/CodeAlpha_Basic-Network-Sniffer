@echo off
title Network Sniffer - Real-time Packet Analyzer
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    NETWORK SNIFFER                           ║
echo ║                Real-time Packet Analyzer                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo    Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import flask, scapy, flask_socketio, rich" >nul 2>&1
if errorlevel 1 (
    echo ❌ Missing dependencies. Installing...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if running as administrator
net session >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Warning: This application requires administrator privileges
    echo    for packet capture functionality.
    echo    If capture doesn't work, please run as Administrator.
    echo.
)

echo ✅ Ready to start Network Sniffer
echo.
echo Choose your interface:
echo   1. Web Interface (Recommended)
echo   2. Command Line Interface
echo   3. List Network Interfaces
echo   4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo 🌐 Launching Web Interface...
    echo    Opening http://localhost:5000
    echo    Press Ctrl+C to stop
    echo.
    python start.py --web
) else if "%choice%"=="2" (
    echo.
    echo 💻 Command Line Interface
    echo    Use: python cli_sniffer.py --help
    echo    Example: python cli_sniffer.py --list
    echo    Example: python cli_sniffer.py -i eth0
    echo.
    pause
) else if "%choice%"=="3" (
    echo.
    echo 📋 Listing Network Interfaces...
    python cli_sniffer.py --list
    echo.
    pause
) else if "%choice%"=="4" (
    echo 👋 Goodbye!
) else (
    echo ❌ Invalid choice. Please enter 1-4.
    pause
) 