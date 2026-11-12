#!/usr/bin/env bash
# ==============================================================================
# Liquid Glass Dark Icon Theme - Uninstaller
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"${SCRIPT_DIR}/install.sh" --uninstall "$@"
