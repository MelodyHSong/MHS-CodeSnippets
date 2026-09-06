# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: setup_context_menu.py
# ☆ Description: Compatibility alias forwarding to setup_integration.py.
# ☆ [Template Tier: Tier 2 (Optional - Windows Shell Integration)]
# ☆ Safe to delete if: Using setup_integration.py directly, or if tool has no shell integration.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import setup_integration

if __name__ == "__main__":
    setup_integration.main()
