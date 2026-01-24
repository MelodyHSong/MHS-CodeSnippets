# ☆ Directory Mapper ☆

> "Mapping the chaos of your folders, one branch at a time."

A Python utility that generates a visual ASCII tree structure of your directories. This is particularly useful for documenting project architectures, sharing file structures in READMEs, or just keeping track of your "Beyond" story assets.

## ☆ Installation & Prerequisites

No external libraries are required! This script uses Python's built-in `os` module.

### Quick Install

1. Copy the code into a file named `DirMapper.py`.
2. Place the script in the root folder you wish to map.

## ☆ Usage

Run the script from your terminal. It will automatically detect the directory it is currently in and map everything beneath it.

###	Example Usage

```powershell
python DirMapper.py
```

*Note: Large directories (like a Unity project's Library folder) can generate very long outputs. It is recommended to run this in your root project folder while avoiding massive build-cache folders*

###☆ License
This project is licensed under the MIT License. You are free to use, modify, and distribute this code in your own projects—just keep the headers intact!

*Lost in the files? Let me draw you a map— by MelodyHSong*
