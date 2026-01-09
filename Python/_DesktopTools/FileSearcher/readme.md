# ☆ File Searcher ☆

An advanced Python-based utility designed to navigate local drives and directories to locate files with precision. This tool replaces slow OS indexing with a lightweight, real-time crawl that ranks results based on string relevance.

## ☆ Features
* **Purpose:** To provide a fast, terminal-based file discovery tool that offers deeper control over search paths, extension filtering, and result exporting than standard OS search bars.
* **Safety Guardrails:** Includes `PermissionError` handling to bypass restricted system directories safely and a robust `while` loop structure to prevent accidental script termination. The search logic is separated from system-critical paths to ensure stability during deep drive crawls.
* **Drive Detection:** Automatically identifies and lists available drive letters (Windows) or root paths (Unix/macOS).
* **Relevance Ranking:** Uses similarity algorithms to ensure that the files most closely matching your input appear at the top of the list.
* **Progress Tracking:** Features a dynamic folder counter and "Matches Found" indicator to show real-time activity.
* **Timestamped Exports:** Allows saving results to unique `.txt` files named with the date and time to prevent overwriting previous searches.
* **Performance Timer:** Measures and displays the exact duration of the search in seconds.

## ☆ Prerequisites
* **Python 3.6+**: The script uses modern Python string formatting and standard libraries.
* **Operating System**: Compatible with Windows, macOS, and Linux.
* **Standard Libraries**: No external dependencies (pip installs) are required. Uses `os`, `difflib`, `string`, `sys`, `time`, and `datetime`.

### Installation

1. **Clone or Copy**: Copy the script content into a file named `file_searcher.py`.
2. **Access Terminal**: Open your Command Prompt, PowerShell, or Terminal.
3. **Execution**: Run the script using the following command:
   
   ```bash
   python file_searcher.py
   ``` 
   OR run using Visual Studio Code ona dedicated terminal. 
