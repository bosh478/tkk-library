@echo off
REM ============================================================
REM  Vault Stack One-Click Startup (v1)
REM  - Start ollama (11434) + rerank_server (8080)
REM  - Wait for ports ready (timeout 90s)
REM  - Health check + status report
REM  - Idempotent: skip if already running
REM ============================================================

setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "VAULT_DIR=D:\AI agent\tkk-library"
set "PYTHON_VENV=%VAULT_DIR%\rerank_venv\Scripts\python.exe"
set "OLLAMA_EXE=%USERPROFILE%\AppData\Local\Programs\Ollama\ollama.exe"
set "LOG_DIR=%VAULT_DIR%\scripts\logs"
REM TIMEOUT=180: BGE Reranker v2-m3 cold-load (transformers + tokenizer + 2.13GB weights -> CUDA) typically needs 60-150s
set "TIMEOUT=180"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

for /f "tokens=2 delims==" %%t in ('wmic os get localdatetime /value 2^>nul') do set "dt=%%t"
set "TS=!dt:~0,4!-!dt:~4,2!-!dt:~6,2!_!dt:~8,2!-!dt:~10,2!-!dt:~12,2!"

echo.
echo =============================================================
echo   Vault Stack One-Click Startup
echo   !date! !time:~0,8!
echo =============================================================
echo.

REM ---- 1. Start ollama ----
echo [1/2] ollama (port 11434)
netstat -an | findstr ":11434.*LISTENING" >nul 2>&1
if !errorlevel! equ 0 (
    echo       Status: ALREADY RUNNING [SKIP]
) else (
    if not exist "!OLLAMA_EXE!" (
        echo       Status: ERROR - not found: !OLLAMA_EXE!
        goto :FAIL
    )
    start "ollama" /MIN "!OLLAMA_EXE!" serve > "!LOG_DIR!\ollama_latest.log" 2>&1
    echo       Status: STARTED
)
echo.

REM ---- 2. Start rerank_server ----
echo [2/2] rerank_server (port 8080)
netstat -an | findstr ":8080.*LISTENING" >nul 2>&1
if !errorlevel! equ 0 (
    echo       Status: ALREADY RUNNING [SKIP]
) else (
    if not exist "!PYTHON_VENV!" (
        echo       Status: ERROR - not found: !PYTHON_VENV!
        goto :FAIL
    )
    if not exist "!SCRIPT_DIR!rerank_server.py" (
        echo       Status: ERROR - not found: !SCRIPT_DIR!rerank_server.py
        goto :FAIL
    )
    start "rerank_server" /MIN "!PYTHON_VENV!" "!SCRIPT_DIR!rerank_server.py" > "!LOG_DIR!\rerank_server_!TS!.log" 2>&1
    echo       Status: STARTED
)
echo.

REM ---- 3. Wait for APIs ready (not just port listening) ----
echo [WAIT] Waiting for APIs ready (timeout !TIMEOUT!s) ...
set "READY=0"
for /l %%i in (1,1,!TIMEOUT!) do (
    set "P1=0"
    set "P2=0"
    REM ollama: 用 curl /api/tags 检测,首次调用会触发模型加载
    curl -s --max-time 5 http://localhost:11434/api/tags >nul 2>&1
    if !errorlevel! equ 0 set "P1=1"
    REM rerank_server: 用 curl /health 检测
    curl -s --max-time 5 http://localhost:8080/health >nul 2>&1
    if !errorlevel! equ 0 set "P2=1"
    if "!P1!"=="1" if "!P2!"=="1" (
        set "READY=1"
        echo       READY (took %%i sec)
        goto :HEALTHCHECK
    )
    set /a "MOD=%%i %% 10"
    if "!MOD!"=="0" echo       ... waited %%i sec
    timeout /t 1 /nobreak >nul
)
echo       TIMEOUT - some APIs not ready
echo.

:HEALTHCHECK
echo [CHECK] Health check
echo.
echo --- ollama 11434 ---
curl -s --max-time 5 http://localhost:11434/api/tags > "!LOG_DIR!\tmp_ollama.json" 2>nul
if !errorlevel! equ 0 (
    for /f "delims=" %%m in ('powershell -NoProfile -Command "$j=Get-Content '!LOG_DIR!\tmp_ollama.json' -Raw|ConvertFrom-Json; $j.models.name -join ', '" 2^>nul') do (
        echo   [OK] Models: %%m
    )
) else (
    echo   [FAIL] API not responding
    echo   Try: ollama serve
)
del "!LOG_DIR!\tmp_ollama.json" 2>nul
echo.

echo --- rerank_server 8080 ---
curl -s --max-time 5 http://localhost:8080/health > "!LOG_DIR!\tmp_rerank.json" 2>nul
if !errorlevel! equ 0 (
    echo   [OK] API responding
    type "!LOG_DIR!\tmp_rerank.json"
    echo.
) else (
    echo   [FAIL] API not responding
    echo   Try: start_rerank_server.bat
)
del "!LOG_DIR!\tmp_rerank.json" 2>nul
echo.

echo =============================================================
if "!READY!"=="1" (
    echo   [OK] Vault Stack READY
) else (
    echo   [FAIL] Some services not ready
    echo   Logs: !LOG_DIR!
)
echo =============================================================
echo.
echo Operations:
echo   - Stop:    stop_vault_stack.bat
echo   - Status:  check_vault_health.bat
echo   - Logs:    !LOG_DIR!
echo.

pause
goto :END

:FAIL
echo.
echo [ABORT] Startup aborted
echo Logs: !LOG_DIR!
pause

:END
endlocal
