@echo off
title Jarvis AI Voice Assistant
echo ========================================================
echo               STARTING JARVIS AI ASSISTANT               
echo ========================================================
echo.

cd /d "%~dp0"

if exist "envjarvis\Scripts\python.exe" (
    echo [System] Launching with Jarvis Python 3.12 Virtual Environment...
    "envjarvis\Scripts\python.exe" main.py
) else (
    echo [System] Launching with Global Python...
    python main.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [Error] Jarvis terminated unexpectedly
    pause
)
