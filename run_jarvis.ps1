Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "              STARTING JARVIS AI ASSISTANT              " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

Set-Location $PSScriptRoot

if (Test-Path ".\envjarvis\Scripts\python.exe") {
    Write-Host "[System] Launching with Jarvis Virtual Environment..." -ForegroundColor Green
    & ".\envjarvis\Scripts\python.exe" "main.py"
} else {
    Write-Host "[System] Launching with System Python..." -ForegroundColor Yellow
    python "main.py"
}
