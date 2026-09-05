# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: network_info.py
# ☆ Date: September 2026
# ☆
# ☆ Description: Melody's Starship Network Visor - Cosmic real-time desktop network monitoring workstation.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import os
import sys
import json
import time
import random
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Enable High-DPI Awareness on Windows
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

try:
    from .utils import (
        load_data, save_data, get_net_io_counters, LatencyTracker,
        format_bytes, get_active_adapter_info, export_telemetry
    )
except (ImportError, ValueError):
    from utils import (
        load_data, save_data, get_net_io_counters, LatencyTracker,
        format_bytes, get_active_adapter_info, export_telemetry
    )

# ==============================================================================
# ☆ COSMIC COLOR PALETTE & THEME
# ==============================================================================
BG_DARK = "#0d1117"          # Deep space obsidian
CONSOLE_FRAME = "#161b22"    # Spaceship hull console deck
SIDEBAR_BG = "#11141c"       # Telemetry sidebar
CARD_BG = "#161c26"          # Unselected HUD card
CARD_ACTIVE = "#222c3d"      # Active card
CARD_HOVER = "#1c2433"       # Hovered card
BORDER_COLOR = "#30363d"     # Panel rim border
BORDER_ACTIVE = "#58a6ff"    # Focused active border
GRAPH_BG = "#0b0e14"         # Deep void background for graphs
GRID_COLOR = "#1a212d"       # Subtle radar grid line

TEXT_PRIMARY = "#e2e8f0"     # Starlight white
TEXT_MUTED = "#8b949e"       # Cosmic dust gray
TEXT_DIM = "#586069"         # Nebula shadow

ACCENT_CYAN = "#58a6ff"      # Starlight cyan (Download / Bandwidth)
ACCENT_MAGENTA = "#bc8cff"   # Nebula magenta (Upload)
ACCENT_MINT = "#7ee787"      # Alien mint (Optimal / Link Online)
ACCENT_GOLD = "#f2cc60"      # Celestial star gold (Marginal / Ping Warning)
ACCENT_CORAL = "#f85149"     # Supernova coral (Dropped / Offline alert)

FONT_UI = ("Segoe UI", 10)
FONT_UI_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 13, "bold")
FONT_SUBTITLE = ("Segoe UI", 10, "bold")
FONT_METRIC = ("Segoe UI", 16, "bold")
FONT_METRIC_SUB = ("Consolas", 10)
FONT_KAOMOJI = ("Segoe UI Symbol", 13, "bold")
FONT_SMALL = ("Segoe UI", 9)
FONT_STATS = ("Consolas", 9)
FONT_TICKER = ("Segoe UI", 10, "italic")


class NetworkVisorApp:
    def __init__(self, root, ping_target=None, fps=None):
        self.root = root
        self.root.title("📡 Melody's Starship Network Visor - [Cosmic Telemetry HUD]")
        self.root.geometry("1160x780")
        self.root.minsize(940, 640)
        self.root.configure(bg=BG_DARK)

        # Resolve paths
        self.app_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # Load Configuration & Data
        self.data = load_data()
        settings = self.data.get("settings", {})
        self.ping_target = ping_target or settings.get("ping_target", "8.8.8.8")
        self.target_fps = fps or settings.get("target_fps", 10)
        self.latency_marginal_ms = float(settings.get("latency_marginal_ms", 100.0))
        self.ping_interval = float(settings.get("ping_interval", 0.8))

        # Metric history ring buffers (60 samples for graphs)
        self.history_size = 60
        self.speed_history = [0.0] * self.history_size
        self.download_history = [0.0] * self.history_size
        self.upload_history = [0.0] * self.history_size
        self.latency_history = [0.0] * self.history_size

        # Telemetry counters
        self.prev_recv, self.prev_sent = get_net_io_counters()
        self.last_sample_time = time.perf_counter()
        self.curr_download_bps = 0.0
        self.curr_upload_bps = 0.0
        self.curr_latency_ms = 0.0

        # Session tracking
        stats = self.data.get("stats", {})
        self.session_total_recv = 0.0
        self.session_total_sent = 0.0
        self.peak_download = float(stats.get("session_peak_download_bps", 0.0))
        self.peak_upload = float(stats.get("session_peak_upload_bps", 0.0))

        # Latency statistics
        self.all_latencies = []

        # Alien Kaomojis & Cosmic Quotes
        self.alien_kaomojis = self.data.get("alien_kaomojis", {})
        self.alien_messages = self.data.get("alien_messages", [
            "Harvesting raw Earth telemetry for Sector 7G...",
            "Sub-space relay beam synchronized with Alpha Centauri...",
            "Translating binary traffic into Intergalactic Morse Code...",
            "Quantum entanglement ping test in progress..."
        ])
        self.current_quote = random.choice(self.alien_messages)
        self.last_quote_time = time.time()
        self.current_kaomoji = "(🛸 ☌⍀⟒⟒⏁⟟⋏⌰⌇ Earthling)"
        self.current_state = "optimal"
        self.last_kaomoji_time = time.time()

        # Application State
        self.is_paused = False
        self.frame_count = 0
        self.actual_fps = float(self.target_fps)
        self.last_fps_time = time.perf_counter()

        # Active Adapter Info
        self.adapter_info = get_active_adapter_info(self.ping_target)

        # Set Window Icon
        self.set_app_icon()

        # Build GUI
        self.build_ui()

        # Bind Global Keyboard Shortcuts
        self.bind_shortcuts()

        # Start Latency Tracker Thread
        self.latency_tracker = LatencyTracker(target_host=self.ping_target, interval=self.ping_interval)
        self.latency_tracker.start()

        # Start Telemetry Loop
        self.schedule_next_frame()

        # Intercept window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)

    # ==========================================================================
    # ☆ ICON MANAGEMENT
    # ==========================================================================
    def set_app_icon(self):
        icon_path = os.path.join(self.app_dir, "assets", "network_info.ico")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(self.base_dir, "assets", "network_info.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

    # ==========================================================================
    # ☆ GUI ARCHITECTURE
    # ==========================================================================
    def build_ui(self):
        # ----------------------------------------------------------------------
        # Top Cockpit Control Deck (Header Bar)
        # ----------------------------------------------------------------------
        self.header_frame = tk.Frame(self.root, bg=CONSOLE_FRAME, height=56)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)

        # Brand / Logo
        self.brand_frame = tk.Frame(self.header_frame, bg=CONSOLE_FRAME)
        self.brand_frame.pack(side=tk.LEFT, padx=(16, 12), pady=8)

        self.brand_icon = tk.Label(
            self.brand_frame,
            text="📡",
            font=("Segoe UI Emoji", 14),
            bg=CONSOLE_FRAME,
            fg=ACCENT_CYAN
        )
        self.brand_icon.pack(side=tk.LEFT, padx=(0, 6))

        self.brand_title = tk.Label(
            self.brand_frame,
            text="MELODY'S STARSHIP NETWORK VISOR",
            font=FONT_TITLE,
            bg=CONSOLE_FRAME,
            fg=ACCENT_CYAN
        )
        self.brand_title.pack(side=tk.LEFT)

        # Health Status Pill Badge
        self.status_pill = tk.Label(
            self.header_frame,
            text="● OPTIMAL (Sub-Space Linked)",
            font=FONT_UI_BOLD,
            bg="#122a1e",
            fg=ACCENT_MINT,
            padx=12,
            pady=4,
            relief=tk.FLAT,
            bd=0
        )
        self.status_pill.pack(side=tk.LEFT, padx=12, pady=10)

        # Header Action Buttons (Right-aligned)
        self.btn_target = self.create_header_btn("🎯 Target", self.open_target_dialog, TEXT_PRIMARY)
        self.btn_pause = self.create_header_btn("⏸ Pause", self.toggle_pause, TEXT_PRIMARY)
        self.btn_reset = self.create_header_btn("🔄 Reset", self.reset_session_stats, ACCENT_GOLD)
        self.btn_export = self.create_header_btn("📤 Export", self.open_export_dialog, TEXT_PRIMARY)
        self.btn_settings = self.create_header_btn("⚙️ Settings", self.open_settings_dialog, TEXT_PRIMARY)

        # ----------------------------------------------------------------------
        # Alien Telemetry & Cosmic Commentary Deck
        # ----------------------------------------------------------------------
        self.alien_deck = tk.Frame(self.root, bg=BG_DARK, padx=12, pady=6)
        self.alien_deck.pack(fill=tk.X)

        # Left: Alien Avatar Kaomoji Card
        self.kaomoji_card = tk.Frame(
            self.alien_deck,
            bg=CARD_BG,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            padx=14,
            pady=8
        )
        self.kaomoji_card.pack(side=tk.LEFT, fill=tk.Y)

        self.kaomoji_label = tk.Label(
            self.kaomoji_card,
            text=self.current_kaomoji,
            font=FONT_KAOMOJI,
            bg=CARD_BG,
            fg=ACCENT_CYAN
        )
        self.kaomoji_label.pack(side=tk.LEFT)

        self.kaomoji_sub = tk.Label(
            self.kaomoji_card,
            text="[Sub-Space Telemetry]",
            font=FONT_SMALL,
            bg=CARD_BG,
            fg=TEXT_MUTED
        )
        self.kaomoji_sub.pack(side=tk.LEFT, padx=(10, 0))

        # Right: Cosmic Commentary Marquee Ticker
        self.ticker_card = tk.Frame(
            self.alien_deck,
            bg=CARD_BG,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            padx=14,
            pady=8
        )
        self.ticker_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0))

        self.ticker_prefix = tk.Label(
            self.ticker_card,
            text="🛸 TRANSMISSION: ",
            font=FONT_UI_BOLD,
            bg=CARD_BG,
            fg=ACCENT_GOLD
        )
        self.ticker_prefix.pack(side=tk.LEFT)

        self.ticker_text = tk.Label(
            self.ticker_card,
            text=self.current_quote,
            font=FONT_TICKER,
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            anchor="w"
        )
        self.ticker_text.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # ----------------------------------------------------------------------
        # Center Graphs Deck (Triple Canvas HUD)
        # ----------------------------------------------------------------------
        self.graphs_container = tk.Frame(self.root, bg=BG_DARK, padx=12, pady=4)
        self.graphs_container.pack(fill=tk.BOTH, expand=True)

        # Configure 3 equal grid rows for the graphs
        self.graphs_container.columnconfigure(0, weight=1)
        self.graphs_container.rowconfigure(0, weight=1)
        self.graphs_container.rowconfigure(1, weight=1)
        self.graphs_container.rowconfigure(2, weight=1)

        # Graph 1: Bandwidth Speed
        self.frame_g1, self.canvas_g1, self.lbl_g1_title, self.lbl_g1_val = self.create_graph_card(
            self.graphs_container, 0, "⚡ SUB-SPACE BANDWIDTH SPEED", ACCENT_CYAN
        )

        # Graph 2: Cosmic Latency (Ping)
        self.frame_g2, self.canvas_g2, self.lbl_g2_title, self.lbl_g2_val = self.create_graph_card(
            self.graphs_container, 1, f"🛰️ COSMIC LATENCY (Target: {self.ping_target})", ACCENT_GOLD
        )

        # Graph 3: Dual Telemetry (Download vs Upload)
        self.frame_g3, self.canvas_g3, self.lbl_g3_title, self.lbl_g3_val = self.create_graph_card(
            self.graphs_container, 2, "⌬ TELEMETRY TRANSMISSION (Cyan = Down | Magenta = Up)", ACCENT_CYAN
        )

        # ----------------------------------------------------------------------
        # Bottom Telemetry Metric Cards
        # ----------------------------------------------------------------------
        self.metrics_container = tk.Frame(self.root, bg=BG_DARK, padx=12, pady=4)
        self.metrics_container.pack(fill=tk.X)

        for i in range(5):
            self.metrics_container.columnconfigure(i, weight=1)

        # Card 1: Downlink
        self.card_dl, self.val_dl, self.sub_dl = self.create_metric_card(
            self.metrics_container, 0, "▼ DOWNLINK", "0.0 B/s", f"Peak: {format_bytes(self.peak_download)}", ACCENT_CYAN
        )

        # Card 2: Uplink
        self.card_ul, self.val_ul, self.sub_ul = self.create_metric_card(
            self.metrics_container, 1, "▲ UPLINK", "0.0 B/s", f"Peak: {format_bytes(self.peak_upload)}", ACCENT_MAGENTA
        )

        # Card 3: Session Data
        self.card_tot, self.val_tot, self.sub_tot = self.create_metric_card(
            self.metrics_container, 2, "💾 SESSION DATA", "0.0 MB", "DL: 0.0 B | UL: 0.0 B", ACCENT_MINT
        )

        # Card 4: Latency & Jitter
        self.card_ping, self.val_ping, self.sub_ping = self.create_metric_card(
            self.metrics_container, 3, "📡 PING / JITTER", "0.0 ms", "Min: -- | Avg: -- | Max: --", ACCENT_GOLD
        )

        # Card 5: Active Adapter
        iface_short = self.adapter_info["interface"]
        if len(iface_short) > 18:
            iface_short = iface_short[:16] + ".."
        self.card_adp, self.val_adp, self.sub_adp = self.create_metric_card(
            self.metrics_container, 4, "🌐 ADAPTER LINK", self.adapter_info["ip"], f"{iface_short} | {self.adapter_info['mac']}", TEXT_PRIMARY
        )

        # ----------------------------------------------------------------------
        # Status Bar (Bottom-most)
        # ----------------------------------------------------------------------
        self.status_bar = tk.Frame(self.root, bg=CONSOLE_FRAME, height=26)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_left = tk.Label(
            self.status_bar,
            text=f"Target: {self.ping_target} | Adapter: {self.adapter_info['interface']} | Mode: Native Win32 Telemetry",
            font=FONT_STATS,
            bg=CONSOLE_FRAME,
            fg=TEXT_MUTED,
            padx=12,
            pady=3
        )
        self.status_left.pack(side=tk.LEFT)

        self.status_fps = tk.Label(
            self.status_bar,
            text=f"FPS: {self.target_fps:.1f} / {self.target_fps}",
            font=FONT_STATS,
            bg=CONSOLE_FRAME,
            fg=ACCENT_CYAN,
            padx=12
        )
        self.status_fps.pack(side=tk.RIGHT)

    def create_header_btn(self, text, command, fg_color):
        btn = tk.Button(
            self.header_frame,
            text=text,
            command=command,
            bg=CARD_BG,
            fg=fg_color,
            activebackground=CARD_ACTIVE,
            activeforeground=fg_color,
            relief=tk.FLAT,
            font=FONT_UI_BOLD,
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2"
        )
        btn.pack(side=tk.RIGHT, padx=4, pady=8)
        btn.bind("<Enter>", lambda e: btn.config(bg=CARD_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=CARD_BG))
        return btn

    def create_graph_card(self, parent, row_idx, title, title_color):
        card = tk.Frame(
            parent,
            bg=CARD_BG,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )
        card.grid(row=row_idx, column=0, sticky="nsew", pady=3)

        # Header bar in graph
        header = tk.Frame(card, bg=CARD_BG, padx=8, pady=3)
        header.pack(fill=tk.X)

        lbl_title = tk.Label(header, text=title, font=FONT_SUBTITLE, bg=CARD_BG, fg=title_color)
        lbl_title.pack(side=tk.LEFT)

        lbl_val = tk.Label(header, text="--", font=FONT_METRIC_SUB, bg=CARD_BG, fg=TEXT_PRIMARY)
        lbl_val.pack(side=tk.RIGHT)

        # Vector Canvas
        canvas = tk.Canvas(card, bg=GRAPH_BG, bd=0, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0, 4))

        return card, canvas, lbl_title, lbl_val

    def create_metric_card(self, parent, col_idx, title, initial_val, initial_sub, accent_color):
        card = tk.Frame(
            parent,
            bg=CARD_BG,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            padx=10,
            pady=6
        )
        card.grid(row=0, column=col_idx, sticky="nsew", padx=3)

        lbl_title = tk.Label(card, text=title, font=FONT_SMALL, bg=CARD_BG, fg=TEXT_MUTED)
        lbl_title.pack(anchor="w")

        lbl_val = tk.Label(card, text=initial_val, font=FONT_METRIC, bg=CARD_BG, fg=accent_color)
        lbl_val.pack(anchor="w", pady=(1, 1))

        lbl_sub = tk.Label(card, text=initial_sub, font=FONT_METRIC_SUB, bg=CARD_BG, fg=TEXT_MUTED)
        lbl_sub.pack(anchor="w")

        return card, lbl_val, lbl_sub

    # ==========================================================================
    # ☆ SHORTCUTS & KEYBOARD BINDINGS
    # ==========================================================================
    def bind_shortcuts(self):
        self.root.bind("<space>", lambda e: self.toggle_pause())
        self.root.bind("<Control-r>", lambda e: self.reset_session_stats())
        self.root.bind("<Control-t>", lambda e: self.open_target_dialog())
        self.root.bind("<Control-e>", lambda e: self.open_export_dialog())
        self.root.bind("<Control-s>", lambda e: self.open_settings_dialog())
        self.root.bind("<Escape>", lambda e: self.on_window_close())
        self.root.bind("<Control-q>", lambda e: self.on_window_close())

    # ==========================================================================
    # ☆ TELEMETRY ENGINE & REAL-TIME FRAME LOOP
    # ==========================================================================
    def schedule_next_frame(self):
        delay_ms = max(20, int(1000.0 / self.target_fps))
        self.root.after(delay_ms, self.frame_tick)

    def frame_tick(self):
        if not self.is_paused:
            self.update_telemetry()
            self.update_ui()
            self.draw_graphs()

        # Framerate tracking
        self.frame_count += 1
        now = time.perf_counter()
        if now - self.last_fps_time >= 1.0:
            self.actual_fps = self.frame_count / (now - self.last_fps_time)
            self.frame_count = 0
            self.last_fps_time = now
            self.status_fps.config(text=f"FPS: {self.actual_fps:.1f} / {self.target_fps}")

        self.schedule_next_frame()

    def update_telemetry(self):
        now = time.perf_counter()
        dt = now - self.last_sample_time
        if dt < 0.12:
            return

        curr_recv, curr_sent = get_net_io_counters()

        # Compute deltas
        d_recv = max(0, curr_recv - self.prev_recv) if self.prev_recv > 0 else 0
        d_sent = max(0, curr_sent - self.prev_sent) if self.prev_sent > 0 else 0

        self.prev_recv = curr_recv
        self.prev_sent = curr_sent
        self.last_sample_time = now

        down_bps = d_recv / dt
        up_bps = d_sent / dt
        total_bps = down_bps + up_bps

        self.curr_download_bps = down_bps
        self.curr_upload_bps = up_bps

        self.session_total_recv += d_recv
        self.session_total_sent += d_sent

        if down_bps > self.peak_download:
            self.peak_download = down_bps
        if up_bps > self.peak_upload:
            self.peak_upload = up_bps

        # Push to ring buffers (KB/s)
        self.download_history.append(down_bps / 1024.0)
        if len(self.download_history) > self.history_size:
            self.download_history.pop(0)

        self.upload_history.append(up_bps / 1024.0)
        if len(self.upload_history) > self.history_size:
            self.upload_history.pop(0)

        self.speed_history.append(total_bps / 1024.0)
        if len(self.speed_history) > self.history_size:
            self.speed_history.pop(0)

        # Current latency
        lat = self.latency_tracker.current_latency_ms
        self.curr_latency_ms = lat
        self.latency_history.append(lat)
        if len(self.latency_history) > self.history_size:
            self.latency_history.pop(0)

        if lat > 0:
            self.all_latencies.append(lat)
            if len(self.all_latencies) > 200:
                self.all_latencies.pop(0)

        # Health state determination
        if lat < 0:
            new_state = "dropped"
        elif lat > self.latency_marginal_ms:
            new_state = "marginal"
        else:
            new_state = "optimal"

        if new_state != self.current_state:
            self.current_state = new_state
            self.update_kaomoji(force=True)

        # Cycle alien kaomoji periodically
        cur_t = time.time()
        if cur_t - self.last_kaomoji_time > 15.0:
            self.update_kaomoji()
            self.last_kaomoji_time = cur_t

        # Cycle cosmic quotes periodically
        if cur_t - self.last_quote_time > 18.0:
            self.current_quote = random.choice(self.alien_messages)
            self.ticker_text.config(text=self.current_quote)
            self.last_quote_time = cur_t

    def update_kaomoji(self, force=False):
        kaos = self.alien_kaomojis.get(self.current_state, ["(🛸 Sub-Space Linked)"])
        self.current_kaomoji = random.choice(kaos)
        self.kaomoji_label.config(text=self.current_kaomoji)

        if self.current_state == "optimal":
            self.status_pill.config(text="● OPTIMAL (Sub-Space Linked)", bg="#122a1e", fg=ACCENT_MINT)
            self.kaomoji_label.config(fg=ACCENT_CYAN)
            self.kaomoji_sub.config(text="[Sub-Space Telemetry: Nominal]")
        elif self.current_state == "marginal":
            self.status_pill.config(text="▲ MARGINAL (Cosmic Jitter)", bg="#322812", fg=ACCENT_GOLD)
            self.kaomoji_label.config(fg=ACCENT_GOLD)
            self.kaomoji_sub.config(text="[High Latency / Jitter Detected]")
        else:
            self.status_pill.config(text="✖ DROPPED (Signal Lost)", bg="#331416", fg=ACCENT_CORAL)
            self.kaomoji_label.config(fg=ACCENT_CORAL)
            self.kaomoji_sub.config(text="[Sub-Space Link Offline]")

    def update_ui(self):
        # Update metric cards
        self.val_dl.config(text=format_bytes(self.curr_download_bps))
        self.sub_dl.config(text=f"Peak: {format_bytes(self.peak_download)}")

        self.val_ul.config(text=format_bytes(self.curr_upload_bps))
        self.sub_ul.config(text=f"Peak: {format_bytes(self.peak_upload)}")

        tot_bytes = self.session_total_recv + self.session_total_sent
        self.val_tot.config(text=format_bytes(tot_bytes))
        self.sub_tot.config(text=f"DL: {format_bytes(self.session_total_recv)} | UL: {format_bytes(self.session_total_sent)}")

        # Latency & Jitter
        if self.curr_latency_ms < 0:
            self.val_ping.config(text="OFFLINE", fg=ACCENT_CORAL)
            self.sub_ping.config(text="Packet Timed Out")
        else:
            color = ACCENT_MINT if self.curr_latency_ms <= self.latency_marginal_ms else ACCENT_GOLD
            self.val_ping.config(text=f"{self.curr_latency_ms:.1f} ms", fg=color)
            if self.all_latencies:
                min_l = min(self.all_latencies)
                avg_l = sum(self.all_latencies) / len(self.all_latencies)
                max_l = max(self.all_latencies)
                self.sub_ping.config(text=f"Min: {min_l:.0f} | Avg: {avg_l:.0f} | Max: {max_l:.0f} ms")

        # Graph values in header
        total_speed = self.curr_download_bps + self.curr_upload_bps
        self.lbl_g1_val.config(text=f"Current: {format_bytes(total_speed)}")
        lat_text = f"{self.curr_latency_ms:.1f} ms" if self.curr_latency_ms >= 0 else "OFFLINE"
        self.lbl_g2_val.config(text=f"RTT: {lat_text}")
        self.lbl_g3_val.config(text=f"▼ {format_bytes(self.curr_download_bps)} | ▲ {format_bytes(self.curr_upload_bps)}")

    # ==========================================================================
    # ☆ REAL-TIME VECTOR GRAPH RENDERING
    # ==========================================================================
    def draw_graphs(self):
        self.render_area_graph(
            self.canvas_g1, self.speed_history, ACCENT_CYAN, "#102a45", unit="KB/s", auto_scale_bytes=True
        )
        self.render_line_graph(
            self.canvas_g2, self.latency_history, ACCENT_GOLD, threshold_val=self.latency_marginal_ms, unit="ms"
        )
        self.render_dual_graph(
            self.canvas_g3, self.download_history, self.upload_history, ACCENT_CYAN, ACCENT_MAGENTA
        )

    def draw_grid(self, canvas, w, h, rows=4, cols=8):
        canvas.delete("all")
        # Horizontal grid lines
        for r in range(1, rows):
            y = int(h * r / rows)
            canvas.create_line(0, y, w, y, fill=GRID_COLOR, dash=(2, 4))

        # Vertical grid lines
        for c in range(1, cols):
            x = int(w * c / cols)
            canvas.create_line(x, 0, x, h, fill=GRID_COLOR, dash=(2, 4))

    def render_area_graph(self, canvas, data, line_color, fill_color, unit="KB/s", auto_scale_bytes=False):
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w <= 10 or h <= 10:
            return

        self.draw_grid(canvas, w, h)

        max_val = max(data) if data and max(data) > 0 else 10.0
        # Add 15% headroom
        scale_max = max_val * 1.15

        # Format max scale label
        if auto_scale_bytes:
            top_label = format_bytes(scale_max * 1024.0)
        else:
            top_label = f"{scale_max:.0f} {unit}"
        canvas.create_text(w - 6, 8, text=top_label, anchor="ne", fill=TEXT_MUTED, font=FONT_STATS)

        n = len(data)
        if n < 2:
            return

        step_x = w / float(n - 1)
        points = []
        poly_points = [0, h]

        for i, val in enumerate(data):
            x = i * step_x
            norm = min(1.0, max(0.0, val / scale_max)) if scale_max > 0 else 0
            y = h - (norm * (h - 14)) - 2
            points.append((x, y))
            poly_points.extend([x, y])

        poly_points.extend([w, h])

        # Fill background under curve
        canvas.create_polygon(poly_points, fill=fill_color, outline="")

        # Draw smooth glow/main line
        flat_pts = [coord for pt in points for coord in pt]
        canvas.create_line(flat_pts, fill=line_color, width=2, smooth=True)

        # Pulse dot at current tip
        if points:
            last_x, last_y = points[-1]
            canvas.create_oval(last_x - 3, last_y - 3, last_x + 3, last_y + 3, fill=line_color, outline="#ffffff")

    def render_line_graph(self, canvas, data, line_color, threshold_val=100.0, unit="ms"):
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w <= 10 or h <= 10:
            return

        self.draw_grid(canvas, w, h)

        valid_vals = [v for v in data if v >= 0]
        max_val = max(valid_vals) if valid_vals else 50.0
        scale_max = max(max_val * 1.25, threshold_val * 1.3, 50.0)

        # Threshold warning line
        if threshold_val < scale_max:
            th_y = h - ((threshold_val / scale_max) * (h - 14)) - 2
            canvas.create_line(0, th_y, w, th_y, fill="#5a4214", width=1, dash=(4, 4))
            canvas.create_text(8, th_y - 8, text=f"Warning Threshold ({threshold_val:.0f} ms)", anchor="nw", fill=ACCENT_GOLD, font=FONT_STATS)

        canvas.create_text(w - 6, 8, text=f"{scale_max:.0f} {unit}", anchor="ne", fill=TEXT_MUTED, font=FONT_STATS)

        n = len(data)
        if n < 2:
            return

        step_x = w / float(n - 1)
        points = []
        for i, val in enumerate(data):
            x = i * step_x
            if val < 0:
                # Dropped packet indicator
                canvas.create_line(x, 4, x, h, fill=ACCENT_CORAL, width=2)
                canvas.create_text(x, h / 2, text="✖", fill=ACCENT_CORAL, font=FONT_UI_BOLD)
                y = h - 2
            else:
                norm = min(1.0, max(0.0, val / scale_max)) if scale_max > 0 else 0
                y = h - (norm * (h - 14)) - 2
                points.append((x, y))

        if len(points) >= 2:
            flat_pts = [coord for pt in points for coord in pt]
            canvas.create_line(flat_pts, fill=line_color, width=2, smooth=True)

        if points:
            last_x, last_y = points[-1]
            canvas.create_oval(last_x - 3, last_y - 3, last_x + 3, last_y + 3, fill=line_color, outline="#ffffff")

    def render_dual_graph(self, canvas, data_down, data_up, color_down, color_up):
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w <= 10 or h <= 10:
            return

        self.draw_grid(canvas, w, h)

        max_d = max(data_down) if data_down else 1.0
        max_u = max(data_up) if data_up else 1.0
        scale_max = max(max_d, max_u, 10.0) * 1.15

        canvas.create_text(w - 6, 8, text=format_bytes(scale_max * 1024.0), anchor="ne", fill=TEXT_MUTED, font=FONT_STATS)

        n = max(len(data_down), len(data_up))
        if n < 2:
            return

        step_x = w / float(n - 1)

        # Plot Download Line
        pts_d = []
        for i, val in enumerate(data_down):
            x = i * step_x
            norm = min(1.0, max(0.0, val / scale_max)) if scale_max > 0 else 0
            y = h - (norm * (h - 14)) - 2
            pts_d.append((x, y))

        if len(pts_d) >= 2:
            flat_d = [c for pt in pts_d for c in pt]
            canvas.create_line(flat_d, fill=color_down, width=2, smooth=True)

        # Plot Upload Line
        pts_u = []
        for i, val in enumerate(data_up):
            x = i * step_x
            norm = min(1.0, max(0.0, val / scale_max)) if scale_max > 0 else 0
            y = h - (norm * (h - 14)) - 2
            pts_u.append((x, y))

        if len(pts_u) >= 2:
            flat_u = [c for pt in pts_u for c in pt]
            canvas.create_line(flat_u, fill=color_up, width=2, smooth=True)

    # ==========================================================================
    # ☆ ACTION HANDLERS & MODALS
    # ==========================================================================
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.btn_pause.config(text="▶ Resume", fg=ACCENT_MINT)
            self.status_pill.config(text="⏸ PAUSED (Stream Frozen)", bg="#2a2412", fg=ACCENT_GOLD)
        else:
            self.btn_pause.config(text="⏸ Pause", fg=TEXT_PRIMARY)
            self.update_kaomoji(force=True)

    def reset_session_stats(self):
        self.session_total_recv = 0.0
        self.session_total_sent = 0.0
        self.peak_download = 0.0
        self.peak_upload = 0.0
        self.all_latencies.clear()

        stats = self.data.get("stats", {})
        stats["session_peak_download_bps"] = 0.0
        stats["session_peak_upload_bps"] = 0.0
        stats["session_total_download_bytes"] = 0.0
        stats["session_total_upload_bytes"] = 0.0
        self.data["stats"] = stats
        save_data(self.data)

        self.update_ui()
        messagebox.showinfo("Stats Reset", "Session telemetry counters and peaks have been reset to zero.")

    def open_target_dialog(self):
        new_target = simpledialog.askstring(
            "Cosmic Ping Target",
            "Enter target hostname or IPv4 address to ping:\n(e.g., 8.8.8.8, 1.1.1.1, 208.67.222.222)",
            initialvalue=self.ping_target,
            parent=self.root
        )
        if new_target and new_target.strip():
            self.ping_target = new_target.strip()
            self.data.setdefault("settings", {})["ping_target"] = self.ping_target
            save_data(self.data)

            # Update Latency Tracker
            self.latency_tracker.stop()
            self.latency_tracker = LatencyTracker(target_host=self.ping_target, interval=self.ping_interval)
            self.latency_tracker.start()

            # Refresh Adapter IP
            self.adapter_info = get_active_adapter_info(self.ping_target)
            self.lbl_g2_title.config(text=f"🛰️ COSMIC LATENCY (Target: {self.ping_target})")
            self.status_left.config(text=f"Target: {self.ping_target} | Adapter: {self.adapter_info['interface']} | Mode: Native Win32 Telemetry")

    def open_export_dialog(self):
        filepath = filedialog.asksaveasfilename(
            parent=self.root,
            title="Export Session Telemetry",
            defaultextension=".json",
            filetypes=[("JSON Files (*.json)", "*.json"), ("CSV Files (*.csv)", "*.csv"), ("All Files (*.*)", "*.*")],
            initialfile=f"telemetry_export_{time.strftime('%Y%m%d_%H%M%S')}.json"
        )
        if filepath:
            fmt = "csv" if filepath.lower().endswith(".csv") else "json"
            export_payload = {
                "timestamp": datetime.now().isoformat(),
                "target_host": self.ping_target,
                "current_download_bps": self.curr_download_bps,
                "current_upload_bps": self.curr_upload_bps,
                "peak_download_bps": self.peak_download,
                "peak_upload_bps": self.peak_upload,
                "session_total_download_bytes": self.session_total_recv,
                "session_total_upload_bytes": self.session_total_sent,
                "download_history": self.download_history,
                "upload_history": self.upload_history,
                "latency_history": self.latency_history,
                "adapter": self.adapter_info
            }
            saved_file = export_telemetry(export_payload, filepath=filepath, export_format=fmt)
            messagebox.showinfo("Export Successful", f"Telemetry data exported successfully to:\n{saved_file}")

    def open_settings_dialog(self):
        win = tk.Toplevel(self.root)
        win.title("⚙️ Telemetry Settings")
        win.geometry("420x330")
        win.configure(bg=CONSOLE_FRAME)
        win.transient(self.root)
        win.grab_set()

        # Center on parent
        x = self.root.winfo_x() + 100
        y = self.root.winfo_y() + 100
        win.geometry(f"+{x}+{y}")

        title_lbl = tk.Label(win, text="COSMIC TELEMETRY SETTINGS", font=FONT_TITLE, bg=CONSOLE_FRAME, fg=ACCENT_CYAN)
        title_lbl.pack(pady=12)

        # Settings Form
        form = tk.Frame(win, bg=CONSOLE_FRAME, padx=20)
        form.pack(fill=tk.BOTH, expand=True)

        # Ping Target
        tk.Label(form, text="Ping Target Host:", font=FONT_UI_BOLD, bg=CONSOLE_FRAME, fg=TEXT_PRIMARY).grid(row=0, column=0, sticky="w", pady=6)
        entry_target = tk.Entry(form, bg=CARD_BG, fg=TEXT_PRIMARY, insertbackground=ACCENT_CYAN, font=FONT_UI)
        entry_target.insert(0, self.ping_target)
        entry_target.grid(row=0, column=1, sticky="e", pady=6)

        # Target FPS
        tk.Label(form, text="Target Framerate (FPS):", font=FONT_UI_BOLD, bg=CONSOLE_FRAME, fg=TEXT_PRIMARY).grid(row=1, column=0, sticky="w", pady=6)
        spin_fps = tk.Spinbox(form, from_=5, to=30, bg=CARD_BG, fg=TEXT_PRIMARY, font=FONT_UI, width=18)
        spin_fps.delete(0, "end")
        spin_fps.insert(0, str(self.target_fps))
        spin_fps.grid(row=1, column=1, sticky="e", pady=6)

        # Latency Warning Threshold
        tk.Label(form, text="Ping Warning (ms):", font=FONT_UI_BOLD, bg=CONSOLE_FRAME, fg=TEXT_PRIMARY).grid(row=2, column=0, sticky="w", pady=6)
        entry_thresh = tk.Entry(form, bg=CARD_BG, fg=TEXT_PRIMARY, insertbackground=ACCENT_CYAN, font=FONT_UI)
        entry_thresh.insert(0, str(int(self.latency_marginal_ms)))
        entry_thresh.grid(row=2, column=1, sticky="e", pady=6)

        # Ping Interval (sec)
        tk.Label(form, text="Ping Interval (sec):", font=FONT_UI_BOLD, bg=CONSOLE_FRAME, fg=TEXT_PRIMARY).grid(row=3, column=0, sticky="w", pady=6)
        entry_int = tk.Entry(form, bg=CARD_BG, fg=TEXT_PRIMARY, insertbackground=ACCENT_CYAN, font=FONT_UI)
        entry_int.insert(0, str(self.ping_interval))
        entry_int.grid(row=3, column=1, sticky="e", pady=6)

        def save_and_close():
            try:
                new_target = entry_target.get().strip()
                new_fps = int(spin_fps.get())
                new_thresh = float(entry_thresh.get())
                new_int = float(entry_int.get())

                self.ping_target = new_target
                self.target_fps = max(5, min(60, new_fps))
                self.latency_marginal_ms = new_thresh
                self.ping_interval = max(0.2, min(5.0, new_int))

                # Update data.json
                settings = self.data.setdefault("settings", {})
                settings["ping_target"] = self.ping_target
                settings["target_fps"] = self.target_fps
                settings["latency_marginal_ms"] = self.latency_marginal_ms
                settings["ping_interval"] = self.ping_interval
                save_data(self.data)

                # Restart tracker if needed
                self.latency_tracker.stop()
                self.latency_tracker = LatencyTracker(target_host=self.ping_target, interval=self.ping_interval)
                self.latency_tracker.start()

                self.lbl_g2_title.config(text=f"🛰️ COSMIC LATENCY (Target: {self.ping_target})")
                self.status_left.config(text=f"Target: {self.ping_target} | Adapter: {self.adapter_info['interface']} | Mode: Native Win32 Telemetry")

                win.destroy()
            except Exception as e:
                messagebox.showerror("Invalid Setting", f"Please check your input values:\n{e}", parent=win)

        btn_box = tk.Frame(win, bg=CONSOLE_FRAME, pady=12)
        btn_box.pack(fill=tk.X)

        btn_save = tk.Button(btn_box, text="💾 Save Settings", command=save_and_close, bg=CARD_BG, fg=ACCENT_CYAN, font=FONT_UI_BOLD, padx=14, pady=4, relief=tk.FLAT, bd=0, cursor="hand2")
        btn_save.pack(side=tk.RIGHT, padx=16)

        btn_cancel = tk.Button(btn_box, text="Cancel", command=win.destroy, bg=CARD_BG, fg=TEXT_MUTED, font=FONT_UI, padx=10, pady=4, relief=tk.FLAT, bd=0, cursor="hand2")
        btn_cancel.pack(side=tk.RIGHT)

    # ==========================================================================
    # ☆ SHUTDOWN & LIFECYCLE
    # ==========================================================================
    def on_window_close(self):
        if hasattr(self, 'latency_tracker'):
            self.latency_tracker.stop()

        # Update saved session stats in data.json
        stats = self.data.setdefault("stats", {})
        stats["session_peak_download_bps"] = max(stats.get("session_peak_download_bps", 0.0), self.peak_download)
        stats["session_peak_upload_bps"] = max(stats.get("session_peak_upload_bps", 0.0), self.peak_upload)
        stats["session_total_download_bytes"] = stats.get("session_total_download_bytes", 0.0) + self.session_total_recv
        stats["session_total_upload_bytes"] = stats.get("session_total_upload_bytes", 0.0) + self.session_total_sent
        self.data["stats"] = stats
        save_data(self.data)

        self.root.destroy()


def main():
    root = tk.Tk()
    app = NetworkVisorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
