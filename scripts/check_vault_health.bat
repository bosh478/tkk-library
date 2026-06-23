@echo off
REM Vault retrieval stack health check
REM Run after reboot to verify ollama + rerank_server are alive

setlocal EnableDelayedExpansion
set "LOG_DIR=%~dp0logs"

echo ============================================
echo   Vault Stack Health Check
echo   %date% %time%
echo ============================================
echo.

REM Check ollama 11434
echo [1] ollama port 11434
netstat -an | findstr ":11434.*LISTENING" >nul 2>&1
if !errorlevel! equ 0 (
    echo     [OK] Port listening
    curl -s --max-time 3 http://localhost:11434/api/tags >nul 2>&1
    if !errorlevel! equ 0 (
        echo     [OK] API responding
    ) else (
        echo     [WARN] Port open but API not responding
    )
) else (
    echo     [FAIL] Port not listening
    echo     Run: start_vault_stack.bat
)
echo.

REM Check rerank_server 8080
echo [2] rerank_server port 8080
curl -s --max-time 3 http://localhost:8080/health >nul 2>&1
if !errorlevel! equ 0 (
    echo     [OK] API responding
) else (
    echo     [FAIL] API not responding
    echo     Run: start_vault_stack.bat
)
echo.

REM Check qmd CLI
echo [3] qmd CLI
where qmd >nul 2>&1
if !errorlevel! equ 0 (
    echo     [OK] qmd found in PATH
    for /f "delims=" %%v in ('qmd --version 2^>nul') do echo     version: %%v
) else (
    echo     [FAIL] qmd not in PATH
    echo     See: project_qmd_cli.md
)
echo.

REM Show last 20 lines of vault_stack.log
echo [4] Recent vault_stack.log
if exist "%LOG_DIR%\vault_stack.log" (
    powershell -NoProfile -Command "Get-Content '%LOG_DIR%\vault_stack.log' -Tail 20"
) else (
    echo     [NONE] vault_stack.log not found
)

echo.
echo ============================================
echo   Health check complete
echo ============================================
endlocal
