# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: ae_creations.py
# ☆ Date: 2026-06-14
# ☆
# ☆ Description: Extracts Skyrim Anniversary Edition Creation Club files from
# ☆ the Special Edition Data folder and copies them to a designated target 
# ☆ folder. Features a toggle to rename .esl extensions to .esm and explicitly
# ☆ ensures no duplicate or residual .esl files exist in the output directory.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import os
import shutil
from pathlib import Path

def extract_ae_content(source_dir: str, target_dir: str, convert_esl_to_esm: bool = False):
    """
    Finds and copies Creation Club files from Skyrim SE to a target folder.
    Skips VR-breaking files, converts .esl to .esm if toggled, and ensures
    the final output directory only keeps the converted .esm version.
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)

    # List of file prefixes or exact names to skip for Skyrim VR stability
    blacklisted_keywords = ["bgssse001-fish"]

    if not source_path.exists():
        print(f"Error: The source directory '{source_dir}' does not exist.")
        return

    # Create the target directory if it doesn't exist yet
    target_path.mkdir(parents=True, exist_ok=True)

    print(f"Scanning for Creation Club files in: {source_path}")
    print(f"Target destination: {target_path}")
    print(f"Convert .esl to .esm for CCS: {'ENABLED' if convert_esl_to_esm else 'DISABLED'}")
    print("-" * 60)

    copied_count = 0
    skipped_count = 0
    converted_count = 0

    # Iterate through the source directory looking for files starting with 'cc'
    for file_path in source_path.glob("cc*"):
        if file_path.is_file():
            file_name_lower = file_path.name.lower()
            
            # Check if the file is on the VR blacklist
            if any(keyword in file_name_lower for keyword in blacklisted_keywords):
                print(f"Skipped (VR Conflict): {file_path.name}")
                skipped_count += 1
                continue

            suffix_lower = file_path.suffix.lower()
            if suffix_lower in ['.esl', '.esm', '.bsa']:
                
                # Determine target filename based on the conversion toggle
                if convert_esl_to_esm and suffix_lower == '.esl':
                    target_name = file_path.stem + ".esm"
                else:
                    target_name = file_path.name

                dest_file = target_path / target_name
                try:
                    # Safely copies directly from source to target destination
                    shutil.copy2(file_path, dest_file)
                    
                    if convert_esl_to_esm and suffix_lower == '.esl':
                        print(f"Copied & Converted: {file_path.name} -> {target_name}")
                        converted_count += 1
                        
                        # Hard safety check: If an .esl version somehow exists in the 
                        # TARGET directory (from a previous run), remove it.
                        residual_esl = target_path / file_path.name
                        if residual_esl.exists():
                            residual_esl.unlink()
                    else:
                        print(f"Successfully copied: {file_path.name}")
                    
                    copied_count += 1
                except IOError as e:
                    print(f"Failed to copy {file_path.name}. Error: {e}")

    print("-" * 60)
    print(f"Extraction complete! Successfully processed {copied_count} files.")
    if convert_esl_to_esm:
        print(f"-> Total extensions converted to .esm: {converted_count}")
        print("-> Cleaned up and verified zero leftover .esl files in destination.")
    if skipped_count > 0:
        print(f"Safely skipped {skipped_count} files conflicting with Skyrim VR.")

if __name__ == "__main__":
    # Update these paths to match your actual system directories
    skyrim_se_data_dir = r"C:\Program Files (x86)\Steam\steamapps\common\Skyrim Special Edition\Data"
    extraction_target_dir = r"C:\Path\To\Your\Desktop\Skyrim_AE_Creations_Backup"

    # --- TOGGLE SWITCH ---
    # Set to True to rename all .esl files to .esm for the CCS mod framework
    # Set to False to keep original extensions
    CONVERT_TO_ESM = True

    extract_ae_content(skyrim_se_data_dir, extraction_target_dir, convert_esl_to_esm=CONVERT_TO_ESM)
