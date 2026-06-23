#!/usr/bin/env bash
# Installs the Ukrainian translation for Zoom (Linux and macOS).
# Run from the directory containing ru.qm:
#   bash install.sh

set -euo pipefail

if [[ ! -f "ru.qm" ]]; then
    echo "Error: ru.qm not found. Run this script from the repository root."
    exit 1
fi

case "$OSTYPE" in
    linux*)
        DEST="/opt/zoom/translations/ru.qm"
        echo "Installing to $DEST (sudo required)..."
        sudo cp ru.qm "$DEST"
        ;;
    darwin*)
        DEST=$(find /Applications/zoom.us.app -name "ru.qm" 2>/dev/null | head -1)
        if [[ -z "$DEST" ]]; then
            echo "Error: Could not find ru.qm inside Zoom.app. Is Zoom installed in /Applications?"
            exit 1
        fi
        echo "Installing to $DEST..."
        cp ru.qm "$DEST"
        ;;
    *)
        echo "Unsupported OS: $OSTYPE. Use zoom-ua-installer.exe on Windows."
        exit 1
        ;;
esac

echo "Done. Restart Zoom, then right-click its tray/dock icon → Switch Languages → Русский"
