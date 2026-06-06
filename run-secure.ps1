# SQL Injection Lab - Secure Version Quick Start
$pythonDir = Join-Path $PSScriptRoot "python"
Set-Location $pythonDir

if (-not (Test-Path "sqli_lab.db")) {
    python db_init.py
}

Write-Host "[*] Starting SECURE version on http://127.0.0.1:5001" -ForegroundColor Green
python secure_app.py