# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: force_delete.py
# ☆ Date: 2026-01-04
# ☆
# ☆ Version 1.0.8a
# ☆ Description: Deletes directories using shutil, psutil, 
# ☆ and Robocopy Mirror. Includes an explicit Reboot Queue option.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import os
import shutil
import stat
import time
import psutil
import subprocess
import ctypes

def remove_readonly(func, path, excinfo):
    """Clears read-only attributes on failure."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def get_locking_processes(target_path):
    """Returns a list of processes currently using the target folder."""
    target_abs = os.path.abspath(target_path)
    locking_procs = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for flist in proc.open_files():
                if flist.path.startswith(target_abs):
                    locking_procs.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return locking_procs

def schedule_delete_on_reboot(target_path):
    """Schedules the folder for deletion on next Windows restart."""
    abs_path = os.path.abspath(target_path)
    # 0x00000004 = MOVEFILE_DELAY_UNTIL_REBOOT
    result = ctypes.windll.kernel32.MoveFileExW(abs_path, None, 0x00000004)
    if result != 0:
        print(f"SUCCESS: '{abs_path}' queued for deletion on next reboot.")
        return True
    else:
        error = ctypes.GetLastError()
        print(f"FAILURE: Error code {error}. Try running as Administrator.")
        return False

def force_nuke_robocopy(target_path):
    """Uses the Robocopy Mirror trick to wipe a folder's contents."""
    temp_empty = os.path.join(os.environ['TEMP'], 'empty_dir_for_wipe')
    if not os.path.exists(temp_empty):
        os.makedirs(temp_empty)
    
    print(f"Applying Robocopy Mirror Force Wipe...")
    subprocess.run(['robocopy', temp_empty, target_path, '/mir', '/purge'], 
                   capture_output=True, text=True)
    
    time.sleep(1)
    try:
        os.rmdir(target_path)
        return True
    except:
        return False

def execute_deletion(folder_path):
    print(f"\n--- [2] NORMAL RUN: PREPARING DELETION ---")
    confirm = input(f"Confirm deletion of '{folder_path}'?\nType 'DELETE' to confirm: ")
    
    if confirm == 'DELETE':
        # 1. Kill user-level processes
        procs = get_locking_processes(folder_path)
        for p in procs:
            try:
                if p.info['name'].lower() != "system":
                    print(f"Terminating {p.info['name']}...")
                    p.kill()
            except: pass
        
        time.sleep(1)
        
        # 2. Try standard deletion
        try:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path, onerror=remove_readonly)
            if not os.path.exists(folder_path):
                print(f"SUCCESS: Folder eliminated.")
                return True
        except:
            print("Standard deletion failed. Attempting Force Mode (Robocopy)...")
        
        # 3. Fallback to Robocopy Nuke
        if force_nuke_robocopy(folder_path):
            print("SUCCESS: Folder eliminated via Force Mode.")
            return True
        else:
            print("FAILURE: Even Force Mode failed. Consider the Reboot Option (Menu Item 3).")
    return False

def main():
    # Set to drive root to ensure script doesn't lock its own path
    os.chdir(os.environ['SystemDrive'] + "\\")
    
    target_path = r"F:\VRChat\Projects\Illumi - Edit"

    while True:
        if not os.path.exists(target_path):
            print(f"\nTarget path '{target_path}' no longer exists.")
            break

        print(f"\nTarget: {target_path}")
        print("1. Dry Run")
        print("2. Normal Run (Standard + Robocopy Force)")
        print("3. Queue for Delete on Reboot")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ")

        if choice == '1':
            print(f"--- Dry Run: Scanning {target_path} ---")
            procs = get_locking_processes(target_path)
            if procs:
                for p in procs: print(f" [LOCK] {p.info['name']} (PID: {p.info['pid']})")
            else:
                print(" No active locks detected.")
            input("Press Enter to return...")
        elif choice == '2':
            if execute_deletion(target_path): break
        elif choice == '3':
            confirm = input(f"Queue '{target_path}' for delete on reboot? (y/n): ")
            if confirm.lower() == 'y':
                if schedule_delete_on_reboot(target_path): break
        elif choice == '4':
            break

if __name__ == "__main__":
    main()
