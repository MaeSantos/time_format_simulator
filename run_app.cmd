@echo off
set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python313\python.exe"

if not exist "%PYTHON_EXE%" (
    echo Python 3.13 was not found at:
    echo %PYTHON_EXE%
    echo Reinstall Python or select a valid interpreter in your IDE.
    pause
    exit /b 1
)

"%PYTHON_EXE%" "%~dp0app.py"
