# ⭐ StellarJiggler ⭐

> "Celestial idle prevention workstation with native Windows wake-lock and hardware mouse emulation."

[![Platform](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-0d1117?style=flat&logo=windows&logoColor=58a6ff)](https://github.com/MelodyHSong/MHS-CodeSnippets)
[![Python](https://img.shields.io/badge/python-3.8%2B-0d1117?style=flat&logo=python&logoColor=f2cc60)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-0d1117?style=flat&color=7ee787)](LICENSE)

**StellarJiggler** is a lightweight, cosmic-themed Windows desktop workstation designed to keep your computer, monitors, screensavers, and workspace communication apps (Microsoft Teams, Slack, Zoom, Skype) continuously active. It accomplishes this via zero-latency Win32 hardware mouse events and native Windows Kernel execution state overrides.

---

## 🌟 Key Features

- 🌌 **Cosmic Command Console**: Handcrafted deep space obsidian aesthetic (`#0d1117`) with starlight cyan, celestial gold, and active mint pulse indicators.
- 🖱️ **Hardware-Level Mouse Simulation**: Dispatches authentic relative mouse move packets via `user32.dll` (`mouse_event`), reliably resetting system idle timers without requiring elevated administrator privileges.
- ⚡ **Windows Kernel Wake Lock**: Direct integration with `kernel32.dll` (`SetThreadExecutionState`) to prevent monitor power-down and lock screens, completely preserving your display state.
- 🛡️ **Smart Activity Guard**: Uses `GetLastInputInfo` to monitor physical keyboard and mouse activity. If you are actively working, StellarJiggler pauses its countdown and defers pulses so it never fights your hand.
- 🎯 **Four Trajectory Modes**:
  - **Subtle Micro-Nudge (±1px)**: Microscopic hardware pulse that restores cursor position immediately. Virtually imperceptible to human eyes, but completely recognized by Windows.
  - **Zen Ghost (0px)**: Absolutely zero mouse cursor movement; relies purely on OS Kernel Wake Lock.
  - **Orbital Circle**: Smooth circular orbit drift (~12px radius) with automated return.
  - **Random Jitter**: Subtle organic micro-wander across random angles.
- ⏱️ **Flexible Pulse Frequency**: Quick interval presets (`10s`, `30s`, `60s`, `2m`, `5m`) alongside a granular 5s–300s slider.
- 📊 **Real-Time Telemetry**: Live digital countdown, smooth progress bar, active uptime stopwatch, total pulses counter, and timestamped color-coded event console.
- 📌 **Always on Top**: Keeps the compact console pinned above other workspace windows for easy monitoring.
- 🖥️ **High-DPI Scaling**: Per-monitor DPI awareness for crisp fonts and graphics on 1080p, 1440p, and 4K displays.
- 🚀 **Zero External Runtime Dependencies**: Built entirely on standard Python modules (`tkinter`, `ctypes`, `threading`, `queue`, `json`).

---

## 🧭 Project Architecture & Structure

```text
Python/_DesktopTools/StellarJiggler/
├── .github/                         # GitHub repository community & automation
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md            # Bug reporting form
│   │   └── feature_request.md       # Feature proposal form
│   ├── workflows/
│   │   └── build-release.yml        # GitHub Actions automated build & release
│   └── FUNDING.yml                  # Funding & sponsorship config
├── assets/
│   ├── app_icon.ico                 # Multi-resolution cosmic icon (256, 48, 32, 16)
│   └── screenshots/
│       └── .gitkeep                 # UI preview screenshots directory
├── misc/
│   └── release_notes.md             # Version release notes draft
├── .editorconfig                    # Editor formatting consistency
├── .gitignore                       # Git ignore rules
├── app.py                           # Main Tkinter application & jiggler engine
├── build.bat                        # 1-click standalone executable builder
├── CHANGELOG.md                     # Semantic version changelog
├── config.json                      # Persistent settings & preferences
├── CONTRIBUTING.md                  # Open-source contributing guidelines
├── generate_icon.py                 # Pillow script synthesizing multi-res icon
├── LICENSE                          # MIT License
├── package_release.py               # Release bundler: compiles .exe, .zip & SHA256
├── requirements.txt                 # Dependencies (Pillow for icon, PyInstaller for build)
├── run.bat                          # Smart launcher (.exe -> pythonw -> python -> py)
└── stellar_jiggler.spec             # PyInstaller compilation specification
```

---

## 🚀 Quick Start & Launching

### Running from Source
1. Ensure Python 3.8+ is installed on your system.
2. Clone or open the repository:
   ```bash
   cd "Python/_DesktopTools/StellarJiggler"
   ```
3. Run the smart launcher:
   ```cmd
   run.bat
   ```
   Or launch directly via Python:
   ```bash
   python app.py
   ```

### ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Space` | Toggle Jiggler Engaged / Disengaged |
| `Ctrl + Q` | Clean exit with wake-lock restoration |

---

## 📦 Building Standalone Executable (.exe)

StellarJiggler can be compiled into a single, portable Windows `.exe` that requires no Python installation:

```cmd
build.bat
```

Or run the full release pipeline (which compiles the binary, stages the portable `.zip` bundle, and computes SHA-256 checksums):

```bash
python package_release.py
```

Compiled binaries and release packages will be saved to the `dist/` directory.

---

## ⚙️ Configuration (`config.json`)

StellarJiggler automatically preserves your preferences across sessions in `config.json`:

```json
{
  "app_name": "StellarJiggler",
  "version": "1.0.0",
  "theme": {
    "palette": "dark_cosmic",
    "high_dpi": true
  },
  "window": {
    "width": 540,
    "height": 680,
    "min_width": 480,
    "min_height": 600,
    "always_on_top": false
  },
  "preferences": {
    "interval_seconds": 30,
    "jiggle_mode": "subtle",
    "smart_pause_enabled": true,
    "smart_pause_threshold_sec": 5,
    "wake_lock_enabled": true,
    "start_active_on_launch": false,
    "stealth_pixels": 1,
    "orbital_radius": 12,
    "log_history_limit": 100
  }
}
```

---

## 🛡️ License

This project is released under the **MIT License**. See [LICENSE](LICENSE) for details.

*Crafted with ♡ by Melody H. Song — Cassiopeia Studios.*
