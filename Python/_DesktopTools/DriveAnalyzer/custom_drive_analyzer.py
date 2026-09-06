# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: custom_drive_analyzer.py
# ☆ Date: 2025-12-19 (Updated 2026-09-05)
# ☆
# ☆ Description: Stellar Snooper CLI - Analyzes a drive for the largest files and folders.
# ☆ Features a minimalist stat tracker and box-styled tables.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

# Pythion-chan is slithering through directories to find the biggest files and folders!
# She uses a sleek minimalist stat tracker to keep you updated without overwhelming you.
# Finally, she presents the findings in elegant box-styled tables for easy reading.

import os
import sys
import shutil
import time
from collections import defaultdict

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Optional tqdm with lightweight zero-dependency fallback
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

    class FallbackProgressBar:
        """Lightweight terminal progress ticker when tqdm is not installed."""
        def __init__(self, desc="☆ Scanning", unit=" files"):
            self.desc = desc
            self.unit = unit
            self.n = 0
            self.start_time = time.time()
            self.last_update = 0

        def update(self, count=1):
            self.n += count
            now = time.time()
            if now - self.last_update >= 0.1:  # Throttle terminal redraws to 10Hz
                self.last_update = now
                elapsed = max(now - self.start_time, 0.001)
                rate = self.n / elapsed
                mins, secs = divmod(int(elapsed), 60)
                time_str = f"{mins:02d}:{secs:02d}"
                sys.stdout.write(f"\r{self.desc}: {self.n:,}{self.unit} [{time_str}, {rate:.0f} files/s]")
                sys.stdout.flush()

        def close(self):
            now = time.time()
            elapsed = max(now - self.start_time, 0.001)
            rate = self.n / elapsed
            mins, secs = divmod(int(elapsed), 60)
            time_str = f"{mins:02d}:{secs:02d}"
            sys.stdout.write(f"\r{self.desc}: {self.n:,}{self.unit} [{time_str}, {rate:.0f} files/s]\n")
            sys.stdout.flush()

    def tqdm(desc=None, unit=None, dynamic_ncols=True, bar_format=None):
        return FallbackProgressBar(desc=desc or "☆ Scanning", unit=unit or " files")


def format_size(size_bytes):
    """Utility to format bytes into readable KB, MB, GB, or TB."""
    if size_bytes >= 1024**4:
        return f"{size_bytes / (1024**4):.2f} TB"
    elif size_bytes >= 1024**3:
        return f"{size_bytes / (1024**3):.2f} GB"
    elif size_bytes >= 1024**2:
        return f"{size_bytes / (1024**2):.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes} B"


def get_largest_items(target=None, file_limit=20, folder_limit=10):
    # ☆ Prompt user for the drive letter or directory if not provided
    print("┌────────────────────────────────────────┐")
    print("│       ☆ STELLAR SNOOPER TOOL ☆         │")
    print("└────────────────────────────────────────┘")

    if not target:
        if len(sys.argv) > 1:
            target = sys.argv[1].strip()
        else:
            target = input("☆ Enter drive letter or path (e.g., C, D, E or C:\\Users): ").strip()

    # ☆ Clean and validate target path
    if len(target) == 1 and target.isalpha():
        drive_path = os.path.normpath(f"{target.upper()}:\\") + os.sep
    elif len(target) == 2 and target[1] == ":" and target[0].isalpha():
        drive_path = os.path.normpath(f"{target.upper()}\\") + os.sep
    else:
        drive_path = os.path.abspath(target)
        if os.path.isdir(drive_path) and not drive_path.endswith(os.sep):
            drive_path += os.sep

    if not os.path.exists(drive_path):
        print(f"☆ Error: Target '{drive_path}' not found or inaccessible.")
        return None

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

        print(f"\n☆ TARGET {drive_path} STATUS:")
        print(f"[{bar}] {pct:.1f}% Full")
        print(f"Total: {total/(1024**3):.2f} GB | Used: {used/(1024**3):.2f} GB | Free: {free/(1024**3):.2f} GB")

        print(f"\n☆ SCAN SUMMARY:")
        print(f"Processed {total_scanned:,} files in {duration:.2f} seconds.")
        print(f"Average speed: {total_scanned/duration:.0f} files/sec.\n")
    except Exception:
        pass

    return {
        "target": drive_path,
        "files": file_list[:file_limit],
        "folders": sorted_folders[:folder_limit],
        "total_scanned": total_scanned,
        "duration": duration,
        "speed": total_scanned / duration if duration > 0 else 0
    }


if __name__ == "__main__":
    get_largest_items()

    # ☆ End of custom_drive_analyzer.py ☆
