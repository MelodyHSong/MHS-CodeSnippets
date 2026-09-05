# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: app.py
# ☆ Description: Desktop Tool Template - Clean, modern Tkinter workstation template with Windows integration.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import sys
import os
import json
import time
import queue
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

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
        # SetProcessDpiAwareness: 1 = System DPI aware, 2 = Per-monitor DPI aware
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
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
BORDER_ACTIVE = "#58a6ff"    # Focused active border

TEXT_PRIMARY = "#e2e8f0"     # Starlight white
TEXT_MUTED = "#8b949e"       # Dust gray
TEXT_DIM = "#586069"         # Nebula shadow

ACCENT_CYAN = "#58a6ff"      # Starlight cyan
ACCENT_GOLD = "#f2cc60"      # Celestial star gold
ACCENT_MINT = "#7ee787"      # Status ok / green
ACCENT_CORAL = "#f85149"     # Alert / danger red

FONT_HEADER = ("Segoe UI", 13, "bold")
FONT_SUBHEADER = ("Segoe UI", 10)
FONT_UI = ("Segoe UI", 9)
FONT_UI_BOLD = ("Segoe UI", 9, "bold")
FONT_CODE = ("Consolas", 10)
FONT_STATS = ("Consolas", 9)


class DesktopToolApp:
    def __init__(self, root, initial_file=None):
        self.root = root
        self.root.title("⭐ Desktop Tool Template - [Workstation Console]")
        self.root.geometry("1080x680")
        self.root.minsize(780, 500)
        self.root.configure(bg=BG_MAIN)

        # Asset & Path Resolution (handles both source .py and PyInstaller .exe)
        self.app_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        # State Variables
        self.config_path = os.path.join(self.base_dir, "config.json")
        self.config = self.load_config()
        self.current_file_path = None
        self.is_dirty = False
        self.autosave_timer = None
        self.background_queue = queue.Queue()

        # Set Window Icon
        self.set_app_icon()

        # Build UI Components
        self.build_ui()

        # Keyboard Shortcut Bindings
        self.bind_shortcuts()

        # Window Close Protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)

        # Periodic Queue Checker for Thread-safe UI updates
        self.root.after(100, self.process_queue)

        # Load initial file if passed from command line or Explorer context menu
        if initial_file and os.path.exists(initial_file):
            self.load_file(initial_file)
        else:
            self.log_message("Workstation initialized and ready for commands.")

    # ==========================================================================
    # ☆ ASSET RESOLUTION & CONFIGURATION
    # ==========================================================================
    def set_app_icon(self):
        icon_candidates = [
            os.path.join(self.app_dir, "assets", "app_icon.ico"),
            os.path.join(self.base_dir, "assets", "app_icon.ico"),
        ]
        for icon_path in icon_candidates:
            if os.path.exists(icon_path):
                try:
                    self.root.iconbitmap(icon_path)
                    break
                except Exception:
                    pass

    def load_config(self):
        default_config = {
            "app_name": "Desktop Tool Template",
            "version": "1.0.0",
            "preferences": {
                "autosave_enabled": True,
                "autosave_interval_ms": 2000,
                "confirm_exit_on_unsaved": True
            }
        }
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[!] Warning: Could not parse config.json: {e}")
        return default_config

    def save_config(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.log_message(f"Error saving configuration: {e}", level="ERROR")

    # ==========================================================================
    # ☆ GUI ARCHITECTURE
    # ==========================================================================
    def build_ui(self):
        # Configure TTK styles for dark theme
        self.setup_ttk_styles()

        # 1. Header Bar
        self.build_header()

        # 2. Main Container (Sidebar + Content Workspace)
        main_container = tk.Frame(self.root, bg=BG_MAIN)
        main_container.pack(fill="both", expand=True, padx=12, pady=(0, 6))

        # Left Sidebar (Controls & Actions)
        self.build_sidebar(main_container)

        # Right Workspace (Tabs / Viewer / Console)
        self.build_workspace(main_container)

        # 3. Bottom Status Bar
        self.build_statusbar()

    def setup_ttk_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Scrollbar styling
        style.configure(
            "Vertical.TScrollbar",
            background=BG_PANEL,
            troughcolor=BG_MAIN,
            bordercolor=BORDER_COLOR,
            arrowcolor=TEXT_MUTED
        )
        style.map("Vertical.TScrollbar", background=[("active", ACCENT_CYAN)])

        # Notebook (Tabs) styling
        style.configure("TNotebook", background=BG_MAIN, borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background=BG_PANEL,
            foreground=TEXT_MUTED,
            padding=[16, 6],
            font=FONT_UI_BOLD,
            borderwidth=0
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", BG_SURFACE)],
            foreground=[("selected", ACCENT_CYAN)]
        )

    def build_header(self):
        header_frame = tk.Frame(self.root, bg=BG_PANEL, height=56, highlightthickness=1, highlightbackground=BORDER_COLOR)
        header_frame.pack(fill="x", padx=12, pady=(10, 8))
        header_frame.pack_propagate(False)

        # Left: Branding & Subtitle
        brand_frame = tk.Frame(header_frame, bg=BG_PANEL)
        brand_frame.pack(side="left", padx=14, pady=6)

        title_lbl = tk.Label(
            brand_frame,
            text="⭐ DESKTOP TOOL TEMPLATE",
            font=FONT_HEADER,
            fg=TEXT_PRIMARY,
            bg=BG_PANEL
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = tk.Label(
            brand_frame,
            text="Modular Workstation Blueprint • Built for Windows & Python",
            font=FONT_SUBHEADER,
            fg=TEXT_MUTED,
            bg=BG_PANEL
        )
        subtitle_lbl.pack(anchor="w")

        # Right: Status Pill & Quick Action Buttons
        actions_frame = tk.Frame(header_frame, bg=BG_PANEL)
        actions_frame.pack(side="right", padx=14, pady=8)

        self.status_pill = tk.Label(
            actions_frame,
            text="● SYSTEM READY",
            font=FONT_UI_BOLD,
            fg=ACCENT_MINT,
            bg=BG_SURFACE,
            padx=10,
            pady=4,
            relief="flat"
        )
        self.status_pill.pack(side="right", padx=(8, 0))

        btn_run = tk.Button(
            actions_frame,
            text="⚡ Run Task",
            font=FONT_UI_BOLD,
            fg=BG_MAIN,
            bg=ACCENT_CYAN,
            activebackground="#79c0ff",
            activeforeground=BG_MAIN,
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.on_run_task
        )
        btn_run.pack(side="right", padx=4)

    def build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=BG_PANEL, width=260, highlightthickness=1, highlightbackground=BORDER_COLOR)
        sidebar.pack(side="left", fill="y", padx=(0, 8))
        sidebar.pack_propagate(False)

        # Sidebar Header
        lbl_actions = tk.Label(sidebar, text="ACTIONS & CONTROLS", font=FONT_UI_BOLD, fg=ACCENT_GOLD, bg=BG_PANEL)
        lbl_actions.pack(anchor="w", padx=14, pady=(14, 8))

        # Primary Action Buttons
        btn_open = tk.Button(
            sidebar,
            text="📂  Open File (Ctrl+O)",
            font=FONT_UI,
            fg=TEXT_PRIMARY,
            bg=BG_SURFACE,
            activebackground=BG_ACTIVE,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            anchor="w",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.on_open_file
        )
        btn_open.pack(fill="x", padx=12, pady=3)

        btn_save = tk.Button(
            sidebar,
            text="💾  Save File (Ctrl+S)",
            font=FONT_UI,
            fg=TEXT_PRIMARY,
            bg=BG_SURFACE,
            activebackground=BG_ACTIVE,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            anchor="w",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.on_save_file
        )
        btn_save.pack(fill="x", padx=12, pady=3)

        btn_async = tk.Button(
            sidebar,
            text="🔄  Async Task (Background)",
            font=FONT_UI,
            fg=TEXT_PRIMARY,
            bg=BG_SURFACE,
            activebackground=BG_ACTIVE,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            anchor="w",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.on_start_async_task
        )
        btn_async.pack(fill="x", padx=12, pady=3)

        btn_clear_log = tk.Button(
            sidebar,
            text="🧹  Clear Activity Log",
            font=FONT_UI,
            fg=TEXT_PRIMARY,
            bg=BG_SURFACE,
            activebackground=BG_ACTIVE,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            anchor="w",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.clear_logs
        )
        btn_clear_log.pack(fill="x", padx=12, pady=3)

        # File Telemetry Card
        lbl_telemetry = tk.Label(sidebar, text="ACTIVE TARGET", font=FONT_UI_BOLD, fg=ACCENT_GOLD, bg=BG_PANEL)
        lbl_telemetry.pack(anchor="w", padx=14, pady=(18, 6))

        self.telemetry_card = tk.Frame(sidebar, bg=BG_SURFACE, highlightthickness=1, highlightbackground=BORDER_COLOR)
        self.telemetry_card.pack(fill="x", padx=12, pady=4)

        self.lbl_target_name = tk.Label(
            self.telemetry_card,
            text="No file loaded",
            font=FONT_UI_BOLD,
            fg=ACCENT_CYAN,
            bg=BG_SURFACE,
            anchor="w",
            wraplength=220
        )
        self.lbl_target_name.pack(anchor="w", padx=10, pady=(8, 2))

        self.lbl_target_info = tk.Label(
            self.telemetry_card,
            text="Select Open File or launch via Windows context menu",
            font=FONT_UI,
            fg=TEXT_MUTED,
            bg=BG_SURFACE,
            anchor="w",
            justify="left",
            wraplength=220
        )
        self.lbl_target_info.pack(anchor="w", padx=10, pady=(0, 8))

        # Bottom Preferences Card
        pref_frame = tk.Frame(sidebar, bg=BG_PANEL)
        pref_frame.pack(side="bottom", fill="x", padx=12, pady=12)

        self.autosave_var = tk.BooleanVar(value=self.config.get("preferences", {}).get("autosave_enabled", True))
        chk_autosave = tk.Checkbutton(
            pref_frame,
            text="Enable Background Autosave",
            variable=self.autosave_var,
            font=FONT_UI,
            fg=TEXT_PRIMARY,
            bg=BG_PANEL,
            activebackground=BG_PANEL,
            activeforeground=TEXT_PRIMARY,
            selectcolor=BG_SURFACE,
            command=self.toggle_autosave
        )
        chk_autosave.pack(anchor="w")

    def build_workspace(self, parent):
        workspace_frame = tk.Frame(parent, bg=BG_MAIN)
        workspace_frame.pack(side="right", fill="both", expand=True)

        self.notebook = ttk.Notebook(workspace_frame)
        self.notebook.pack(fill="both", expand=True)

        # Tab 1: Editor / Content Workspace
        tab_editor = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(tab_editor, text="  Workspace Editor  ")

        editor_box = tk.Frame(tab_editor, bg=BG_MAIN, highlightthickness=1, highlightbackground=BORDER_COLOR)
        editor_box.pack(fill="both", expand=True, padx=8, pady=8)

        self.editor = tk.Text(
            editor_box,
            font=FONT_CODE,
            bg=BG_MAIN,
            fg=TEXT_PRIMARY,
            insertbackground=ACCENT_CYAN,
            selectbackground=BG_ACTIVE,
            selectforeground=TEXT_PRIMARY,
            relief="flat",
            wrap="word",
            undo=True,
            padx=10,
            pady=10
        )
        scroll_editor = ttk.Scrollbar(editor_box, orient="vertical", command=self.editor.yview)
        self.editor.configure(yscrollcommand=scroll_editor.set)

        scroll_editor.pack(side="right", fill="y")
        self.editor.pack(side="left", fill="both", expand=True)

        # Insert starter placeholder text
        starter_text = (
            "# ⭐ Welcome to Desktop Tool Template! ⭐\n\n"
            "This modular workstation provides a production-ready starting point for your next Python utility.\n\n"
            "✨ Built-in Features:\n"
            "  • High-DPI Windows Scaling & Cosmic Dark Mode Styling\n"
            "  • Windows Explorer Context Menu & Desktop Shortcut Setup\n"
            "  • Dual Mode: Dev Script (pythonw) and Standalone Exe (PyInstaller)\n"
            "  • Background Task Runner with Thread-Safe UI Messaging\n"
            "  • Debounced Autosave & Dirty State Management\n"
            "  • Multi-resolution Icon Generator (Pillow)\n\n"
            "Press 'Run Task' above or 'Ctrl + O' to open a file!\n"
        )
        self.editor.insert("1.0", starter_text)
        self.editor.bind("<<Modified>>", self.on_content_modified)

        # Tab 2: Activity Log / Console
        tab_console = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(tab_console, text="  Activity Log & Telemetry  ")

        console_box = tk.Frame(tab_console, bg=BG_MAIN, highlightthickness=1, highlightbackground=BORDER_COLOR)
        console_box.pack(fill="both", expand=True, padx=8, pady=8)

        self.log_text = tk.Text(
            console_box,
            font=FONT_CODE,
            bg=BG_MAIN,
            fg=TEXT_MUTED,
            relief="flat",
            wrap="word",
            padx=10,
            pady=10
        )
        scroll_log = ttk.Scrollbar(console_box, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scroll_log.set)

        scroll_log.pack(side="right", fill="y")
        self.log_text.pack(side="left", fill="both", expand=True)

        # Log styling tags
        self.log_text.tag_config("INFO", foreground=ACCENT_CYAN)
        self.log_text.tag_config("SUCCESS", foreground=ACCENT_MINT)
        self.log_text.tag_config("WARNING", foreground=ACCENT_GOLD)
        self.log_text.tag_config("ERROR", foreground=ACCENT_CORAL)

    def build_statusbar(self):
        status_bar = tk.Frame(self.root, bg=BG_PANEL, height=26, highlightthickness=1, highlightbackground=BORDER_COLOR)
        status_bar.pack(fill="x", side="bottom")

        self.status_lbl = tk.Label(status_bar, text="Ready", font=FONT_STATS, fg=TEXT_MUTED, bg=BG_PANEL)
        self.status_lbl.pack(side="left", padx=14)

        version_lbl = tk.Label(
            status_bar,
            text=f"Version {self.config.get('version', '1.0.0')} • Cassiopeia Studios",
            font=FONT_STATS,
            fg=TEXT_DIM,
            bg=BG_PANEL
        )
        version_lbl.pack(side="right", padx=14)

        self.stats_lbl = tk.Label(status_bar, text="Chars: 0 | Lines: 0", font=FONT_STATS, fg=TEXT_MUTED, bg=BG_PANEL)
        self.stats_lbl.pack(side="right", padx=14)
        self.update_content_stats()

    # ==========================================================================
    # ☆ EVENT HANDLERS & LOGIC
    # ==========================================================================
    def bind_shortcuts(self):
        self.root.bind("<Control-o>", lambda e: self.on_open_file())
        self.root.bind("<Control-s>", lambda e: self.on_save_file())
        self.root.bind("<Control-r>", lambda e: self.on_run_task())
        self.root.bind("<Control-q>", lambda e: self.on_window_close())
        self.root.bind("<F5>", lambda e: self.on_run_task())

    def log_message(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] ", "DIM")
        self.log_text.insert("end", f"[{level:<7}] ", level)
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")

    def set_status_pill(self, text, color):
        self.status_pill.config(text=text, fg=color)

    def on_content_modified(self, event=None):
        if self.editor.edit_modified():
            self.is_dirty = True
            self.update_content_stats()
            self.status_lbl.config(text="● Unsaved changes")

            if self.autosave_var.get():
                if self.autosave_timer is not None:
                    self.root.after_cancel(self.autosave_timer)
                interval = self.config.get("preferences", {}).get("autosave_interval_ms", 2000)
                self.autosave_timer = self.root.after(interval, self.trigger_autosave)

            self.editor.edit_modified(False)

    def update_content_stats(self):
        content = self.editor.get("1.0", "end-1c")
        chars = len(content)
        lines = content.count("\n") + 1 if content else 0
        self.stats_lbl.config(text=f"Chars: {chars} | Lines: {lines}")

    def trigger_autosave(self):
        if self.is_dirty and self.current_file_path:
            self.save_file(self.current_file_path, is_autosave=True)

    def on_open_file(self):
        file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("Supported Files", "*.txt;*.md;*.json;*.log;*.py"), ("All Files", "*.*")]
        )
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", content)
            self.current_file_path = file_path
            self.is_dirty = False

            name = os.path.basename(file_path)
            size = os.path.getsize(file_path)
            self.lbl_target_name.config(text=name)
            self.lbl_target_info.config(text=f"Size: {size:,} bytes\nPath: {file_path}")
            self.root.title(f"⭐ Desktop Tool Template - [{name}]")
            self.status_lbl.config(text=f"Loaded: {name}")
            self.log_message(f"Opened file: {file_path}", level="SUCCESS")
            self.update_content_stats()
        except Exception as e:
            messagebox.showerror("Error Opening File", f"Could not open file:\n{e}")
            self.log_message(f"Failed to open {file_path}: {e}", level="ERROR")

    def on_save_file(self):
        if not self.current_file_path:
            file_path = filedialog.asksaveasfilename(
                title="Save As",
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("Markdown", "*.md"), ("All Files", "*.*")]
            )
            if not file_path:
                return
            self.current_file_path = file_path

        self.save_file(self.current_file_path)

    def save_file(self, file_path, is_autosave=False):
        try:
            content = self.editor.get("1.0", "end-1c")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            self.is_dirty = False
            msg = "Autosaved to disk" if is_autosave else f"Saved to {os.path.basename(file_path)}"
            self.status_lbl.config(text=f"✓ {msg}")
            self.log_message(msg, level="SUCCESS")
        except Exception as e:
            messagebox.showerror("Error Saving File", f"Could not save file:\n{e}")
            self.log_message(f"Save failed: {e}", level="ERROR")

    def toggle_autosave(self):
        val = self.autosave_var.get()
        if "preferences" not in self.config:
            self.config["preferences"] = {}
        self.config["preferences"]["autosave_enabled"] = val
        self.save_config()
        status = "enabled" if val else "disabled"
        self.log_message(f"Autosave {status}.", level="INFO")

    def on_run_task(self):
        """Simulates running the primary tool action."""
        self.log_message("Executing main tool action on workspace buffer...", level="INFO")
        self.set_status_pill("● PROCESSING", ACCENT_GOLD)

        # Example action: append summary banner or transform text
        def task():
            time.sleep(0.5)  # Simulate brief processing
            return "Task completed successfully! Output verified."

        def on_done(result):
            self.set_status_pill("● SYSTEM READY", ACCENT_MINT)
            self.log_message(result, level="SUCCESS")

        self.run_in_background(task, on_complete=on_done)

    # ==========================================================================
    # ☆ THREAD-SAFE BACKGROUND WORKER
    # ==========================================================================
    def run_in_background(self, target_func, on_complete=None, on_error=None):
        """Executes a callable in a background daemon thread without freezing the Tkinter GUI."""
        def worker():
            try:
                res = target_func()
                self.background_queue.put(("SUCCESS", on_complete, res))
            except Exception as err:
                self.background_queue.put(("ERROR", on_error, err))

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def process_queue(self):
        """Polls background task queue and dispatches callbacks to main thread."""
        try:
            while not self.background_queue.empty():
                status, callback, data = self.background_queue.get_nowait()
                if status == "SUCCESS" and callback:
                    callback(data)
                elif status == "ERROR":
                    if callback:
                        callback(data)
                    else:
                        self.log_message(f"Background task exception: {data}", level="ERROR")
                        self.set_status_pill("● SYSTEM READY", ACCENT_MINT)
        except Exception:
            pass
        finally:
            self.root.after(100, self.process_queue)

    def on_start_async_task(self):
        """Demonstrates a long-running background task with live progress reporting."""
        self.set_status_pill("● BACKGROUND BUSY", ACCENT_CYAN)
        self.log_message("Starting asynchronous background sequence...", level="INFO")

        def background_job():
            for step in range(1, 4):
                time.sleep(0.7)
                self.background_queue.put(("SUCCESS", lambda s=step: self.log_message(f"Step {s}/3 finished..."), None))
            return "Async sequence completed without UI blocking!"

        def on_finished(result):
            self.set_status_pill("● SYSTEM READY", ACCENT_MINT)
            self.log_message(result, level="SUCCESS")

        self.run_in_background(background_job, on_complete=on_finished)

    def clear_logs(self):
        self.log_text.delete("1.0", "end")
        self.log_message("Activity log cleared.", level="INFO")

    def on_window_close(self):
        if self.is_dirty and self.config.get("preferences", {}).get("confirm_exit_on_unsaved", True):
            resp = messagebox.askyesnocancel("Unsaved Changes", "You have unsaved changes. Save before exiting?")
            if resp is True:
                if self.current_file_path:
                    self.save_file(self.current_file_path)
                else:
                    self.on_save_file()
                self.root.destroy()
            elif resp is False:
                self.root.destroy()
            # If Cancel, do nothing
        else:
            self.root.destroy()


def main():
    root = tk.Tk()
    initial_file = None
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        initial_file = sys.argv[1]

    app = DesktopToolApp(root, initial_file=initial_file)
    root.mainloop()


if __name__ == "__main__":
    main()
