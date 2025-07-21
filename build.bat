@echo off
REM Password Guardian Pro Build Script

REM Create virtual environment if not exists
if not exist .venv (
    py -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
python -m pip install -r requirements.txt
python -m pip install pyinstaller

REM Build executable
python -m PyInstaller --onefile --noconsole main.py --icon=assets/logo.ico --clean

echo Build complete! Check dist\main.exe
pause