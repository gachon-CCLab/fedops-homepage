$ErrorActionPreference = 'Stop'
$previewRoot = $PSScriptRoot
$consoleRoot = Join-Path (Split-Path $previewRoot -Parent) 'FedOps-Web\client'
$pythonExe = (Get-Command python.exe -ErrorAction Stop).Source
$nodeExe = (Get-Command node.exe -ErrorAction Stop).Source
Push-Location $previewRoot
try {
    & $pythonExe 'build.py'
    if ($LASTEXITCODE -ne 0) { throw 'Homepage build failed.' }
} finally { Pop-Location }
if (-not (Get-NetTCPConnection -State Listen -LocalPort 4313 -ErrorAction SilentlyContinue)) {
    Start-Process -FilePath $pythonExe -ArgumentList @('serve.py', '--port', '4313') -WorkingDirectory $previewRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $previewRoot 'preview-4313.stdout.log') -RedirectStandardError (Join-Path $previewRoot 'preview-4313.stderr.log') | Out-Null
}
if (-not (Get-NetTCPConnection -State Listen -LocalPort 4314 -ErrorAction SilentlyContinue)) {
    $startScript = Join-Path $consoleRoot 'node_modules\react-scripts\scripts\start.js'
    if (-not (Test-Path -LiteralPath $startScript)) { throw 'Install the existing Console client dependencies before starting the preview.' }
    # This older CRA proxy produces an empty allowedHosts entry on loopback.
    # Keep the listener strictly local while using its supported dev-only workaround.
    $previewEnv = @{ PORT='4314'; HOST='127.0.0.1'; BROWSER='none'; REACT_APP_CONSOLE_PREVIEW='false'; DANGEROUSLY_DISABLE_HOST_CHECK='true' }
    $previousEnv = @{}
    foreach ($key in $previewEnv.Keys) {
        $previousEnv[$key] = [Environment]::GetEnvironmentVariable($key, 'Process')
        [Environment]::SetEnvironmentVariable($key, $previewEnv[$key], 'Process')
    }
    try {
        Start-Process -FilePath $nodeExe -ArgumentList @('node_modules/react-scripts/scripts/start.js') -WorkingDirectory $consoleRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $consoleRoot 'preview-4314.stdout.log') -RedirectStandardError (Join-Path $consoleRoot 'preview-4314.stderr.log') | Out-Null
    } finally {
        foreach ($key in $previewEnv.Keys) { [Environment]::SetEnvironmentVariable($key, $previousEnv[$key], 'Process') }
    }
}
Write-Output 'Home:    http://127.0.0.1:4313/version-2/'
Write-Output 'Console: http://127.0.0.1:4314/fedops/task'
Write-Output 'Docs:    https://gachon-cclab.github.io/fedops-docs-1.3/'
Write-Output 'React may take a moment to finish its initial compile. Logs are in each project folder.'
