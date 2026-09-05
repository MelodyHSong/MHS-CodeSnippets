# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: utils.py
# ☆ Date: September 2026
# ☆ Description: Network samplers, Win32 ICMP ping, ASCII renderers, and telemetry utilities
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import os
import sys
import json
import time
import socket
import shutil
import subprocess
import threading
from typing import Tuple, List, Dict, Any

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


import re
import unicodedata

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
        # 1. Check if user has data.json next to executable
        exe_dir = os.path.dirname(sys.executable)
        exe_data = os.path.join(exe_dir, "data.json")
        if os.path.exists(exe_data):
            return exe_data

        # 2. Check PyInstaller _MEIPASS bundle directory
        if hasattr(sys, "_MEIPASS"):
            bundle_root = os.path.join(sys._MEIPASS, "data.json")
            if os.path.exists(bundle_root):
                return bundle_root
            bundle_sub = os.path.join(sys._MEIPASS, "NetworkInfo", "data.json")
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
            "settings": {"target_fps": 10, "ping_target": "8.8.8.8"},
            "alien_kaomojis": {"optimal": ["(👽 ⟟⋏⏁⟒⍀⋏⟒⏁ ⍜⌿⏁⟟⌲⏃⌰)"]},
            "alien_messages": ["Transmitting alien telemetry..."],
            "stats": {}
        }


def save_data(data: Dict[str, Any], filepath: str = None):
    if filepath is None:
        if getattr(sys, "frozen", False):
            # When frozen, save to the executable directory to persist across runs
            filepath = os.path.join(os.path.dirname(sys.executable), "data.json")
        else:
            filepath = get_data_file_path()
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


# Windows Win32 ctypes helper for zero-subprocess network stats & ICMP ping
if sys.platform == "win32":
    import ctypes
    import struct

    class MIB_IFROW(ctypes.Structure):
        _fields_ = [
            ('wszName', ctypes.c_wchar * 256),
            ('dwIndex', ctypes.c_ulong),
            ('dwType', ctypes.c_ulong),
            ('dwMtu', ctypes.c_ulong),
            ('dwSpeed', ctypes.c_ulong),
            ('dwPhysAddrLen', ctypes.c_ulong),
            ('bPhysAddr', ctypes.c_ubyte * 8),
            ('dwAdminStatus', ctypes.c_ulong),
            ('dwOperStatus', ctypes.c_ulong),
            ('dwLastChange', ctypes.c_ulong),
            ('dwInOctets', ctypes.c_ulong),
            ('dwInUcastPkts', ctypes.c_ulong),
            ('dwInNUcastPkts', ctypes.c_ulong),
            ('dwInDiscards', ctypes.c_ulong),
            ('dwInErrors', ctypes.c_ulong),
            ('dwInUnknownProtos', ctypes.c_ulong),
            ('dwOutOctets', ctypes.c_ulong),
            ('dwOutUcastPkts', ctypes.c_ulong),
            ('dwOutNUcastPkts', ctypes.c_ulong),
            ('dwOutDiscards', ctypes.c_ulong),
            ('dwOutErrors', ctypes.c_ulong),
            ('dwOutQLen', ctypes.c_ulong),
            ('dwDescrLen', ctypes.c_ulong),
            ('bDescr', ctypes.c_ubyte * 256),
        ]

    class MIB_IFTABLE(ctypes.Structure):
        _fields_ = [
            ('dwNumEntries', ctypes.c_ulong),
            ('table', MIB_IFROW * 1)
        ]

    def _get_win32_net_counters() -> Tuple[int, int]:
        """Reads network interface bytes directly from Windows iphlpapi.dll (0 subprocesses)."""
        try:
            iphlpapi = ctypes.windll.iphlpapi
            buf_len = ctypes.c_ulong(0)
            iphlpapi.GetIfTable(None, ctypes.byref(buf_len), False)
            if buf_len.value == 0:
                return 0, 0

            buf = ctypes.create_string_buffer(buf_len.value)
            if iphlpapi.GetIfTable(ctypes.cast(buf, ctypes.POINTER(MIB_IFTABLE)), ctypes.byref(buf_len), False) == 0:
                table = ctypes.cast(buf, ctypes.POINTER(MIB_IFTABLE)).contents
                num_entries = table.dwNumEntries
                if num_entries == 0:
                    return 0, 0

                entries = (MIB_IFROW * num_entries).from_address(ctypes.addressof(table.table))
                total_in = 0
                total_out = 0
                for row in entries:
                    if row.dwType != 24:  # Exclude loopback (IF_TYPE_SOFTWARE_LOOPBACK = 24)
                        total_in += row.dwInOctets
                        total_out += row.dwOutOctets
                return total_in, total_out
        except Exception:
            pass
        return 0, 0

    class IP_OPTION_INFORMATION(ctypes.Structure):
        _fields_ = [
            ('Ttl', ctypes.c_ubyte),
            ('Tos', ctypes.c_ubyte),
            ('Flags', ctypes.c_ubyte),
            ('OptionsSize', ctypes.c_ubyte),
            ('OptionsData', ctypes.c_void_p),
        ]

    class ICMP_ECHO_REPLY(ctypes.Structure):
        _fields_ = [
            ('Address', ctypes.c_ulong),
            ('Status', ctypes.c_ulong),
            ('RoundTripTime', ctypes.c_ulong),
            ('DataSize', ctypes.c_ushort),
            ('Reserved', ctypes.c_ushort),
            ('Data', ctypes.c_void_p),
            ('Options', IP_OPTION_INFORMATION),
        ]

    try:
        _iphlpapi = ctypes.windll.iphlpapi
        _iphlpapi.IcmpCreateFile.restype = ctypes.c_void_p
        _iphlpapi.IcmpCloseHandle.argtypes = [ctypes.c_void_p]
        _iphlpapi.IcmpCloseHandle.restype = ctypes.c_bool
        _iphlpapi.IcmpSendEcho.argtypes = [
            ctypes.c_void_p, ctypes.c_ulong, ctypes.c_void_p, ctypes.c_ushort,
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong, ctypes.c_ulong
        ]
        _iphlpapi.IcmpSendEcho.restype = ctypes.c_ulong
    except Exception:
        _iphlpapi = None

    def _win32_icmp_ping(target_host: str, timeout_ms: int = 1000) -> float:
        """Performs native Win32 ICMP ping using iphlpapi.dll with zero subprocess overhead."""
        if not _iphlpapi:
            return -1.0
        handle = None
        try:
            ip_str = socket.gethostbyname(target_host)
            target_ip = struct.unpack('<I', socket.inet_aton(ip_str))[0]

            handle = _iphlpapi.IcmpCreateFile()
            if not handle:
                return -1.0

            send_data = b'ping'
            reply_size = ctypes.sizeof(ICMP_ECHO_REPLY) + len(send_data) + 32
            reply_buf = ctypes.create_string_buffer(reply_size)

            res = _iphlpapi.IcmpSendEcho(
                handle,
                target_ip,
                send_data,
                len(send_data),
                None,
                reply_buf,
                reply_size,
                timeout_ms
            )

            if res > 0:
                reply = ICMP_ECHO_REPLY.from_buffer(reply_buf)
                if reply.Status == 0:  # IP_SUCCESS = 0
                    return float(reply.RoundTripTime)
        except Exception:
            pass
        finally:
            if handle:
                try:
                    _iphlpapi.IcmpCloseHandle(handle)
                except Exception:
                    pass
        return -1.0


def get_net_io_counters() -> Tuple[int, int]:
    """Returns (bytes_received, bytes_sent). Tries psutil first, falls back to native OS calls."""
    try:
        import psutil
        io = psutil.net_io_counters()
        return io.bytes_recv, io.bytes_sent
    except Exception:
        pass

    # Windows native ctypes fallback (0 subprocess overhead!)
    if sys.platform == "win32":
        return _get_win32_net_counters()

    # Linux /proc/net/dev fallback
    elif sys.platform.startswith("linux"):
        try:
            recv_total = 0
            sent_total = 0
            with open("/proc/net/dev", "r", encoding="utf-8") as f:
                lines = f.readlines()[2:]  # Skip header lines
                for line in lines:
                    if ":" in line:
                        iface, data = line.split(":", 1)
                        if iface.strip() == "lo":
                            continue  # Ignore loopback interface
                        cols = data.split()
                        if len(cols) >= 9:
                            recv_total += int(cols[0])
                            sent_total += int(cols[8])
            return recv_total, sent_total
        except Exception:
            pass

    return 0, 0


class LatencyTracker(threading.Thread):
    """Background thread to continuously measure ping latency without blocking the frame loop."""

    def __init__(self, target_host: str = "8.8.8.8", interval: float = 0.8):
        super().__init__(daemon=True)
        self.target_host = target_host
        self.interval = interval
        self.current_latency_ms: float = 0.0
        self.running = True

    def run(self):
        while self.running:
            start_time = time.perf_counter()
            success = False
            lat = -1.0

            # 1. On Windows, use Win32 IcmpSendEcho (native C call, 0 subprocesses, true ICMP ping)
            if sys.platform == "win32":
                lat = _win32_icmp_ping(self.target_host, timeout_ms=1000)
                if lat >= 0:
                    success = True

            # 2. Cross-platform fallback: Try TCP socket timing on common ports (53, 80, 443)
            if not success:
                for port in (53, 80, 443):
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(1.0)
                        s.connect((self.target_host, port))
                        s.close()
                        lat = (time.perf_counter() - start_time) * 1000.0
                        success = True
                        break
                    except Exception:
                        pass

            if success:
                self.current_latency_ms = round(lat, 1)
            else:
                self.current_latency_ms = -1.0  # -1 indicates timeout/dropped

            time.sleep(self.interval)

    def stop(self):
        self.running = False


def format_bytes(bytes_per_sec: float) -> str:
    """Formats byte counts into standard unit strings."""
    if bytes_per_sec < 1024:
        return f"{bytes_per_sec:6.1f} B/s"
    elif bytes_per_sec < 1024 * 1024:
        return f"{bytes_per_sec / 1024:6.1f} KB/s"
    elif bytes_per_sec < 1024 * 1024 * 1024:
        return f"{bytes_per_sec / (1024 * 1024):6.2f} MB/s"
    else:
        return f"{bytes_per_sec / (1024 * 1024 * 1024):6.2f} GB/s"


def render_ascii_graph(values: List[float], width: int = 40, height: int = 4, title: str = "", unit: str = "", main_color: str = CLR_LIGHT_GREEN, border_color: str = CLR_GREEN) -> List[str]:
    """Generates Alien ASCII graph rows using unicode block chars with dynamic width/height."""
    if not values:
        values = [0.0]

    padded = values[-width:]
    if len(padded) < width:
        padded = [0.0] * (width - len(padded)) + padded

    max_val = max(padded) if max(padded) > 0 else 1.0
    latest = padded[-1]

    header = f"{CLR_BOLD}{border_color}⎔─ {title} {CLR_RESET}{CLR_DIM}(Current: {latest:.1f}{unit} | Peak: {max_val:.1f}{unit}){CLR_RESET}"
    lines = [header]

    for h in reversed(range(height)):
        row_str = f"{CLR_BOLD}{border_color}│{CLR_RESET}"
        threshold_low = h / height
        threshold_high = (h + 1) / height

        for val in padded:
            norm = val / max_val if max_val > 0 else 0
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


def render_dual_ascii_graph(down_values: List[float], up_values: List[float], width: int = 40, height: int = 4, title: str = "", main_color: str = CLR_LIGHT_GREEN, border_color: str = CLR_GREEN) -> List[str]:
    """Renders Alien dual graph for Download vs Upload."""
    p_down = down_values[-width:]
    p_up = up_values[-width:]
    if len(p_down) < width:
        p_down = [0.0] * (width - len(p_down)) + p_down
    if len(p_up) < width:
        p_up = [0.0] * (width - len(p_up)) + p_up

    max_down = max(p_down) if max(p_down) > 0 else 1.0
    max_up = max(p_up) if max(p_up) > 0 else 1.0
    max_combined = max(max_down, max_up)

    curr_down = format_bytes(p_down[-1])
    curr_up = format_bytes(p_up[-1])

    header = f"{CLR_BOLD}{border_color}⌬─ {title} {CLR_RESET}{CLR_LIGHT_CYAN}▼ {curr_down}{CLR_RESET} | {CLR_LIGHT_MAGENTA}▲ {curr_up}{CLR_RESET}"
    lines = [header]

    for h in reversed(range(height)):
        row_str = f"{CLR_BOLD}{border_color}│{CLR_RESET}"
        threshold_low = h / height
        threshold_high = (h + 1) / height

        for d_val, u_val in zip(p_down, p_up):
            d_norm = d_val / max_combined if max_combined > 0 else 0
            u_norm = u_val / max_combined if max_combined > 0 else 0

            d_idx = 8 if d_norm >= threshold_high else (0 if d_norm <= threshold_low else min(8, max(1, int((d_norm - threshold_low) * height * 8))))
            u_idx = 8 if u_norm >= threshold_high else (0 if u_norm <= threshold_low else min(8, max(1, int((u_norm - threshold_low) * height * 8))))

            if d_idx > 0 and u_idx > 0:
                row_str += f"{CLR_LIGHT_YELLOW}█{CLR_RESET}"
            elif d_idx > 0:
                row_str += f"{CLR_LIGHT_CYAN}{BLOCK_CHARS[d_idx]}{CLR_RESET}"
            elif u_idx > 0:
                row_str += f"{CLR_LIGHT_MAGENTA}{BLOCK_CHARS[u_idx]}{CLR_RESET}"
            else:
                row_str += " "

        lines.append(row_str)

    footer = f"{CLR_BOLD}{border_color}└{'─' * width}{CLR_RESET}"
    lines.append(footer)
    return lines


def get_active_adapter_info(target_host: str = "8.8.8.8") -> Dict[str, str]:
    """Resolves active network adapter name, local IPv4 address, and MAC address."""
    info = {
        "interface": "Auto-Detect Interface",
        "ip": "127.0.0.1",
        "mac": "N/A",
        "status": "Offline"
    }

    local_ip = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect((target_host, 80))
        local_ip = s.getsockname()[0]
        s.close()
        info["ip"] = local_ip
        info["status"] = "Connected"
    except Exception:
        pass

    try:
        import psutil
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        matched_iface = None
        if local_ip:
            for iface_name, iface_addrs in addrs.items():
                for addr in iface_addrs:
                    if addr.family == socket.AF_INET and addr.address == local_ip:
                        matched_iface = iface_name
                        info["interface"] = iface_name
                        break
                if matched_iface:
                    break

        if not matched_iface:
            for iface_name, iface_stat in stats.items():
                if iface_stat.isup and "loopback" not in iface_name.lower():
                    matched_iface = iface_name
                    info["interface"] = iface_name
                    break

        if matched_iface and matched_iface in addrs:
            for addr in addrs[matched_iface]:
                if getattr(addr, 'family', None) not in (socket.AF_INET, getattr(socket, 'AF_INET6', 23)):
                    if addr.address and len(addr.address.replace('-', ':').split(':')) == 6:
                        info["mac"] = addr.address.replace('-', ':').upper()
                        break
    except Exception:
        pass

    return info


def export_telemetry(metrics_data: Dict[str, Any], filepath: str = None, export_format: str = "json") -> str:
    """Exports session telemetry metrics to disk in JSON or CSV format."""
    if filepath is None:
        ts = time.strftime("%Y%m%d_%H%M%S")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = f"telemetry_export_{ts}.{export_format.lower()}"
        filepath = os.path.join(base_dir, filename)

    if export_format.lower() == "csv":
        import csv
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Sample_Index", "Download_KBps", "Upload_KBps", "Latency_ms"])
            downloads = metrics_data.get("download_history", [])
            uploads = metrics_data.get("upload_history", [])
            latencies = metrics_data.get("latency_history", [])
            n = max(len(downloads), len(uploads), len(latencies))
            for i in range(n):
                d = downloads[i] if i < len(downloads) else 0.0
                u = uploads[i] if i < len(uploads) else 0.0
                l = latencies[i] if i < len(latencies) else 0.0
                writer.writerow([i, round(d, 2), round(u, 2), round(l, 2)])
    else:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(metrics_data, f, indent=2, ensure_ascii=False)

    return filepath

