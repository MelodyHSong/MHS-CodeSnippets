# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: __main__.py
# ☆ Date: 2026-08-13
# ☆
# ☆ Description: CLI entry point for NetworkInfo real-time 
# ☆ terminal performance analyzer with kaomoji status displays.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import os
import sys
import argparse
from .core import NetworkAnalyzer



def main():
    # Enable ANSI escape sequence processing on Windows terminals
    if sys.platform == "win32":
        os.system("")

    parser = argparse.ArgumentParser(
        description="Real-Time Network Performance Analyzer (Alien HUD)"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=10,
        help="Target framerate limit to prevent flicker (default: 10 FPS)",
    )
    parser.add_argument(
        "--target",
        type=str,
        default="8.8.8.8",
        help="Target host to ping for latency measurement (default: 8.8.8.8)",
    )

    args = parser.parse_args()

    analyzer = NetworkAnalyzer(fps=args.fps, ping_target=args.target)
    analyzer.run()


if __name__ == "__main__":
    main()
