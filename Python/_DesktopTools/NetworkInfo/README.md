# ☆ Melody's Starship Network Visor ☆

> "Pinging distant galaxies... sub-space network telemetry online!"

Welcome to **Melody's Starship Network Visor**! 👽📡 This is a continuous, terminal-based network monitoring dashboard powered by cute alien expressions, hilarious cosmic commentary, real-time ASCII sparkline graphs, and sub-space latency tracking.

Perfect for keeping an eye on your Wi-Fi/Ethernet speed, monitoring ping spikes during gaming sessions, or having a cool sci-fi HUD running on a secondary laptop display.

### ✨ Key Features

- 📊 **Triple Real-Time ASCII Graphs**:
  - **Sub-Space Bandwidth Speed**: Live network throughput auto-scaled (B/s, KB/s, MB/s, GB/s).
  - **Cosmic Latency (Ping)**: Real-time round-trip latency tracking in milliseconds (ms).
  - **Telemetry Transmission**: Side-by-side Download (Cyan) vs Upload (Magenta) traffic graphs.
- 🎨 **Dynamic Health Engine**: Adapts terminal colors based on your network health:
  - 🟢 **OPTIMAL**: Strong link with sub-space low latency ($\le 100\text{ ms}$).
  - 🟡 **MARGINAL**: High cosmic jitter or ping spikes detected ($> 100\text{ ms}$).
  - 🔴 **DROPPED**: Signal lost, network connection down, or ping timeout (`OFFLINE`).
- 🔒 **Flicker-Free Rendering**: Single-buffer ANSI cursor re-positioning (`\033[H`) with capped framerate loop.
- 🖥️ **Responsive Auto-Scaling**: Dynamically resizes graphs to fill your terminal window cleanly.
- 🌐 **Cross-Platform Ready**: Windows (`psutil` + PowerShell fallback), Linux (`psutil` + kernel fallback), and macOS.

---

## ☆ Installation & Prerequisites

Get running in seconds! Choose between pre-built binaries, a Python wheel package, or running directly with Python.

- **For Standalone Executable**: Zero dependencies required!
- **For Wheel/Python Module**: Python 3.7+ and `psutil`.

### Quick Install

**Option 1: Standalone `.exe` (Recommended for Windows)**
Run directly without needing Python installed:
```cmd
dist\NetworkInfo.exe
```

**Option 2: Install Python Wheel (`.whl`)**
```bash
pip install dist/networkinfo-1.0.0-py3-none-any.whl
networkinfo
```

**Option 3: Direct Python Execution**
```bash
python -m NetworkInfo
```

---

## ☆ Usage

Launch the network analyzer from your terminal or command prompt.

### Example Usage

Standard run with default ping target (`8.8.8.8`) at 10 FPS:
```bash
python -m NetworkInfo
```

Custom framerate and custom ping target:
```bash
python -m NetworkInfo --fps 15 --target 1.1.1.1
```

- `--fps`: Target framerate limit to eliminate screen flicker (Default: `10`).
- `--target`: IP address or domain hostname to ping (Default: `8.8.8.8`).

---

## ☆ Customization

Want to add your own alien expressions, tweak ping warning thresholds, or write custom alien quotes?

All alien reactions, messaging, and alert thresholds are configured inside [`data.json`](file:///c:/Users/Melody/Desktop/Cassiopeia%20Studios/Codebase/MHS-CodeSnippets/Python/_DesktopTools/NetworkInfo/data.json). Feel free to tweak them to your heart's content!

---

## ☆ File Structure

```
NetworkInfo/
├── README.md         # Documentation and usage guide
├── __main__.py       # CLI entry point & argument parser
├── core.py           # NetworkAnalyzer engine & telemetry loop
├── utils.py          # Network samplers & ASCII graph renderers
├── data.json         # Alien expressions, quotes, thresholds, and stats
├── setup.py          # Wheel packaging manifest
├── NetworkInfo.spec  # PyInstaller executable spec
└── dist/             # Pre-built executable & wheel distribution
    ├── NetworkInfo.exe
    └── networkinfo-1.0.0-py3-none-any.whl
```

---

## ☆ License

This project is licensed under the MIT License. You are free to use, modify, and distribute this code in your own projects— just keep the headers intact!

---

*(If your ping spikes over 9000ms, blaming cosmic radiation interference is officially permitted.) — MelodyHSong*

