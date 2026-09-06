# ⭐ Stellar Visor v2.0.0 — The Cosmic Rebrand & Telemetry HUD Overhaul 🛸📡

> *"Pinging distant galaxies... sub-space network telemetry online!"*

Welcome to the landmark **v2.0.0** release of **Stellar Visor**! ⭐🛸📡

Formerly known as *Starship Network Visor* (`NetworkInfo`), this major release represents a full cosmic rebrand and architectural overhaul. **Stellar Visor** officially joins the cosmic desktop utility family crafted by **Melody H. Song** and **Cassiopeia Studios**, aligning alongside sibling tools **[StellarNotes](https://github.com/MelodyHSong/StellarNotes)** (cosmic desktop note-taking and voice narration) and **[Stellar Snooper](https://github.com/MelodyHSong/Stellar-Snooper)** (cosmic storage analysis and disk space investigator).

Whether you are monitoring bandwidth surges during warp-speed downloads, hunting down latency spikes across the galaxy, or simply enjoying having a friendly alien co-pilot watching over your broadband connection, **Stellar Visor v2.0.0** turns routine network monitoring into an immersive starship flight experience.

---

## 👽 Meet Your Alien Pilot & Cockpit Co-Pilot

Sitting front and center on your starship dashboard is your reactive alien co-pilot! Driven by an adaptive real-time emotion engine, your extraterrestrial companion keeps you informed with expressive galactic kaomojis:

- **🟢 Optimal Link (`<= 100 ms`)**: `(👽 ⟟⋏⏁⟒⍀⋏⟒⏁ ⍜⌿⏁⟟⌲⏃⌰)` & `(👽⚡ Hyper-Drive Active)` — Smooth sailing through the cosmos with low latency and clean throughput.
- **🟡 Marginal Link (`> 100 ms`)**: `(👽💦 ⏁⟒⌰⟒⌿⍜⌠⏁ ⌰⏃⌰!)` & `(👽🌀 Wormhole Packet Jitter)` — Cosmic turbulence, solar flares, or bufferbloat detected.
- **🔴 Dropped Link (`OFFLINE`)**: `(👽💥 ⎎⏃⏁⏃⏃⌰ ⌰⟟⋏☍ ⌰⍜⌇⏁!)` & `(👽💀 Mothership Offline)` — Antenna disconnect or total packet loss in the deep void.

Coupled with the **Sub-Space Relay Ticker**, the cockpit continuously cycles intercepted extraterrestrial chatter, SETI radio gossip, and transmissions from Sector 7G.

---

## ✨ Features & Polish in v2.0.0

### 🎨 Cosmic Cockpit HUD Aesthetics
- **Deep Space Obsidian Palette**: Refined dark workspace styled with `#0d1117`, spaceship console decking (`#161b22`), starlight cyan (`#58a6ff`), nebula magenta (`#bc8cff`), and alien mint (`#7ee787`).
- **High-DPI Awareness**: Native Windows `ctypes.windll.shcore` integration ensures razor-sharp text, smooth curve rendering, and crisp UI borders across 1080p, 1440p, and 4K displays.
- **Dynamic Holographic Cards**: Metric cards with hover highlights and active states showcasing peak speeds, session totals, and current bandwidth.

### 📊 Real-Time Hologram Telemetry Charts
- **Sub-Space Bandwidth Beams**: Dual-curve live timeline tracking **Download** (Starlight Cyan) and **Upload** (Nebula Magenta) simultaneously.
- **Auto-Scaling Speed Curves**: Seamlessly scales from single bytes (`B/s`) through `KB/s`, `MB/s`, and warp-speed gigabytes (`GB/s`).
- **Cosmic Latency Radar**: Precision ping timeline with an amber threshold line indicating jitter and red markers highlighting dropped packets.

### 🌐 Deep Hardware & Adapter Sniffing
- **Zero-Latency Adapter Detection**: Automatically identifies your active physical or wireless adapter, local IPv4 address, and hardware MAC address without sluggish external subprocesses.
- **Dynamic Target Beaconing**: Ping Google Public DNS (`8.8.8.8`), Cloudflare (`1.1.1.1`), or custom galactic coordinates with on-the-fly reconfiguration (`Ctrl + T`).

### 💾 Holocron Telemetry Exports
- **Session Snapshots (`Ctrl + E`)**: Save your full bandwidth history, upload/download metrics, and latency samples directly into formatted `.json` or `.csv` spreadsheets for diagnostics and archiving.

### 🖥️ Dual Flight Modes
- **Cockpit Desktop GUI (Default)**: Full graphical dashboard with animated canvas plots, reactive kaomojis, and cockpit controls (`python stellar_visor.py` or `run.bat`).
- **Retro Terminal HUD (`--cli`)**: Flicker-free ANSI ASCII console experience featuring dual terminal sparkline graphs, live network stats, and alien telemetry for headless servers.

### 🛸 Multi-Resolution Flying Saucer Icon
- Built-in Pillow synthesizer (`generate_icon.py`) generates multi-layered Windows `.ico` assets (256x256, 48x48, 32x32, 16x16) and PNG assets depicting an alien piloting a glowing flying saucer.

### 🔄 Project Rebrand & Repository Harmonization
- **Repository Rename**: Transitioned from `NetworkInfo` to `StellarVisor` (`Stellar-Visor`).
- **Module Restructuring**: Renamed `network_info.py` $\rightarrow$ `stellar_visor.py` and `NetworkInfo.spec` $\rightarrow$ `stellar_visor.spec`.
- **Packaging & Entry Points**: Updated `setup.py` with standard console commands `stellarvisor` and `stellarvisor-cli`.
- **Cross-Repo Alignment**: Synchronized with the Cassiopeia Studios ecosystem alongside **StellarNotes** and **Stellar Snooper**.

### 🛠️ 1-Click Automation Suite
- `run.bat` — 1-click launcher supporting compiled binary or silent `pythonw` execution.
- `build.bat` — Automated PyInstaller compilation into standalone single-file `dist\stellar_visor.exe`.
- `install.bat` — Zero-admin Desktop and Start Menu shortcut installer (HKCU).
- `uninstall.bat` — 1-click clean removal of desktop shortcuts.

---

## ⌨️ Cockpit Controls & Flight Hotkeys

| Shortcut | Action |
| :--- | :--- |
| `Space` | Pause / Resume real-time telemetry streaming |
| `Ctrl + R` | Reset session telemetry counters and peak records |
| `Ctrl + T` | Open Target Beacon dialog (Change Ping Target) |
| `Ctrl + E` | Export session telemetry holocron (`.json` / `.csv`) |
| `Ctrl + S` | Open Cockpit Telemetry Settings panel |
| `Ctrl + Q` / `Esc` | Safely park the ship, log session stats, and exit |

---

## 📦 Getting Started

### 🖱️ 1-Click Quick Launch
Double-click `run.bat` in the project root or use the Desktop shortcut created via `install.bat`.

### 💻 Launch via Terminal
```bash
# Launch Cockpit Desktop GUI
python stellar_visor.py

# Launch via package module
python -m StellarVisor

# Target a custom beacon at 15 FPS
python -m StellarVisor --target 1.1.1.1 --fps 15

# Launch Retro Terminal HUD
python -m StellarVisor --cli
```

---

## 📜 Metadata
- **Release Version**: `v2.0.0`
- **Previous Name**: *Melody's Starship Network Visor* / *NetworkInfo*
- **Author**: Melody H. Song / Cassiopeia Studios
- **License**: MIT License
- **Target OS**: Windows 10 / 11 (High-DPI Ready)
- **Tagline**: *"Pinging distant galaxies... sub-space network telemetry online!"*

*Made with 🛸 by Melody H. Song / Cassiopeia Studios*
