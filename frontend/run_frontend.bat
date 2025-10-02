@echo off
echo Starting Resume Screening Frontend Server...
echo.
echo Opening browser at http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.
cd /d "%~dp0"
python server.py
pause