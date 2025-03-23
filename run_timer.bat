@echo off
:: Change to the directory containing this batch file
cd /d %~dp0

:: Set the path to your Python script
set SCRIPT_PATH=\\wsl.localhost\Ubuntu\home\nunichego\workspace\github.com\nunichego\Mind_Before_Machine\main.py
:: Run the Python script
python "%SCRIPT_PATH%"

:: Alternatively, if you need to use a specific Python version or virtual environment
:: py -3 "%SCRIPT_PATH%"
:: OR
:: "C:\path\to\python.exe" "%SCRIPT_PATH%"