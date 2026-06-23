#!/usr/bin/env bash
# Installs the Ukrainian translation for Zoom (Linux and macOS).
# Run from the directory containing uk.qm:
#   bash install.sh

set -euo pipefail

if [[ ! -f "uk.qm" ]]; then
    echo "Error: uk.qm not found. Run this script from the repository root."
    exit 1
fi

case "$OSTYPE" in
    linux*)
        DEST="/opt/zoom/translations/uk.qm"
        echo "Installing to $DEST (sudo required)..."
        sudo cp uk.qm "$DEST"
        ;;
    darwin*)
        DEST=$(find /Applications/zoom.us.app -name "uk.qm" 2>/dev/null | head -1)
        if [[ -z "$DEST" ]]; then
            echo "Error: Could not find uk.qm inside Zoom.app. Is Zoom installed in /Applications?"
            exit 1
        fi
        echo "Installing to $DEST..."
        cp uk.qm "$DEST"
        ;;
    *)
        echo "Unsupported OS: $OSTYPE. Use install.ps1 on Windows."
        exit 1
        ;;
esac

echo "Done. Restart Zoom for the changes to take effect."
