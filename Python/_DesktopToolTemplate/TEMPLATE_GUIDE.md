# ⭐ Desktop Tool Template — Architectural & Scaffolding Guide ⭐

> "A modular blueprint for crafting cosmic Windows desktop applications."

This guide explains the structural architecture of the **Desktop Tool Template** and provides clear rules for both **AI Agents** and **Human Developers** to determine which components are necessary for a new project and which can be safely omitted.

---

## 🧭 Overview: The 4-Tier Architecture

Not every project requires a full open-source repository structure with CI/CD workflows, registry installers, or zip packaging. This template is designed as a **modular super-set** modeled after production utilities like **StellarNotes**.

Components are divided into **4 distinct functional tiers**:

```text
┌─────────────────────────────────────────────────────────────────┐
│ Tier 4: GitHub Ecosystem & CI/CD                                │
│ (.github/, CONTRIBUTING.md, CHANGELOG.md, pyproject.toml, etc.) │
├─────────────────────────────────────────────────────────────────┤
│ Tier 3: Binary Compilation & Distribution                       │
│ (desktop_tool.spec, build.bat, package_release.py, misc/)       │
├─────────────────────────────────────────────────────────────────┤
│ Tier 2: Windows Shell Integration                               │
│ (setup_integration.py, install.bat, uninstall.bat)             │
├─────────────────────────────────────────────────────────────────┤
│ Tier 1: Core Essentials (Mandatory)                             │
│ (app.py, run.bat, requirements.txt, assets/, .gitignore, etc.)  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Component Selection Matrix

| File / Folder | Tier | Purpose | Safe to Delete If... |
| :--- | :--- | :--- | :--- |
| `app.py` | **Tier 1 (Core)** | Main Tkinter workstation entry point | ❌ **Never** (Core application code) |
| `run.bat` | **Tier 1 (Core)** | Smart launcher (`.exe` -> `pythonw` -> `python`) | ❌ **Never** (Primary Windows launch entry) |
| `requirements.txt` | **Tier 1 (Core)** | Python package dependencies | ❌ **Never** |
| `assets/app_icon.ico` | **Tier 1 (Core)** | Multi-res icon asset (256, 48, 32, 16) | ❌ **Never** (Window & shortcut branding) |
| `generate_icon.py` | **Tier 1 (Core)** | Pillow-based icon synthesizer | Optional if `app_icon.ico` is pre-baked |
| `config.json` | **Tier 1 (Core)** | Default user settings & preferences | Safe if app has no persistent preferences |
| `.gitignore` | **Tier 1 (Core)** | Git ignore rules | ❌ **Never** |
| `LICENSE` | **Tier 1 (Core)** | MIT license | ❌ **Never** |
| `README.md` | **Tier 1 (Core)** | Documentation & user guide | ❌ **Never** |
| `setup_integration.py` | **Tier 2 (Windows)** | Context menu verbs & `.lnk` shortcut manager | Tool does not need right-click or shortcuts |
| `setup_context_menu.py` | **Tier 2 (Windows)** | StellarNotes compatibility alias | Tool uses `setup_integration.py` directly |
| `install.bat` | **Tier 2 (Windows)** | 1-click HKCU installer | Tool has no shell integration |
| `uninstall.bat` | **Tier 2 (Windows)** | 1-click clean registry uninstaller | Tool has no shell integration |
| `desktop_tool.spec` | **Tier 3 (Packaging)** | PyInstaller specification | Tool is only run from Python source |
| `build.bat` | **Tier 3 (Packaging)** | 1-click PyInstaller / packaging runner | Tool is only run from Python source |
| `package_release.py` | **Tier 3 (Packaging)** | Builds `.exe`, `.zip`, and SHA-256 checksums | Tool is not distributed as zipped binaries |
| `misc/release_notes.md` | **Tier 3 (Packaging)** | Release announcement draft | Project has no public release notes |
| `assets/screenshots/` | **Tier 4 (GitHub)** | Directory for README UI preview images | Project documentation has no local images |
| `.github/workflows/` | **Tier 4 (GitHub)** | GitHub Actions automated build & release | Project is not a standalone GitHub repository |
| `.github/ISSUE_TEMPLATE/` | **Tier 4 (GitHub)** | Bug report & feature request templates | Project is not a standalone public GitHub repo |
| `.github/FUNDING.yml` | **Tier 4 (GitHub)** | GitHub sponsor buttons | Project does not accept sponsorships |
| `CONTRIBUTING.md` | **Tier 4 (GitHub)** | Open-source contribution guidelines | Tool is private or maintained internally |
| `CHANGELOG.md` | **Tier 4 (GitHub)** | Historical version change tracking | Tool does not follow semantic release logs |
| `pyproject.toml` | **Tier 4 (GitHub)** | PEP 518/621 packaging metadata | Tool is not distributed via pip/PyPI |
| `.editorconfig` | **Tier 4 (GitHub)** | Formatting rules across IDEs | Repository does not enforce editorconfig |
| `template_manifest.json` | **Meta** | Machine-readable manifest of tiers & files | Can be removed after project is scaffolded |
| `scaffold.py` | **Meta** | Automated scaffolding & pruning CLI | Can be removed after project is scaffolded |

---

## 🎯 Predefined Project Profiles

When scaffolding a new project, choose one of four profiles:

### 1. Minimal / Embedded Utility (`--profile minimal`)
- **Use Case**: A lightweight internal tool, code snippet, quick dashboard, or floating widget living inside `Python\_DesktopTools\`.
- **Keeps**: **Tier 1 (Core)** only.
- **Removes**: Tiers 2, 3, 4.

### 2. Shell-Integrated Desktop App (`--profile shell`)
- **Use Case**: A full desktop application that opens files from Windows Explorer (e.g. text editors, image inspectors) or needs Desktop/Start Menu shortcuts.
- **Keeps**: **Tier 1 (Core)** + **Tier 2 (Windows)**.
- **Removes**: Tiers 3, 4.

### 3. Portable Binary Distribution (`--profile dist`)
- **Use Case**: A desktop tool distributed to end-users as a compiled standalone Windows `.exe` and portable `.zip` bundle with SHA-256 checksums, but hosted in an existing repo.
- **Keeps**: **Tier 1 (Core)** + **Tier 2 (Windows)** + **Tier 3 (Packaging)**.
- **Removes**: Tier 4.

### 4. Full Standalone GitHub Repository (`--profile full`)
- **Use Case**: A flagship open-source project split into its own independent GitHub repository (like **StellarNotes**).
- **Keeps**: **All Tiers (1, 2, 3, 4)**.

---

## 🤖 Instructions for AI Coding Agents

When a user asks you to create a new desktop tool or scaffold a project from this template:

1. **Analyze User Intent**:
   - *Is this a quick internal utility?* Use **Minimal Profile**.
   - *Does the user mention right-clicking files or desktop shortcuts?* Include **Tier 2 (Windows)**.
   - *Does the user want a compiled `.exe` or release zip?* Include **Tier 3 (Packaging)**.
   - *Is the user creating a standalone GitHub repository with CI/CD?* Include **Tier 4 (GitHub)**.
2. **Scaffold Using `scaffold.py`**:
   Run the scaffolding script to automatically copy, rebrand, and prune:
   ```bash
   python scaffold.py --create "StellarVisor" --dest "Python/_DesktopTools/StellarVisor" --profile shell
   ```
   Or, if copying manually, consult `template_manifest.json` and delete files from excluded tiers.
3. **Customize Configuration**:
   - Update `APP_TITLE`, `APP_SLUG`, `APP_DESCRIPTION` in `setup_integration.py` (if present) and `package_release.py` (if present).
   - Update window title and UI widgets in `app.py`.
   - Update `requirements.txt` with any extra libraries.
   - Regenerate `assets/app_icon.ico` using `python generate_icon.py`.

---

## 🛠️ Developer CLI Reference

You can inspect the template structure and perform automated operations using `scaffold.py`:

```bash
# View template components and tier statuses
python scaffold.py --inspect

# Scaffold a new tool with a specific profile
python scaffold.py --create "StellarAudio" --dest "../_DesktopTools/StellarAudio" --profile dist

# Prune an existing project folder to a lighter profile
python scaffold.py --prune --profile minimal
```
