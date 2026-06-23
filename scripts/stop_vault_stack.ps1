# Vault Stack Stop (v2.1) - min-invasive + path-verified
# 仅 kill 监听 11434/8080 LISTENING 状态且路径匹配的进程

$vaultRerankVenv = 'tkk-library\rerank_venv'
$ollamaExe = 'ollama.exe'
$ollamaServe = 'serve'

$ports = @(
    @{ Port = '8080';  Service = 'rerank_server';  MatchCheck = {
            param($cmd) $cmd -like '*rerank_server.py*' -and $cmd -like "*$vaultRerankVenv*"
        }
    },
    @{ Port = '11434'; Service = 'ollama';         MatchCheck = {
            param($cmd) $cmd -like "*$ollamaExe*" -and $cmd -match $ollamaServe
        }
    }
)

$totalKilled = 0

foreach ($entry in $ports) {
    $port = $entry.Port
    $service = $entry.Service
    $match = $entry.MatchCheck
    Write-Host "[$port] $service - checking LISTENING..." -ForegroundColor Cyan

    $pids = netstat -ano | Select-String ":$port .*LISTENING" | ForEach-Object {
        ($_ -split '\s+')[-1]
    } | Where-Object { $_ -match '^\d+$' } | Select-Object -Unique

    $killed = 0
    foreach ($p in $pids) {
        $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$p" -ErrorAction SilentlyContinue
        if (-not $proc) {
            Write-Host "  PID ${p}: (process not accessible, skip)" -ForegroundColor Gray
            continue
        }
        $cmd = $proc.CommandLine
        if (-not $cmd) {
            Write-Host "  PID ${p}: (no command line, skip)" -ForegroundColor Gray
            continue
        }

        # 路径校验
        if ($match.Invoke($cmd)) {
            Write-Host "  PID ${p}  [VAULT MATCH - KILL]" -ForegroundColor Green
            Write-Host "    CMD: $cmd"
            if ($service -eq 'ollama') {
                # ollama 用树形 kill,清理 runner 子进程
                Stop-Process -Id $p -Force
            } else {
                Stop-Process -Id $p -Force
            }
            $killed++
        } else {
            Write-Host "  PID ${p}  [SKIP - not vault process]" -ForegroundColor Yellow
            Write-Host "    CMD: $cmd"
        }
    }

    if ($killed -eq 0 -and $pids.Count -eq 0) {
        Write-Host "  No process listening on $port [SKIP]" -ForegroundColor Gray
    } elseif ($killed -eq 0) {
        Write-Host "  Found $($pids.Count) PID(s) on $port but none matched vault path [0 killed]" -ForegroundColor Yellow
    } else {
        Write-Host "  Killed $killed process(es) on $port" -ForegroundColor Green
    }
    $totalKilled += $killed
    Write-Host ""
}

Write-Host "============================================================="
Write-Host "  Total killed: $totalKilled process(es)" -ForegroundColor $(if ($totalKilled -gt 0) { 'Green' } else { 'Yellow' })
Write-Host "============================================================="
Write-Host "Note: only vault-related processes killed; others preserved"
