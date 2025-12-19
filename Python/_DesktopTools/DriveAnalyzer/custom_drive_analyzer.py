# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: custom_drive_analyzer.py
# ☆ Date: 2025-12-19
# ☆
# ☆ Description: Analyzes a drive for the largest files and folders.
# ☆ Features a minimalist stat tracker (no bar) and box-styled tables.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

# Pythion-chan is slithering through directories to find the biggest files and folders!
# She uses a sleek minimalist stat tracker to keep you updated without overwhelming you.
# Finally, she presents the findings in elegant box-styled tables for easy reading.

import os
import shutil
import time
from tqdm import tqdm
from collections import defaultdict

def get_largest_items(file_limit=20, folder_limit=10):
    # ☆ Prompt user for the drive letter
    print("┌────────────────────────────────────────┐")
    print("│      ☆ STORAGE ANALYSIS TOOL ☆         │")
    print("└────────────────────────────────────────┘")
    user_input = input("☆ Enter drive letter (e.g., C, D, E): ").strip().upper()
    
    # ☆ Clean and validate drive path
    drive_path = os.path.normpath(user_input.rstrip(":\\") + ":") + os.sep
    
    if not os.path.exists(drive_path):
        print(f"☆ Error: Drive '{drive_path}' not found or inaccessible.")
        return

    file_list = []
    folder_sizes = defaultdict(int)
    start_time = time.time()
    
    # ☆ Minimalist Stat Tracker: Shows description, file count, elapsed time, and speed.
    pbar = tqdm(
        desc=f"☆ Scanning {drive_path}", 
        unit=" files",
        dynamic_ncols=True,
        bar_format='{desc}: {n_fmt}{unit} [{elapsed}, {rate_fmt}]'
    )

    for root, dirs, files in os.walk(drive_path):
        for name in files:
            try:
                filepath = os.path.join(root, name)
                file_size = os.path.getsize(filepath)
                
                _, extension = os.path.splitext(name)
                extension = extension.lower() if extension else "None"
                
                file_list.append((name, extension, root, file_size))
                
                # ☆ Aggregate sizes upward
                temp_path = root
                while True:
                    folder_sizes[temp_path] += file_size
                    parent = os.path.dirname(temp_path)
                    if parent == temp_path:
                        break
                    temp_path = parent
                
                pbar.update(1)
            except (OSError, PermissionError):
                continue
    
    total_scanned = pbar.n
    pbar.close()
    
    duration = max(time.time() - start_time, 0.1)

    # ☆ Sort data
    file_list.sort(key=lambda x: x[3], reverse=True)
    sorted_folders = sorted(folder_sizes.items(), key=lambda x: x[1], reverse=True)

    # --- NICE FORMATTED OUTPUT ---

    # ☆ Top Files Table
    print(f"\n╔{'═'*112}╗")
    print(f"║ {'TOP ' + str(file_limit) + ' LARGEST FILES':^110} ║")
    print(f"╠{'═'*32}╦{'═'*10}╦{'═'*12}╦{'═'*55}╣")
    print(f"║ {'FILE NAME':<30} ║ {'TYPE':<8} ║ {'SIZE (GB)':<10} ║ {'DIRECTORY':<53} ║")
    print(f"╠{'═'*32}╬{'═'*10}╬{'═'*12}╬{'═'*55}╣")
    
    for i in range(min(file_limit, len(file_list))):
        name, ftype, folder, size = file_list[i]
        print(f"║ {name[:30]:<30} ║ {ftype[:8]:<8} ║ {size / (1024**3):>10.2f} ║ {folder[:53]:<53} ║")
    print(f"╚{'═'*32}╩{'═'*10}╩{'═'*12}╩{'═'*55}╝")

    # ☆ Top Folders Table
    print(f"\n╔{'═'*75}╗")
    print(f"║ {'TOP ' + str(folder_limit) + ' LARGEST FOLDERS':^73} ║")
    print(f"╠{'═'*62}╦{'═'*12}╣")
    print(f"║ {'FOLDER PATH':<60} ║ {'SIZE (GB)':<10} ║")
    print(f"╠{'═'*62}╬{'═'*12}╣")
    for i in range(min(folder_limit, len(sorted_folders))):
        path, size = sorted_folders[i]
        print(f"║ {path[:60]:<60} ║ {size / (1024**3):>10.2f} ║")
    print(f"╚{'═'*62}╩{'═'*12}╝")

    # ☆ Final Summary Bar and Performance Stats
    try:
        total, used, free = shutil.disk_usage(drive_path)
        pct = (used / total) * 100
        bar = '█' * int(pct / 4) + '░' * (25 - int(pct / 4))
        
        print(f"\n☆ DRIVE {drive_path} STATUS:")
        print(f"[{bar}] {pct:.1f}% Full")
        print(f"Total: {total/(1024**3):.2f} GB | Used: {used/(1024**3):.2f} GB | Free: {free/(1024**3):.2f} GB")
        
        print(f"\n☆ SCAN SUMMARY:")
        print(f"Processed {total_scanned:,} files in {duration:.2f} seconds.")
        print(f"Average speed: {total_scanned/duration:.0f} files/sec.\n")
    except Exception:
        pass

    
if __name__ == "__main__": 
    get_largest_items() 

    # ☆ End of custom_drive_analyzer.py ☆ 
