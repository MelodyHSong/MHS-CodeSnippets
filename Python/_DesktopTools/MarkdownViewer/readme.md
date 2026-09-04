# ☆ Galactic Markdown Editor ☆

> "Beam up your Markdown to the transmission console!"

Welcome to the **Galactic Markdown Editor**! 🛸✨ A sleek, real-time split-screen Markdown writing console and previewer featuring a dark spaceship hull console, live document rendering, and seamless Windows Explorer context menu integration.

---

## ✨ Features

- 🛸 **Right-Click Context Menu Integration**: Seamlessly open any `.md`, `.markdown`, `.mdown`, or `.mkd` file straight from Windows Explorer.
- ⚡ **Live Real-Time Rendering**: Instant split-pane preview as you type with debounced document compilation.
- 🎨 **Spaceship Trim & Authentic Canvas**:
  - **Left Console**: Deep slate hull (`#0f131a`) with alien mint accents (`#7ee787`) and Consolas typography.
  - **Right Preview**: True-to-output document canvas (`#ffffff`) for authentic reading and export checks.
- 🚀 **Zero-Admin Installation**: Installs cleanly into `HKEY_CURRENT_USER`. No UAC prompts or Administrator privileges needed.
- 🔄 **Dual Engine Modes**:
  - **Standalone Mode (`.exe`)**: Fast, self-contained single-file executable. Zero dependencies required.
  - **Development Mode (`.py`)**: Uses `pythonw.exe` for silent windowless launch while hacking on the script.
- 📡 **Instant Shell Sync**: Calls Windows Shell APIs (`SHChangeNotify`) on install/uninstall—no PC restart or Explorer reload required.

---

## ☆ Installation & Context Menu Setup

### Option 1: 1-Click Setup (Easiest)
Simply double-click:
```cmd
install.bat
```
This automatically registers the `🛸 Open with Galactic Markdown Editor` verb in your Windows context menu for Markdown files.

### Option 2: Python Terminal CLI
You can also run the setup manager directly with Python:

```bash
# Auto-detect and install (prefers standalone .exe if compiled)
python setup_context_menu.py --install

# Install specifically in Python script mode (runs with pythonw.exe)
python setup_context_menu.py --install --mode python

# Check current registry status
python setup_context_menu.py --status

# Rebuild the standalone executable with PyInstaller
python setup_context_menu.py --build
```

### Option 3: Interactive Menu
Run without arguments to launch the Galactic Terminal UI:
```bash
python setup_context_menu.py
```
```text
============================================================
   🛸 GALACTIC MARKDOWN EDITOR — CONTEXT MENU SETUP 🛸   
============================================================
  [1] Install Context Menu (Standalone Executable Mode)
  [2] Install Context Menu (Python Script / Dev Mode)
  [3] Check Installation Status
  [4] Rebuild Standalone Executable (PyInstaller)
  [5] Uninstall Context Menu
  [6] Exit
------------------------------------------------------------
```

---

## ☆ Usage

### 🖱️ Right-Click Context Menu (Explorer)
1. In Windows Explorer, right-click any `.md` or `.markdown` file.
2. Select **🛸 Open with Galactic Markdown Editor**.
   > **Note for Windows 11**: If using the compact modern Windows 11 menu, choose **"Show more options"** (or press `Shift + Right Click`) to access the classic context menu verb, or select it from the **"Open with"** list.

### ⌨️ Keyboard Shortcuts
| Shortcut | Action |
| :--- | :--- |
| `Ctrl + S` / `Cmd + S` | Transmit to Base (Save file) |
| Typing | Auto-updates live preview after 300ms |

---

## ☆ Uninstallation

To cleanly remove all context menu entries and registry associations at any time:

- **1-Click**: Double-click `uninstall.bat`
- **CLI**: `python setup_context_menu.py --uninstall`

All registry keys under `HKCU` are cleanly wiped, and the Windows shell cache is immediately refreshed.

---

## ☆ Prerequisites (For Python / Dev Mode)

If running from source rather than the pre-compiled `.exe`:
```bash
python -m pip install markdown tkhtmlview pillow pyinstaller
```

---

## ☆ License
This project is licensed under the MIT License. Keep the galaxy headers intact!

---

*Made with ♡ by MelodyHSong*
