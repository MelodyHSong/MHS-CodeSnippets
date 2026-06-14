# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: ae_creations.py
# ☆ Date: 2026-06-14
# ☆
# ☆ Description: Extracts Skyrim Anniversary Edition Creation Club files from
# ☆ the Special Edition Data folder and copies them to a designated target 
# ☆ folder, automatically skipping known problematic VR files (like Fishing).
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import os
import shutil
from pathlib import Path

def extract_ae_content(source_dir: str, target_dir: str):
    """
    Finds and copies Creation Club files from Skyrim SE to a target folder,
    excluding files known to cause issues or crashes in Skyrim VR.
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)

    # List of file prefixes or exact names to skip for Skyrim VR stability
    # Fishing (ccbgssse001-fish) is known to cause heavy scripting issues/crashes.
    blacklisted_keywords = ["bgssse001-fish"]

    if not source_path.exists():
        print(f"Error: The source directory '{source_dir}' does not exist.")
        return

    # Create the target directory if it doesn't exist yet
    target_path.mkdir(parents=True, exist_ok=True)

    print(f"Scanning for Creation Club files in: {source_path}")
    print(f"Target destination: {target_path}\n" + "-"*50)

    copied_count = 0
    skipped_count = 0

    # Iterate through the source directory looking for files starting with 'cc'
    for file_path in source_path.glob("cc*"):
        if file_path.is_file():
            file_name_lower = file_path.name.lower()
            
            # Check if the file is on the VR blacklist
            if any(keyword in file_name_lower for keyword in blacklisted_keywords):
                print(f"Skipped (VR Conflict): {file_path.name}")
                skipped_count += 1
                continue

            # Copy allowed .esl, .esm, and .bsa files
            if file_path.suffix.lower() in ['.esl', '.esm', '.bsa']:
                dest_file = target_path / file_path.name
                try:
                    shutil.copy2(file_path, dest_file)
                    print(f"Successfully copied: {file_path.name}")
                    copied_count += 1
                except IOError as e:
                    print(f"Failed to copy {file_path.name}. Error: {e}")

    print("-"*50)
    print(f"Extraction complete! Successfully copied {copied_count} files.")
    if skipped_count > 0:
        print(f"Safely skipped {skipped_count} files conflicting with Skyrim VR.")

if __name__ == "__main__":
    # Update these paths to match your actual system directories
    # Use raw strings (r"...") to handle Windows backslashes properly
    skyrim_se_data_dir = r"C:\Program Files (x86)\Steam\steamapps\common\Skyrim Special Edition\Data"
    extraction_target_dir = r"C:\Path\To\Your\Desktop\Skyrim_AE_Creations_Backup"

    extract_ae_content(skyrim_se_data_dir, extraction_target_dir)
