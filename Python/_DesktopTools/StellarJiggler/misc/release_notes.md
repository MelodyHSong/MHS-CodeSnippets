# ⭐ StellarJiggler v1.0.0 — Official Galactic Release 🛸

> *"Celestial idle prevention workstation with native Windows wake-lock and hardware mouse emulation."*

Welcome to the inaugural release of **StellarJiggler**! Designed as a sleek, cosmic workstation that keeps your PC, screensaver, and communication tools (Teams, Slack, Zoom) active with imperceptible hardware micro-nudges and native Windows kernel wake-locks.

---

## 🌟 Key Highlights & Features

### 🎨 Cosmic Workstation UI
- Handcrafted obsidian theme inspired by deep space command centers (`#0d1117`, `#161b22`, `#21262d`).
- Windows High-DPI awareness (`ctypes.windll.shcore`) ensuring ultra-crisp fonts and icons on 1080p, 1440p, and 4K displays.
- Real-time pulse countdown, session uptime stopwatch, and color-coded telemetry activity console.

### 🖱️ Hardware-Level Mouse Emulation
- Direct Win32 hardware relative cursor events (`mouse_event(0x0001, dx, dy, 0, 0)`).
- **Subtle Micro-Nudge Mode (±1px)**: Shifts cursor 1 pixel and restores it instantly—imperceptible to your eyes, but fully recognized by Windows and workplace apps.
- **Zen Ghost Mode (0px)**: Refreshes the OS Kernel Wake Lock with absolutely zero cursor movement.
- **Orbital Circle Mode**: Drifts the cursor smoothly around a cosmic orbit (~12px radius) and returns.
- **Random Jitter Mode**: Organic micro-jitter for natural activity patterns.

### 🛡️ Smart Activity Guard
- Monitors physical keyboard and mouse activity via `GetLastInputInfo`.
- If you are actively typing or moving the mouse, StellarJiggler quietly defers the pulse so it never interrupts your workflow.

### ⚡ Windows Kernel Wake Lock
- Calls `SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)` to prevent monitor sleep or lock screens without modifying system power plans.

### ⚙️ Customizable Timing & Pinning
- Pulse frequency slider (5s to 300s) + quick presets (`10s`, `30s`, `60s`, `120s`, `5m`).
- "Always on Top" toggle to pin above all desktop windows.

---

## ⌨️ Keyboard Shortcuts Reference

| Shortcut | Action |
| :--- | :--- |
| `Space` | Toggle Jiggler Engaged / Disengaged |
| `Ctrl + Q` | Clean exit with wake-lock release |

---

## 📦 Installation & Setup

### 1. Standalone Portable Package (Recommended)
Download `stellar_jiggler.exe` (or `StellarJiggler-Windows-x64.zip`) from the release assets:
1. Extract the `.zip` to your desired folder.
2. Double-click `run.bat` or `stellar_jiggler.exe` to launch!

### 2. Running From Source (Development Mode)
```bash
git clone https://github.com/MelodyHSong/MHS-CodeSnippets.git
cd "Python/_DesktopTools/StellarJiggler"
python -m pip install -r requirements.txt
python app.py
```

---

- **Compatibility**: Windows 10 / Windows 11 (x64)
- **Runtime Dependencies**: None! Standard library `ctypes` & `tkinter` only.
- **Dev Requirements**: Python 3.8+ (Pillow only needed if synthesizing icons).

---

*Made with ♡ by Melody H. Song (Cassiopeia Studios)*
