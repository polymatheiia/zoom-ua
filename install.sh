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
        DEST=$(find \
            /Applications/zoom.us.app \
            ~/Applications/zoom.us.app \
            ~/Library/Application\ Support/zoom.us \
            -name "ru.qm" 2>/dev/null | head -1)
        if [[ -z "$DEST" ]]; then
            echo "Error: Could not find ru.qm in any known Zoom location."
            echo ""
            echo "Diagnostic — all .qm files found in Zoom directories:"
            find /Applications/zoom.us.app ~/Applications/zoom.us.app \
                 ~/Library/Application\ Support/zoom.us \
                 -name "*.qm" 2>/dev/null || true
            echo ""
            echo "Please share the output above at:"
            echo "  https://github.com/polymatheiia/zoom-ua/issues"
            echo "  or github@grabovska.com"
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
