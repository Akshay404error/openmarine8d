@echo off
REM Batch file to run the Missing Person Finder application

echo Starting Missing Person Finder Application...
echo =========================================

REM Set the working directory to the script's directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.7 or later from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check and install required packages
echo Checking for required packages...
pip install --upgrade pip
pip install -r requirements.txt

REM Set environment variables if needed
set PYTHONPATH=%~dp0

REM Run the Streamlit app
echo Starting the application...
echo.
echo Application is running. Please wait for the browser to open...
echo If the browser doesn't open automatically, go to: http://localhost:8501

start http://localhost:8501
streamlit run app.py

REM Keep the window open if there's an error
if %ERRORLEVEL% neq 0 (
    echo.
    echo The application encountered an error.
    echo Please check the error messages above.
    pause
)

exit /b
