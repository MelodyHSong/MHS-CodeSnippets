# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: app.py
# ☆ Description: StellarJiggler - Modern cosmic mouse jiggler with native Windows wake-lock & hardware input simulation.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import sys
import os
import json
import time
import math
import random
import queue
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Enable Windows High-DPI Awareness for crisp rendering
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            import ctypes
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

# ==============================================================================
# ☆ COSMIC COLOR PALETTE & THEME
# ==============================================================================
BG_MAIN = "#0d1117"          # Deep space obsidian
BG_PANEL = "#161b22"         # Surface / card background
BG_SURFACE = "#21262d"       # Elevated widget background
BG_ACTIVE = "#30363d"        # Hover / selected item
BORDER_COLOR = "#30363d"     # Panel rim border
BORDER_ACTIVE = "#58a6ff"    # Focused active border / Starlight cyan

TEXT_PRIMARY = "#e2e8f0"     # Starlight white
TEXT_MUTED = "#8b949e"       # Dust gray
TEXT_DIM = "#586069"         # Nebula shadow

ACCENT_CYAN = "#58a6ff"      # Starlight cyan
ACCENT_GOLD = "#f2cc60"      # Celestial star gold
ACCENT_MINT = "#7ee787"      # Status active / pulse green
ACCENT_CORAL = "#f85149"     # Alert / stopped red
ACCENT_PURPLE = "#bc8cff"    # Cosmic nebula purple

FONT_TITLE = ("Segoe UI", 13, "bold")
FONT_SUBTITLE = ("Segoe UI", 8)
FONT_HERO = ("Segoe UI", 11, "bold")
FONT_COUNTDOWN = ("Consolas", 15, "bold")
FONT_HEADER = ("Segoe UI", 10, "bold")
FONT_UI = ("Segoe UI", 9)
FONT_UI_BOLD = ("Segoe UI", 9, "bold")
FONT_CODE = ("Consolas", 9)
FONT_STATS_NUM = ("Consolas", 14, "bold")
FONT_STATS_LBL = ("Segoe UI", 8)


# ==============================================================================
# ☆ WINDOWS HARDWARE INPUT & WAKE-LOCK UTILITIES
# ==============================================================================
if sys.platform == "win32":
    import ctypes

    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002
    ES_AWAYMODE_REQUIRED = 0x00000040

    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    def win32_get_cursor_pos():
        pt = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return pt.x, pt.y

    def win32_set_cursor_pos(x, y):
        ctypes.windll.user32.SetCursorPos(int(x), int(y))

    def win32_mouse_event(dx, dy):
        """Dispatches hardware relative mouse move event (0x0001 = MOUSEEVENTF_MOVE)."""
        ctypes.windll.user32.mouse_event(0x0001, int(dx), int(dy), 0, 0)

    def win32_get_idle_seconds():
        """Returns seconds since user last moved mouse or pressed a physical key."""
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
            millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
            return max(0.0, millis / 1000.0)
        return 9999.0

    def win32_set_wake_lock(enable=True):
        """Commands Windows Kernel to prevent display and system sleep without modifying power schemes."""
        if enable:
            ctypes.windll.kernel32.SetThreadExecutionState(
                ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
            )
        else:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
else:
    # Non-Windows stub fallbacks
    def win32_get_cursor_pos(): return (0, 0)
    def win32_set_cursor_pos(x, y): pass
    def win32_mouse_event(dx, dy): pass
    def win32_get_idle_seconds(): return 9999.0
    def win32_set_wake_lock(enable=True): pass


# ==============================================================================
# ☆ STELLAR JIGGLER APPLICATION CLASS
# ==============================================================================
class StellarJigglerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⭐ StellarJiggler - Celestial Idle Prevention Workstation")
        self.root.configure(bg=BG_MAIN)

        # Asset & Directory Resolution
        self.app_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # State Variables & Config
        self.config_path = os.path.join(self.base_dir, "config.json")
        self.config = self.load_config()

        # Window geometry from config
        win_w = self.config.get("window", {}).get("width", 540)
        win_h = self.config.get("window", {}).get("height", 680)
        min_w = self.config.get("window", {}).get("min_width", 480)
        min_h = self.config.get("window", {}).get("min_height", 600)
        self.root.geometry(f"{win_w}x{win_h}")
        self.root.minsize(min_w, min_h)

        # Runtime Engine State
        self.is_active = False
        self.worker_thread = None
        self.stop_event = threading.Event()
        self.queue = queue.Queue()

        # Thread-safe primitive caches (updated by UI on main thread)
        self.current_interval = 30
        self.current_mode = "subtle"
        self.current_smart_pause = True
        self.current_wake_lock = True

        # Telemetry Stats
        self.pulse_count = 0
        self.session_start_time = None
        self.last_pulse_str = "--:--:--"
        self.uptime_ticker_id = None

        # Set Window Icon
        self.set_app_icon()

        # Build UI Architecture
        self.build_ui()

        # Synchronize UI with Loaded Preferences
        self.apply_preferences_to_ui()

        # Window protocols & Keybindings
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.root.bind("<space>", lambda e: self.toggle_jiggler())
        self.root.bind("<Control-q>", lambda e: self.on_window_close())

        # Start Queue Consumer
        self.root.after(100, self.process_queue)

        # Start Uptime Ticker
        self.update_uptime()

        # Log initial welcome
        self.log_message("StellarJiggler workstation initialized and ready.", level="INFO")
        if sys.platform != "win32":
            self.log_message("Warning: Non-Windows OS detected. Mouse simulation will run in test mode.", level="WARN")

        # Auto-start if configured
        if self.config.get("preferences", {}).get("start_active_on_launch", False):
            self.start_jiggler()

    # ==========================================================================
    # ☆ CONFIGURATION PERSISTENCE
    # ==========================================================================
    def load_config(self):
        default_config = {
            "app_name": "StellarJiggler",
            "version": "1.0.0",
            "theme": {
                "palette": "dark_cosmic",
                "high_dpi": True
            },
            "window": {
                "width": 540,
                "height": 680,
                "min_width": 480,
                "min_height": 600,
                "always_on_top": False
            },
            "preferences": {
                "interval_seconds": 30,
                "jiggle_mode": "subtle",
                "smart_pause_enabled": True,
                "smart_pause_threshold_sec": 5,
                "wake_lock_enabled": True,
                "start_active_on_launch": False,
                "stealth_pixels": 1,
                "orbital_radius": 12,
                "log_history_limit": 100
            }
        }
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Merge nested defaults
                    for k, v in default_config.items():
                        if k not in data:
                            data[k] = v
                        elif isinstance(v, dict):
                            for sub_k, sub_v in v.items():
                                if sub_k not in data[k]:
                                    data[k][sub_k] = sub_v
                    return data
            except Exception as e:
                print(f"[!] Warning: Could not parse config.json: {e}")
        return default_config

    def save_config(self):
        try:
            # Sync current UI values into config
            prefs = self.config.setdefault("preferences", {})
            prefs["interval_seconds"] = int(self.interval_var.get())
            prefs["jiggle_mode"] = self.mode_var.get()
            prefs["smart_pause_enabled"] = self.smart_pause_var.get()
            prefs["wake_lock_enabled"] = self.wake_lock_var.get()
            prefs["always_on_top"] = self.always_on_top_var.get()

            # Window geometry
            try:
                self.config["window"]["width"] = self.root.winfo_width()
                self.config["window"]["height"] = self.root.winfo_height()
                self.config["window"]["always_on_top"] = self.always_on_top_var.get()
            except Exception:
                pass

            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.log_message(f"Error saving config: {e}", level="ERROR")

    def set_app_icon(self):
        candidates = [
            os.path.join(self.app_dir, "assets", "app_icon.ico"),
            os.path.join(self.base_dir, "assets", "app_icon.ico"),
        ]
        for icon_path in candidates:
            if os.path.exists(icon_path):
                try:
                    self.root.iconbitmap(icon_path)
                    break
                except Exception:
                    pass

    # ==========================================================================
    # ☆ GUI ARCHITECTURE
    # ==========================================================================
    def build_ui(self):
        # Configure custom TTK styles
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Custom progressbar style
        self.style.configure(
            "Cosmic.Horizontal.TProgressbar",
            troughcolor=BG_PANEL,
            background=ACCENT_CYAN,
            lightcolor=ACCENT_CYAN,
            darkcolor=ACCENT_CYAN,
            bordercolor=BORDER_COLOR,
            thickness=6
        )

        # Main scrollable or structured container
        main_frame = tk.Frame(self.root, bg=BG_MAIN)
        main_frame.pack(fill="both", expand=True, padx=16, pady=14)

        # 1. HEADER SECTION
        self.build_header(main_frame)

        # 2. HERO STATUS & POWER CONTROL
        self.build_hero_section(main_frame)

        # 3. METRICS / TELEMETRY CARDS
        self.build_metrics_section(main_frame)

        # 4. CONFIGURATION CONTROLS
        self.build_controls_section(main_frame)

        # 5. ACTIVITY CONSOLE LOG
        self.build_log_section(main_frame)

        # 6. STATUS FOOTER
        self.build_footer(main_frame)

    def build_header(self, parent):
        header_frame = tk.Frame(parent, bg=BG_MAIN)
        header_frame.pack(fill="x", pady=(0, 10))

        title_box = tk.Frame(header_frame, bg=BG_MAIN)
        title_box.pack(side="left", fill="y")

        lbl_title = tk.Label(
            title_box,
            text="⭐ STELLAR JIGGLER",
            font=FONT_TITLE,
            fg=TEXT_PRIMARY,
            bg=BG_MAIN,
            anchor="w"
        )
        lbl_title.pack(anchor="w")

        lbl_subtitle = tk.Label(
            title_box,
            text="CASSIOPEIA STUDIOS • CELESTIAL IDLE PREVENTION WORKSTATION",
            font=FONT_SUBTITLE,
            fg=ACCENT_CYAN,
            bg=BG_MAIN,
            anchor="w"
        )
        lbl_subtitle.pack(anchor="w")

        # Status Pill Badge (Top Right)
        self.badge_frame = tk.Frame(header_frame, bg=BG_SURFACE, highlightbackground=BORDER_COLOR, highlightthickness=1)
        self.badge_frame.pack(side="right", pady=4, padx=2)

        self.lbl_status_pill = tk.Label(
            self.badge_frame,
            text="○ DISENGAGED",
            font=FONT_UI_BOLD,
            fg=TEXT_MUTED,
            bg=BG_SURFACE,
            padx=10,
            pady=3
        )
        self.lbl_status_pill.pack()

    def build_hero_section(self, parent):
        hero_card = tk.Frame(parent, bg=BG_PANEL, highlightbackground=BORDER_COLOR, highlightthickness=1)
        hero_card.pack(fill="x", pady=(0, 10))

        inner = tk.Frame(hero_card, bg=BG_PANEL, padx=16, pady=14)
        inner.pack(fill="x")

        # Main Engage / Disengage Action Button
        self.btn_toggle = tk.Button(
            inner,
            text="🚀  ENGAGE ORBITAL JIGGLER  (SPACE)",
            font=FONT_HERO,
            fg="#0d1117",
            bg=ACCENT_CYAN,
            activeforeground="#0d1117",
            activebackground="#79b8ff",
            relief="flat",
            cursor="hand2",
            pady=10,
            command=self.toggle_jiggler
        )
        self.btn_toggle.pack(fill="x", pady=(0, 10))

        # Countdown & Pulse Progress bar
        cd_row = tk.Frame(inner, bg=BG_PANEL)
        cd_row.pack(fill="x", pady=(2, 4))

        self.lbl_countdown_label = tk.Label(
            cd_row,
            text="Pulse Status:",
            font=FONT_UI,
            fg=TEXT_MUTED,
            bg=BG_PANEL
        )
        self.lbl_countdown_label.pack(side="left")

        self.lbl_countdown_val = tk.Label(
            cd_row,
            text="Standby",
            font=FONT_COUNTDOWN,
            fg=ACCENT_GOLD,
            bg=BG_PANEL
        )
        self.lbl_countdown_val.pack(side="right")

        # Progress bar for interval countdown
        self.progress_var = tk.DoubleVar(value=0.0)
        self.progressbar = ttk.Progressbar(
            inner,
            style="Cosmic.Horizontal.TProgressbar",
            variable=self.progress_var,
            maximum=100.0,
            mode="determinate"
        )
        self.progressbar.pack(fill="x", pady=(2, 0))

    def build_metrics_section(self, parent):
        metrics_frame = tk.Frame(parent, bg=BG_MAIN)
        metrics_frame.pack(fill="x", pady=(0, 10))

        metrics_frame.columnconfigure(0, weight=1)
        metrics_frame.columnconfigure(1, weight=1)
        metrics_frame.columnconfigure(2, weight=1)

        # Card 1: Pulses Dispatched
        c1 = tk.Frame(metrics_frame, bg=BG_PANEL, highlightbackground=BORDER_COLOR, highlightthickness=1)
        c1.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        tk.Label(c1, text="PULSES DISPATCHED", font=FONT_STATS_LBL, fg=TEXT_MUTED, bg=BG_PANEL, pady=4).pack()
        self.lbl_stat_pulses = tk.Label(c1, text="0", font=FONT_STATS_NUM, fg=ACCENT_CYAN, bg=BG_PANEL, pady=2)
        self.lbl_stat_pulses.pack()

        # Card 2: Active Session Uptime
        c2 = tk.Frame(metrics_frame, bg=BG_PANEL, highlightbackground=BORDER_COLOR, highlightthickness=1)
        c2.grid(row=0, column=1, sticky="nsew", padx=2)
        tk.Label(c2, text="ACTIVE UPTIME", font=FONT_STATS_LBL, fg=TEXT_MUTED, bg=BG_PANEL, pady=4).pack()
        self.lbl_stat_uptime = tk.Label(c2, text="00:00:00", font=FONT_STATS_NUM, fg=ACCENT_MINT, bg=BG_PANEL, pady=2)
        self.lbl_stat_uptime.pack()

        # Card 3: Last Pulse Time
        c3 = tk.Frame(metrics_frame, bg=BG_PANEL, highlightbackground=BORDER_COLOR, highlightthickness=1)
        c3.grid(row=0, column=2, sticky="nsew", padx=(4, 0))
        tk.Label(c3, text="LAST PULSE", font=FONT_STATS_LBL, fg=TEXT_MUTED, bg=BG_PANEL, pady=4).pack()
        self.lbl_stat_last = tk.Label(c3, text="--:--:--", font=FONT_STATS_NUM, fg=ACCENT_GOLD, bg=BG_PANEL, pady=2)
        self.lbl_stat_last.pack()

    def build_controls_section(self, parent):
        ctrl_card = tk.Frame(parent, bg=BG_PANEL, highlightbackground=BORDER_COLOR, highlightthickness=1)
        ctrl_card.pack(fill="x", pady=(0, 10))

        inner = tk.Frame(ctrl_card, bg=BG_PANEL, padx=14, pady=12)
        inner.pack(fill="x")

        # --- A. JIGGLE MODE SELECTOR ---
        mode_header = tk.Frame(inner, bg=BG_PANEL)
        mode_header.pack(fill="x", pady=(0, 4))
        tk.Label(mode_header, text="JIGGLE TRAJECTORY MODE", font=FONT_UI_BOLD, fg=TEXT_PRIMARY, bg=BG_PANEL).pack(side="left")

        self.mode_var = tk.StringVar(value="subtle")
        mode_row = tk.Frame(inner, bg=BG_PANEL)
        mode_row.pack(fill="x", pady=(0, 10))

        modes = [
            ("Subtle Nudge (±1px)", "subtle", "Hardware micro-nudge; imperceptible to eyes, resets idle timers"),
            ("Zen Ghost (0px)", "zen", "Zero movement; relies solely on Windows Kernel Wake Lock"),
            ("Orbital Circle", "orbital", "Moves in a small smooth cosmic orbit"),
            ("Random Jitter", "random", "Random celestial micro-jitter")
        ]

        for text, val, desc in modes:
            rb = tk.Radiobutton(
                mode_row,
                text=text,
                variable=self.mode_var,
                value=val,
                font=FONT_UI,
                fg=TEXT_PRIMARY,
                bg=BG_PANEL,
                activeforeground=ACCENT_CYAN,
                activebackground=BG_PANEL,
                selectcolor=BG_SURFACE,
                highlightthickness=0,
                command=self.on_mode_changed
            )
            rb.pack(side="left", padx=(0, 10))

        # Mode explanation label
        self.lbl_mode_desc = tk.Label(
            inner,
            text="Hardware micro-nudge; imperceptible to eyes, resets idle timers without disturbing cursor position.",
            font=FONT_SUBTITLE,
            fg=TEXT_MUTED,
            bg=BG_PANEL,
            anchor="w"
        )
        self.lbl_mode_desc.pack(fill="x", pady=(0, 10))

        # --- B. INTERVAL SLIDER & PRESETS ---
        int_header = tk.Frame(inner, bg=BG_PANEL)
        int_header.pack(fill="x", pady=(0, 4))

        tk.Label(int_header, text="PULSE FREQUENCY (INTERVAL)", font=FONT_UI_BOLD, fg=TEXT_PRIMARY, bg=BG_PANEL).pack(side="left")
        self.lbl_interval_display = tk.Label(int_header, text="30s", font=FONT_CODE, fg=ACCENT_GOLD, bg=BG_PANEL)
        self.lbl_interval_display.pack(side="right")

        self.interval_var = tk.IntVar(value=30)
        slider_frame = tk.Frame(inner, bg=BG_PANEL)
        slider_frame.pack(fill="x", pady=(0, 6))

        slider = tk.Scale(
            slider_frame,
            from_=5,
            to=300,
            orient="horizontal",
            variable=self.interval_var,
            showvalue=0,
            bg=BG_SURFACE,
            fg=TEXT_PRIMARY,
            activebackground=ACCENT_CYAN,
            troughcolor=BG_MAIN,
            highlightthickness=0,
            bd=0,
            command=self.on_interval_slider
        )
        slider.pack(fill="x")

        # Preset Buttons Row
        preset_row = tk.Frame(inner, bg=BG_PANEL)
        preset_row.pack(fill="x", pady=(0, 10))

        tk.Label(preset_row, text="Presets:", font=FONT_UI, fg=TEXT_MUTED, bg=BG_PANEL).pack(side="left", padx=(0, 6))
        for sec in [10, 30, 60, 120, 300]:
            lbl = f"{sec}s" if sec < 60 else f"{sec // 60}m"
            b = tk.Button(
                preset_row,
                text=lbl,
                font=FONT_SUBTITLE,
                fg=TEXT_PRIMARY,
                bg=BG_SURFACE,
                activeforeground=ACCENT_CYAN,
                activebackground=BG_ACTIVE,
                relief="flat",
                padx=8,
                pady=1,
                cursor="hand2",
                command=lambda s=sec: self.set_interval_preset(s)
            )
            b.pack(side="left", padx=3)

        # --- C. TOGGLES & FLAGS ---
        toggles_row = tk.Frame(inner, bg=BG_PANEL)
        toggles_row.pack(fill="x", pady=(4, 0))

        # Smart User Activity Guard
        self.smart_pause_var = tk.BooleanVar(value=True)
        cb_guard = tk.Checkbutton(
            toggles_row,
            text="Smart Activity Guard (Pause if user is typing/moving mouse)",
            variable=self.smart_pause_var,
            font=FONT_UI,
            fg=TEXT_PRIMARY,
            bg=BG_PANEL,
            activeforeground=ACCENT_CYAN,
            activebackground=BG_PANEL,
            selectcolor=BG_SURFACE,
            highlightthickness=0,
            command=self.on_smart_pause_toggle
        )
        cb_guard.pack(anchor="w", pady=1)

        # Windows Wake Lock Toggle
        self.wake_lock_var = tk.BooleanVar(value=True)
        cb_wake = tk.Checkbutton(
            toggles_row,
            text="Windows Wake Lock (Prevent display & system sleep via OS Kernel)",
            variable=self.wake_lock_var,
            font=FONT_UI,
            fg=TEXT_PRIMARY,
            bg=BG_PANEL,
            activeforeground=ACCENT_CYAN,
            activebackground=BG_PANEL,
            selectcolor=BG_SURFACE,
            highlightthickness=0,
            command=self.on_wake_lock_toggle
        )
        cb_wake.pack(anchor="w", pady=1)

        # Always on Top
        self.always_on_top_var = tk.BooleanVar(value=False)
        cb_top = tk.Checkbutton(
            toggles_row,
            text="Always on Top (Keep window pinned above other apps)",
            variable=self.always_on_top_var,
            font=FONT_UI,
            fg=TEXT_PRIMARY,
            bg=BG_PANEL,
            activeforeground=ACCENT_CYAN,
            activebackground=BG_PANEL,
            selectcolor=BG_SURFACE,
            highlightthickness=0,
            command=self.on_always_on_top_toggle
        )
        cb_top.pack(anchor="w", pady=1)

    def build_log_section(self, parent):
        log_frame = tk.Frame(parent, bg=BG_PANEL, highlightbackground=BORDER_COLOR, highlightthickness=1)
        log_frame.pack(fill="both", expand=True, pady=(0, 6))

        # Log Header
        lh = tk.Frame(log_frame, bg=BG_PANEL, padx=10, pady=6)
        lh.pack(fill="x")

        tk.Label(lh, text="ACTIVITY & TELEMETRY LOG", font=FONT_UI_BOLD, fg=TEXT_PRIMARY, bg=BG_PANEL).pack(side="left")

        btn_clear = tk.Button(
            lh,
            text="Clear",
            font=FONT_SUBTITLE,
            fg=TEXT_MUTED,
            bg=BG_SURFACE,
            activeforeground=TEXT_PRIMARY,
            activebackground=BG_ACTIVE,
            relief="flat",
            padx=6,
            pady=0,
            cursor="hand2",
            command=self.clear_log
        )
        btn_clear.pack(side="right", padx=2)

        # Log Text Box with Scrollbar
        tb_frame = tk.Frame(log_frame, bg=BG_PANEL, padx=8, pady=4)
        tb_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(tb_frame, bg=BG_SURFACE, troughcolor=BG_PANEL)
        scrollbar.pack(side="right", fill="y")

        self.log_text = tk.Text(
            tb_frame,
            height=6,
            bg=BG_MAIN,
            fg=TEXT_PRIMARY,
            font=FONT_CODE,
            relief="flat",
            wrap="word",
            yscrollcommand=scrollbar.set,
            padx=6,
            pady=6
        )
        self.log_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.log_text.yview)

        # Color tags for log output
        self.log_text.tag_config("TIME", foreground=TEXT_MUTED)
        self.log_text.tag_config("INFO", foreground=ACCENT_CYAN)
        self.log_text.tag_config("PULSE", foreground=ACCENT_MINT)
        self.log_text.tag_config("GUARD", foreground=ACCENT_GOLD)
        self.log_text.tag_config("WARN", foreground=ACCENT_GOLD)
        self.log_text.tag_config("ERROR", foreground=ACCENT_CORAL)

    def build_footer(self, parent):
        footer = tk.Frame(parent, bg=BG_MAIN)
        footer.pack(fill="x")

        self.lbl_footer_left = tk.Label(
            footer,
            text="Space: Toggle | Ctrl+Q: Exit | Engine: Native Win32",
            font=FONT_SUBTITLE,
            fg=TEXT_MUTED,
            bg=BG_MAIN
        )
        self.lbl_footer_left.pack(side="left")

        lbl_footer_right = tk.Label(
            footer,
            text=f"v{self.config.get('version', '1.0.0')}",
            font=FONT_SUBTITLE,
            fg=TEXT_DIM,
            bg=BG_MAIN
        )
        lbl_footer_right.pack(side="right")

    # ==========================================================================
    # ☆ PREFERENCES SYNCHRONIZATION
    # ==========================================================================
    def apply_preferences_to_ui(self):
        prefs = self.config.get("preferences", {})
        interval = prefs.get("interval_seconds", 30)
        self.interval_var.set(interval)
        self.current_interval = interval
        self.lbl_interval_display.config(text=f"{interval}s")

        mode = prefs.get("jiggle_mode", "subtle")
        self.mode_var.set(mode)
        self.current_mode = mode
        self.update_mode_description()

        smart_pause = prefs.get("smart_pause_enabled", True)
        self.smart_pause_var.set(smart_pause)
        self.current_smart_pause = smart_pause

        wake_lock = prefs.get("wake_lock_enabled", True)
        self.wake_lock_var.set(wake_lock)
        self.current_wake_lock = wake_lock

        top_val = self.config.get("window", {}).get("always_on_top", False)
        self.always_on_top_var.set(top_val)
        self.root.attributes("-topmost", top_val)

    def on_mode_changed(self):
        self.current_mode = self.mode_var.get()
        self.update_mode_description()
        self.save_config()
        self.log_message(f"Trajectory mode switched to: {self.current_mode.upper()}", level="INFO")

    def update_mode_description(self):
        mode = self.mode_var.get()
        descs = {
            "subtle": "Hardware micro-nudge (±1px). Invisible to eyes, resets idle timers without interrupting work.",
            "zen": "Zero cursor movement. Keeps Windows and display awake strictly via OS Kernel Wake Lock.",
            "orbital": "Moves cursor smoothly in a small celestial orbit (~12px radius) and returns.",
            "random": "Dispatches gentle micro-jitter in random celestial directions and returns."
        }
        self.lbl_mode_desc.config(text=descs.get(mode, ""))

    def on_interval_slider(self, val):
        sec = int(float(val))
        self.current_interval = sec
        self.lbl_interval_display.config(text=f"{sec}s")
        self.save_config()

    def set_interval_preset(self, sec):
        self.current_interval = sec
        self.interval_var.set(sec)
        self.lbl_interval_display.config(text=f"{sec}s")
        self.save_config()
        self.log_message(f"Pulse interval adjusted to: {sec} seconds", level="INFO")

    def on_smart_pause_toggle(self):
        self.current_smart_pause = self.smart_pause_var.get()
        self.save_config()
        status = "ENABLED" if self.current_smart_pause else "DISABLED"
        self.log_message(f"Smart Activity Guard {status}", level="INFO")

    def on_wake_lock_toggle(self):
        self.current_wake_lock = self.wake_lock_var.get()
        self.save_config()
        if self.is_active:
            win32_set_wake_lock(self.current_wake_lock)
            status = "ENABLED" if self.current_wake_lock else "DISABLED"
            self.log_message(f"Windows Wake Lock {status}", level="INFO")

    def on_always_on_top_toggle(self):
        is_top = self.always_on_top_var.get()
        self.root.attributes("-topmost", is_top)
        self.save_config()

    # ==========================================================================
    # ☆ LOGGING & TELEMETRY
    # ==========================================================================
    def log_message(self, message, level="INFO"):
        now_str = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{now_str}] ", "TIME")
        self.log_text.insert("end", f"[{level:<5}] ", level)
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")

    def clear_log(self):
        self.log_text.delete("1.0", "end")

    def update_uptime(self):
        if self.is_active and self.session_start_time:
            elapsed = int(time.time() - self.session_start_time)
            hrs = elapsed // 3600
            mins = (elapsed % 3600) // 60
            secs = elapsed % 60
            self.lbl_stat_uptime.config(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")
        self.uptime_ticker_id = self.root.after(1000, self.update_uptime)

    # ==========================================================================
    # ☆ JIGGLER CONTROL & THREADING ENGINE
    # ==========================================================================
    def toggle_jiggler(self):
        if self.is_active:
            self.stop_jiggler()
        else:
            self.start_jiggler()

    def start_jiggler(self):
        if self.is_active:
            return

        self.is_active = True
        self.session_start_time = time.time()
        self.stop_event.clear()

        # Update UI Controls to Active State
        self.btn_toggle.config(
            text="⏸  DISENGAGE JIGGLER  (SPACE)",
            bg=ACCENT_CORAL,
            activebackground="#ff7b72"
        )
        self.lbl_status_pill.config(
            text="● ENGAGED",
            fg=ACCENT_MINT
        )
        self.badge_frame.config(highlightbackground=ACCENT_MINT)

        # Apply OS Wake Lock if enabled
        if self.wake_lock_var.get():
            win32_set_wake_lock(True)

        # Spawn Engine Worker Thread
        self.worker_thread = threading.Thread(target=self._jiggler_loop, daemon=True)
        self.worker_thread.start()

        self.log_message(
            f"Orbital Jiggler ENGAGED [Interval: {self.interval_var.get()}s, Mode: {self.mode_var.get().upper()}]",
            level="INFO"
        )

    def stop_jiggler(self):
        if not self.is_active:
            return

        self.is_active = False
        self.stop_event.set()

        # Release OS Wake Lock
        win32_set_wake_lock(False)

        # Update UI Controls to Disengaged State
        self.btn_toggle.config(
            text="🚀  ENGAGE ORBITAL JIGGLER  (SPACE)",
            bg=ACCENT_CYAN,
            activebackground="#79b8ff"
        )
        self.lbl_status_pill.config(
            text="○ DISENGAGED",
            fg=TEXT_MUTED
        )
        self.badge_frame.config(highlightbackground=BORDER_COLOR)

        self.lbl_countdown_val.config(text="Standby", fg=ACCENT_GOLD)
        self.progress_var.set(0.0)

        self.log_message("Orbital Jiggler DISENGAGED. Workstation on standby.", level="INFO")

    def _jiggler_loop(self):
        """Worker thread loop managing countdown, user activity checks, and hardware pulses."""
        while not self.stop_event.is_set():
            interval = max(1, self.current_interval)
            elapsed = 0.0

            # Countdown sub-loop with 100ms precision for responsive cancel
            last_tick_sec = -1
            while elapsed < interval:
                if self.stop_event.is_set():
                    return

                remaining = int(math.ceil(interval - elapsed))
                if remaining != last_tick_sec:
                    last_tick_sec = remaining
                    pct = (elapsed / float(interval)) * 100.0
                    self.queue.put({
                        "action": "tick",
                        "remaining": remaining,
                        "percent": pct
                    })

                time.sleep(0.1)
                elapsed += 0.1

            if self.stop_event.is_set():
                return

            # Smart Activity Guard Check: Is user actively working?
            if self.current_smart_pause:
                idle_sec = win32_get_idle_seconds()
                guard_threshold = self.config.get("preferences", {}).get("smart_pause_threshold_sec", 5)
                if idle_sec < guard_threshold:
                    self.queue.put({
                        "action": "smart_guard",
                        "idle_sec": idle_sec
                    })
                    # Pause briefly and recheck instead of interrupting user
                    time.sleep(1.0)
                    continue

            # Dispatch Mouse Pulse Action
            mode = self.current_mode
            pulse_info = self._dispatch_pulse(mode)

            self.queue.put({
                "action": "pulse_done",
                "mode": mode,
                "info": pulse_info
            })

    def _dispatch_pulse(self, mode):
        """Executes the chosen mouse movement or OS wake pulse."""
        if mode == "zen":
            # Zero movement: Refresh wake lock kernel flag
            win32_set_wake_lock(True)
            return "Zero movement; Windows OS Kernel Wake Lock refreshed."

        elif mode == "orbital":
            # Smooth circular orbit
            radius = self.config.get("preferences", {}).get("orbital_radius", 12)
            steps = 12
            start_x, start_y = win32_get_cursor_pos()
            for i in range(steps):
                if self.stop_event.is_set():
                    break
                angle = (2 * math.pi / steps) * i
                dx = int(radius * math.cos(angle))
                dy = int(radius * math.sin(angle))
                win32_set_cursor_pos(start_x + dx, start_y + dy)
                time.sleep(0.015)
            # Restore exact start position
            win32_set_cursor_pos(start_x, start_y)
            return f"Orbital circle completed ({steps} steps, r={radius}px)."

        elif mode == "random":
            # Random micro jitter
            delta = random.choice([-2, -1, 1, 2])
            start_x, start_y = win32_get_cursor_pos()
            win32_mouse_event(delta, -delta)
            time.sleep(0.02)
            win32_mouse_event(-delta, delta)
            win32_set_cursor_pos(start_x, start_y)
            return f"Random jitter dispatched (delta={delta}px)."

        else:  # "subtle" (default)
            # Micro-nudge ±1px hardware event and instant restore
            pixels = self.config.get("preferences", {}).get("stealth_pixels", 1)
            start_x, start_y = win32_get_cursor_pos()
            win32_mouse_event(pixels, 0)
            time.sleep(0.02)
            win32_mouse_event(-pixels, 0)
            win32_set_cursor_pos(start_x, start_y)
            return f"Hardware micro-nudge dispatched (±{pixels}px). Idle timer reset."

    # ==========================================================================
    # ☆ QUEUE CONSUMER (THREAD-SAFE GUI UPDATES)
    # ==========================================================================
    def process_queue(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                action = msg.get("action")

                if action == "tick":
                    rem = msg.get("remaining")
                    pct = msg.get("percent")
                    self.lbl_countdown_val.config(text=f"{rem}s", fg=ACCENT_CYAN)
                    self.progress_var.set(pct)

                elif action == "smart_guard":
                    idle_sec = msg.get("idle_sec", 0.0)
                    self.lbl_countdown_val.config(text="User Active", fg=ACCENT_GOLD)
                    self.log_message(f"Activity Guard: User active ({idle_sec:.1f}s ago). Pulse deferred.", level="GUARD")

                elif action == "pulse_done":
                    self.pulse_count += 1
                    self.last_pulse_str = datetime.now().strftime("%H:%M:%S")
                    self.lbl_stat_pulses.config(text=str(self.pulse_count))
                    self.lbl_stat_last.config(text=self.last_pulse_str)

                    # Pulse animation on badge
                    self.lbl_status_pill.config(text="● PULSING...", fg=ACCENT_GOLD)
                    self.root.after(400, lambda: self.lbl_status_pill.config(text="● ENGAGED", fg=ACCENT_MINT) if self.is_active else None)

                    self.log_message(f"Pulse #{self.pulse_count}: {msg.get('info')}", level="PULSE")

        except queue.Empty:
            pass

        self.root.after(100, self.process_queue)

    # ==========================================================================
    # ☆ WINDOW CLOSURE & CLEANUP
    # ==========================================================================
    def on_window_close(self):
        # Stop jiggler and restore OS power state
        if self.is_active:
            self.stop_jiggler()

        # Cancel ticker
        if self.uptime_ticker_id:
            self.root.after_cancel(self.uptime_ticker_id)

        # Save config
        self.save_config()

        # Destroy window
        self.root.destroy()


# ==============================================================================
# ☆ APPLICATION ENTRY POINT
# ==============================================================================
def main():
    root = tk.Tk()
    app = StellarJigglerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
