# 👽 Kaomoji Hardware Performance & Responsiveness Analyzer (Alien HUD)

A continuous, real-time command-line hardware performance and system responsiveness analyzer built in Python. Designed for desktop resource monitoring, server health checks, gaming setups, and full-screen terminal dashboards.

Features **Alien Kaomojis**, funny cosmic quotes, 3 real-time ASCII dual-sparkline graphs, a high-precision micro-second kernel responsiveness jitter probe, an adaptive health color state engine, and locked-framerate rendering to eliminate terminal flicker.

---

## ✨ Features

- **📊 3 Real-Time ASCII Graphs**:
  1. **Sub-Space CPU Load (%) vs Responsiveness Jitter (ms)**: Live CPU utilization paired with micro-second kernel scheduling latency.
  2. **Earth Memory Matrix (%) vs Pagefile/Swap (%)**: Side-by-side RAM vs Pagefile/Swap memory load overlay graph.
  3. **Cosmic GPU Core (%) vs VRAM Matrix (%)**: Dual tracking for Dedicated GPU core load vs VRAM utilization.
- **⏱️ System Responsiveness Probe**:
  - High-precision micro-second timer scheduling probe detecting thread stutter, DPC spikes, and kernel interrupts in real time.
- **🎨 Dynamic Health State Engine**:
  - **🟢 OPTIMAL (Green Theme)**: Sub-space silicon synchronized ($\le 1.0\text{ ms}$ jitter), nominal CPU/RAM load.
  - **🟡 WARNING (Yellow Theme)**: Tachyon decoherence / high load ($> 85\%$) or minor micro-stutter ($> 5.0\text{ ms}$).
  - **🔴 CRITICAL (Red Theme)**: Mothership core meltdown ($> 95\%$) or severe thread lag ($> 15\text{ ms}$).
- **🔒 Locked Framerate & Zero Flicker**: Single-buffer ANSI output with cursor re-positioning (`\033[H`) prevents screen flickering.
- **🖥️ Fullscreen Responsive Scaling**: Automatically detects terminal window dimensions (`shutil.get_terminal_size()`) and scales graph widths and heights to fill displays cleanly.
- **⏱️ Sticky Readable Messages**: Cosmic quotes stay visible for 18 seconds and Kaomojis hold for 15 seconds per state for easy reading, without throttling the 10 FPS live metric polling loop.
- **🌐 Cross-Platform Ready**: Windows (Win32 API `GlobalMemoryStatusEx` + WMI/NVML fallbacks), Linux (`psutil`), and macOS.

---

## 📦 Quick Start & Usage

### Option 1: Standalone `.exe` Executable ⭐ (Recommended for Windows)
- **Location**: `HardwareMonitor/dist/HardwareMonitor.exe`
- **Dependencies**: **None** (Python and `pip` are not required).
- **Run**:
  ```cmd
  dist\HardwareMonitor.exe
  ```

---

### Option 2: Direct Python Module
- **Location**: `HardwareMonitor/`
- **Run**:
  ```bash
  python -m HardwareMonitor
  ```

---

## ⚙️ CLI Options

Customize target framerate:

```bash
python -m HardwareMonitor --fps 15
```

- `--fps`: Target framerate limit to prevent screen flicker (default: `10`).

---

## 📁 File Structure

```
HardwareMonitor/
├── README.md            # Documentation and usage guide
├── __main__.py          # CLI entry point with argument parsing
├── core.py              # HardwareAnalyzer engine, metric ring buffers, FPS locked loop, frame assembly
├── utils.py             # RAM/CPU/GPU samplers, ResponsivenessTracker, ASCII graph builders
├── data.json            # Kaomojis, cosmic quotes, and persistent session stats
├── setup.py             # Standard setuptools wheel packaging manifest
├── HardwareMonitor.spec # PyInstaller standalone executable specification
└── dist/                # Standalone executable binaries
    └── HardwareMonitor.exe
```

---

## 📄 Customizing Kaomojis & Messages

All Kaomoji reactions, quotes, and thresholds are stored in [`HardwareMonitor/data.json`](file:///c:/Users/Melody/Desktop/Cassiopeia%20Studios/Codebase/MHS-CodeSnippets/Python/_DesktopTools/HardwareMonitor/data.json). You can edit `data.json` directly to customize Kaomojis or add your own cosmic quotes!
