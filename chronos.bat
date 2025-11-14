@echo off
REM Chronos Outreach System - Quick Launcher (Windows)

echo ================================
echo CHRONOS OUTREACH SYSTEM
echo ================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    echo [✓] Virtual environment created
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import anthropic" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo [✓] Dependencies installed
)

REM Check if config exists
if not exist "config.json" (
    echo.
    echo Configuration file not found.
    echo Running setup wizard...
    echo.
    python setup.py setup
)

REM Main menu
echo.
echo What would you like to do?
echo.
echo 1. Research brands in a category
echo 2. Generate email sequences
echo 3. Launch web interface (review ^& send)
echo 4. View statistics
echo 5. Run setup wizard
echo 6. Exit
echo.

set /p choice="Choose option (1-6): "

if "%choice%"=="1" (
    set /p category="Enter category (e.g., 'Irish Whiskey'): "
    set /p limit="How many brands? (default 20): "
    if "%limit%"=="" set limit=20
    python main.py research --category "%category%" --limit %limit%
)

if "%choice%"=="2" (
    python main.py generate
)

if "%choice%"=="3" (
    python main.py review
)

if "%choice%"=="4" (
    python main.py stats
)

if "%choice%"=="5" (
    python setup.py setup
)

if "%choice%"=="6" (
    echo Goodbye!
    exit
)

pause
