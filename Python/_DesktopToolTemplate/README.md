# ⭐ Desktop Tool Template ⭐

> "Blueprint for the stars — scaffolding cosmic desktop utilities with ease."

Welcome to the **Desktop Tool Template**! ⭐🛸✨ This directory provides a production-grade, modular foundation for building modern Windows desktop utilities with Python and Tkinter — modeled directly after the architecture, aesthetics, release pipelines, and Windows integration patterns established in **StellarNotes**, **Stellar Snooper**, and **Stellar Visor**.

---

## 🧭 The 4-Tier Component Architecture

**Note:** Not every desktop tool will need every component in this repository. To keep projects lean, the template is organized into **4 functional tiers**. Developers and AI agents can consult the matrix below (or [TEMPLATE_GUIDE.md](file:///c:/Users/Melody/Desktop/Cassiopeia%20Studios/Codebase/MHS-CodeSnippets/Python/_DesktopToolTemplate/TEMPLATE_GUIDE.md) and [template_manifest.json](file:///c:/Users/Melody/Desktop/Cassiopeia%20Studios/Codebase/MHS-CodeSnippets/Python/_DesktopToolTemplate/template_manifest.json)) to determine which tiers apply to their project.

```text
┌─────────────────────────────────────────────────────────────────┐
│ Tier 4: GitHub Ecosystem & CI/CD                                │
│ (.github/, CONTRIBUTING.md, CHANGELOG.md, pyproject.toml, etc.) │
├─────────────────────────────────────────────────────────────────┤
│ Tier 3: Binary Compilation & Release Packaging                  │
│ (desktop_tool.spec, build.bat, package_release.py, misc/)       │
├─────────────────────────────────────────────────────────────────┤
│ Tier 2: Windows Shell Integration                               │
│ (setup_integration.py, install.bat, uninstall.bat)              │
├─────────────────────────────────────────────────────────────────┤
│ Tier 1: Core Essentials (Mandatory)                             │
│ (app.py, run.bat, requirements.txt, assets/, .gitignore, etc.)  │
└─────────────────────────────────────────────────────────────────┘
```

### 🎯 Predefined Project Profiles

| Profile | Included Tiers | Best For |
| :--- | :--- | :--- |
| **Minimal / Embedded** (`minimal`) | **Tier 1 (Core)** | Quick internal utilities, snippet scripts, dashboards, and floating widgets. |
| **Shell-Integrated** (`shell`) | **Tier 1** + **Tier 2** | Tools that associate with file extensions or need Desktop/Start Menu shortcuts. |
| **Portable Distribution** (`dist`) | **Tier 1** + **Tier 2** + **Tier 3** | Standalone compiled `.exe` tools distributed as portable `.zip` bundles with SHA-256 hashes. |
| **Full GitHub Repository** (`full`) | **All Tiers (1, 2, 3, 4)** | Standalone open-source repositories (like StellarNotes) with CI/CD releases and issue templates. |

---

## 📁 Template Directory Structure

```text
Python/_DesktopToolTemplate/
├── .github/                         # [Tier 4] GitHub repository community & automation
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md            # Issue template for bug tracking
│   │   └── feature_request.md       # Issue template for feature ideas
│   ├── workflows/
│   │   └── build-release.yml        # CI/CD: Automated PyInstaller builds & GitHub Releases
│   └── FUNDING.yml                  # GitHub sponsorship configuration
├── assets/
│   ├── app_icon.ico                 # [Tier 1] Multi-resolution Windows icon (256, 48, 32, 16)
│   └── screenshots/
│       └── .gitkeep                 # [Tier 4] Directory for README UI preview screenshots
├── misc/
│   └── release_notes.md             # [Tier 3] Version release announcement draft
├── .editorconfig                    # [Tier 4] Cross-editor formatting consistency
├── .gitignore                       # [Tier 1] Git ignore rules for builds, pycache, dist
├── app.py                           # [Tier 1] Core Tkinter application boilerplate
├── build.bat                        # [Tier 3] 1-click PyInstaller and release package builder
├── CHANGELOG.md                     # [Tier 4] Version history following Keep a Changelog
├── config.json                      # [Tier 1] Default user configuration & persistent preferences
├── CONTRIBUTING.md                  # [Tier 4] Open-source contribution guidelines
├── desktop_tool.spec                # [Tier 3] PyInstaller specification for standalone binary
├── generate_icon.py                 # [Tier 1] Pillow script to synthesize custom .ico assets
├── install.bat                      # [Tier 2] 1-click HKCU context menu & shortcut installer
├── LICENSE                          # [Tier 1] MIT License
├── package_release.py               # [Tier 3] Packaging pipeline: builds exe, zip & SHA256 checksums
├── pyproject.toml                   # [Tier 4] Standard PEP 518/621 packaging metadata
├── README.md                        # [Tier 1] Documentation and project guide
├── requirements.txt                 # [Tier 1] Python dependencies (Pillow, PyInstaller)
├── run.bat                          # [Tier 1] Smart launcher (.exe -> pythonw -> python -> py)
├── scaffold.py                      # [Meta] CLI utility to scaffold or prune profiles
├── setup_context_menu.py            # [Tier 2] StellarNotes compatibility alias wrapper
├── setup_integration.py             # [Tier 2] Universal Windows context menu & shortcut manager
├── TEMPLATE_GUIDE.md                # [Meta] Architectural reference and AI agent guide
├── template_manifest.json           # [Meta] Machine-readable component & tier manifest
└── uninstall.bat                    # [Tier 2] 1-click clean uninstaller
```

---

## 🚀 How to Scaffold a New Tool

### Option A: Using the Automated Scaffolding Utility (Recommended)

Run `scaffold.py` from your terminal or command prompt:

```bash
# 1. Inspect all components and available profiles
python scaffold.py --inspect

# 2. Scaffold a new tool with your desired profile:
# Minimal utility:
python scaffold.py --create "StellarClock" --dest "../_DesktopTools/StellarClock" --profile minimal

# Shell-integrated app:
python scaffold.py --create "StellarHex" --dest "../_DesktopTools/StellarHex" --profile shell

# Full standalone release (like StellarNotes):
python scaffold.py --create "StellarAudio" --dest "../_DesktopTools/StellarAudio" --profile full
```

The scaffolding script will automatically:
1. Copy only the files belonging to your chosen profile.
2. Substitute the application name and slug across scripts, specs, and config files.
3. Rename the `.spec` file to match your tool's name.

### Option B: Manual Scaffolding & Pruning

1. **Copy the Template Folder**:
   ```cmd
   xcopy /E /I "Python\_DesktopToolTemplate" "Python\_DesktopTools\MyNewTool"
   ```
2. **Prune Unneeded Tiers**:
   - If you don't need GitHub Actions or issue templates: delete `.github/`, `CONTRIBUTING.md`, `CHANGELOG.md`, `pyproject.toml`, `.editorconfig`.
   - If you don't need standalone compiled binaries: delete `desktop_tool.spec`, `package_release.py`, `build.bat`, `misc/`.
   - If you don't need right-click context menus or shortcuts: delete `setup_integration.py`, `setup_context_menu.py`, `install.bat`, `uninstall.bat`.
   - Or run `python scaffold.py --prune --profile <profile>` inside your new folder!
3. **Configure Identity in `setup_integration.py` & `package_release.py`**:
   Update `APP_TITLE`, `APP_SLUG`, `DIST_EXE_NAME`, and `TARGET_EXTENSIONS`.
4. **Customize UI in `app.py`**:
   Update window title, widgets, sidebars, and application logic.
5. **Regenerate Branding Icon**:
   Run `python generate_icon.py` to synthesize fresh icons in `assets/app_icon.ico`.

---

## ✨ Built-in Architecture & Features

- 🎨 **Cosmic Workstation Aesthetics**:
  - Deep obsidian dark theme (`#0d1117`, `#161b22`, `#21262d`, `#30363d`) with starlight cyan (`#58a6ff`) and celestial gold (`#f2cc60`) accents.
  - Windows High-DPI awareness (`ctypes.windll.shcore`) ensuring ultra-crisp fonts and icons on 1080p, 1440p, and 4K displays.
- 🛸 **Dual Windows Shell Integration**:
  - **Explorer Context Menu**: Register right-click verbs for custom file extensions (e.g. `⭐ Open with YourTool`).
  - **Desktop & Start Menu Shortcuts**: Seamless 1-click `.lnk` creation via native Windows APIs.
  - **Zero-Admin Installation**: Integrates directly into `HKEY_CURRENT_USER` — no UAC prompts or Administrator privileges required.
  - **Instant Explorer Refresh**: Dispatches `SHChangeNotify` to reload the Windows Shell cache immediately without restarting Explorer.
- 🔄 **Triple Execution Modes**:
  - **Standalone Mode (`.exe`)**: Self-contained single-file binary built using PyInstaller.
  - **Development Mode (`.py`)**: Silent, windowless background launch via `pythonw.exe`.
  - **Console Debug Mode**: Standard launch via `python.exe` / `py.exe`.
- ⚡ **Thread-Safe Background Worker**:
  - Built-in queue-based asynchronous task runner — run heavy operations without freezing the Tkinter GUI.
- 💾 **State & Autosave Management**:
  - Debounced autosave mechanism, dirty-state change tracking, and graceful exit prompt on unsaved modifications.
  - JSON configuration loader for persistent user settings (`config.json`).
- 🎨 **Multi-Resolution Icon Pipeline**:
  - Automated Pillow-based icon synthesizer producing multi-layered `.ico` assets (256x256, 48x48, 32x32, 16x16).
- 📦 **Automated Release Pipeline (`package_release.py`)**:
  - Builds standalone binary via PyInstaller.
  - Stages and creates portable release archives (`AppName-vX.X.X-Windows-x64.zip` and `AppName-Windows-x64.zip`).
  - Generates verifiable `SHA256SUMS.txt` checksums.
- 🚀 **GitHub Actions CI/CD Workflow**:
  - Automated Windows build matrix publishing release binaries directly to GitHub Releases upon pushing version tags (`v*`).

---

## 🖱️ Windows Integration & CLI Commands

### 1-Click Batch Files
| Script | Description |
| :--- | :--- |
| `run.bat` | Smart launcher: runs `.exe` if present; otherwise launches `app.py` silently via `pythonw.exe` / `python.exe` / `py.exe`. |
| `build.bat` | Checks Python in PATH, installs dependencies, and runs `package_release.py` (or PyInstaller). |
| `install.bat` | Registers Explorer context menus and creates Desktop/Start Menu shortcuts under HKCU. |
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

# Run full packaging pipeline (binary + portable zip + SHA256 checksums)
python package_release.py

# Cleanly wipe all integrations
python setup_integration.py --uninstall
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
This project is licensed under the MIT License. You are free to use, modify, and distribute this template in your own projects — just keep the headers intact!

---

*Made with ♡ by MelodyHSong (Cassiopeia Studios)*
