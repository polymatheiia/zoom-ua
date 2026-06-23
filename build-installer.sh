#!/usr/bin/env bash
# Rebuild zoom-ua-installer.exe after updating ru.qm.
# Requires Go with Windows cross-compilation support.
set -euo pipefail

cp ru.qm installer/ru.qm
GOOS=windows GOARCH=amd64 go build \
    -C installer \
    -ldflags="-H windowsgui -s -w" \
    -o ../zoom-ua-installer.exe \
    .
rm installer/ru.qm
echo "Built: zoom-ua-installer.exe ($(du -h zoom-ua-installer.exe | cut -f1))"
