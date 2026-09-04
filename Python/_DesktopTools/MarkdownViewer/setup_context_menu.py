# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: setup_context_menu.py
# ☆ Date: September 3, 2026
# ☆
# ☆ Description: Windows context menu installer and uninstaller for Galactic Markdown Editor.
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

# Constants & Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_EXE = os.path.join(BASE_DIR, "dist", "live_md_editor.exe")
SCRIPT_PATH = os.path.join(BASE_DIR, "live_md_editor.py")
ASSET_ICON = os.path.join(BASE_DIR, "assets", "galaxy_md.ico")
SPEC_PATH = os.path.join(BASE_DIR, "live_md_editor.spec")

MENU_VERB = "GalacticMarkdownEditor"
MENU_LABEL = "🛸 Open with Galactic Markdown Editor"
TARGET_EXTENSIONS = [".md", ".markdown", ".mdown", ".mkd"]

def get_pythonw_path():
    """Locate pythonw.exe to run without opening a console window."""
    py_dir = os.path.dirname(sys.executable)
    pythonw = os.path.join(py_dir, "pythonw.exe")
    if os.path.exists(pythonw):
        return pythonw
    return sys.executable

def refresh_explorer():
    """Notify the Windows Shell to reload file association and context menu caches immediately."""
    try:
        # SHCNE_ASSOCCHANGED = 0x08000000, SHCNF_IDLIST = 0x0000
        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
        return True
    except Exception as e:
        print(f"[!] Warning: Could not refresh Explorer shell cache: {e}")
        return False

def delete_key_recursive(root_hkey, subkey_path):
    """Recursively delete a Windows registry key and all its subkeys."""
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

def check_status():
    """Inspect current registry keys and display the installation status."""
    print("\n🔍 Checking Galactic Markdown Editor Registry Status...")
    found_any = False
    
    for ext in TARGET_EXTENSIONS:
        sys_key_path = f"Software\\Classes\\SystemFileAssociations\\{ext}\\shell\\{MENU_VERB}"
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sys_key_path, 0, winreg.KEY_READ) as k:
                val, _ = winreg.QueryValueEx(k, "")
                cmd_path = f"{sys_key_path}\\command"
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, cmd_path, 0, winreg.KEY_READ) as ck:
                    cmd_val, _ = winreg.QueryValueEx(ck, "")
                print(f"  [✓] {ext:<10} -> Registered ({val})")
                print(f"      Command: {cmd_val}")
                found_any = True
        except FileNotFoundError:
            print(f"  [ ] {ext:<10} -> Not registered")
        except Exception as e:
            print(f"  [!] {ext:<10} -> Error: {e}")

    app_key_path = f"Software\\Classes\\Applications\\live_md_editor.exe\\shell\\open\\command"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, app_key_path, 0, winreg.KEY_READ) as k:
            app_cmd, _ = winreg.QueryValueEx(k, "")
            print(f"  [✓] Open-With App Entry: Registered")
            print(f"      Command: {app_cmd}")
            found_any = True
    except FileNotFoundError:
        print(f"  [ ] Open-With App Entry: Not registered")

    if found_any:
        print("\n✨ Context menu integration is currently ACTIVE.")
    else:
        print("\n💤 Context menu integration is currently NOT INSTALLED.")
    return found_any

def install(mode="auto"):
    """
    Install right-click context menu into HKCU\\Software\\Classes.
    mode: 'auto' | 'exe' | 'python'
    """
    print("\n🚀 Initializing Galactic Context Menu Installation...")

    # Determine execution mode and command
    target_command = ""
    icon_target = ""

    if mode == "auto":
        if os.path.exists(DIST_EXE):
            mode = "exe"
        else:
            mode = "python"

    if mode == "exe":
        if not os.path.exists(DIST_EXE):
            print(f"[!] Error: Standalone binary not found at:\n    {DIST_EXE}")
            print("[i] You can compile it using --build or install in Python mode using --mode python.")
            return False
        target_command = f'"{DIST_EXE}" "%1"'
        icon_target = DIST_EXE
        print(f"  Mode: Standalone Executable\n  Target: {DIST_EXE}")
    else:
        pythonw = get_pythonw_path()
        if not os.path.exists(SCRIPT_PATH):
            print(f"[!] Error: Python script not found at:\n    {SCRIPT_PATH}")
            return False
        target_command = f'"{pythonw}" "{SCRIPT_PATH}" "%1"'
        icon_target = ASSET_ICON if os.path.exists(ASSET_ICON) else pythonw
        print(f"  Mode: Python Script (Dev Mode)\n  Engine: {pythonw}\n  Script: {SCRIPT_PATH}")

    # Fallback to asset icon if available
    if os.path.exists(ASSET_ICON):
        icon_target = ASSET_ICON

    success_count = 0

    # 1. Register for each extension in SystemFileAssociations
    for ext in TARGET_EXTENSIONS:
        sys_key_path = f"Software\\Classes\\SystemFileAssociations\\{ext}\\shell\\{MENU_VERB}"
        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, sys_key_path) as k:
                winreg.SetValueEx(k, "", 0, winreg.REG_SZ, MENU_LABEL)
                if icon_target and os.path.exists(icon_target):
                    winreg.SetValueEx(k, "Icon", 0, winreg.REG_SZ, icon_target)

            cmd_key_path = f"{sys_key_path}\\command"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_key_path) as ck:
                winreg.SetValueEx(ck, "", 0, winreg.REG_SZ, target_command)
            
            success_count += 1
        except Exception as e:
            print(f"[!] Failed to register {sys_key_path}: {e}")

    # 2. Register also in Classes\{ext}\shell for maximum compatibility
    for ext in TARGET_EXTENSIONS:
        ext_key_path = f"Software\\Classes\\{ext}\\shell\\{MENU_VERB}"
        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, ext_key_path) as k:
                winreg.SetValueEx(k, "", 0, winreg.REG_SZ, MENU_LABEL)
                if icon_target and os.path.exists(icon_target):
                    winreg.SetValueEx(k, "Icon", 0, winreg.REG_SZ, icon_target)

            cmd_key_path = f"{ext_key_path}\\command"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_key_path) as ck:
                winreg.SetValueEx(ck, "", 0, winreg.REG_SZ, target_command)
        except Exception as e:
            pass  # Optional fallback

    # 3. Register under Applications\live_md_editor.exe for Open With flyout
    try:
        app_base = "Software\\Classes\\Applications\\live_md_editor.exe"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, app_base) as ak:
            winreg.SetValueEx(ak, "", 0, winreg.REG_SZ, "Galactic Markdown Editor")
            winreg.SetValueEx(ak, "FriendlyAppName", 0, winreg.REG_SZ, "Galactic Markdown Editor")

        supported_types = f"{app_base}\\SupportedTypes"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, supported_types) as stk:
            for ext in TARGET_EXTENSIONS:
                winreg.SetValueEx(stk, ext, 0, winreg.REG_SZ, "")

        app_cmd_key = f"{app_base}\\shell\\open\\command"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, app_cmd_key) as ack:
            winreg.SetValueEx(ack, "", 0, winreg.REG_SZ, target_command)
    except Exception as e:
        print(f"[!] Note: Could not register Applications subkey: {e}")

    # Refresh Windows Shell
    refresh_explorer()

    print(f"\n✨ Context menu successfully installed for {success_count} extensions!")
    print(f"🛸 Menu Label: {MENU_LABEL}")
    print(f"🎯 Command: {target_command}")
    print("💡 Windows Explorer cache refreshed. Right-click any .md file to test!")
    return True

def uninstall():
    """Remove all registered context menu keys from the registry."""
    print("\n🧹 Initializing Galactic Context Menu Removal...")
    removed_count = 0

    for ext in TARGET_EXTENSIONS:
        # SystemFileAssociations
        sys_key_path = f"Software\\Classes\\SystemFileAssociations\\{ext}\\shell\\{MENU_VERB}"
        if delete_key_recursive(winreg.HKEY_CURRENT_USER, sys_key_path):
            removed_count += 1

        # Classes\{ext}\shell
        ext_key_path = f"Software\\Classes\\{ext}\\shell\\{MENU_VERB}"
        delete_key_recursive(winreg.HKEY_CURRENT_USER, ext_key_path)

    # Applications subkey
    app_base = "Software\\Classes\\Applications\\live_md_editor.exe"
    delete_key_recursive(winreg.HKEY_CURRENT_USER, app_base)

    refresh_explorer()
    print(f"\n✨ Context menu successfully uninstalled! All registry entries removed.")
    print("💡 Windows Explorer cache refreshed.")
    return True

def build_executable():
    """Build or rebuild standalone executable with PyInstaller."""
    print("\n🛸 Launching PyInstaller build sequence...")
    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", SPEC_PATH]
    try:
        res = subprocess.run(cmd, cwd=BASE_DIR)
        if res.returncode == 0:
            print("\n✨ Executable built successfully in dist/live_md_editor.exe!")
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
        print("   🛸 GALACTIC MARKDOWN EDITOR — CONTEXT MENU SETUP 🛸   ")
        print("=" * 60)
        print("  [1] Install Context Menu (Standalone Executable Mode)")
        print("  [2] Install Context Menu (Python Script / Dev Mode)")
        print("  [3] Check Installation Status")
        print("  [4] Rebuild Standalone Executable (PyInstaller)")
        print("  [5] Uninstall Context Menu")
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
            print("\nExiting. Safe travels across the galaxy! 👽✨\n")
            break
        else:
            print("[!] Invalid option. Please enter a number between 1 and 6.")

def main():
    parser = argparse.ArgumentParser(description="Galactic Markdown Editor Context Menu Setup")
    parser.add_argument("--install", action="store_true", help="Install context menu")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall context menu")
    parser.add_argument("--status", action="store_true", help="Check current registration status")
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
