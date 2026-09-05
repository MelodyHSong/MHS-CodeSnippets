# ☆ Melody's Starship Network Visor ☆

> "Pinging distant galaxies... sub-space network telemetry online!"

Greetings, Earthling! 🛸👋✨ Strap yourself into the pilot's chair and welcome to **Melody's Starship Network Visor**! 

Ever wonder if your dropped packets got sucked into a passing black hole, or if solar flare space dust is choking your Wi-Fi antenna? 🌌📡 The **Starship Network Visor** is a quirky, delightfully cosmic desktop dashboard that monitors your real-time internet speeds, tracks galactic ping latency, and translates boring network statistics into expressive alien kaomojis and chaotic space chatter.

Park it on a secondary monitor during intense gaming sessions, watch your broadband beams surge while downloading massive files, or just enjoy having a friendly little alien co-pilot keeping watch over your home galaxy connection.

---

## ✨ Features From Across the Cosmos

- 📊 **Triple Real-Time Hologram Charts**:
  - **Sub-Space Bandwidth Beams**: Live speed curves auto-scaling from tiny bytes all the way to warp-speed gigabytes (B/s, KB/s, MB/s, GB/s)!
  - **Cosmic Latency Radar**: Real-time ping timeline monitoring round-trip millisecond delays, with an amber alert threshold for solar flare spikes and red markers for dropped packets.
  - **Dual Telemetry Streams**: Download (Starlight Cyan) and Upload (Nebula Magenta) traffic dancing side-by-side across the timeline.
- 🎨 **Dynamic Link Health Indicator**:
  - 🟢 **OPTIMAL**: Crystal-clear connection with sub-space low latency ($\le 100\text{ ms}$).
  - 🟡 **MARGINAL**: Wormhole turbulence, high cosmic jitter, or ping spikes detected ($> 100\text{ ms}$).
  - 🔴 **DROPPED**: Signal lost, mothership offline, or cable unplugged (`OFFLINE`).
- 👽 **Moody Alien Co-Pilot & Reactive Kaomojis**:
  - A responsive alien face in your cockpit who celebrates when signals are crisp, sweats nervously during packet jitter, and flatlines when the internet drops into the void!
- 🛸 **Sub-Space Relay Chatter (Cosmic Ticker)**:
  - An interstellar newsfeed cycling hilarious intercepted transmissions, SETI radio gossip, and alien commentary from Sector 7G.
- 🌐 **Deep Hardware & Adapter Sniffing**:
  - Automatically identifies your terrestrial network adapter, local planet IPv4 address, and hardware MAC address without sluggish subprocesses.
- 💾 **Holocron Telemetry Exports**:
  - Snapshot your full bandwidth and ping history straight into `.json` or `.csv` format at any time with `Ctrl + E`.
- 🚀 **Zero-Bureaucracy 1-Click Launch**:
  - Installs cleanly into your user profile with a custom Alien Flying Saucer icon—no annoying Earthling Administrator / UAC popups required!
- 🔄 **Dual Engine Modes**:
  - **Starship Desktop GUI (Default)**: Modern, windowless Tkinter cockpit dashboard powered by Python or standalone `.exe`.
  - **Retro Terminal HUD**: Run with `--cli` for a flicker-free ANSI ASCII console experience when exploring headless servers.

---

## ☆ Installation & Starship Setup

### Option 1: 1-Click Setup (Easiest)
Simply double-click:
```cmd
install.bat
```
This drops the **Melody's Starship Network Visor** shortcut directly onto your Windows Desktop and Start Menu with the custom alien ship icon!

### Option 2: Terminal Navigation
Prefer taking manual control of the console? You can manage everything via terminal:

```bash
# Auto-detect and install (prefers standalone .exe if compiled, falls back to pythonw)
python setup_desktop.py --install

# Install specifically in Python script mode
python setup_desktop.py --install --mode python

# Inspect installation and shortcut status
python setup_desktop.py --status

# Rebuild the standalone executable with PyInstaller
python setup_desktop.py --build
```

### Option 3: Interactive Starship Menu
Run the setup tool without flags to launch the interactive terminal deck:
```bash
python setup_desktop.py
```
```text
============================================================
      🛸 NETWORK VISOR — DESKTOP SETUP & BUILDER 📡      
============================================================
  [1] Install Desktop & Start Menu Shortcuts (Standalone .EXE)
  [2] Install Desktop & Start Menu Shortcuts (Python Script / Dev)
  [3] Check Installation Status
  [4] Rebuild Standalone Executable (PyInstaller)
  [5] Uninstall Desktop Shortcuts
  [6] Exit
------------------------------------------------------------
```

---

## ☆ Flying the Ship (Usage)

### 🖱️ 1-Click Launch
Double-click `run.bat` or the Desktop shortcut created during setup:
```cmd
run.bat
```

### 💻 Command Line Flights

**Desktop Cockpit HUD (Default):**
```bash
# Standard warp speed launch
python network_info.py

# Or via package module
python -m NetworkInfo

# Target a custom space beacon (e.g., Cloudflare 1.1.1.1) at 15 FPS
python -m NetworkInfo --target 1.1.1.1 --fps 15
```

**Classic Terminal HUD (For Cyberpunk Explorers):**
```bash
python -m NetworkInfo --cli
```

### ⌨️ Cockpit Controls & Hotkeys
| Shortcut | Action |
| :--- | :--- |
| `Space` | Pause / Resume live telemetry stream |
| `Ctrl + R` | Reset session telemetry counters and peak records |
| `Ctrl + T` | Open Target Beacon dialog (Change Ping Target) |
| `Ctrl + E` | Export session telemetry holocron (JSON / CSV) |
| `Ctrl + S` | Open Cockpit Telemetry Settings panel |
| `Ctrl + Q` / `Esc` | Safely park the ship, log stats, and exit |

---

## ☆ Customization & Alien Lore

Want to teach the alien pilot your own bizarre quotes, tweak ping panic thresholds, or change default beacon servers?

All alien reactions, transmissions, and telemetry thresholds live inside [`data.json`](data.json):

```json
{
  "settings": {
    "target_fps": 10,
    "ping_target": "8.8.8.8",
    "ping_interval": 0.8,
    "latency_marginal_ms": 100.0
  },
  "alien_kaomojis": { ... },
  "alien_messages": [ ... ]
}
```

Toss in your own hilarious alien quotes, adjust ping sensitivity, and make the starship uniquely yours!

---

## ☆ Starship Architecture

```
NetworkInfo/
├── assets/                  # High-resolution cosmic icons
│   ├── network_info.ico     # Multi-res Windows icon (256, 48, 32, 16)
│   └── network_info.png     # 256x256 Alien Saucer PNG asset
├── build.bat                # 1-Click PyInstaller executable builder
├── data.json                # Alien expressions, lore, settings & stats
├── generate_icon.py         # Pillow-based multi-resolution icon generator
├── install.bat              # 1-Click Desktop & Start Menu shortcut installer
├── LICENSE                  # MIT License (Melody H. Song / Cassiopeia Studios)
├── network_info.py          # Starship Network Visor desktop GUI workstation
├── NetworkInfo.spec         # PyInstaller windowed executable specification
├── README.md                # Cosmic documentation & flight manual
├── requirements.txt         # Documented Python dependencies
├── run.bat                  # 1-Click application launcher
├── setup_desktop.py         # Shortcut installer & PyInstaller builder utility
├── setup.py                 # Setuptools package manifest
├── uninstall.bat            # 1-Click Desktop shortcut uninstaller
├── utils.py                 # Network samplers, Win32 ICMP ping & telemetry helpers
├── core.py                  # Classic terminal ANSI HUD engine
├── __init__.py              # Package initialization
└── __main__.py              # Dual-mode entry point (GUI default, CLI via --cli)
```

---

## ☆ Uninstallation

To cleanly decommission the desktop and start menu shortcuts at any time:
- **1-Click**: Double-click `uninstall.bat`
- **CLI**: `python setup_desktop.py --uninstall`

All shortcuts are cleanly purged without leaving any space debris behind.

---

## ☆ License

This project is licensed under the MIT License. You are free to explore, modify, and transmit this software across the universe—just keep the author headers intact!

*Made with 🛸 by Melody H. Song / Cassiopeia Studios*
