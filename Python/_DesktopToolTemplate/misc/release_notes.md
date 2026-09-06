<!-- [Template Tier: Tier 3 (Optional - Release Packaging & Notes)] -->
<!-- Safe to delete if: This tool does not maintain release notes drafts. -->

# ⭐ Desktop Tool v1.0.0 — Official Galactic Release 🛸

> *"Scaffolding cosmic desktop utilities with precision and style."*

Welcome to the inaugural release of **Desktop Tool**! Designed as a sleek, cosmic workstation with seamless Windows Explorer context menu integration, clean high-DPI scaling, and resilient background state persistence.

---

## 🌟 Key Highlights & Features

### 🎨 Cosmic Workstation UI
- Handcrafted obsidian theme inspired by deep space command centers (`#0d1117`, `#161b22`, `#21262d`).
- Windows High-DPI awareness (`ctypes.windll.shcore`) ensuring ultra-crisp fonts and icons on 1080p, 1440p, and 4K displays.
- Real-time dirty-state tracking and graceful unsaved change protection.

### 🛸 Seamless Windows Explorer Integration
- Right-click custom file associations registered directly under `HKCU\Software\Classes`.
- Zero-admin setup: no UAC elevation or Administrator privileges required.
- Shell notification integration (`SHChangeNotify`) instantly refreshes the Windows Explorer cache without restarting.

### ⚡ Thread-Safe Background Workers
- Queue-based asynchronous worker prevents GUI freezes during heavy I/O or computations.
- Real-time status console and progress updates.

### 💾 Dual-Save Architecture & Config Persistence
- Background autosave mechanism paired with manual `Ctrl + S` disk synchronization.
- JSON configuration loader for user preferences (`config.json`).

---

## ⌨️ Keyboard Shortcuts Reference

| Shortcut | Action |
| :--- | :--- |
| `Ctrl + O` | Open file dialog |
| `Ctrl + S` | Save file / synchronize workspace |
| `Ctrl + R` / `F5` | Execute main workstation action |
| `Ctrl + Q` | Clean exit with unsaved change check |

---

## 📦 Installation & Setup

### 1. Standalone Portable Package (Recommended)
Download `desktop_tool.exe` (or `Desktop-Tool-Windows-x64.zip`) from the release assets:
1. Extract the `.zip` to your desired folder.
2. Run `install.bat` to register right-click context menus and desktop shortcuts.
3. Double-click `run.bat` or `desktop_tool.exe` to launch!

### 2. Running From Source (Development Mode)
```bash
git clone https://github.com/MelodyHSong/MHS-CodeSnippets.git
cd "Python/_DesktopToolTemplate"
python -m pip install -r requirements.txt
python app.py
```

---

- **Compatibility**: Windows 10 / Windows 11 (x64)
- **Prerequisites**: 0 external runtime dependencies required for standalone binary (`.exe` / `.zip`)
- **Dev Requirements**: Python 3.8+ & Pillow >= 10.0.0 (only when running from source)

---

*Made with ♡ by MelodyHSong (Cassiopeia Studios)*
