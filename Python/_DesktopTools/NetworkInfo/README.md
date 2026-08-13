# 👽 Network Performance Analyzer (Alien HUD)

A continuous, real-time command-line network performance analyzer built in Python. Designed for dedicated laptop displays, server monitoring, and full-screen terminal dashboards.

Features **Alien Kaomojis**, funny cosmic quotes, 3 real-time ASCII sparkline graphs, an adaptive health color state machine, and locked-framerate rendering to eliminate terminal flicker.

---

## ✨ Features

- **📊 3 Real-Time ASCII Graphs**:
  1. **Sub-Space Bandwidth Speed**: Live network throughput in B/s, KB/s, MB/s, or GB/s.
  2. **Cosmic Latency (Ping)**: Live round-trip latency graph in milliseconds (`ms`).
  3. **Telemetry Transmission (Dual Graph)**: Side-by-side Download (Cyan) vs Upload (Magenta) bandwidth traffic.
- **🎨 Dynamic Health State Engine**:
  - **🟢 OPTIMAL (Green Theme)**: Active link with sub-space low latency ($\le 100\text{ ms}$).
  - **🟡 MARGINAL (Yellow Theme)**: High cosmic jitter or latency spikes ($> 100\text{ ms}$).
  - **🔴 DROPPED (Red Theme)**: Signal lost, network disconnection, or ping timeout (`OFFLINE`).
- **🔒 Locked Framerate & Zero Flicker**: Single-buffer ANSI output with cursor re-positioning (`\033[H`) prevents terminal screen flickering.
- **🖥️ Fullscreen Responsive Scaling**: Automatically detects terminal window dimensions (`shutil.get_terminal_size()`) and scales graph widths and heights to fill laptop displays cleanly.
- **⏱️ Dynamic Animated Quotes & Kaomojis**: Cosmic quotes and Kaomojis rotate every second for a lively animated HUD display without throttling the 10 FPS live metric polling loop.
- **🌐 Cross-Platform Ready**: Windows (psutil + PowerShell CIM fallback), Linux (psutil + `/proc/net/dev` native kernel fallback), and macOS.

---

## 📦 Distribution & Quick Start

Everything belonging to the utility is packaged inside this directory:

### Option 1: Standalone `.exe` Executable ⭐ (Recommended for Windows Laptop)
- **Location**: `NetworkInfo/dist/NetworkInfo.exe`
- **Dependencies**: **None** (Python and `pip` are not required).
- **Run**:
  ```cmd
  dist\NetworkInfo.exe
  ```

---

### Option 2: Python Wheel (`.whl`)
- **Location**: `NetworkInfo/dist/networkinfo-1.0.0-py3-none-any.whl`
- **Dependencies**: Any system with Python 3.7+.
- **Install & Run**:
  ```bash
  pip install dist/networkinfo-1.0.0-py3-none-any.whl
  networkinfo
  ```

---

### Option 3: Direct Python Module
- **Location**: `NetworkInfo/`
- **Run**:
  ```bash
  python -m NetworkInfo
  ```

---

## ⚙️ CLI Options

Customize framerate or target ping host:

```bash
python -m NetworkInfo --fps 15 --target 1.1.1.1
```

- `--fps`: Target framerate limit to prevent screen flicker (default: `10`).
- `--target`: IP address or domain to measure ping latency (default: `8.8.8.8`).

---

## 📁 File Structure

```
NetworkInfo/
├── README.md         # Documentation and usage guide
├── __main__.py       # CLI entry point with argument parsing
├── core.py           # NetworkAnalyzer engine, metric ring buffers, FPS locked loop, frame assembly
├── utils.py          # Network IO sampler, latency thread, ASCII graph builders, UTF-8 renderer
├── data.json         # Kaomojis, alien quotes, thresholds, and persistent session stats
├── setup.py          # Standard setuptools wheel packaging manifest
├── NetworkInfo.spec  # PyInstaller standalone executable specification
└── dist/             # Pre-built distribution binaries
    ├── NetworkInfo.exe
    └── networkinfo-1.0.0-py3-none-any.whl
```

---

## 📄 Customizing Kaomojis & Messages

All Kaomoji reactions, quotes, and thresholds are stored in [`data.json`](data.json). You can edit `data.json` directly to add your own custom Kaomojis, memes, or adjust latency thresholds!
