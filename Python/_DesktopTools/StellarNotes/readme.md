# ☆ StellarNotes ☆

> "Transmitting ideas across the cosmos, one thought at a time."

Welcome to **StellarNotes**! ⭐🛸✨ A sleek, cosmic desktop note-taking and voice-narration workstation designed for effortless writing, instant galactic search, note prioritization, and offline voice read-aloud—complete with seamless Windows Explorer context menu integration.

---

## ✨ Features

- ⭐ **Star & Pin Priority Transmissions**: Keep your most vital thoughts pinned to the top of your catalog.
- ⚡ **Instant Galactic Search**: Real-time debounced filtering across all note titles and previews as you type.
- 🔊 **Cosmic Audio ("Talking Notes")**: Built-in voice narration engine powered by Windows' native offline Speech Synthesis API—listen to your notes narrated aloud with one click or `Ctrl + Space`!
- 🛸 **Right-Click Context Menu Integration**: Seamlessly open any `.md`, `.markdown`, `.txt`, or `.note` file directly from Windows Explorer.
- 🎨 **Spaceship Hull Console Aesthetic**:
  - **Catalog Sidebar**: Deep obsidian console (`#11141c`) with glowing celestial amber stars (`#f2cc60`) and starlight cyan badges (`#58a6ff`).
  - **Transmission Editor**: Deep slate interior (`#0b0e14`) with starlight typography (`#e2e8f0`) and live character/word counters.
- 💾 **Dual-Save Architecture**: Smooth background autosave ensures you never lose a thought, with manual `Ctrl + S` instantly synchronizing to disk.
- 🚀 **Zero-Admin Installation**: Installs cleanly into `HKEY_CURRENT_USER`. No UAC prompts or Administrator privileges required.
- 🔄 **Dual Engine Modes**:
  - **Standalone Mode (`.exe`)**: Fast, self-contained single-file executable built with PyInstaller.
  - **Development Mode (`.py`)**: Uses `pythonw.exe` for silent windowless launch while hacking on the script.
- 📡 **Instant Shell Sync**: Calls Windows Shell APIs (`SHChangeNotify`) on install/uninstall—no PC restart or Explorer reload required.

---

## ☆ Installation & Context Menu Setup

### Option 1: 1-Click Setup (Easiest)
Simply double-click:
```cmd
install.bat
```
This automatically registers the `⭐ Open with StellarNotes` verb in your Windows context menu for all supported note and markdown files.

### Option 2: Python Terminal CLI
You can also manage the context menu directly from your terminal:

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
      ⭐ STELLAR NOTES — CONTEXT MENU SETUP 🛸      
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
1. In Windows Explorer, right-click any `.md`, `.markdown`, or `.txt` file.
2. Select **⭐ Open with StellarNotes**.
   > **Note for Windows 11**: If using the compact modern Windows 11 menu, choose **"Show more options"** (or press `Shift + Right Click`) to access the classic context menu verb, or select it from the **"Open with"** list.

### ⌨️ Keyboard Shortcuts
| Shortcut | Action |
| :--- | :--- |
| `Ctrl + N` | Create a new star transmission (New Note) |
| `Ctrl + S` | Synchronize to Base (Save file to disk) |
| `Ctrl + F` | Jump focus to the cosmic search bar |
| `Ctrl + P` | Toggle Pin / Star priority on current note |
| `Ctrl + D` | Purge / delete current note from disk |
| `Ctrl + Space` | Toggle Ship Audio / Read Aloud (Voice Narration) |
| `Ctrl + Z` / `Ctrl + Y` | Undo / Redo text edits |

---

## ☆ Uninstallation

To cleanly remove all context menu entries and registry associations at any time:

- **1-Click**: Double-click `uninstall.bat`
- **CLI**: `python setup_context_menu.py --uninstall`

All registry keys under `HKCU` are cleanly wiped, and the Windows shell cache is immediately refreshed.

---

## ☆ Quick Launch & Standalone Building

- **Launch StellarNotes**: Double-click `run.bat` (automatically launches the compiled `.exe` or starts windowless via `pythonw`).
- **Build Standalone Executable**: Double-click `build.bat` to compile `dist\stellar_notes.exe` using PyInstaller.

---

## ☆ Prerequisites (For Python / Dev Mode)

If running directly from source or compiling the executable:
```bash
python -m pip install -r requirements.txt
```
*(Windows SAPI audio and Tkinter GUI use built-in standard Windows and Python libraries—no heavy external dependencies required!)*

---

## ☆ License
This project is licensed under the [MIT License](LICENSE). Keep the galaxy headers intact!

---

*Made with ♡ by MelodyHSong*
