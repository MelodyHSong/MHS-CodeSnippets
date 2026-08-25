import os
import sys
import argparse
try:
    from .core import NetworkAnalyzer
except (ImportError, ValueError):
    from core import NetworkAnalyzer



def main():
    # Enable ANSI escape sequence processing on Windows terminals
    if sys.platform == "win32":
        os.system("")

    parser = argparse.ArgumentParser(
        description="Kaomoji Real-Time Network Performance Analyzer (Framerate Locked)"
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
