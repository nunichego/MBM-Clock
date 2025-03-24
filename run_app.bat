@echo off
echo Starting Mind Before Machine Timer...

rem Check if the executable exists in the expected location
if exist "dist\Mind_Before_Machine\Mind_Before_Machine.exe" (
    start "" "dist\Mind_Before_Machine\Mind_Before_Machine.exe"
) else (
    echo Executable not found. Did you build the application?
    echo Run build_app.py to create the executable.
    pause
)