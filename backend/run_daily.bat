@echo off
echo ========================================
echo SIH Daily Problem Classification Runner
echo ========================================
echo.

REM Check if API key is set
if "%GEMINI_API_KEY%"=="" (
    echo ERROR: GEMINI_API_KEY not set!
    echo Please set your API key first:
    echo set GEMINI_API_KEY=your_api_key_here
    echo.
    echo Get your API key from: https://aistudio.google.com/app/apikey
    pause
    exit /b 1
)

echo Starting pipeline...
echo Current time: %date% %time%
echo.

cd /d "%~dp0"
python server.py

echo.
echo Pipeline finished at: %date% %time%
echo Press any key to close...
pause
