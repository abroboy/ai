@echo off
setlocal

echo ========================================================
echo  NL2Find Environment Setup
echo ========================================================
echo.

REM Set the specific Python executable path
set PYTHON_EXE="C:\Users\rexouyang\AppData\Local\Programs\Python\Python39\python.exe"

REM Check for Python
echo Checking for Python at %PYTHON_EXE%...
if not exist %PYTHON_EXE% (
    echo Error: Python not found at the specified path.
    echo Please ensure Python 3.9 is installed at:
    echo C:\Users\rexouyang\AppData\Local\Programs\Python\Python39
    pause
    exit /b 1
)
echo Python found.
echo.

REM Create virtual environment
echo Creating virtual environment in 'venv' directory...
if not exist venv (
    %PYTHON_EXE% -m venv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo Virtual environment created.
) else (
    echo Virtual environment 'venv' already exists.
)
echo.

REM Define the Python executable inside the virtual environment
set VENV_PYTHON=".\venv\Scripts\python.exe"

REM Install packages using the venv's Python directly
echo Installing dependencies from local 'libs' folder...
%VENV_PYTHON% -m pip install --no-index --find-links=./libs -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo *******************************************************************
    echo * ERROR: Failed to install dependencies.
    echo * Please check the integrity of the 'libs' folder and 'requirements.txt'.
    echo *******************************************************************
    pause
    exit /b 1
)
echo.
echo ========================================================
echo  Setup Complete!
echo ========================================================
echo You can now start the server by running start_server.bat
echo.
pause 