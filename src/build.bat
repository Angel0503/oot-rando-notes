@echo off
REM Run this from the project root (the folder containing launcher.py, back\ and web\).
REM Builds ONE exe that carries everything it needs (web page + tracker template).
REM Change ..\data\oot-tracker below if your template folder is somewhere else.

pyinstaller --noconfirm --clean --onefile --add-data "web;web" --add-data "..\data\oot-tracker;data/oot-tracker" -n "OOTR-AutoTracker" launcher.py
if errorlevel 1 (
    echo Build failed.
    pause
    exit /b 1
)

echo.
echo Done: dist\OOTR-AutoTracker.exe  (this single file is all you need to share)
pause