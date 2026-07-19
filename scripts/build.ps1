$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "====================================="
Write-Host " Building Project Athena"
Write-Host "====================================="
Write-Host ""

# ------------------------------------------------------------------
# Activate virtual environment
# ------------------------------------------------------------------

$venv = ".\.venv\Scripts\Activate.ps1"

if (!(Test-Path $venv))
{
    Write-Host "Virtual environment not found."
    exit 1
}

& $venv

# ------------------------------------------------------------------
# Clean previous build
# ------------------------------------------------------------------

Write-Host ""
Write-Host "Cleaning previous build..."

Remove-Item build -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item dist -Recurse -Force -ErrorAction SilentlyContinue

# ------------------------------------------------------------------
# Ruff
# ------------------------------------------------------------------

Write-Host ""
Write-Host "Running Ruff..."

ruff check .

if ($LASTEXITCODE -ne 0)
{
    throw "Ruff failed."
}

# ------------------------------------------------------------------
# MyPy
# ------------------------------------------------------------------

Write-Host ""
Write-Host "Running MyPy..."

mypy src

if ($LASTEXITCODE -ne 0)
{
    throw "MyPy failed."
}

# ------------------------------------------------------------------
# Pytest
# ------------------------------------------------------------------

Write-Host ""
Write-Host "Running Pytest..."

pytest

if ($LASTEXITCODE -ne 0)
{
    throw "Pytest failed."
}

# ------------------------------------------------------------------
# Build
# ------------------------------------------------------------------

Write-Host ""
Write-Host "Building executable..."

pyinstaller `
    --clean `
    Athena.spec

if ($LASTEXITCODE -ne 0)
{
    throw "PyInstaller failed."
}

# ------------------------------------------------------------------
# Finished
# ------------------------------------------------------------------

Write-Host ""
Write-Host "====================================="
Write-Host " Build completed successfully"
Write-Host "====================================="
Write-Host ""

Write-Host "Executable location:"
Write-Host "dist\Athena\Athena.exe"
Write-Host ""