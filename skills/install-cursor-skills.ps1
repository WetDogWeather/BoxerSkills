# Windows wrapper for the cross-platform Python installer.
$ErrorActionPreference = "Stop"

$Script = Join-Path $PSScriptRoot "install-cursor-skills.py"
$Python = Get-Command python, python3 -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $Python) {
    Write-Error "Python 3 is required to install skills."
    exit 1
}

& $Python.Source $Script @args
exit $LASTEXITCODE
