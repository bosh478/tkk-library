@echo off
REM ============================================================
REM  Vault Stack One-Click Stop (v2.1 - min-invasive)
REM  Wrapper that calls stop_vault_stack.ps1
REM  - Only kills 11434/8080 LISTENING + vault path match
REM  - ollama: tree-kill (cleans runner children)
REM ============================================================

setlocal

set "SCRIPT_DIR=%~dp0"
set "PS_SCRIPT=%SCRIPT_DIR%stop_vault_stack.ps1"

if not exist "%PS_SCRIPT%" (
    echo [ERROR] %PS_SCRIPT% not found
    pause
    exit /b 1
)

echo.
echo =============================================================
echo   Vault Stack Stop (min-invasive + path-verified)
echo   %date% %time:~0,8%
echo =============================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%"

echo.
pause
endlocal
