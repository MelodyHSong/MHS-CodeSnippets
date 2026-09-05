# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: setup_integration.py
# ☆ Description: Windows context menu, desktop shortcut installer, and PyInstaller builder for Desktop Tool Template.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import sys
import os
import winreg
import ctypes
import argparse
import subprocess

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ==============================================================================
# ☆ TOOL CONFIGURATION & INTEGRATION SETTINGS
# ==============================================================================
# Edit these settings to rebrand or customize for any new tool project:
APP_TITLE = "Desktop Tool Template"
APP_SLUG = "desktop_tool_template"
APP_DESCRIPTION = "Desktop Tool Template - Modern Tkinter Workstation Blueprint"
DIST_EXE_NAME = "desktop_tool.exe"
ENTRY_SCRIPT = "app.py"
SPEC_FILE = "desktop_tool.spec"
ICON_SUBPATH = os.path.join("assets", "app_icon.ico")

# Feature Toggles:
ENABLE_CONTEXT_MENU = True
CONTEXT_MENU_VERB = APP_SLUG
CONTEXT_MENU_LABEL = "⭐ Open with Desktop Tool"
TARGET_EXTENSIONS = [".txt", ".md", ".json", ".log"]

ENABLE_DESKTOP_SHORTCUT = True
ENABLE_START_MENU_SHORTCUT = True
SHORTCUT_NAME = f"{APP_TITLE}.lnk"

# Derived Absolute Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_EXE = os.path.join(BASE_DIR, "dist", DIST_EXE_NAME)
SCRIPT_PATH = os.path.join(BASE_DIR, ENTRY_SCRIPT)
ASSET_ICON = os.path.join(BASE_DIR, ICON_SUBPATH)
SPEC_PATH = os.path.join(BASE_DIR, SPEC_FILE)


def get_pythonw_path():
    """Locate pythonw.exe to run without opening an unnecessary console window."""
    py_dir = os.path.dirname(sys.executable)
    pythonw = os.path.join(py_dir, "pythonw.exe")
    if os.path.exists(pythonw):
        return pythonw
    return sys.executable


def get_desktop_path():
    """Retrieve the current user's Desktop folder."""
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
    """Notify the Windows Shell to reload file associations, shortcuts, and icon caches."""
    try:
        # SHCNE_ASSOCCHANGED = 0x08000000, SHCNF_IDLIST = 0x0000
        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
        return True
    except Exception as e:
        print(f"[!] Warning: Could not refresh Explorer shell cache: {e}")
        return False


def delete_key_recursive(root_hkey, subkey_path):
    """Recursively delete a Windows registry key and all subkeys."""
    try:
        key = winreg.OpenKey(root_hkey, subkey_path, 0, winreg.KEY_ALL_ACCESS)
    except FileNotFoundError:
        return True
    except PermissionError:
        return False

    while True:
        try:
            sub = winreg.EnumKey(key, 0)
            delete_key_recursive(root_hkey, f"{subkey_path}\\{sub}")
        except OSError:
            break
    winreg.CloseKey(key)

    try:
        winreg.DeleteKey(root_hkey, subkey_path)
        return True
    except OSError:
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


# ==============================================================================
# ☆ CORE ACTIONS: STATUS, INSTALL, UNINSTALL, BUILD
# ==============================================================================
def check_status():
    """Inspect current registry keys and shortcuts, displaying installation status."""
    print(f"\n🔍 Checking {APP_TITLE} Installation Status...")
    found_any = False

    # 1. Check Context Menu Entries
    if ENABLE_CONTEXT_MENU:
        print("\n--- Right-Click Context Menu Associations ---")
        for ext in TARGET_EXTENSIONS:
            sys_key = f"Software\\Classes\\SystemFileAssociations\\{ext}\\shell\\{CONTEXT_MENU_VERB}"
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sys_key, 0, winreg.KEY_READ) as k:
                    val, _ = winreg.QueryValueEx(k, "")
                    cmd_key = f"{sys_key}\\command"
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, cmd_key, 0, winreg.KEY_READ) as ck:
                        cmd_val, _ = winreg.QueryValueEx(ck, "")
                    print(f"  [✓] {ext:<10} -> Registered ('{val}')")
                    print(f"      Command: {cmd_val}")
                    found_any = True
            except FileNotFoundError:
                print(f"  [ ] {ext:<10} -> Not registered")

    # 2. Check Shortcuts
    print("\n--- Windows Shortcuts ---")
    shortcuts = []
    if ENABLE_DESKTOP_SHORTCUT:
        shortcuts.append(("Desktop Shortcut", os.path.join(get_desktop_path(), SHORTCUT_NAME)))
    if ENABLE_START_MENU_SHORTCUT:
        sm = get_start_menu_path()
        if sm:
            shortcuts.append(("Start Menu Shortcut", os.path.join(sm, SHORTCUT_NAME)))

    for label, path in shortcuts:
        if os.path.exists(path):
            found_any = True
            print(f"  [✓] {label:<20} -> Present ({path})")
        else:
            print(f"  [ ] {label:<20} -> Missing")

    # 3. Check Executable & Assets
    print("\n--- Binaries & Assets ---")
    if os.path.exists(DIST_EXE):
        print(f"  [✓] Standalone Binary   -> Present ({DIST_EXE})")
    else:
        print(f"  [ ] Standalone Binary   -> Not compiled (Run --build to generate)")

    if os.path.exists(ASSET_ICON):
        print(f"  [✓] Application Icon    -> Present ({ASSET_ICON})")
    else:
        print(f"  [ ] Application Icon    -> Missing (Run generate_icon.py)")

    if found_any:
        print(f"\n✨ {APP_TITLE} is currently ACTIVE.")
    else:
        print(f"\n💤 {APP_TITLE} integration is currently NOT INSTALLED.")
    return found_any


def install(mode="auto"):
    """
    Installs Windows shell integrations:
      - Context menu entries in HKCU\\Software\\Classes
      - Desktop & Start Menu .lnk shortcuts
    mode: 'auto' | 'exe' | 'python'
    """
    print(f"\n🚀 Initializing {APP_TITLE} Integration Setup...")

    # Determine execution target
    if mode == "auto":
        mode = "exe" if os.path.exists(DIST_EXE) else "python"

    if mode == "exe":
        if not os.path.exists(DIST_EXE):
            print(f"[!] Standalone binary not found at:\n    {DIST_EXE}")
            print("[i] Hint: Compile it with --build, or install in Python mode with --mode python.")
            return False
        target_path = DIST_EXE
        arguments = ""
        context_cmd = f'"{DIST_EXE}" "%1"'
        icon_target = DIST_EXE
        print(f"  Target Mode: Standalone Executable (.exe)")
    else:
        pythonw = get_pythonw_path()
        if not os.path.exists(SCRIPT_PATH):
            print(f"[!] Error: Entry script not found at:\n    {SCRIPT_PATH}")
            return False
        target_path = pythonw
        arguments = f'"{SCRIPT_PATH}"'
        context_cmd = f'"{pythonw}" "{SCRIPT_PATH}" "%1"'
        icon_target = ASSET_ICON if os.path.exists(ASSET_ICON) else pythonw
        print(f"  Target Mode: Python Script (pythonw.exe)")

    if os.path.exists(ASSET_ICON):
        icon_target = ASSET_ICON

    # 1. Register Context Menus
    context_success = 0
    if ENABLE_CONTEXT_MENU:
        print("\n  [+] Registering context menus...")
        for ext in TARGET_EXTENSIONS:
            sys_key = f"Software\\Classes\\SystemFileAssociations\\{ext}\\shell\\{CONTEXT_MENU_VERB}"
            try:
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, sys_key) as k:
                    winreg.SetValueEx(k, "", 0, winreg.REG_SZ, CONTEXT_MENU_LABEL)
                    if icon_target and os.path.exists(icon_target):
                        winreg.SetValueEx(k, "Icon", 0, winreg.REG_SZ, icon_target)

                cmd_key = f"{sys_key}\\command"
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_key) as ck:
                    winreg.SetValueEx(ck, "", 0, winreg.REG_SZ, context_cmd)

                context_success += 1
            except Exception as e:
                print(f"  [!] Failed to register {sys_key}: {e}")

        # Open-With Application entry
        try:
            app_base = f"Software\\Classes\\Applications\\{DIST_EXE_NAME}"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, app_base) as ak:
                winreg.SetValueEx(ak, "", 0, winreg.REG_SZ, APP_TITLE)
                winreg.SetValueEx(ak, "FriendlyAppName", 0, winreg.REG_SZ, APP_TITLE)

            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{app_base}\\SupportedTypes") as stk:
                for ext in TARGET_EXTENSIONS:
                    winreg.SetValueEx(stk, ext, 0, winreg.REG_SZ, "")

            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{app_base}\\shell\\open\\command") as ack:
                winreg.SetValueEx(ack, "", 0, winreg.REG_SZ, context_cmd)
        except Exception as e:
            print(f"  [!] Open-With registration notice: {e}")

    # 2. Create Desktop & Start Menu Shortcuts
    shortcut_success = 0
    if ENABLE_DESKTOP_SHORTCUT:
        desk_file = os.path.join(get_desktop_path(), SHORTCUT_NAME)
        if create_shortcut(target_path, arguments, desk_file, icon_target, BASE_DIR, APP_DESCRIPTION):
            print(f"  [✓] Desktop shortcut created: {desk_file}")
            shortcut_success += 1

    if ENABLE_START_MENU_SHORTCUT:
        sm = get_start_menu_path()
        if sm:
            sm_file = os.path.join(sm, SHORTCUT_NAME)
            if create_shortcut(target_path, arguments, sm_file, icon_target, BASE_DIR, APP_DESCRIPTION):
                print(f"  [✓] Start Menu shortcut created: {sm_file}")
                shortcut_success += 1

    # Refresh Windows Shell
    refresh_explorer()

    print(f"\n✨ Installation complete!")
    if ENABLE_CONTEXT_MENU:
        print(f"  • Context Menu: Enabled for {context_success} extensions ('{CONTEXT_MENU_LABEL}')")
    if shortcut_success > 0:
        print(f"  • Shortcuts: {shortcut_success} placed")
    print("  • Explorer shell cache refreshed successfully.")
    return True


def uninstall():
    """Removes all registered context menu keys and Windows shortcuts."""
    print(f"\n🧹 Initializing {APP_TITLE} Uninstallation...")

    # 1. Clean Context Menus
    if ENABLE_CONTEXT_MENU:
        for ext in TARGET_EXTENSIONS:
            sys_key = f"Software\\Classes\\SystemFileAssociations\\{ext}\\shell\\{CONTEXT_MENU_VERB}"
            delete_key_recursive(winreg.HKEY_CURRENT_USER, sys_key)

            ext_key = f"Software\\Classes\\{ext}\\shell\\{CONTEXT_MENU_VERB}"
            delete_key_recursive(winreg.HKEY_CURRENT_USER, ext_key)

        app_base = f"Software\\Classes\\Applications\\{DIST_EXE_NAME}"
        delete_key_recursive(winreg.HKEY_CURRENT_USER, app_base)
        print("  [✓] Registry context menu entries removed.")

    # 2. Remove Shortcuts
    shortcuts = [
        os.path.join(get_desktop_path(), SHORTCUT_NAME),
    ]
    sm = get_start_menu_path()
    if sm:
        shortcuts.append(os.path.join(sm, SHORTCUT_NAME))

    for sc in shortcuts:
        if os.path.exists(sc):
            try:
                os.remove(sc)
                print(f"  [✓] Removed shortcut: {sc}")
            except Exception as e:
                print(f"  [!] Failed to remove shortcut {sc}: {e}")

    refresh_explorer()
    print(f"\n✨ Clean uninstallation completed. Windows Explorer cache refreshed.")
    return True


def build_executable():
    """Builds standalone windowed executable using PyInstaller."""
    print(f"\n🛸 Launching PyInstaller build for {APP_TITLE}...")
    if not os.path.exists(SPEC_PATH):
        print(f"[!] Spec file not found at: {SPEC_PATH}")
        return False

    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", SPEC_PATH]
    try:
        res = subprocess.run(cmd, cwd=BASE_DIR)
        if res.returncode == 0:
            print(f"\n✨ Executable built successfully in dist\\{DIST_EXE_NAME}!")
            return True
        else:
            print(f"\n[!] Build failed with exit code {res.returncode}")
            return False
    except Exception as e:
        print(f"\n[!] Build error: {e}")
        return False


def interactive_menu():
    """Terminal UI for interactive setup and management."""
    while True:
        print("\n" + "=" * 62)
        print(f"   ⭐ {APP_TITLE.upper()} — SETUP & INTEGRATION 🛸   ")
        print("=" * 62)
        print("  [1] Install (Standalone Executable Mode)")
        print("  [2] Install (Python Script / Dev Mode)")
        print("  [3] Check Installation Status")
        print("  [4] Rebuild Standalone Executable (PyInstaller)")
        print("  [5] Uninstall All Integrations & Shortcuts")
        print("  [6] Exit")
        print("-" * 62)

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
            print("\nExiting. May the stars guide your journey! ⭐✨\n")
            break
        else:
            print("[!] Invalid choice. Please enter a number between 1 and 6.")


def main():
    parser = argparse.ArgumentParser(description=f"{APP_TITLE} Setup & Integration Utility")
    parser.add_argument("--install", action="store_true", help="Install context menu and shortcuts")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall context menu and shortcuts")
    parser.add_argument("--status", action="store_true", help="Check current installation status")
    parser.add_argument("--mode", choices=["auto", "exe", "python"], default="auto", help="Execution mode (default: auto)")
    parser.add_argument("--build", action="store_true", help="Build standalone executable with PyInstaller")

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
