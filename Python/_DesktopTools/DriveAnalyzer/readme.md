# ☆ Stellar Snooper ☆

> "Cosmic storage telemetry—mapping stellar byte constellations across local disks."

Welcome to **Stellar Snooper**! ⭐🛸🔍 This project is a modern Windows desktop workstation utility built with Python and Tkinter—converted from a command-line script into the full **Desktop Tool Template** architecture with cosmic dark aesthetics, non-blocking asynchronous scanning, interactive tables, and Windows Explorer right-click integration.

---

## ✨ Architecture & Key Features

- 🎨 **Cosmic Workstation Aesthetics**:
  - Deep space obsidian theme (`#0d1117`, `#161b22`, `#21262d`, `#30363d`) with starlight cyan (`#58a6ff`), celestial gold (`#f2cc60`), and status mint (`#7ee787`) accents.
  - Native Windows High-DPI awareness (`ctypes.windll.shcore`) ensuring ultra-crisp fonts and icons on 1080p, 1440p, and 4K displays.
- ⚡ **Non-Blocking Background Scanning Engine**:
  - Queue-based asynchronous worker running in a daemon thread—scans multi-terabyte drives without freezing the Tkinter GUI.
  - Live progress telemetry: files indexed counter, real-time scan rate (`files/sec`), elapsed timer (`mm:ss.s`), and active directory monitor.
  - 1-click scan cancellation (`⏹ Stop Scan` / `Escape`) for immediate, graceful interruption.
- 🛸 **Dual Windows Shell Integration**:
  - **Drive & Folder Context Menus**: Register right-click verbs on drives (`Drive\shell`) and folders (`Directory\shell` & `Directory\Background\shell`): *⭐ Snoop Storage with Stellar Snooper*.
  - **Desktop & Start Menu Shortcuts**: Seamless 1-click `.lnk` creation via native Windows APIs.
  - **Zero-Admin Installation**: Integrates cleanly into `HKEY_CURRENT_USER`—no UAC prompts or Administrator privileges required.
  - **Instant Shell Refresh**: Dispatches `SHChangeNotify` to reload the Windows Shell cache immediately.
- 📊 **Interactive Data Workstation**:
  - **Top Largest Files Table** (`ttk.Treeview`): Sortable columns for Rank, File Name, Extension, Size, and Directory.
  - **Top Largest Folders Table** (`ttk.Treeview`): Recursive folder aggregation identifying top directory disk hogs.
  - **Storage Analytics Tab**: Breakdown of storage consumption by file extension (`.mp4`, `.zip`, `.iso`, etc.) and key target metrics.
  - **Activity Log & Terminal**: Real-time event logging and classic box-styled ASCII summary report tables.
  - **Explorer Shell Reveals**: Double-click or right-click any file to highlight it directly in Windows Explorer (`explorer /select,"path"`), copy paths, or launch files.
- 💾 **Report Exporter**:
  - Export complete storage analysis reports to **JSON**, **CSV**, or formatted **Text** formats (`Ctrl+S`).
- 🔄 **Multi-Mode Execution**:
  - **Desktop GUI Mode**: Full interactive workstation console (`run.bat` or `python app.py`).
  - **Standalone Binary Mode**: Compiled single-file `.exe` via PyInstaller (`build.bat`).
  - **Headless CLI Mode**: Terminal output with box-styled ASCII tables (`python app.py --cli [TARGET]` or `python custom_drive_analyzer.py [TARGET]`).
- 🎨 **Multi-Resolution Icon Pipeline**:
  - Automated Pillow script synthesizes multi-layered `.ico` assets (256x256, 48x48, 32x32, 16x16) featuring a cute cosmic alien snooper peeking through a golden magnifying glass discovering a celestial star!

---

## 📁 Project Directory Structure

```text
Python/_DesktopTools/DriveAnalyzer/
├── assets/
│   └── app_icon.ico                 # Multi-resolution icon asset (256, 48, 32, 16)
├── app.py                           # Core Tkinter workstation application & CLI bridge
├── config.json                      # Persistent settings (default drive, limits, themes)
├── custom_drive_analyzer.py         # Standalone CLI analyzer with zero-dependency fallback
├── generate_icon.py                 # Pillow script synthesizing cute alien snooper icon
├── setup_integration.py             # Windows context menu & shortcut installer
├── stellar_snooper.spec             # PyInstaller specification for windowed standalone .exe
├── run.bat                          # Smart launcher (.exe -> pythonw -> python)
├── build.bat                        # 1-click PyInstaller build automation
├── install.bat                      # 1-click context menu & shortcut installer
├── uninstall.bat                    # 1-click clean uninstaller
├── requirements.txt                 # Dependencies (pillow, pyinstaller, optional tqdm)
├── .gitignore                       # Git ignore rules for builds, pycache, dist
├── LICENSE                          # MIT License (Cassiopeia Studios)
└── readme.md                        # Documentation and quick-start guide
```

---

## 🚀 Getting Started

### 1. Launch the Desktop GUI
Double-click `run.bat` or run:
```bash
python app.py
```
To analyze a specific drive or folder directly:
```bash
python app.py D:\
```

### 2. Run in CLI Terminal Mode
Run headless without launching the GUI:
```bash
python app.py --cli C:
# or
python custom_drive_analyzer.py D:\Projects
```

### 3. Install Windows Explorer Integration
Register right-click shortcuts for all drives and folders:
- Double-click `install.bat`, or run:
```bash
python setup_integration.py --install
```

### 4. Build Standalone Executable (`.exe`)
Compile into a single standalone windowed executable:
- Double-click `build.bat`, or run:
```bash
python setup_integration.py --build
```
The compiled binary will be placed in `dist\stellar_snooper.exe`.

---

## 🖱️ Windows Integration & CLI Commands

### 1-Click Batch Files
| Script | Description |
| :--- | :--- |
| `run.bat` | Launches standalone `.exe` if compiled; otherwise launches `app.py` silently via `pythonw.exe`. |
| `build.bat` | Checks Python in PATH, installs dependencies, and compiles with PyInstaller. |
| `install.bat` | Registers Explorer right-click menus for drives and folders, and places Desktop/Start Menu shortcuts. |
| `uninstall.bat` | Cleanly removes all registry keys and shortcuts from the system. |

### Terminal CLI Options
```bash
# Auto-detect and install shell integration (prefers .exe if compiled, else pythonw)
python setup_integration.py --install

# Install specifically in Python development mode
python setup_integration.py --install --mode python

# Inspect current Windows registry & shortcut status
python setup_integration.py --status

# Compile standalone executable with PyInstaller
python setup_integration.py --build

# Cleanly wipe all integrations and shortcuts
python setup_integration.py --uninstall
```

### Interactive Menu
Run without arguments to launch the Terminal Setup UI:
```bash
python setup_integration.py
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `F5` or `Ctrl + R` | Start / Toggle Storage Scan |
| `Escape` | Cancel Active Scan |
| `Ctrl + O` | Browse Custom Target Folder |
| `Ctrl + S` | Export Storage Analysis Report (JSON / CSV / TXT) |
| `Ctrl + Q` | Exit Application |

---

## 📜 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

*Made with ♡ by Melody H. Song*
