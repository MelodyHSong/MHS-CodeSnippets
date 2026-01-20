# ☆ UniTranslator ☆
### Version 1.0.0a

## ☆ Description
**UniTranslator** is a Python-based automation utility designed to bulk-translate file and folder names within a specific directory. It features a language-detection filter, allowing users to target specific source languages (e.g., Japanese, Spanish, German) while skipping others. 

This tool is particularly useful for organizing international assets, such as VRChat content or compressed archives, by normalizing filenames into a target language (default: English).

---

## ☆ Features
* **Flexible Targeting**: Translate specific file extensions (zip, txt, png) or entire folder structures.
* **Language Filtering**: Target specific source languages or use 'all' to process everything.
* **Dry Run Safety**: Preview all proposed name changes before applying them to the filesystem.
* **Sanitization**: Automatically removes invalid filesystem characters while preserving readability.
* **Summary Reporting**: Provides a final count of processed, skipped, and conflicted items.

---

## ☆ Prerequisites

### Python Version
* **Python 3.13+** (Optimized for environments where the `cgi` module is deprecated).

### Dependencies
Install the required libraries via PowerShell or CMD:
```powershell
pip install deep-translator langdetect
