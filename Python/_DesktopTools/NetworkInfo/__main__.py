# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: __main__.py
# ☆ Date: September 2026
# ☆ Description: Dual-mode entry point (Desktop GUI HUD by default, ANSI Terminal with --cli)
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import os
import sys
import argparse

try:
    from .core import NetworkAnalyzer
    from .network_info import NetworkVisorApp
except (ImportError, ValueError):
    from core import NetworkAnalyzer
    from network_info import NetworkVisorApp


def main():
    # Enable ANSI escape sequence processing on Windows terminals
    if sys.platform == "win32":
        os.system("")

    parser = argparse.ArgumentParser(
        description="Melody's Starship Network Visor - Cosmic Real-Time Network Telemetry Workstation"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Launch in classic terminal ANSI HUD mode instead of desktop GUI",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=None,
        help="Target telemetry framerate (default: 10 FPS)",
    )
    parser.add_argument(
        "--target",
        type=str,
        default=None,
        help="Target host or IP to ping for latency measurement (default: 8.8.8.8)",
    )

    args = parser.parse_args()

    if args.cli:
        analyzer = NetworkAnalyzer(fps=args.fps, ping_target=args.target)
        analyzer.run()
    else:
        import tkinter as tk
        root = tk.Tk()
        app = NetworkVisorApp(root, ping_target=args.target, fps=args.fps)
        root.mainloop()


if __name__ == "__main__":
    main()
