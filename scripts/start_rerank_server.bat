@echo off
REM BGE Reranker 服务启动脚本
REM 监听 0.0.0.0:8080
REM 模型：D:\AI agent\tkk-library\models\bge-reranker-v2-m3

setlocal
set "SCRIPT_DIR=%~dp0"
set "LOG_FILE=%SCRIPT_DIR%rerank_server.log"

echo ==============================================
echo   BGE Reranker v2-m3 启动脚本
echo ==============================================
echo.

REM 检查 ollama 是否在跑（用于 embed）
curl -s --max-time 3 http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARN] ollama 未运行，bge-m3 embed 将不可用
    echo        启动 ollama: ollama serve
    echo.
) else (
    echo [OK] ollama 已在 11434 端口运行
)

REM 检查 8080 端口是否被占用
netstat -an | findstr ":8080.*LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo [WARN] 8080 端口已被占用，可能服务已在运行
    echo        日志位置: %LOG_FILE%
    echo.
    pause
    exit /b 1
)

REM 启动服务
echo [INFO] 启动 rerank_server.py (GPU venv) ...
echo [INFO] 日志将输出到: %LOG_FILE%
echo [INFO] 按 Ctrl+C 停止服务
echo.

cd /d "%SCRIPT_DIR%"
"D:\AI agent\tkk-library\rerank_venv\Scripts\python.exe" rerank_server.py

REM 异常退出提示
echo.
echo [ERROR] 服务已停止
pause
