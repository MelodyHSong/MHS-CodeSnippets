# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: DirMapper.py
# ☆ Date: 2026-01-24
# ☆
# ☆ Description: Recursively maps a directory structure into a visual tree.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import os

def map_directory(start_path, indent=""):
    try:
        # Get a list of files and folders, excluding hidden ones
        items = [i for i in os.listdir(start_path) if not i.startswith('.')]
        
        for index, item in enumerate(items):
            path = os.path.join(start_path, item)
            is_last = (index == len(items) - 1)
            
            # Use ASCII symbols for the tree branches
            connector = "└── " if is_last else "├── "
            print(f"{indent}{connector}{item}")
            
            if os.path.isdir(path):
                # Add extra indent for sub-folders
                extension = "    " if is_last else "│   "
                map_directory(path, indent + extension)
                
    except PermissionError:
        print(f"{indent}└── [Permission Denied]")

if __name__ == "__main__":
    # Get the current directory where the script is located
    current_dir = os.getcwd()
    print(f"☆ Directory Map for: {current_dir}\n")
    map_directory(current_dir)