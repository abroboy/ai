@echo off
setlocal

echo Starting NL2Find Server...

REM Define the Python executable inside the virtual environment
set VENV_PYTHON=".\venv\Scripts\python.exe"

REM Check if the virtual environment's Python exists
if not exist %VENV_PYTHON% (
    echo Error: Virtual environment python.exe not found.
    echo Please run setup.bat first to create and populate the environment.
    pause
    exit /b 1
)

REM Run the server directly with the venv's Python. No 'activate' needed.
echo Starting server with the correct Python interpreter...
%VENV_PYTHON% main.py --server

echo.
echo Server has been stopped.
pause 