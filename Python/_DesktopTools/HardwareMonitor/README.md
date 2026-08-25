# ☆ Melody's Starship Hardware Analyzer ☆

> "May your frame rates stay high and your silicon temperatures stay cool in the cosmos."

Welcome to **Melody's Starship Hardware Analyzer**! 👽✨ This is a real-time, terminal-based hardware monitoring HUD that brings your terminal display to life with cute alien expressions, hilarious cosmic commentary, real-time ASCII dual-sparkline graphs, and microsecond system latency tracking.

Whether you're stress-testing a gaming rig, keeping an eye on server health, or just want a sleek, flicker-free sci-fi dashboard on your screen, this tool keeps you informed in style.

<img width="2212" height="1156" alt="image" src="https://github.com/user-attachments/assets/26b1fa6b-6a2e-474f-aacf-44c5b5f2dba1" />


### ✨ Key Features

- 📊 **Triple Real-Time ASCII Dual-Graphs**:
  - **Sub-Space CPU Load vs Jitter**: Tracks CPU usage (%) alongside microsecond kernel thread scheduling latency (ms).
  - **Earth Memory Matrix vs Swap**: Overlay graph of physical RAM vs Pagefile/Swap utilization.
  - **Cosmic GPU Core vs VRAM**: Dual telemetry tracking GPU core load (%) and VRAM allocation (%).
- ⏱️ **Microsecond Responsiveness Probe**: Detects subtle thread stuttering, DPC spikes, and kernel lags in real time.
- 🎨 **Dynamic Health Engine**: Automatically switches color themes based on hardware status:
  - 🟢 **OPTIMAL**: Silicon perfectly synced, low jitter & load.
  - 🟡 **WARNING**: High load or minor micro-stutter detected.
  - 🔴 **CRITICAL**: Core overload or severe scheduling lag.
- 🔒 **Flicker-Free Rendering**: Single-buffer ANSI positioning with capped framerate rendering (`\033[H`).
- 🖥️ **Responsive Auto-Scaling**: Dynamically adjusts graph sizes to fit your full-screen or side-terminal window.
- 🌐 **Cross-Platform Ready**: Windows (Win32 API + WMI/NVML), Linux (`psutil`), and macOS.

---

## ☆ Installation & Prerequisites

No complicated setups! You can run this tool directly as a standalone executable (no Python needed) or execute it via Python.

- **For Standalone Executable**: No prerequisites required!
- **For Python Module**: Python 3.7+ with `psutil` (optional `pynvml` / `WMI` on Windows for GPU stats).

### Quick Install

**Option 1: Standalone `.exe` (Recommended for Windows)**
Run the pre-compiled binary directly without installing Python:
```cmd
dist\HardwareMonitor.exe
```

**Option 2: Direct Python Execution**
Run directly as a Python module:
```bash
python -m HardwareMonitor
```

---

## ☆ Usage

Launch the monitor from your terminal of choice (PowerShell, Command Prompt, Windows Terminal, Alacritty, iTerm2, etc.).

### Example Usage

Run with default settings (10 FPS flicker-free update loop):
```bash
python -m HardwareMonitor
```

Customize the target framerate limit:
```bash
python -m HardwareMonitor --fps 15
```

- `--fps`: Set frame rate cap to prevent terminal flicker (Default: `10`).

---

## ☆ Customization

Want to add your own alien expressions or write funny cosmic status quotes?

All alien reactions, status messages, and alert thresholds live inside [`data.json`](file:///c:/Users/Melody/Desktop/Cassiopeia%20Studios/Codebase/MHS-CodeSnippets/Python/_DesktopTools/HardwareMonitor/data.json). Feel free to customize them to match your personal vibe!

---

## ☆ File Structure

```
HardwareMonitor/
├── README.md            # Documentation and usage guide
├── __main__.py          # CLI entry point & argument parser
├── core.py              # HardwareAnalyzer engine & render loop
├── utils.py             # Hardware samplers & ASCII graph renderers
├── data.json            # Alien expressions, cosmic quotes, and alert thresholds
├── setup.py             # Packaging manifest
├── HardwareMonitor.spec # PyInstaller spec file
└── dist/                # Pre-built standalone executable
    └── HardwareMonitor.exe
```

---

## ☆ License

This project is licensed under the MIT License. You are free to use, modify, and distribute this code in your own projects— just keep the headers intact!

---

*(Remember: if your CPU turns into a miniature star, it's just operating at peak cosmic efficiency!) — MelodyHSong*

