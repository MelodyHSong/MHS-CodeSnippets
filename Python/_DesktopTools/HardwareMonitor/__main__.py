import os
import sys
import argparse
try:
    from .core import HardwareAnalyzer
except (ImportError, ValueError):
    from core import HardwareAnalyzer


def main():
    # Enable ANSI escape sequence processing on Windows terminals
    if sys.platform == "win32":
        os.system("")

    parser = argparse.ArgumentParser(
        description="Kaomoji Real-Time Hardware Performance & Responsiveness Analyzer HUD"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=10,
        help="Target framerate limit to prevent screen flicker (default: 10 FPS)",
    )

    args = parser.parse_args()

    analyzer = HardwareAnalyzer(fps=args.fps)
    analyzer.run()


if __name__ == "__main__":
    main()
