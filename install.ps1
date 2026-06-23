# Installs the Ukrainian translation for Zoom (Windows).
# Run from the directory containing uk.qm:
#   powershell -ExecutionPolicy Bypass -File install.ps1

$ErrorActionPreference = "Stop"

if (-not (Test-Path "uk.qm")) {
    Write-Error "uk.qm not found. Run this script from the repository root."
    exit 1
}

$candidates = @(
    "$env:APPDATA\Zoom\bin\translations",
    "$env:ProgramFiles\Zoom\bin\translations",
    "${env:ProgramFiles(x86)}\Zoom\bin\translations"
)

$dest = $null
foreach ($path in $candidates) {
    if (Test-Path "$path\uk.qm") {
        $dest = "$path\uk.qm"
        break
    }
}

if (-not $dest) {
    # Broader search as fallback
    $found = Get-ChildItem -Path "$env:APPDATA\Zoom", "$env:ProgramFiles\Zoom" `
        -Filter "uk.qm" -Recurse -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($found) { $dest = $found.FullName }
}

if (-not $dest) {
    Write-Error "Could not find Zoom's uk.qm file. Is Zoom installed?"
    exit 1
}

Copy-Item -Path "uk.qm" -Destination $dest -Force
Write-Host "Installed to $dest"
Write-Host "Restart Zoom for the changes to take effect."
