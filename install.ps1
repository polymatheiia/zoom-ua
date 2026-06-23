# Installs the Ukrainian translation for Zoom (Windows).
# Alternative to zoom-ua-installer.exe for advanced users.
# Run from the directory containing ru.qm:
#   powershell -ExecutionPolicy Bypass -File install.ps1

$ErrorActionPreference = "Stop"

if (-not (Test-Path "ru.qm")) {
    Write-Error "ru.qm not found. Run this script from the repository root."
    exit 1
}

$candidates = @(
    "$env:APPDATA\Zoom\bin\translations",
    "$env:ProgramFiles\Zoom\bin\translations",
    "${env:ProgramFiles(x86)}\Zoom\bin\translations"
)

$dest = $null
foreach ($path in $candidates) {
    if (Test-Path "$path\ru.qm") {
        $dest = "$path\ru.qm"
        break
    }
}

if (-not $dest) {
    $found = Get-ChildItem -Path "$env:APPDATA\Zoom", "$env:ProgramFiles\Zoom" `
        -Filter "ru.qm" -Recurse -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($found) { $dest = $found.FullName }
}

if (-not $dest) {
    Write-Error "Could not find Zoom's ru.qm file. Is Zoom installed?"
    exit 1
}

Copy-Item -Path "ru.qm" -Destination $dest -Force
Write-Host "Installed to $dest"
Write-Host "Restart Zoom and set language: Settings -> General -> Language -> Русский"
