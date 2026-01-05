# ☆ Force Deleter ☆

A high-privilege Python utility designed to eliminate stubborn, locked, or system-protected directories that standard Windows commands cannot remove.

## ☆ Features
* **Purpose:** Forcefully deletes directories that return "Access Denied" or "File in Use" (WinError 32) errors.
* **Stage 1: Standard Kill:** Uses `psutil` to identify and terminate user-level processes (like Unity or VRChat Creator Companion) holding locks.
* **Stage 2: Robocopy Mirror:** A fallback "Force Mode" that mirrors an empty directory into the target to wipe contents at a low level.
* **Stage 3: Reboot Queue:** A manual option to use the `MoveFileEx` Windows API to delete the folder during the next system boot sequence.
* **Dry Run Mode:** Scans the folder to list all files and identify which specific PIDs/Process names are currently holding handles.
* **Safety Guardrails:** Requires an explicit `DELETE` string confirmation and includes `os.chdir` logic to prevent the script from locking its own path.
* **Persistent UI:** A looping menu system that allows for testing and execution in a single session.

## ☆ Prerequisites
Ensure you have Python installed. You must run your terminal as **Administrator** to allow the script to kill processes and access the Windows boot registry.

### Installation
```bash
python -m pip install psutil
