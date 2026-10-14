# Serve dashboard/preview.html locally (avoids file:// and CDN issues).
# Usage: .\scripts\serve_dashboard.ps1
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
$port = 8766
Write-Host "Dashboard: http://localhost:$port/dashboard/preview.html"
Write-Host "Press Ctrl+C to stop."
python -m http.server $port
