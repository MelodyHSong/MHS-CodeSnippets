# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: setup_desktop.py
# ☆ Date: September 2026
# ☆
# ☆ Description: Desktop & Start Menu shortcut manager and PyInstaller builder for Network Visor.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import sys
import os
import ctypes
import argparse
import subprocess

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Constants & Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_EXE = os.path.join(BASE_DIR, "dist", "NetworkInfo.exe")
SCRIPT_PATH = os.path.join(BASE_DIR, "network_info.py")
ASSET_ICON = os.path.join(BASE_DIR, "assets", "network_info.ico")
SPEC_PATH = os.path.join(BASE_DIR, "NetworkInfo.spec")

SHORTCUT_NAME = "Melody's Starship Network Visor.lnk"
APP_DESCRIPTION = "Melody's Starship Network Visor - Cosmic Real-Time Network Telemetry Workstation"


def get_pythonw_path():
    """Locate pythonw.exe for silent windowless launch."""
    py_dir = os.path.dirname(sys.executable)
    pythonw = os.path.join(py_dir, "pythonw.exe")
    if os.path.exists(pythonw):
        return pythonw
    return sys.executable


def get_desktop_path():
    """Retrieve the Windows user Desktop folder."""
    return os.path.join(os.path.expanduser("~"), "Desktop")


def get_start_menu_path():
    """Retrieve the Windows user Start Menu Programs folder."""
    appdata = os.environ.get("APPDATA", "")
    if appdata:
        p = os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs")
        if os.path.exists(p):
            return p
    return None


def refresh_explorer():
    """Notify the Windows Shell to refresh desktop and shell caches."""
    try:
        # SHCNE_ASSOCCHANGED = 0x08000000, SHCNF_IDLIST = 0x0000
        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
        return True
    except Exception as e:
        print(f"[!] Warning: Could not refresh Explorer shell cache: {e}")
        return False


def create_shortcut(target_path, arguments, shortcut_path, icon_path, working_dir, description):
    """Creates a Windows .lnk shortcut file using native PowerShell WScript.Shell."""
    ps_script = f"""
    $ws = New-Object -ComObject WScript.Shell;
    $s = $ws.CreateShortcut('{shortcut_path}');
    $s.TargetPath = '{target_path}';
    $s.Arguments = '{arguments}';
    $s.WorkingDirectory = '{working_dir}';
    $s.IconLocation = '{icon_path},0';
    $s.Description = '{description}';
    $s.Save();
    """
    cmd = ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps_script]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.returncode == 0
    except Exception as e:
        print(f"[!] Error creating shortcut {shortcut_path}: {e}")
        return False


def check_status():
    """Inspect current shortcut locations and display status."""
    print("\n🔍 Checking Network Visor Installation Status...")
    found_any = False

    targets = [
        ("Desktop Shortcut", os.path.join(get_desktop_path(), SHORTCUT_NAME)),
    ]
    sm = get_start_menu_path()
    if sm:
        targets.append(("Start Menu Shortcut", os.path.join(sm, SHORTCUT_NAME)))

    for label, path in targets:
        if os.path.exists(path):
            found_any = True
            print(f"  [+] {label}: INSTALLED")
            print(f"      Path: {path}")
        else:
            print(f"  [-] {label}: Not installed")

    # Check executable
    if os.path.exists(DIST_EXE):
        print(f"  [+] Standalone Executable: PRESENT ({DIST_EXE})")
    else:
        print("  [-] Standalone Executable: Not compiled (run --build to compile)")

    # Check icon asset
    if os.path.exists(ASSET_ICON):
        print(f"  [+] Application Icon: PRESENT ({ASSET_ICON})")
    else:
        print("  [-] Application Icon: Missing (run generate_icon.py to generate)")

    if not found_any:
        print("\n💡 Recommendation: Run with --install to place 1-click shortcuts on your Desktop & Start Menu.")


def install(mode="auto"):
    """Installs Desktop and Start Menu shortcuts."""
    print(f"\n🛸 Installing Melody's Starship Network Visor shortcuts (Mode: {mode.upper()})...")

    # Ensure icon exists
    if not os.path.exists(ASSET_ICON):
        print("[i] Icon asset not found. Generating now...")
        try:
            from generate_icon import create_network_visor_icon
            create_network_visor_icon(os.path.join(BASE_DIR, "assets"))
        except Exception as e:
            print(f"[!] Warning: Could not auto-generate icon: {e}")

    # Determine execution target
    target_path = None
    arguments = ""

    if mode == "auto":
        if os.path.exists(DIST_EXE):
            target_path = DIST_EXE
            print(f"[i] Auto-detected standalone binary: {DIST_EXE}")
        else:
            target_path = get_pythonw_path()
            arguments = f'"{SCRIPT_PATH}"'
            print(f"[i] Standalone .exe not found; using Python script mode with {target_path}")
    elif mode == "exe":
        if not os.path.exists(DIST_EXE):
            print(f"[!] Standalone executable not found at {DIST_EXE}.")
            print("    Run with --build to compile the executable first, or install with --mode python.")
            return False
        target_path = DIST_EXE
    elif mode == "python":
        target_path = get_pythonw_path()
        arguments = f'"{SCRIPT_PATH}"'

    shortcut_targets = []
    desktop_dir = get_desktop_path()
    if os.path.exists(desktop_dir):
        shortcut_targets.append(os.path.join(desktop_dir, SHORTCUT_NAME))

    start_menu_dir = get_start_menu_path()
    if start_menu_dir and os.path.exists(start_menu_dir):
        shortcut_targets.append(os.path.join(start_menu_dir, SHORTCUT_NAME))

    success_count = 0
    for sc_path in shortcut_targets:
        if create_shortcut(
            target_path=target_path,
            arguments=arguments,
            shortcut_path=sc_path,
            icon_path=ASSET_ICON if os.path.exists(ASSET_ICON) else target_path,
            working_dir=BASE_DIR,
            description=APP_DESCRIPTION
        ):
            print(f"  [+] Shortcut created: {sc_path}")
            success_count += 1
        else:
            print(f"  [!] Failed to create shortcut at: {sc_path}")

    refresh_explorer()
    print(f"\n✨ Installation complete! Created {success_count} shortcut(s).")
    print(f"🎯 Target: {target_path} {arguments}".strip())
    print("💡 Double-click the shortcut on your Desktop or search 'Network Visor' in Start Menu to launch!")
    return True


def uninstall():
    """Removes created Desktop and Start Menu shortcuts."""
    print("\n🧹 Initializing Network Visor Shortcut Removal...")
    removed_count = 0

    shortcut_targets = [
        os.path.join(get_desktop_path(), SHORTCUT_NAME)
    ]
    sm = get_start_menu_path()
    if sm:
        shortcut_targets.append(os.path.join(sm, SHORTCUT_NAME))

    for sc_path in shortcut_targets:
        if os.path.exists(sc_path):
            try:
                os.remove(sc_path)
                print(f"  [-] Removed: {sc_path}")
                removed_count += 1
            except Exception as e:
                print(f"  [!] Could not remove {sc_path}: {e}")

    refresh_explorer()
    print(f"\n✨ Uninstallation complete! Removed {removed_count} shortcut(s).")
    return True


def build_executable():
    """Build or rebuild standalone executable with PyInstaller."""
    print("\n🛸 Launching PyInstaller build sequence for Starship Network Visor...")

    # Ensure icon exists
    if not os.path.exists(ASSET_ICON):
        print("[i] Ensuring icon assets are ready...")
        try:
            from generate_icon import create_network_visor_icon
            create_network_visor_icon(os.path.join(BASE_DIR, "assets"))
        except Exception as e:
            print(f"[!] Warning: Icon generation error: {e}")

    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", SPEC_PATH]
    try:
        res = subprocess.run(cmd, cwd=BASE_DIR)
        if res.returncode == 0:
            print(f"\n✨ Executable built successfully in {DIST_EXE}!")
            return True
        else:
            print(f"\n[!] Build failed with exit code {res.returncode}")
            return False
    except Exception as e:
        print(f"\n[!] Build execution error: {e}")
        return False


def interactive_menu():
    """Terminal UI for interactive setup."""
    while True:
        print("\n" + "=" * 60)
        print("      🛸 NETWORK VISOR — DESKTOP SETUP & BUILDER 📡      ")
        print("=" * 60)
        print("  [1] Install Desktop & Start Menu Shortcuts (Standalone .EXE)")
        print("  [2] Install Desktop & Start Menu Shortcuts (Python Script / Dev)")
        print("  [3] Check Installation Status")
        print("  [4] Rebuild Standalone Executable (PyInstaller)")
        print("  [5] Uninstall Desktop Shortcuts")
        print("  [6] Exit")
        print("-" * 60)

        choice = input("Select an option [1-6]: ").strip()

        if choice == "1":
            install(mode="exe")
        elif choice == "2":
            install(mode="python")
        elif choice == "3":
            check_status()
        elif choice == "4":
            build_executable()
        elif choice == "5":
            uninstall()
        elif choice == "6":
            print("\nExiting. May your sub-space network latency remain low! 🛸✨\n")
            break
        else:
            print("[!] Invalid option. Please enter a number between 1 and 6.")


def main():
    parser = argparse.ArgumentParser(description="Starship Network Visor Desktop Setup")
    parser.add_argument("--install", action="store_true", help="Install Desktop and Start Menu shortcuts")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall shortcuts")
    parser.add_argument("--status", action="store_true", help="Check current installation status")
    parser.add_argument("--mode", choices=["auto", "exe", "python"], default="auto", help="Launch target mode (default: auto)")
    parser.add_argument("--build", action="store_true", help="Rebuild executable using PyInstaller")

    args = parser.parse_args()

    if args.build:
        build_executable()
    elif args.install:
        install(mode=args.mode)
    elif args.uninstall:
        uninstall()
    elif args.status:
        check_status()
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
