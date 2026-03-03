@echo off
REM Quick start script for Cosmetic Alena Flask Application (Windows)

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║     Cosmetic Alena - Flask Website Application Setup              ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

echo ✓ Python found: 
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

echo.

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

echo ✓ Virtual environment activated
echo.

REM Install requirements
echo 📥 Installing dependencies...
pip install -q -r requirements.txt
echo ✓ Dependencies installed

echo.

REM Create .env if it doesn't exist
if not exist ".env" (
    echo ⚙️  Creating .env file...
    (
        echo FLASK_APP=app.py
        echo FLASK_ENV=development
        echo SECRET_KEY=cosmetic-alena-dev-key-change-in-production
    ) > .env
    echo ✓ .env file created
) else (
    echo ✓ .env file already exists
)

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                   Setup Complete! 🎉                              ║
echo ╠════════════════════════════════════════════════════════════════════╣
echo ║                                                                    ║
echo ║  To start the development server, run:                            ║
echo ║                                                                    ║
echo ║      python app.py                                               ║
echo ║                                                                    ║
echo ║  Then open your browser and visit:                               ║
echo ║                                                                    ║
echo ║      http://localhost:5000                                       ║
echo ║                                                                    ║
echo ╠════════════════════════════════════════════════════════════════════╣
echo ║  Project Documentation: See SETUP_AND_RUN.md                      ║
echo ║  API Endpoints: See app.py for all available routes               ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

pause
