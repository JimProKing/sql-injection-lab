# SQL Injection Lab - Quick Start (Windows PowerShell)
# Double-click or run: .\run-vulnerable.ps1

Write-Host "=== SQL Injection Lab (Vulnerable) ===" -ForegroundColor Cyan

$pythonDir = Join-Path $PSScriptRoot "python"
Set-Location $pythonDir

# Check if DB exists
if (-not (Test-Path "sqli_lab.db")) {
    Write-Host "[*] Database not found. Initializing..." -ForegroundColor Yellow
    python db_init.py
}

Write-Host "[*] Starting vulnerable app on http://127.0.0.1:5000" -ForegroundColor Green
Write-Host "[*] Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

python vulnerable_app.py