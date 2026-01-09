# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: file_searcher.py
# ☆ Date: 2026-01-09
# ☆ Version: 1.0.2a
# ☆
# ☆ Description: Advanced file searcher with drive detection, progress 
# ☆ indicators, relevance ranking, timestamped exports, adjustable 
# ☆ limits, and a search duration timer.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import os
import difflib
import string
import sys
import time
from datetime import datetime

def get_available_drives():
    """Detects available drive letters on Windows or root on Unix-like systems."""
    drives = []
    if sys.platform == "win32":
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)
    else:
        drives = ["/"]
    return drives

def save_results_to_file(results, target_name, duration):
    """Saves the search results to a text file with a unique timestamped filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"search_results_{timestamp}.txt"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Search Results for: {target_name if target_name else 'All Files'}\n")
            f.write(f"Date of Search: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Search Duration: {duration:.2f} seconds\n")
            f.write("="*80 + "\n")
            f.write(f"{'Relevance':<10} | {'File Name':<30} | {'Full Path'}\n")
            f.write("-" * 80 + "\n")
            for name, path in results:
                score = "N/A"
                if target_name:
                    score = f"{difflib.SequenceMatcher(None, target_name.lower(), name.lower()).ratio():.1%}"
                f.write(f"{score:<10} | {name[:30]:<30} | {path}\n")
        print(f"\n☆ Results successfully saved to: {filename} ☆")
    except Exception as e:
        print(f"\nError saving file: {e}")

def get_limit_choice():
    """Prompts the user to select how many files to list."""
    print("\nHow many results would you like to see?")
    print("1. 25")
    print("2. 50")
    print("3. 100")
    print("4. ALL")
    
    limit_map = {"1": 25, "2": 50, "3": 100, "4": None}
    while True:
        choice = input("Select an option (1-4): ").strip()
        if choice in limit_map:
            return limit_map[choice]
        print("Invalid choice. Please select 1, 2, 3, or 4.")

def search_files():
    while True:
        print("\n" + "="*40)
        print(" ☆ FILE SEARCHER MENU ☆")
        print("="*40)
        
        drives = get_available_drives()
        for i, drive in enumerate(drives, 1):
            print(f"{i}. Scan Drive {drive}")
        
        print(f"{len(drives) + 1}. Enter a manual path")
        print(f"{len(drives) + 2}. Exit")
        
        choice = input("\nSelect an option: ").strip()

        if choice == str(len(drives) + 2):
            print("Exiting searcher. Goodbye! ☆")
            break

        if choice == str(len(drives) + 1):
            search_path = input("Enter the full directory path: ").strip()
        elif choice.isdigit() and 1 <= int(choice) <= len(drives):
            search_path = drives[int(choice) - 1]
        else:
            print("Invalid selection. Please try again.")
            continue

        if not os.path.exists(search_path):
            print(f"Error: The path '{search_path}' does not exist.")
            continue

        target_name = input("Enter filename (Leave blank to list all files): ").strip()
        ext_input = input("Enter file extension (e.g., 'pdf', 'txt') or 'ANY' for all: ").strip().lower()

        if ext_input == "any" and not target_name:
            print("\n[!] Error: You cannot search for 'ANY' extension without a filename.")
            print("Restarting the script logic...\n")
            continue

        limit = get_limit_choice()

        print(f"\nSearching in: {search_path}...")
        
        # Start Timer
        start_time = time.time()
        
        matches = []
        dir_count = 0

        try:
            for root, dirs, files in os.walk(search_path):
                dir_count += 1
                sys.stdout.write(f"\rScanning... Folders processed: {dir_count} | Found: {len(matches)}")
                sys.stdout.flush()

                for file in files:
                    file_name_part, file_ext = os.path.splitext(file)
                    clean_ext = file_ext.lower().replace('.', '')
                    ext_match = (ext_input == "any" or ext_input == clean_ext)
                    
                    if ext_match:
                        if not target_name or (target_name.lower() in file.lower()):
                            full_path = os.path.join(root, file)
                            matches.append((file, full_path))
            
            # End Timer
            end_time = time.time()
            duration = end_time - start_time
            
            sys.stdout.write("\r" + " " * 70 + "\r")
            sys.stdout.flush()

        except PermissionError:
            print(f"\nWarning: Access denied to some folders in {search_path}.")
            duration = time.time() - start_time
        except KeyboardInterrupt:
            print(f"\nSearch cancelled by user.")
            continue

        if not matches:
            print(f"No matching files found. (Scan took {duration:.2f} seconds)")
        else:
            if target_name:
                matches.sort(
                    key=lambda x: difflib.SequenceMatcher(None, target_name.lower(), x[0].lower()).ratio(),
                    reverse=True
                )
            
            results = matches[:limit]
            
            print(f"\nSearch Complete! Time taken: {duration:.2f} seconds")
            print(f"Results (Showing {len(results)} of {len(matches)} found):")
            print(f"{'Relevance':<10} | {'File Name':<30} | {'Full Path'}")
            print("-" * 100)

            for name, path in results:
                score_str = f"{difflib.SequenceMatcher(None, target_name.lower(), name.lower()).ratio():>9.1%}" if target_name else "   N/A    "
                display_name = (name[:27] + '...') if len(name) > 30 else name
                print(f"{score_str} | {display_name:<30} | {path}")

            export_choice = input("\nWould you like to export these results to a text file? (y/n): ").strip().lower()
            if export_choice == 'y':
                save_results_to_file(results, target_name, duration)

        input("\nPress Enter to return to the menu...")

if __name__ == "__main__":
    search_files()
