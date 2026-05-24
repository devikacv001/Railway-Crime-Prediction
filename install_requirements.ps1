# PowerShell script: run with appropriate execution policy (e.g. 'powershell -ExecutionPolicy Bypass -File .\install_requirements.ps1')
Write-Output "Creating virtual environment .venv..."
python -m venv .venv

$pipPath = Join-Path -Path ".venv" -ChildPath "Scripts\pip.exe"
if (Test-Path $pipPath) {
    & $pipPath install --upgrade pip
    & $pipPath install -r requirements.txt
    Write-Output "Installation complete. Activate with: .\.venv\Scripts\Activate.ps1"
} else {
    Write-Error "Failed to create virtual environment. Ensure Python is installed and on PATH."
    exit 1
}

