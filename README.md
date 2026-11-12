# Liquid Glass Dark Icon Theme

<p align="center">
  <img src="https://img.shields.io/badge/Release-v1.0.0-blue?style=for-the-badge" alt="Release">
  <img src="https://img.shields.io/badge/License-GPL--3.0-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Platform-Linux-orange?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/Desktops-GNOME%20%7C%20XFCE%20%7C%20KDE%20%7C%20Cinnamon-purple?style=for-the-badge" alt="Compatibility">
</p>

A modern, high-fidelity macOS **Liquid Glass** dark icon theme for Linux desktops. It unites the depth-rich, translucent squircle aesthetics of macOS Liquid Glass with next-generation **macOS Tahoe** directory folders and a sleek, high-contrast dark status bar panel.

---

## Highlights & Features

* **Liquid Glass Application Squircles**: Authentic glassy dark application icons featuring reflections, inner glows, and layered textures.
* **Dock-Perfect Proportions**: All application icons are normalized to an authentic **81.25% canvas ratio** (416px active squircle content on a 512px canvas), eliminating oversized or stretched icons in **Plank**, **Dash to Dock**, **Cairo-Dock**, and **Latte Dock**.
* **macOS Tahoe Directory Folders**: Rounded, sky-blue folder icons with debossed monochrome glyphs for standard XDG directories:
  * Downloads, Documents, Pictures, Music, Videos
  * Desktop, User Home, Templates, Public Share, and generic folders.
* **High-Contrast Dark Status Panel**:
  * **Audio / Volume**: macOS speaker glyph with 3 acoustic wave arcs and muted states.
  * **Network & Wi-Fi**: Multi-level radiating signal arcs and Ethernet indicators.
  * **Battery & Power Manager**: Sleek battery capsule with charge states and lightning bolt charging indicator.
  * **Bluetooth**: Authentic Bluetooth rune for Blueman and system trays.
  * **Night Shift / Redshift**: Custom radiant warm amber sun for active night mode and soft outline sun when disabled.
* **Desktop Integration Fixes**:
  * Pre-configured `StartupWMClass=Mail` descriptor for Mozilla Thunderbird preventing duplicate dock instances.
  * Native desktop docklet and panel icon support (`show-desktop` and `org.xfce.panel.showdesktop`).

---

## Desktop Environment Compatibility

| Desktop Environment | Supported | Notes |
| :--- | :---: | :--- |
| **XFCE** (4.16, 4.18, 4.20) | Full | Native support for panel plugins, systray, and Thunar. |
| **GNOME Shell** (3.38 – 47+) | Full | Compatible with Tweaks, Dash to Dock, and Nautilus. |
| **KDE Plasma** (5 & 6) | Full | Compatible with System Settings and Dolphin. |
| **Cinnamon** | Full | Works with panel applets and Nemo. |
| **MATE / Budgie / LXQt** | Full | Fully compliant with FreeDesktop icon theme specs. |

---

## Installation

### Method 1: Automated Installation Script (Recommended)

Clone the repository and run the installer:

```bash
git clone https://github.com/Yhorx/Liquid-Glass-Icons.git
cd Liquid-Glass-Icons
chmod +x install.sh
./install.sh
```

To install system-wide for all users:

```bash
sudo ./install.sh -a
```

### Method 2: Manual Installation (GNOME-Look / Pling)

1. Download the latest `Liquid-Glass-Dark.tar.xz` or `Liquid-Glass-Dark.tar.gz` archive from the Releases page or [GNOME-Look.org](https://www.gnome-look.org/browse?cat=132&ord=latest).
2. Extract the archive into your personal icons directory:
   ```bash
   mkdir -p ~/.local/share/icons
   tar -xf Liquid-Glass-Dark.tar.xz -C ~/.local/share/icons/
   ```
3. Update the icon cache:
   ```bash
   gtk-update-icon-cache -f ~/.local/share/icons/Liquid-Glass-Dark/
   ```

---

## Applying the Theme

### Via Command Line

* **GNOME**:
  ```bash
  gsettings set org.gnome.desktop.interface icon-theme "Liquid-Glass-Dark"
  ```
* **XFCE**:
  ```bash
  xfconf-query -c xsettings -p /Net/IconThemeName -s "Liquid-Glass-Dark"
  ```
* **KDE Plasma**:
  ```bash
  kwriteconfig5 --file kdeglobals --group Icons --key Theme "Liquid-Glass-Dark"
  ```

### Via Graphical Settings
* **GNOME**: Open **GNOME Tweaks** -> **Appearance** -> **Icons** -> Select **Liquid-Glass-Dark**.
* **XFCE**: Open **Settings** -> **Appearance** -> **Icons** -> Select **Liquid-Glass-Dark**.
* **KDE Plasma**: Open **System Settings** -> **Appearance** -> **Icons** -> Select **Liquid-Glass-Dark**.

---

## Plank Dock Optimization Tips

For the most authentic macOS dock presentation:
* **Icon Size**: Set Plank icon size between **64px** and **72px** (`Preferences` -> `Appearance` -> `Icon Size: 70`).
* **Theme**: Use a frosted glass or transparent Plank theme (e.g., Matte or Transparent).
* **Show Desktop Docklet**: The desktop toggle icon in Plank (`docklet://desktop`) automatically maps to the Tahoe Desktop folder icon.

---

## Uninstallation

To remove the theme, run the provided uninstaller:

```bash
./uninstall.sh
```

Or remove the theme directory manually:

```bash
rm -rf ~/.local/share/icons/Liquid-Glass-Dark ~/.icons/Liquid-Glass-Dark
```

---

## Credits & Acknowledgements

* **Application Icons**: The [macOSicons](https://macosicons.com) community of graphic designers.
* **Design Language**: Inspired by Apple Inc. macOS Big Sur, Monterey, Sonoma, and Tahoe design concepts.

---

## License

This project is licensed under the **GNU General Public License v3.0** (GPL-3.0). See the [LICENSE](LICENSE) file for details.
