# Build and start a preview independently of the chat's terminal session.
$ErrorActionPreference = 'Stop'
$siteRoot = Split-Path -Parent $PSScriptRoot
$siteOutput = Join-Path $siteRoot '_site'
$previewLog = Join-Path $siteRoot 'preview.log'
$previewErrorLog = Join-Path $siteRoot 'preview-error.log'
$pythonExe = (Get-Command python).Source
& $pythonExe (Join-Path $PSScriptRoot 'build.py')
if ($LASTEXITCODE -ne 0) { throw 'Website build failed.' }

$previewListener = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if (-not $previewListener) {
    Start-Process -FilePath $pythonExe -ArgumentList @('-m', 'http.server', '8000', '--bind', '127.0.0.1', '--directory', '_site') -WorkingDirectory $siteRoot -WindowStyle Hidden -RedirectStandardOutput $previewLog -RedirectStandardError $previewErrorLog | Out-Null
}
for ($previewAttempt = 0; $previewAttempt -lt 20; $previewAttempt++) {
    try {
        $previewResponse = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/index.html' -TimeoutSec 2
        if ($previewResponse.StatusCode -eq 200 -and $previewResponse.Content.Contains('Embodied Intelligence Lab')) {
            Write-Output 'Preview ready: http://127.0.0.1:8000/index.html'
            return
        }
    } catch {
        Start-Sleep -Milliseconds 250
    }
}
throw 'Preview did not respond. See preview-error.log.'
