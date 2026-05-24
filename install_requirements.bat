@echo off
REM Create a virtual environment in .venv and install dependencies from requirements.txt
python -m venv .venv

if exist .venv\Scripts\pip.exe (
    echo Upgrading pip...
    .venv\Scripts\pip.exe install --upgrade pip
    echo Installing requirements...
    .venv\Scripts\pip.exe install -r requirements.txt
    echo Installation complete. To activate: .venv\Scripts\activate
    exit /b 0
) else (
    echo Failed to create virtual environment. Ensure Python is installed and on PATH.
    exit /b 1
)

