import os
import sys
import json
import time
import shutil
import re
import unicodedata
import subprocess
import threading
import importlib
from typing import Tuple, List, Dict, Any, Optional

# ANSI Color and Control Codes
CLR_RESET = "\033[0m"
CLR_BOLD = "\033[1m"
CLR_DIM = "\033[2m"
CLR_BLINK = "\033[5m"

CLR_CYAN = "\033[36m"
CLR_LIGHT_CYAN = "\033[96m"
CLR_GREEN = "\033[32m"
CLR_LIGHT_GREEN = "\033[92m"
CLR_YELLOW = "\033[33m"
CLR_LIGHT_YELLOW = "\033[93m"
CLR_RED = "\033[31m"
CLR_LIGHT_RED = "\033[91m"
CLR_MAGENTA = "\033[35m"
CLR_LIGHT_MAGENTA = "\033[95m"
CLR_BLUE = "\033[34m"
CLR_WHITE = "\033[97m"

# Terminal control
ANSI_HIDE_CURSOR = "\033[?25l"
ANSI_SHOW_CURSOR = "\033[?25h"
ANSI_CURSOR_HOME = "\033[H"
ANSI_CLEAR_BOTTOM = "\033[J"

BLOCK_CHARS = [" ", " ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]

# UTF-8 Encoding setup for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ANSI_REGEX = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')


def visible_width(s: str) -> int:
    """Calculates true visual column width of a string in terminal (handling ANSI and Emojis)."""
    clean = ANSI_REGEX.sub('', s)
    w = 0
    for ch in clean:
        code = ord(ch)
        if code >= 0x1F000:
            w += 2
        elif unicodedata.east_asian_width(ch) in ('W', 'F'):
            w += 2
        else:
            w += 1
    return w


def truncate_ansi(s: str, max_width: int) -> str:
    """Safely truncates string to max_width visual columns while preserving active ANSI formatting codes."""
    if visible_width(s) <= max_width:
        return s

    v_width = 0
    result = []
    i = 0
    n = len(s)

    while i < n:
        match = ANSI_REGEX.match(s, i)
        if match:
            result.append(match.group(0))
            i = match.end()
            continue

        ch = s[i]
        code = ord(ch)
        cw = 2 if (code >= 0x1F000 or unicodedata.east_asian_width(ch) in ('W', 'F')) else 1

        if v_width + cw > max_width:
            break

        v_width += cw
        result.append(ch)
        i += 1

    result.append(CLR_RESET)
    return "".join(result)


def center_ansi(s: str, total_width: int) -> str:
    """Pads string centered according to its visual column width, truncating safely if too long."""
    if visible_width(s) > total_width:
        s = truncate_ansi(s, total_width)

    v_len = visible_width(s)
    if v_len >= total_width:
        return s

    pad_total = total_width - v_len
    left_pad = pad_total // 2
    right_pad = pad_total - left_pad
    return ' ' * left_pad + s + ' ' * right_pad


def safe_write(text: str):
    """Safely writes UTF-8 text to stdout across all platforms without charmap encoding crashes."""
    try:
        sys.stdout.write(text)
        sys.stdout.flush()
    except UnicodeEncodeError:
        try:
            sys.stdout.buffer.write(text.encode("utf-8", errors="replace"))
            sys.stdout.buffer.flush()
        except Exception:
            pass


def hide_cursor():
    safe_write(ANSI_HIDE_CURSOR)


def show_cursor():
    safe_write(ANSI_SHOW_CURSOR)


def get_terminal_dimensions() -> Tuple[int, int]:
    """Returns (columns, lines) of current terminal window."""
    size = shutil.get_terminal_size(fallback=(80, 24))
    return size.columns, size.lines


def get_data_file_path() -> str:
    """Returns absolute path to data.json, supporting PyInstaller bundles and external config."""
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(sys.executable)
        exe_data = os.path.join(exe_dir, "data.json")
        if os.path.exists(exe_data):
            return exe_data

        if hasattr(sys, "_MEIPASS"):
            bundle_root = os.path.join(sys._MEIPASS, "data.json")
            if os.path.exists(bundle_root):
                return bundle_root
            bundle_sub = os.path.join(sys._MEIPASS, "HardwareMonitor", "data.json")
            if os.path.exists(bundle_sub):
                return bundle_sub

    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "data.json")


def load_data(filepath: str = None) -> Dict[str, Any]:
    if filepath is None:
        filepath = get_data_file_path()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "settings": {"target_fps": 10, "cpu_warn_pct": 85.0, "ram_warn_pct": 85.0},
            "alien_kaomojis": {"optimal": ["(👽 ⟟⋏⏁⟒⌰⌰⏃⌠⏁ Quantum Cores Nominal)"]},
            "alien_messages": ["Alien Mothership telemetry operational..."],
            "stats": {}
        }


def save_data(data: Dict[str, Any], filepath: str = None):
    if filepath is None:
        if getattr(sys, "frozen", False):
            filepath = os.path.join(os.path.dirname(sys.executable), "data.json")
        else:
            filepath = get_data_file_path()
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


# Windows Win32 ctypes helper for zero-subprocess RAM stats
if sys.platform == "win32":
    import ctypes

    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    def _win32_get_ram() -> Tuple[float, float, float, float]:
        """Returns (percent_used, used_gb, total_gb, swap_pct) using Win32 API directly."""
        try:
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                total_gb = stat.ullTotalPhys / (1024 ** 3)
                avail_gb = stat.ullAvailPhys / (1024 ** 3)
                used_gb = total_gb - avail_gb
                pct = float(stat.dwMemoryLoad)

                total_pf = stat.ullTotalPageFile / (1024 ** 3)
                avail_pf = stat.ullAvailPageFile / (1024 ** 3)
                used_pf = total_pf - avail_pf
                swap_pct = ((used_pf / total_pf) * 100.0) if total_pf > 0 else 0.0
                return pct, used_gb, total_gb, swap_pct
        except Exception:
            pass
        return 0.0, 0.0, 0.0, 0.0


def get_ram_metrics() -> Dict[str, Any]:
    """Returns dict with RAM usage percent, used_gb, total_gb, swap_percent."""
    try:
        import psutil
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        total_gb = mem.total / (1024 ** 3)
        used_gb = mem.used / (1024 ** 3)
        return {
            "percent": mem.percent,
            "used_gb": used_gb,
            "total_gb": total_gb,
            "swap_percent": swap.percent if swap else 0.0
        }
    except Exception:
        pass

    if sys.platform == "win32":
        pct, used_gb, total_gb, swap_pct = _win32_get_ram()
        return {"percent": pct, "used_gb": used_gb, "total_gb": total_gb, "swap_percent": swap_pct}

    return {"percent": 0.0, "used_gb": 0.0, "total_gb": 0.0, "swap_percent": 0.0}


def get_cpu_metrics() -> Dict[str, Any]:
    """Returns CPU usage percent, clock frequency in GHz, and per-cpu breakdown."""
    try:
        import psutil
        pct = psutil.cpu_percent(interval=None)
        freq = psutil.cpu_freq()
        freq_ghz = (freq.current / 1000.0) if (freq and freq.current) else 0.0
        per_cpu = psutil.cpu_percent(interval=None, percpu=True)
        return {
            "percent": pct,
            "freq_ghz": freq_ghz,
            "per_cpu": per_cpu or []
        }
    except Exception:
        return {"percent": 0.0, "freq_ghz": 0.0, "per_cpu": []}


_NVML_INITED = False
_NVML_HANDLE = None

def _get_nvidia_nvml_gpu() -> Optional[Dict[str, Any]]:
    """Attempts to read NVIDIA GPU metrics using pynvml ctypes wrapper or native nvml.dll."""
    global _NVML_INITED, _NVML_HANDLE
    try:
        pynvml = importlib.import_module("pynvml")
        if not _NVML_INITED:
            pynvml.nvmlInit()
            _NVML_INITED = True
            if pynvml.nvmlDeviceGetCount() > 0:
                _NVML_HANDLE = pynvml.nvmlDeviceGetHandleByIndex(0)

        if _NVML_HANDLE:
            util = pynvml.nvmlDeviceGetUtilizationRates(_NVML_HANDLE)
            mem = pynvml.nvmlDeviceGetMemoryInfo(_NVML_HANDLE)
            name_bytes = pynvml.nvmlDeviceGetName(_NVML_HANDLE)
            name = name_bytes.decode("utf-8") if isinstance(name_bytes, bytes) else str(name_bytes)
            return {
                "available": True,
                "name": name,
                "percent": float(util.gpu),
                "vram_used_gb": mem.used / (1024 ** 3),
                "vram_total_gb": mem.total / (1024 ** 3)
            }
    except Exception:
        pass
    return None


def _get_nvidia_smi_gpu() -> Optional[Dict[str, Any]]:
    """Fallback: Queries nvidia-smi CLI for GPU load and VRAM."""
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"],
            timeout=1.0, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        ).decode("utf-8").strip()
        if out:
            parts = [p.strip() for p in out.split(",")]
            if len(parts) >= 4:
                return {
                    "available": True,
                    "name": parts[0],
                    "percent": float(parts[1]),
                    "vram_used_gb": float(parts[2]) / 1024.0,
                    "vram_total_gb": float(parts[3]) / 1024.0
                }
    except Exception:
        pass
    return None


def get_gpu_metrics() -> Dict[str, Any]:
    """Returns GPU metrics dict: available, name, percent, vram_used_gb, vram_total_gb."""
    nv_res = _get_nvidia_nvml_gpu()
    if nv_res:
        return nv_res

    smi_res = _get_nvidia_smi_gpu()
    if smi_res:
        return smi_res

    return {
        "available": False,
        "name": "N/A (Integrated Graphics)",
        "percent": 0.0,
        "vram_used_gb": 0.0,
        "vram_total_gb": 0.0
    }


class ResponsivenessTracker(threading.Thread):
    """
    Background thread measuring micro-second timer scheduling variance (jitter in ms).
    When CPU / Kernel / Interrupt load is high, scheduled timer wakes overshoot.
    """

    def __init__(self, interval: float = 0.05):
        super().__init__(daemon=True)
        self.interval = interval
        self.current_jitter_ms: float = 0.0
        self.running = True

    def run(self):
        alpha = 0.2  # Exponential smoothing factor
        while self.running:
            t0 = time.perf_counter()
            time.sleep(self.interval)
            t1 = time.perf_counter()
            elapsed = t1 - t0
            overshoot_ms = max(0.0, (elapsed - self.interval) * 1000.0)

            self.current_jitter_ms = (alpha * overshoot_ms) + ((1.0 - alpha) * self.current_jitter_ms)

    def stop(self):
        self.running = False


def format_gb(gb: float) -> str:
    return f"{gb:5.1f} GB"


def render_ascii_graph(
    values: List[float], width: int = 40, height: int = 4,
    title: str = "", unit: str = "", main_color: str = CLR_LIGHT_GREEN,
    border_color: str = CLR_GREEN, max_val_override: Optional[float] = None
) -> List[str]:
    """Generates ASCII graph rows using unicode block chars with dynamic width/height."""
    if not values:
        values = [0.0]

    padded = values[-width:]
    if len(padded) < width:
        padded = [0.0] * (width - len(padded)) + padded

    if max_val_override is not None and max_val_override > 0:
        max_val = max_val_override
    else:
        max_val = max(padded) if max(padded) > 0 else 1.0

    latest = padded[-1]

    header = f"{CLR_BOLD}{border_color}⎔─ {title} {CLR_RESET}{CLR_DIM}(Current: {latest:.1f}{unit} | Peak: {max_val:.1f}{unit}){CLR_RESET}"
    lines = [header]

    for h in reversed(range(height)):
        row_str = f"{CLR_BOLD}{border_color}│{CLR_RESET}"
        threshold_low = h / height
        threshold_high = (h + 1) / height

        for val in padded:
            norm = min(1.0, max(0.0, val / max_val)) if max_val > 0 else 0
            if norm >= threshold_high:
                idx = 8
            elif norm <= threshold_low:
                idx = 0
            else:
                fraction = (norm - threshold_low) * height
                idx = min(8, max(1, int(fraction * 8)))

            char = BLOCK_CHARS[idx]
            if idx > 0:
                row_str += f"{main_color}{char}{CLR_RESET}"
            else:
                row_str += " "

        lines.append(row_str)

    footer = f"{CLR_BOLD}{border_color}└{'─' * width}{CLR_RESET}"
    lines.append(footer)
    return lines


def render_dual_ascii_graph(
    val1_list: List[float], val2_list: List[float],
    width: int = 40, height: int = 4, title: str = "",
    label1: str = "Metric 1", label2: str = "Metric 2",
    color1: str = CLR_LIGHT_CYAN, color2: str = CLR_LIGHT_MAGENTA,
    main_color: str = CLR_LIGHT_GREEN, border_color: str = CLR_GREEN,
    max_val_override: Optional[float] = None
) -> List[str]:
    """Renders dual graph comparing two metrics side-by-side."""
    p1 = val1_list[-width:]
    p2 = val2_list[-width:]
    if len(p1) < width:
        p1 = [0.0] * (width - len(p1)) + p1
    if len(p2) < width:
        p2 = [0.0] * (width - len(p2)) + p2

    if max_val_override is not None and max_val_override > 0:
        max_combined = max_val_override
    else:
        m1 = max(p1) if max(p1) > 0 else 1.0
        m2 = max(p2) if max(p2) > 0 else 1.0
        max_combined = max(m1, m2)

    curr1 = p1[-1]
    curr2 = p2[-1]

    header = f"{CLR_BOLD}{border_color}⌬─ {title} {CLR_RESET}{color1}■ {label1}: {curr1:.1f}%{CLR_RESET} | {color2}■ {label2}: {curr2:.1f}%{CLR_RESET}"
    lines = [header]

    for h in reversed(range(height)):
        row_str = f"{CLR_BOLD}{border_color}│{CLR_RESET}"
        threshold_low = h / height
        threshold_high = (h + 1) / height

        for v1, v2 in zip(p1, p2):
            n1 = min(1.0, max(0.0, v1 / max_combined)) if max_combined > 0 else 0
            n2 = min(1.0, max(0.0, v2 / max_combined)) if max_combined > 0 else 0

            i1 = 8 if n1 >= threshold_high else (0 if n1 <= threshold_low else min(8, max(1, int((n1 - threshold_low) * height * 8))))
            i2 = 8 if n2 >= threshold_high else (0 if n2 <= threshold_low else min(8, max(1, int((n2 - threshold_low) * height * 8))))

            if i1 > 0 and i2 > 0:
                row_str += f"{CLR_LIGHT_YELLOW}█{CLR_RESET}"
            elif i1 > 0:
                row_str += f"{color1}{BLOCK_CHARS[i1]}{CLR_RESET}"
            elif i2 > 0:
                row_str += f"{color2}{BLOCK_CHARS[i2]}{CLR_RESET}"
            else:
                row_str += " "

        lines.append(row_str)

    footer = f"{CLR_BOLD}{border_color}└{'─' * width}{CLR_RESET}"
    lines.append(footer)
    return lines
