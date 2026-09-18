# ⭐ Changelog ⭐

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## ⭐ [1.0.0] - 2026-09-15

### Added
- **Initial Release**: Production-ready celestial mouse jiggler workstation for Windows.
- **Cosmic Dark Theme**: High-contrast obsidian palette (`#0d1117`) with starlight cyan (`#58a6ff`), celestial gold (`#f2cc60`), and pulse mint (`#7ee787`) accents.
- **Hardware Mouse Emulation**: Native `win32` relative cursor events (`mouse_event(0x0001, dx, dy, 0, 0)`) resetting Windows idle timers and communication platform statuses (Teams, Slack, Zoom).
- **Windows Kernel Wake Lock**: Direct `SetThreadExecutionState` integration to prevent screen sleep and lock screen triggers without disturbing system power schemes.
- **Smart Activity Guard**: Automatic user input monitoring (`GetLastInputInfo`) deferring jiggles when user is typing or moving mouse.
- **Multiple Trajectory Modes**:
  - `Subtle Micro-Nudge`: Hardware ±1px imperceptible pulse.
  - `Zen Ghost`: Zero cursor movement, OS Kernel wake lock only.
  - `Orbital Circle`: Smooth celestial orbit traversal.
  - `Random Jitter`: Organic micro-jitter.
- **Telemetry & Telemetry Console**: Real-time pulses dispatched counter, active session uptime, last pulse timestamp, and color-coded event log.
- **Windows High-DPI Awareness**: System DPI aware scaling for sharp fonts on High-DPI screens.
- **Standalone Build & Packaging**: 1-click `build.bat`, PyInstaller spec (`stellar_jiggler.spec`), and automated portable release bundler (`package_release.py`).
