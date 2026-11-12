#!/usr/bin/env bash
# ==============================================================================
# Liquid Glass Dark Icon Theme - Installer
# License: GNU General Public License v3.0
# ==============================================================================

set -eo pipefail

C_RESET='\033[0m'
C_BOLD='\033[1m'
C_GREEN='\033[32m'
C_BLUE='\033[34m'
C_YELLOW='\033[33m'
C_RED='\033[31m'

log_info() {
  printf "${C_BLUE}${C_BOLD}[INFO]${C_RESET} %s\n" "$1"
}

log_success() {
  printf "${C_GREEN}${C_BOLD}[SUCCESS]${C_RESET} %s\n" "$1"
}

log_warn() {
  printf "${C_YELLOW}${C_BOLD}[WARNING]${C_RESET} %s\n" "$1"
}

log_error() {
  printf "${C_RED}${C_BOLD}[ERROR]${C_RESET} %s\n" "$1"
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
THEME_NAME="Liquid-Glass-Dark"
SRC_THEME_DIR="${SCRIPT_DIR}/${THEME_NAME}"

# Fallback check if script is executed from inside the theme folder
if [[ ! -d "${SRC_THEME_DIR}" && -f "${SCRIPT_DIR}/index.theme" ]]; then
  SRC_THEME_DIR="${SCRIPT_DIR}"
fi

# Default installation directory
if [[ "$EUID" -eq 0 ]]; then
  DEST_DIR="/usr/share/icons"
else
  DEST_DIR="${HOME}/.local/share/icons"
fi

usage() {
  cat << USAGE
${C_BOLD}Liquid Glass Dark Icon Theme - Installer${C_RESET}

Usage: $(basename "$0") [OPTIONS]

Options:
  -d, --dest DIR       Specify target destination directory
                       (Default: ${DEST_DIR})
  -n, --name NAME      Specify custom theme name
                       (Default: ${THEME_NAME})
  -a, --all-users      Install system-wide to /usr/share/icons (requires sudo)
  -u, --uninstall      Remove previously installed theme
  -h, --help           Display this help message

Examples:
  ./install.sh                    # Install for current user
  sudo ./install.sh -a            # Install system-wide for all users
  ./install.sh -u                 # Uninstall theme
USAGE
}

UNINSTALL=false

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -d|--dest)
      DEST_DIR="$2"
      shift 2
      ;;
    -n|--name)
      THEME_NAME="$2"
      shift 2
      ;;
    -a|--all-users)
      DEST_DIR="/usr/share/icons"
      shift
      ;;
    -u|--uninstall|--remove)
      UNINSTALL=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      log_error "Unknown option: $1"
      usage
      exit 1
      ;;
  esac
done

TARGET_PATH="${DEST_DIR}/${THEME_NAME}"

# ------------------------------------------------------------------------------
# Uninstall Routine
# ------------------------------------------------------------------------------
if [[ "${UNINSTALL}" == "true" ]]; then
  log_info "Removing '${THEME_NAME}' from '${DEST_DIR}'..."
  if [[ -d "${TARGET_PATH}" || -L "${TARGET_PATH}" ]]; then
    rm -rf "${TARGET_PATH}"
    log_success "Theme '${THEME_NAME}' successfully removed."
  else
    log_warn "Theme '${THEME_NAME}' not found in '${DEST_DIR}'."
  fi
  exit 0
fi

# ------------------------------------------------------------------------------
# Installation Routine
# ------------------------------------------------------------------------------
if [[ ! -d "${SRC_THEME_DIR}" ]]; then
  log_error "Source theme directory not found at: ${SRC_THEME_DIR}"
  exit 1
fi

log_info "Installing '${THEME_NAME}' into '${DEST_DIR}'..."
mkdir -p "${DEST_DIR}"

# Remove existing installation to avoid stale caches or symlinks
if [[ -d "${TARGET_PATH}" || -L "${TARGET_PATH}" ]]; then
  log_info "Removing existing installation at '${TARGET_PATH}'..."
  rm -rf "${TARGET_PATH}"
fi

cp -a "${SRC_THEME_DIR}" "${TARGET_PATH}"

log_info "Updating GTK icon cache..."
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache -f -q "${TARGET_PATH}" || true
  log_success "GTK icon cache updated."
else
  log_warn "gtk-update-icon-cache command not found; skipping cache update."
fi

# Optional legacy ~/.icons symlink for maximum compatibility with older software
if [[ "$EUID" -ne 0 && "${DEST_DIR}" == "${HOME}/.local/share/icons" ]]; then
  mkdir -p "${HOME}/.icons"
  if [[ ! -e "${HOME}/.icons/${THEME_NAME}" ]]; then
    ln -s "${TARGET_PATH}" "${HOME}/.icons/${THEME_NAME}" || true
    log_info "Created compatibility symlink at '~/.icons/${THEME_NAME}'."
  fi
fi

log_success "Installation complete! '${THEME_NAME}' is now ready to use."
printf "\n${C_BOLD}To apply the icon theme:${C_RESET}\n"
printf "  • GNOME:         gsettings set org.gnome.desktop.interface icon-theme '%s'\n" "${THEME_NAME}"
printf "  • XFCE:          xfconf-query -c xsettings -p /Net/IconThemeName -s '%s'\n" "${THEME_NAME}"
printf "  • KDE Plasma:    kwriteconfig5 --file kdeglobals --group Icons --key Theme '%s'\n" "${THEME_NAME}"
printf "  • Or select it graphically in your desktop environment's Appearance / Theme Settings.\n\n"
