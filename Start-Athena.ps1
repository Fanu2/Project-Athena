# ================================================
# Project Athena Launcher
# ================================================

Clear-Host

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "        Starting Project Athena" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Change to the Athena project directory
Set-Location "C:\Users\singh\Documents\Project-Athena"

# Deactivate Conda if it is active
if ($env:CONDA_DEFAULT_ENV) {
    Write-Host "Deactivating Conda environment: $($env:CONDA_DEFAULT_ENV)" -ForegroundColor Yellow
    conda deactivate
    Write-Host ""
}

# Activate the project's virtual environment
Write-Host "Activating Athena virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

# Stop if activation failed
if (-not $?) {
    Write-Host "ERROR: Failed to activate the virtual environment." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Python Version:" -ForegroundColor Cyan
python --version

Write-Host ""
Write-Host "Working Directory:" -ForegroundColor Cyan
Get-Location

Write-Host ""
Write-Host "Launching Athena..." -ForegroundColor Green
Write-Host ""

# Launch Athena
python -m athena.main

# Save exit code
$ExitCode = $LASTEXITCODE

Write-Host ""
if ($ExitCode -eq 0) {
    Write-Host "Athena exited normally." -ForegroundColor Green
}
else {
    Write-Host "Athena exited with code $ExitCode." -ForegroundColor Red
}

Read-Host "Press Enter to close this window"