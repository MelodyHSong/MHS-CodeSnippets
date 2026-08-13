# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: extract_fo4_dlc.py
# ☆ Date: 2026-06-18
# ☆
# ☆ Description: Extracts official Fallout 4 DLC and Workshop files from 
# ☆ the installation's Data folder and copies them to a designated target 
# ☆ folder on the Desktop (explicitly excluding Creation Club content).
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import os
import shutil
from pathlib import Path

def extract_fo4_dlc(source_dir: str, target_dir: str):
    """
    Finds and copies official Fallout 4 DLC and Workshop files to a target folder.
    Matches master files, light masters, and BA2 archives, completely ignoring
    any Creation Club content.
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)

    # Specific prefixes for official FO4 DLCs & Workshop content
    dlc_prefixes = [
        "dlccoast",       # Far Harbor
        "dlcnukaworld",   # Nuka-World
        "dlcrobot",       # Automatron
        "dlcworkshop01",  # Wasteland Workshop
        "dlcworkshop02",  # Contraptions Workshop
        "dlcworkshop03"   # Vault-Tec Workshop
    ]

    if not source_path.exists():
        print(f"Error: The source directory '{source_dir}' does not exist.")
        return

    # Create the target directory if it doesn't exist yet
    target_path.mkdir(parents=True, exist_ok=True)

    print(f"Scanning for Fallout 4 DLC files in: {source_path}")
    print(f"Target destination: {target_path}")
    print("-" * 60)

    copied_count = 0

    # Iterate through all files in the source Data directory
    for file_path in source_path.iterdir():
        if file_path.is_file():
            file_name_lower = file_path.name.lower()
            
            # Check if the file matches any official DLC/Workshop prefixes
            if any(file_name_lower.startswith(prefix) for prefix in dlc_prefixes):
                suffix_lower = file_path.suffix.lower()
                
                # Capture plugins (.esm, .esl) and archive packages (.ba2)
                if suffix_lower in ['.esm', '.esl', '.ba2']:
                    dest_file = target_path / file_path.name
                    try:
                        print(f"Copying: {file_path.name} ...")
                        shutil.copy2(file_path, dest_file)
                        copied_count += 1
                    except IOError as e:
                        print(f"Failed to copy {file_path.name}. Error: {e}")

    print("-" * 60)
    print(f"Extraction complete! Successfully processed {copied_count} files.")

if __name__ == "__main__":
    # Dynamically locate the Desktop path for the user
    desktop_path = Path(os.path.expanduser("~")) / "Desktop"
    
    # --- SETUP CONFIGURATION PATHS ---
    # Update the source path if your Steam library is on a different drive
    fo4_data_dir = r"C:\Program Files (x86)\Steam\steamapps\common\Fallout 4\Data"
    extraction_target_dir = str(desktop_path / "Fallout4_DLC_Backup")

    extract_fo4_dlc(fo4_data_dir, extraction_target_dir)
