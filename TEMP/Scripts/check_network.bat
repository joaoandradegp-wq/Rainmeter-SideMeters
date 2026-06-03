@echo off

for /f "tokens=2 delims=," %%a in ('
    tasklist /v /fo csv ^| findstr /i "check_network.ps1"
') do (
    taskkill /F /PID %%~a >nul 2>&1
)

powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File "%USERPROFILE%\Documents\Rainmeter\Scripts\check_network.ps1"
