# ☆ Desktop Tool Template ☆

> "Blueprint for the stars—scaffolding cosmic desktop utilities with ease."

Welcome to the **Desktop Tool Template**! ⭐🛸✨ This directory provides a production-grade, modular foundation for building modern Windows desktop utilities with Python and Tkinter—modeled directly after the architecture, aesthetics, and Windows integration patterns established in **StellarNotes** and **Network Visor**.

---

## ✨ Built-in Architecture & Features

- 🎨 **Cosmic Workstation Aesthetics**:
  - Deep obsidian dark theme (`#0d1117`, `#161b22`, `#21262d`, `#30363d`) with starlight cyan (`#58a6ff`) and celestial gold (`#f2cc60`) accents.
  - Windows High-DPI awareness (`ctypes.windll.shcore`) ensuring ultra-crisp fonts and icons on 1080p, 1440p, and 4K displays.
- 🛸 **Dual Windows Shell Integration**:
  - **Explorer Context Menu**: Register right-click verbs for custom file extensions (e.g. `⭐ Open with YourTool`).
  - **Desktop & Start Menu Shortcuts**: Seamless 1-click `.lnk` creation via native Windows APIs.
  - **Zero-Admin Installation**: Integrates directly into `HKEY_CURRENT_USER`—no UAC prompts or Administrator privileges required.
  - **Instant Explorer Refresh**: Dispatches `SHChangeNotify` to reload the Windows Shell cache immediately without restarting Explorer.
- 🔄 **Dual Execution Modes**:
  - **Standalone Mode (`.exe`)**: Self-contained single-file binary built using PyInstaller.
  - **Development Mode (`.py`)**: Silent, windowless background launch via `pythonw.exe`.
- ⚡ **Thread-Safe Background Worker**:
  - Built-in queue-based asynchronous task runner—run heavy operations without freezing the Tkinter GUI.
- 💾 **State & Autosave Management**:
  - Debounced autosave mechanism, dirty-state change tracking, and graceful exit prompt on unsaved modifications.
  - JSON configuration loader for persistent user settings (`config.json`).
- 🎨 **Multi-Resolution Icon Pipeline**:
  - Automated Pillow-based icon synthesizer producing multi-layered `.ico` assets (256x256, 48x48, 32x32, 16x16).
- 🛠️ **1-Click Batch Automation**:
  - `run.bat` • `build.bat` • `install.bat` • `uninstall.bat`

---

## 📁 Template Directory Structure

```text
Python/_DesktopToolTemplate/
├── assets/
│   └── app_icon.ico                 # Multi-resolution icon asset (256, 48, 32, 16)
├── app.py                           # Core Tkinter application boilerplate
├── config.json                      # Default user configuration & preferences
├── generate_icon.py                 # Pillow script to synthesize custom .ico assets
├── setup_integration.py             # Universal Windows context menu & shortcut manager
├── desktop_tool.spec                # PyInstaller specification for windowed standalone .exe
├── run.bat                          # Smart launcher (.exe -> pythonw -> python)
├── build.bat                        # 1-click PyInstaller build automation
├── install.bat                      # 1-click context menu & shortcut installer
├── uninstall.bat                    # 1-click clean uninstaller
├── requirements.txt                 # Optional dependencies (pillow, pyinstaller)
├── .gitignore                       # Git ignore rules for builds, pycache, dist
├── LICENSE                          # MIT License (Cassiopeia Studios)
└── readme.md                        # Documentation and quick-start guide
```

---

## 🚀 How to Use This Template for a New Project

Starting a new desktop tool takes less than 2 minutes:

### 1. Copy the Template Folder
Copy `_DesktopToolTemplate` and rename it to your project name inside `Python\_DesktopTools\`:
```cmd
xcopy /E /I "Python\_DesktopToolTemplate" "Python\_DesktopTools\MyNewTool"
```

### 2. Configure Settings in `setup_integration.py`
Open `setup_integration.py` and update the configuration block at the top:
```python
APP_TITLE = "My New Tool"
APP_SLUG = "my_new_tool"
APP_DESCRIPTION = "My New Tool - Cosmic System Utility"
DIST_EXE_NAME = "my_new_tool.exe"
SPEC_FILE = "my_new_tool.spec"

# Toggle integrations to fit your tool:
ENABLE_CONTEXT_MENU = True            # Set False if not a file-association tool
CONTEXT_MENU_LABEL = "⭐ Open with My New Tool"
TARGET_EXTENSIONS = [".txt", ".json"] # Extensions to associate

ENABLE_DESKTOP_SHORTCUT = True        # Place shortcut on Desktop
ENABLE_START_MENU_SHORTCUT = True     # Place shortcut in Start Menu
```

### 3. Customize Branding in `app.py`
In `app.py`, update the window title and branding text in `build_header()`:
```python
self.root.title("⭐ My New Tool - [Workstation Console]")
# Add your custom widgets, sidebars, or tool logic!
```

### 4. (Optional) Customize the Icon in `generate_icon.py`
Tweak the colors or shapes in `generate_icon.py`, then run:
```bash
python generate_icon.py
```
This regenerates `assets/app_icon.ico` in all required Windows resolutions.

### 5. Build and Test!
- **Run in dev mode**: Double-click `run.bat` or run `python app.py`
- **Build standalone `.exe`**: Double-click `build.bat`
- **Install Windows shortcuts/context menus**: Double-click `install.bat`

---

## 🖱️ Windows Integration & CLI Commands

### 1-Click Batch Files
| Script | Description |
| :--- | :--- |
| `run.bat` | Launches standalone `.exe` if compiled; otherwise launches `app.py` silently via `pythonw.exe`. |
| `build.bat` | Checks Python in PATH, installs dependencies, and compiles with PyInstaller. |
| `install.bat` | Registers Explorer context menus and creates Desktop/Start Menu shortcuts. |
| `uninstall.bat` | Cleanly removes all registry keys and shortcuts from the system. |

### Terminal CLI Options
```bash
# Auto-detect and install (prefers .exe if present, else pythonw)
python setup_integration.py --install

# Install specifically for development mode
python setup_integration.py --install --mode python

# Inspect current Windows registry & shortcut status
python setup_integration.py --status

# Compile standalone executable with PyInstaller
python setup_integration.py --build

# Cleanly wipe all integrations
python setup_integration.py --uninstall
```

### Interactive Menu
Run without arguments to launch the Terminal UI:
```bash
python setup_integration.py
```
```text
==============================================================
   ⭐ DESKTOP TOOL TEMPLATE — SETUP & INTEGRATION 🛸   
==============================================================
  [1] Install (Standalone Executable Mode)
  [2] Install (Python Script / Dev Mode)
  [3] Check Installation Status
  [4] Rebuild Standalone Executable (PyInstaller)
  [5] Uninstall All Integrations & Shortcuts
  [6] Exit
--------------------------------------------------------------
```

---

## ⌨️ Standard Keyboard Shortcuts
| Shortcut | Action |
| :--- | :--- |
| `Ctrl + O` | Open file dialog |
| `Ctrl + S` | Save file / synchronize workspace |
| `Ctrl + R` / `F5` | Execute main workstation action |
| `Ctrl + Q` | Clean exit with unsaved change check |

---

## ☆ License
This project is licensed under the MIT License. You are free to use, modify, and distribute this template in your own projects—just keep the headers intact!

---

*Made with ♡ by MelodyHSong / Cassiopeia Studios*
