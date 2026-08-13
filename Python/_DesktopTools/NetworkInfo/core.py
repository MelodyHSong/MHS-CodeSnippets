# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: core.py
# ☆ Date: 2026-08-13
# ☆
# ☆ Description: Core engine for real-time network performance 
# ☆ monitoring, rendering ASCII graph HUDs, kaomojis, and stats.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import sys
import time
import random
from typing import List, Dict, Any

from .utils import (
    load_data, save_data, get_net_io_counters, LatencyTracker,
    format_bytes, render_ascii_graph, render_dual_ascii_graph,
    get_terminal_dimensions, hide_cursor, show_cursor, safe_write, center_ansi,
    ANSI_CURSOR_HOME, ANSI_CLEAR_BOTTOM, CLR_RESET, CLR_BOLD, CLR_DIM,
    CLR_BLINK, CLR_CYAN, CLR_LIGHT_CYAN, CLR_GREEN, CLR_LIGHT_GREEN,
    CLR_YELLOW, CLR_LIGHT_YELLOW, CLR_RED, CLR_LIGHT_RED,
    CLR_MAGENTA, CLR_LIGHT_MAGENTA, CLR_WHITE
)


class NetworkAnalyzer:
    def __init__(self, fps: int = None, ping_target: str = None):
        self.data = load_data()
        settings = self.data.get("settings", {})

        self.target_fps = fps or settings.get("target_fps", 10)
        self.ping_target = ping_target or settings.get("ping_target", "8.8.8.8")
        self.latency_marginal_ms = settings.get("latency_marginal_ms", 100.0)

        self.frame_duration = 1.0 / self.target_fps
        self.running = False

        # Metric history ring buffers
        self.speed_history: List[float] = []
        self.latency_history: List[float] = []
        self.download_history: List[float] = []
        self.upload_history: List[float] = []

        # Network IO counters
        self.prev_recv, self.prev_sent = get_net_io_counters()
        self.last_sample_time = time.perf_counter()

        # Session tracking
        self.session_total_recv = 0.0
        self.session_total_sent = 0.0
        self.peak_download = 0.0
        self.peak_upload = 0.0

        # Background Ping Tracker thread
        self.latency_tracker = LatencyTracker(target_host=self.ping_target, interval=0.8)

        # Alien Kaomojis & Messages stickiness control
        self.alien_kaomojis = self.data.get("alien_kaomojis", {})
        self.alien_messages = self.data.get("alien_messages", ["Telemetry operational..."])
        self.current_quote = random.choice(self.alien_messages)
        self.quote_timer = time.time()
        self.quote_duration = 1.0  # Rotate messages every second for dynamic animated display

        self.current_kaomoji = None
        self.kaomoji_state = None
        self.kaomoji_timer = time.time()
        self.kaomoji_duration = 1.0  # Rotate Kaomojis every second for dynamic animated display


    def update_metrics(self):
        now = time.perf_counter()
        dt = now - self.last_sample_time
        if dt <= 0.001:
            return

        curr_recv, curr_sent = get_net_io_counters()

        # Counter deltas
        d_recv = max(0, curr_recv - self.prev_recv) if self.prev_recv > 0 else 0
        d_sent = max(0, curr_sent - self.prev_sent) if self.prev_sent > 0 else 0

        self.prev_recv = curr_recv
        self.prev_sent = curr_sent
        self.last_sample_time = now

        down_bps = d_recv / dt
        up_bps = d_sent / dt
        total_bps = down_bps + up_bps

        self.session_total_recv += d_recv
        self.session_total_sent += d_sent

        if down_bps > self.peak_download:
            self.peak_download = down_bps
        if up_bps > self.peak_upload:
            self.peak_upload = up_bps

        # Store KB/s values in history
        self.download_history.append(down_bps / 1024.0)
        self.upload_history.append(up_bps / 1024.0)
        self.speed_history.append(total_bps / 1024.0)

        lat = self.latency_tracker.current_latency_ms
        self.latency_history.append(max(0.0, lat) if lat > 0 else 0.0)

        # Cap history buffer to max 200 samples
        if len(self.download_history) > 200:
            self.download_history.pop(0)
            self.upload_history.pop(0)
            self.speed_history.pop(0)
            self.latency_history.pop(0)

        # Rotate quote every 1 second for animated HUD updates
        if time.time() - self.quote_timer > self.quote_duration:
            self.current_quote = random.choice(self.alien_messages)
            self.quote_timer = time.time()

    def get_sticky_kaomoji(self, state: str) -> str:
        now = time.time()
        # Change kaomoji if state changed OR if sticky duration expired
        if self.kaomoji_state != state or not self.current_kaomoji or (now - self.kaomoji_timer > self.kaomoji_duration):
            self.kaomoji_state = state
            self.kaomoji_timer = now
            key = state.lower()
            kao_list = self.alien_kaomojis.get(key, ["(👽)"])
            self.current_kaomoji = random.choice(kao_list)
        return self.current_kaomoji

    def determine_network_state(self) -> tuple:
        """Determines network health state: ('DROPPED' | 'MARGINAL' | 'OPTIMAL', main_color, border_color, kaomoji, status_msg)."""
        lat = self.latency_tracker.current_latency_ms

        # 1. DROPPED STATE (RED) - Connection timeout or lost
        if lat < 0:
            kao = self.get_sticky_kaomoji("dropped")
            status_msg = "DROPPED: ALIEN SIGNAL LOST! (SUB-SPACE DISCONNECTED)"
            return "DROPPED", CLR_LIGHT_RED, CLR_RED, kao, status_msg

        # 2. MARGINAL STATE (YELLOW) - High ping (> 100ms)
        if lat > self.latency_marginal_ms:
            kao = self.get_sticky_kaomoji("marginal")
            status_msg = f"MARGINAL: HIGH COSMIC JITTER ({lat:.0f} ms)! TACHYON DECOHERENCE!"
            return "MARGINAL", CLR_LIGHT_YELLOW, CLR_YELLOW, kao, status_msg

        # 3. OPTIMAL STATE (GREEN) - Clean fast link
        kao = self.get_sticky_kaomoji("optimal")
        status_msg = f"OPTIMAL: SUB-SPACE BEAM SYNCHRONIZED ({lat:.1f} ms)"
        return "OPTIMAL", CLR_LIGHT_GREEN, CLR_GREEN, kao, status_msg

    def build_frame(self, actual_fps: float) -> str:
        term_cols, term_lines = get_terminal_dimensions()

        # Dynamic graph sizing for full screen
        graph_width = min(140, max(30, term_cols - 8))
        graph_height = max(3, min(8, (term_lines - 16) // 3))

        state_name, main_color, border_color, kao, status_msg = self.determine_network_state()

        cur_down = format_bytes(self.download_history[-1] * 1024.0) if self.download_history else "0 B/s"
        cur_up = format_bytes(self.upload_history[-1] * 1024.0) if self.upload_history else "0 B/s"
        cur_total = format_bytes(self.speed_history[-1] * 1024.0) if self.speed_history else "0 B/s"
        lat_val = self.latency_tracker.current_latency_ms
        cur_lat = f"{lat_val:.1f} ms" if lat_val >= 0 else "OFFLINE"

        frame_lines = []
        box_width = graph_width + 4

        # Header Box (Colored according to state: GREEN/YELLOW/RED)
        frame_lines.append(f"{CLR_BOLD}{border_color}╔{'═' * box_width}╗{CLR_RESET}")
        title = f" 👽 ALIEN HUD NETWORK ANALYZER 👽 [STATE: {state_name}] (FPS: {actual_fps:4.1f}/{self.target_fps}) "
        frame_lines.append(f"{CLR_BOLD}{border_color}║{CLR_RESET}{main_color}{center_ansi(title, box_width)}{CLR_RESET}{CLR_BOLD}{border_color}║{CLR_RESET}")
        frame_lines.append(f"{CLR_BOLD}{border_color}╠{'═' * box_width}╣{CLR_RESET}")

        # Alien Kaomoji & Status message row
        banner = f"{CLR_BOLD}{main_color}{kao}{CLR_RESET}  {main_color}{status_msg}{CLR_RESET}"
        frame_lines.append(f"{CLR_BOLD}{border_color}║{CLR_RESET}{center_ansi(banner, box_width)}{CLR_BOLD}{border_color}║{CLR_RESET}")

        # Alien quote row
        quote_line = f"{CLR_DIM}\"{self.current_quote}\"{CLR_RESET}"
        frame_lines.append(f"{CLR_BOLD}{border_color}║{CLR_RESET}{center_ansi(quote_line, box_width)}{CLR_BOLD}{border_color}║{CLR_RESET}")

        # Metric summary row
        summary_str = f"{CLR_LIGHT_CYAN}▼ Down: {cur_down}{CLR_RESET} | {CLR_LIGHT_MAGENTA}▲ Up: {cur_up}{CLR_RESET} | {main_color}⚡ Total: {cur_total}{CLR_RESET} | {main_color}⏱ Ping: {cur_lat}{CLR_RESET}"
        frame_lines.append(f"{CLR_BOLD}{border_color}║{CLR_RESET}{center_ansi(summary_str, box_width)}{CLR_BOLD}{border_color}║{CLR_RESET}")
        frame_lines.append(f"{CLR_BOLD}{border_color}╠{'═' * box_width}╣{CLR_RESET}")

        # Graph 1: Overall Network Speed
        speed_graph = render_ascii_graph(
            self.speed_history, width=graph_width, height=graph_height,
            title="SUB-SPACE BANDWIDTH SPEED", unit=" KB/s", main_color=main_color, border_color=border_color
        )
        for line in speed_graph:
            frame_lines.append(f"  {line}")

        frame_lines.append("")

        # Graph 2: Latency Graph
        lat_graph = render_ascii_graph(
            self.latency_history, width=graph_width, height=graph_height,
            title=f"COSMIC LATENCY (Target: {self.ping_target})", unit=" ms", main_color=main_color, border_color=border_color
        )
        for line in lat_graph:
            frame_lines.append(f"  {line}")

        frame_lines.append("")

        # Graph 3: Upload vs Download Dual Graph
        dual_graph = render_dual_ascii_graph(
            self.download_history, self.upload_history, width=graph_width, height=graph_height,
            title="TELEMETRY TRANSMISSION (Cyan = Down | Magenta = Up)", main_color=main_color, border_color=border_color
        )
        for line in dual_graph:
            frame_lines.append(f"  {line}")

        # Footer Box
        frame_lines.append(f"{CLR_BOLD}{border_color}╚{'═' * box_width}╝{CLR_RESET}")
        session_down = format_bytes(self.session_total_recv)
        session_up = format_bytes(self.session_total_sent)
        peak_d = format_bytes(self.peak_download)
        footer_msg = f"{CLR_DIM}Session DL: {session_down} | UL: {session_up} | Peak DL: {peak_d} | Fullscreen Adaptive HUD | Ctrl+C to disconnect{CLR_RESET}"
        frame_lines.append(f"  {footer_msg}")

        return "\n".join(frame_lines)

    def run(self):
        hide_cursor()
        self.running = True
        self.latency_tracker.start()

        last_fps_check = time.perf_counter()
        frame_count = 0
        actual_fps = float(self.target_fps)

        try:
            while self.running:
                frame_start = time.perf_counter()

                self.update_metrics()
                frame_count += 1

                now = time.perf_counter()
                if now - last_fps_check >= 1.0:
                    actual_fps = frame_count / (now - last_fps_check)
                    frame_count = 0
                    last_fps_check = now

                # Build & safe-write full frame buffer
                frame_buffer = self.build_frame(actual_fps)
                safe_write(ANSI_CURSOR_HOME + frame_buffer + ANSI_CLEAR_BOTTOM)

                # Framerate locking sleep
                elapsed = time.perf_counter() - frame_start
                sleep_needed = self.frame_duration - elapsed
                if sleep_needed > 0:
                    time.sleep(sleep_needed)

        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()

    def cleanup(self):
        self.latency_tracker.stop()
        show_cursor()

        # Update saved session stats in data.json
        stats = self.data.get("stats", {})
        stats["session_peak_download_bps"] = max(stats.get("session_peak_download_bps", 0), self.peak_download)
        stats["session_peak_upload_bps"] = max(stats.get("session_peak_upload_bps", 0), self.peak_upload)
        stats["session_total_download_bytes"] = stats.get("session_total_download_bytes", 0) + self.session_total_recv
        stats["session_total_upload_bytes"] = stats.get("session_total_upload_bytes", 0) + self.session_total_sent
        self.data["stats"] = stats
        save_data(self.data)

        # Print clean exit message with alien goodbye kaomoji
        goodbye_kao = random.choice(self.alien_kaomojis.get("dropped", ["(👽👋 ⏁⟒⌰⟒⌿⍜⌠⏁ Out!)"]))
        print(f"\n\n{CLR_BOLD}{CLR_LIGHT_CYAN}{goodbye_kao} Telemetry link closed. Session stats logged to data.json. Live long and prosper! 🛸{CLR_RESET}\n")
