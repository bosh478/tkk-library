@echo off
REM Vault retrieval stack auto-start script
REM Starts: ollama (11434) + rerank_server (8080)
REM Drop into shell:startup for boot auto-start

setlocal

set "SCRIPT_DIR=%~dp0"
set "VAULT_DIR=D:\AI agent\tkk-library"
set "PYTHON_VENV=%VAULT_DIR%\rerank_venv\Scripts\python.exe"
set "OLLAMA_EXE=%USERPROFILE%\AppData\Local\Programs\Ollama\ollama.exe"
set "LOG_DIR=%VAULT_DIR%\scripts\logs"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Use wmic localdatetime to avoid CJK characters in %date% (e.g. "周四") corrupting the log
for /f "tokens=2 delims==" %%t in ('wmic os get localdatetime /value 2^>nul') do set "DT=%%t"
set "STAMP=%DT:~0,4%-%DT:~4,2%-%DT:~6,2% %DT:~8,2%:%DT:~10,2%:%DT:~12,2%"
set "TIMESTAMP=%DT:~0,4%-%DT:~4,2%-%DT:~6,2%_%DT:~8,2%-%DT:~10,2%-%DT:~12,2%"

netstat -an | findstr ":11434.*LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo [%STAMP%] [SKIP] ollama 11434 already running >> "%LOG_DIR%\vault_stack.log"
) else (
    if not exist "%OLLAMA_EXE%" (
        echo [%STAMP%] [ERROR] ollama not found: %OLLAMA_EXE% >> "%LOG_DIR%\vault_stack.log"
    ) else (
        echo [%STAMP%] [INFO] starting ollama ... >> "%LOG_DIR%\vault_stack.log"
        start "ollama" /B "%OLLAMA_EXE%" serve > "%LOG_DIR%\ollama_%TIMESTAMP%.log" 2>&1
    )
)

netstat -an | findstr ":8080.*LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo [%STAMP%] [SKIP] rerank_server 8080 already running >> "%LOG_DIR%\vault_stack.log"
) else (
    echo [%STAMP%] [INFO] starting rerank_server ... >> "%LOG_DIR%\vault_stack.log"
    cd /d "%SCRIPT_DIR%"
    start "rerank_server" /B "%PYTHON_VENV%" "%SCRIPT_DIR%rerank_server.py" > "%LOG_DIR%\rerank_server_%TIMESTAMP%.log" 2>&1
)

echo [%STAMP%] [DONE] vault stack start commands issued >> "%LOG_DIR%\vault_stack.log"
endlocal