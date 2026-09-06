# ☆ Changelog ☆

All notable changes to **Stellar Visor** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## ☆ [2.0.0] - 2026-09-05

### Changed
- **Cosmic Suite Harmonization**: Rebranded project from *Melody's Starship Network Visor* (`NetworkInfo`) to **Stellar Visor** (`stellar-visor`), aligning with sibling utilities **StellarNotes** and **Stellar Snooper**.
- **Module Restructuring**: Renamed main GUI entry script from `network_info.py` to `stellar_visor.py` and PyInstaller spec to `stellar_visor.spec`.
- **Application Class**: Renamed core application class to `StellarVisorApp` (maintaining `NetworkVisorApp` alias for backward compatibility).
- **HUD & Title Banners**: Refreshed window title to `⭐ Stellar Visor - [Cosmic Telemetry HUD]` and cockpit banner to `⭐ STELLAR VISOR`.
- **Console HUD**: Updated ANSI terminal header to `⭐ STELLAR VISOR TELEMETRY ANALYZER ⭐`.
- **Asset Pipeline**: Updated `generate_icon.py` to synthesize multi-resolution `assets/stellar_visor.ico` and `assets/stellar_visor.png`.
- **Setup & Package Manifest**: Updated `setup.py` with entry points `stellarvisor` (GUI) and `stellarvisor-cli` (Console), targeting the `StellarVisor` package namespace.
- **Automation Scripts**: Synchronized all batch utilities (`run.bat`, `build.bat`, `install.bat`, `uninstall.bat`) to target `stellar_visor.py` and `dist\stellar_visor.exe`.

### Added
- **Triple Real-Time Hologram Charts**:
  - Live auto-scaling Sub-Space Bandwidth Beams supporting dynamic units (`B/s`, `KB/s`, `MB/s`, `GB/s`).
  - Cosmic Latency Radar tracking round-trip millisecond delays with amber warning lines and red dropped packet markers.
  - Dual Download (Starlight Cyan) and Upload (Nebula Magenta) real-time trajectory curves.
- **Moody Alien Co-Pilot**: Interactive alien kaomoji companion responding dynamically to network link states (`Optimal`, `Marginal`, `Dropped`).
- **Sub-Space Relay Chatter**: Dynamic cockpit newsfeed ticker cycling transmissions, galactic gossip, and SETI radio chatter from Sector 7G.
- **Hardware & Adapter Sniffing**: Non-blocking native socket and psutil resolution for active interface, local IPv4, and MAC addresses.
- **Holocron Telemetry Exports**: Instant snapshot of session bandwidth and latency history into `.json` or `.csv` files via `Ctrl + E`.
- **Dual Execution Engine**: Modern Tkinter desktop cockpit dashboard alongside a flicker-free ANSI terminal HUD via `--cli`.
- **Zero-Admin Desktop Integration**: Native Windows shortcut installation to Desktop and Start Menu without requiring UAC elevation (`install.bat`).

---

## ☆ [1.0.0] - 2026-09-05

### Added
- Initial release of *Melody's Starship Network Visor* prototype.
- Real-time network I/O traffic monitoring via `psutil`.
- ICMP / socket ping latency measurement engine.
- Windowless custom Tkinter cockpit frame with dark obsidian aesthetic.
- Terminal ANSI graph rendering engine (`core.py`).
