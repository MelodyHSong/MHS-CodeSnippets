import sys
import time
import random
from typing import List, Dict, Any
try:
    from .utils import (
        load_data, save_data, get_ram_metrics, get_cpu_metrics,
        get_gpu_metrics, ResponsivenessTracker,
        render_ascii_graph, render_dual_ascii_graph, format_gb,
        get_terminal_dimensions, hide_cursor, show_cursor, safe_write, center_ansi,
        visible_width, truncate_ansi,
        ANSI_CURSOR_HOME, ANSI_CLEAR_BOTTOM, CLR_RESET, CLR_BOLD, CLR_DIM,
        CLR_BLINK, CLR_CYAN, CLR_LIGHT_CYAN, CLR_GREEN, CLR_LIGHT_GREEN,
        CLR_YELLOW, CLR_LIGHT_YELLOW, CLR_RED, CLR_LIGHT_RED,
        CLR_MAGENTA, CLR_LIGHT_MAGENTA, CLR_WHITE
    )
except (ImportError, ValueError):
    from utils import (
        load_data, save_data, get_ram_metrics, get_cpu_metrics,
        get_gpu_metrics, ResponsivenessTracker,
        render_ascii_graph, render_dual_ascii_graph, format_gb,
        get_terminal_dimensions, hide_cursor, show_cursor, safe_write, center_ansi,
        visible_width, truncate_ansi,
        ANSI_CURSOR_HOME, ANSI_CLEAR_BOTTOM, CLR_RESET, CLR_BOLD, CLR_DIM,
        CLR_BLINK, CLR_CYAN, CLR_LIGHT_CYAN, CLR_GREEN, CLR_LIGHT_GREEN,
        CLR_YELLOW, CLR_LIGHT_YELLOW, CLR_RED, CLR_LIGHT_RED,
        CLR_MAGENTA, CLR_LIGHT_MAGENTA, CLR_WHITE
    )


class HardwareAnalyzer:
    def __init__(self, fps: int = None):
        self.data = load_data()
        settings = self.data.get("settings", {})

        self.target_fps = fps or settings.get("target_fps", 10)
        self.cpu_warn_pct = settings.get("cpu_warn_pct", 85.0)
        self.cpu_crit_pct = settings.get("cpu_crit_pct", 95.0)
        self.ram_warn_pct = settings.get("ram_warn_pct", 85.0)
        self.ram_crit_pct = settings.get("ram_crit_pct", 95.0)
        self.responsiveness_warn_ms = settings.get("responsiveness_warn_ms", 5.0)
        self.responsiveness_crit_ms = settings.get("responsiveness_crit_ms", 15.0)

        self.frame_duration = 1.0 / self.target_fps
        self.running = False

        # Metric history ring buffers
        self.cpu_history: List[float] = []
        self.ram_history: List[float] = []
        self.swap_history: List[float] = []
        self.gpu_history: List[float] = []
        self.vram_history: List[float] = []
        self.jitter_history: List[float] = []

        # Current live metric snapshot
        self.current_cpu = {"percent": 0.0, "freq_ghz": 0.0, "per_cpu": []}
        self.current_ram = {"percent": 0.0, "used_gb": 0.0, "total_gb": 0.0, "swap_percent": 0.0}
        self.current_gpu = {"available": False, "name": "N/A", "percent": 0.0, "vram_used_gb": 0.0, "vram_total_gb": 0.0}

        # Background Responsiveness Jitter Tracker
        self.responsiveness_tracker = ResponsivenessTracker(interval=0.05)

        # Session tracking
        self.peak_cpu_pct = 0.0
        self.peak_ram_pct = 0.0
        self.peak_gpu_pct = 0.0
        self.worst_jitter_ms = 0.0

        # Alien Kaomojis & Messages stickiness control
        self.alien_kaomojis = self.data.get("alien_kaomojis", {})
        self.alien_messages = self.data.get("alien_messages", ["Telemetry operational..."])
        self.current_quote = random.choice(self.alien_messages)
        self.quote_timer = time.time()
        self.quote_duration = 18.0

        self.current_kaomoji = None
        self.kaomoji_state = None
        self.kaomoji_timer = time.time()
        self.kaomoji_duration = 15.0

    def update_metrics(self):
        self.current_cpu = get_cpu_metrics()
        self.current_ram = get_ram_metrics()
        self.current_gpu = get_gpu_metrics()
        jitter_ms = self.responsiveness_tracker.current_jitter_ms

        cpu_pct = self.current_cpu["percent"]
        ram_pct = self.current_ram["percent"]
        swap_pct = self.current_ram.get("swap_percent", 0.0)

        gpu_pct = self.current_gpu["percent"] if self.current_gpu["available"] else 0.0
        vram_pct = ((self.current_gpu["vram_used_gb"] / self.current_gpu["vram_total_gb"]) * 100.0) if (self.current_gpu["available"] and self.current_gpu["vram_total_gb"] > 0) else 0.0

        # History ring buffers
        self.cpu_history.append(cpu_pct)
        self.ram_history.append(ram_pct)
        self.swap_history.append(swap_pct)
        self.gpu_history.append(gpu_pct)
        self.vram_history.append(vram_pct)
        self.jitter_history.append(jitter_ms)

        # Peak stats tracking
        self.peak_cpu_pct = max(self.peak_cpu_pct, cpu_pct)
        self.peak_ram_pct = max(self.peak_ram_pct, ram_pct)
        self.peak_gpu_pct = max(self.peak_gpu_pct, gpu_pct)
        self.worst_jitter_ms = max(self.worst_jitter_ms, jitter_ms)

        # Cap history buffers to max 200 samples
        if len(self.cpu_history) > 200:
            self.cpu_history.pop(0)
            self.ram_history.pop(0)
            self.swap_history.pop(0)
            self.gpu_history.pop(0)
            self.vram_history.pop(0)
            self.jitter_history.pop(0)

        # Rotate quote every 18 seconds
        if time.time() - self.quote_timer > self.quote_duration:
            self.current_quote = random.choice(self.alien_messages)
            self.quote_timer = time.time()

    def get_sticky_kaomoji(self, state: str) -> str:
        now = time.time()
        if self.kaomoji_state != state or not self.current_kaomoji or (now - self.kaomoji_timer > self.kaomoji_duration):
            self.kaomoji_state = state
            self.kaomoji_timer = now
            key = state.lower()
            kao_list = self.alien_kaomojis.get(key, ["(👽)"])
            self.current_kaomoji = random.choice(kao_list)
        return self.current_kaomoji

    def determine_hardware_state(self) -> tuple:
        """Determines health state: ('CRITICAL' | 'WARNING' | 'OPTIMAL', main_color, border_color, kaomoji, status_msg)."""
        cpu_pct = self.current_cpu["percent"]
        ram_pct = self.current_ram["percent"]
        jitter_ms = self.responsiveness_tracker.current_jitter_ms

        # 1. CRITICAL STATE (RED)
        if (cpu_pct >= self.cpu_crit_pct) or (ram_pct >= self.ram_crit_pct) or (jitter_ms >= self.responsiveness_crit_ms):
            kao = self.get_sticky_kaomoji("critical")
            status_msg = f"CRITICAL: MOTHERSHIP CORE OVERLOAD ({jitter_ms:.1f} ms)"
            return "CRITICAL", CLR_LIGHT_RED, CLR_RED, kao, status_msg

        # 2. WARNING STATE (YELLOW)
        if (cpu_pct >= self.cpu_warn_pct) or (ram_pct >= self.ram_warn_pct) or (jitter_ms >= self.responsiveness_warn_ms):
            kao = self.get_sticky_kaomoji("warning")
            status_msg = f"WARNING: TACHYON DECOHERENCE / HIGH LOAD ({cpu_pct:.0f}% CPU)"
            return "WARNING", CLR_LIGHT_YELLOW, CLR_YELLOW, kao, status_msg

        # 3. OPTIMAL STATE (GREEN)
        kao = self.get_sticky_kaomoji("optimal")
        freq_str = f"{self.current_cpu['freq_ghz']:.2f} GHz" if self.current_cpu['freq_ghz'] > 0 else "Active"
        status_msg = f"OPTIMAL: SUB-SPACE SILICON SYNCHRONIZED ({jitter_ms:.1f} ms)"
        return "OPTIMAL", CLR_LIGHT_GREEN, CLR_GREEN, kao, status_msg

    def build_frame(self, actual_fps: float) -> str:
        term_cols, term_lines = get_terminal_dimensions()

        # Dynamic graph sizing for responsive UI
        graph_width = min(140, max(30, term_cols - 8))
        graph_height = max(3, min(8, (term_lines - 16) // 3))

        state_name, main_color, border_color, kao, status_msg = self.determine_hardware_state()

        cpu_str = f"{self.current_cpu['percent']:5.1f}%"
        ram_used = format_gb(self.current_ram['used_gb'])
        ram_total = format_gb(self.current_ram['total_gb'])
        ram_pct = f"{self.current_ram['percent']:5.1f}%"

        if self.current_gpu["available"]:
            v_used = format_gb(self.current_gpu['vram_used_gb'])
            v_tot = format_gb(self.current_gpu['vram_total_gb'])
            gpu_str = f"{self.current_gpu['name'][:16]}: {self.current_gpu['percent']:.0f}% (VRAM: {v_used}/{v_tot})"
        else:
            gpu_str = "GPU: Integrated/N/A"

        jitter_val = self.responsiveness_tracker.current_jitter_ms
        jitter_str = f"{jitter_val:4.2f} ms"

        frame_lines = []
        box_width = graph_width + 4

        # Header Box (Alien HUD Title)
        frame_lines.append(f"{CLR_BOLD}{border_color}╔{'═' * box_width}╗{CLR_RESET}")
        title = f" 👽 ALIEN HUD HARDWARE ANALYZER 👽 [STATE: {state_name}] (FPS: {actual_fps:4.1f}/{self.target_fps}) "
        frame_lines.append(f"{CLR_BOLD}{border_color}║{CLR_RESET}{main_color}{center_ansi(title, box_width)}{CLR_RESET}{CLR_BOLD}{border_color}║{CLR_RESET}")
        frame_lines.append(f"{CLR_BOLD}{border_color}╠{'═' * box_width}╣{CLR_RESET}")

        # Alien Kaomoji Banner & Status Row
        banner = f"{CLR_BOLD}{main_color}{kao}{CLR_RESET}  {main_color}{status_msg}{CLR_RESET}"
        frame_lines.append(f"{CLR_BOLD}{border_color}║{CLR_RESET}{center_ansi(banner, box_width)}{CLR_BOLD}{border_color}║{CLR_RESET}")

        # Alien Quote Row
        quote_line = f"{CLR_DIM}\"{self.current_quote}\"{CLR_RESET}"
        frame_lines.append(f"{CLR_BOLD}{border_color}║{CLR_RESET}{center_ansi(quote_line, box_width)}{CLR_BOLD}{border_color}║{CLR_RESET}")

        # Metric Summary Row
        summary_str = (
            f"{CLR_LIGHT_CYAN}⚙ CPU: {cpu_str}{CLR_RESET} | "
            f"{CLR_LIGHT_GREEN}🧠 RAM: {ram_used}/{ram_total} ({ram_pct}){CLR_RESET} | "
            f"{CLR_LIGHT_MAGENTA}🎮 {gpu_str}{CLR_RESET} | "
            f"{main_color}⏱ Latency: {jitter_str}{CLR_RESET}"
        )
        frame_lines.append(f"{CLR_BOLD}{border_color}║{CLR_RESET}{center_ansi(summary_str, box_width)}{CLR_BOLD}{border_color}║{CLR_RESET}")
        frame_lines.append(f"{CLR_BOLD}{border_color}╠{'═' * box_width}╣{CLR_RESET}")

        # Graph 1: CPU Load vs System Responsiveness Jitter
        g1 = render_dual_ascii_graph(
            self.cpu_history, self.jitter_history, width=graph_width, height=graph_height,
            title="SUB-SPACE CPU LOAD (%) VS RESPONSIVENESS JITTER (ms)",
            label1="CPU %", label2="Jitter ms",
            color1=CLR_LIGHT_CYAN, color2=CLR_LIGHT_YELLOW,
            main_color=main_color, border_color=border_color
        )
        for line in g1:
            frame_lines.append(f"  {line}")

        frame_lines.append("")

        # Graph 2: RAM vs Pagefile/Swap Usage Dual Graph
        g2 = render_dual_ascii_graph(
            self.ram_history, self.swap_history, width=graph_width, height=graph_height,
            title="EARTH MEMORY MATRIX (%) VS PAGEFILE/SWAP (%)",
            label1="RAM %", label2="Swap %",
            color1=CLR_LIGHT_GREEN, color2=CLR_LIGHT_CYAN,
            main_color=main_color, border_color=border_color,
            max_val_override=100.0
        )
        for line in g2:
            frame_lines.append(f"  {line}")

        frame_lines.append("")

        # Graph 3: GPU Core Utilization vs VRAM Usage Dual Graph
        g3 = render_dual_ascii_graph(
            self.gpu_history, self.vram_history, width=graph_width, height=graph_height,
            title="COSMIC GPU CORE (%) VS VRAM MATRIX (%)",
            label1="GPU %", label2="VRAM %",
            color1=CLR_LIGHT_MAGENTA, color2=CLR_LIGHT_YELLOW,
            main_color=main_color, border_color=border_color,
            max_val_override=100.0
        )
        for line in g3:
            frame_lines.append(f"  {line}")

        # Footer Box
        frame_lines.append(f"{CLR_BOLD}{border_color}╚{'═' * box_width}╝{CLR_RESET}")
        raw_footer = (
            f"Peak CPU: {self.peak_cpu_pct:.1f}% | Peak RAM: {self.peak_ram_pct:.1f}% | "
            f"Peak GPU: {self.peak_gpu_pct:.1f}% | Max Jitter: {self.worst_jitter_ms:.2f}ms | Ctrl+C to disconnect"
        )
        if visible_width(raw_footer) > term_cols - 4:
            raw_footer = raw_footer[:term_cols - 4]
        footer_msg = f"{CLR_DIM}{raw_footer}{CLR_RESET}"
        frame_lines.append(f"  {footer_msg}")

        return "\n".join(frame_lines)

    def run(self):
        hide_cursor()
        self.running = True
        self.responsiveness_tracker.start()

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

                frame_buffer = self.build_frame(actual_fps)
                safe_write(ANSI_CURSOR_HOME + frame_buffer + ANSI_CLEAR_BOTTOM)

                elapsed = time.perf_counter() - frame_start
                sleep_needed = self.frame_duration - elapsed
                if sleep_needed > 0:
                    time.sleep(sleep_needed)

        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()

    def cleanup(self):
        self.responsiveness_tracker.stop()
        show_cursor()

        stats = self.data.get("stats", {})
        stats["session_peak_cpu_pct"] = max(stats.get("session_peak_cpu_pct", 0), self.peak_cpu_pct)
        stats["session_peak_ram_pct"] = max(stats.get("session_peak_ram_pct", 0), self.peak_ram_pct)
        stats["session_peak_gpu_pct"] = max(stats.get("session_peak_gpu_pct", 0), self.peak_gpu_pct)
        stats["session_worst_jitter_ms"] = max(stats.get("session_worst_jitter_ms", 0), self.worst_jitter_ms)
        self.data["stats"] = stats
        save_data(self.data)

        goodbye_kao = random.choice(self.alien_kaomojis.get("critical", ["(👽👋 ⏁⟒⌰⟒⌿⍜⌠⏁ Telemetry Closed!)"]))
        print(f"\n\n{CLR_BOLD}{CLR_LIGHT_CYAN}{goodbye_kao} Telemetry link closed. Session stats logged to data.json. Live long and prosper! 🛸{CLR_RESET}\n")
