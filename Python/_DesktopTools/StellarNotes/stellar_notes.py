# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: stellar_notes.py
# ☆ Date: September 3, 2026
# ☆
# ☆ Description: StellarNotes - A sleek cosmic desktop note-taking and voice-narration workstation with Windows Explorer integration.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import sys
import os
import json
import time
import tempfile
import threading
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ==============================================================================
# ☆ COSMIC COLOR PALETTE & THEME
# ==============================================================================
BG_DARK = "#0d1117"          # Deep space obsidian
CONSOLE_FRAME = "#161b22"    # Spaceship hull console
SIDEBAR_BG = "#11141c"       # Star catalog sidebar
CARD_BG = "#161c26"          # Unselected note card
CARD_ACTIVE = "#222c3d"      # Selected note card
CARD_HOVER = "#1c2433"       # Hovered note card
EDITOR_BG = "#0b0e14"        # Note editor interior
BORDER_COLOR = "#30363d"     # Panel rim border
BORDER_ACTIVE = "#58a6ff"    # Focused active border

TEXT_PRIMARY = "#e2e8f0"     # Starlight white
TEXT_MUTED = "#8b949e"       # Cosmic dust gray
TEXT_DIM = "#586069"         # Nebula shadow

ACCENT_GOLD = "#f2cc60"      # Radiant celestial star gold
ACCENT_CYAN = "#58a6ff"      # Starlight cyan
ACCENT_MINT = "#7ee787"      # Alien mint / active voice green
ACCENT_CORAL = "#f85149"     # Supernova coral / delete red

FONT_UI = ("Segoe UI", 10)
FONT_UI_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 15, "bold")
FONT_EDITOR = ("Consolas", 12)
FONT_SMALL = ("Segoe UI", 9)
FONT_STATS = ("Consolas", 9)


class StellarNotesApp:
    def __init__(self, root, initial_file=None):
        self.root = root
        self.root.title("⭐ StellarNotes - [Galactic Transmission Console]")
        self.root.geometry("1120x680")
        self.root.minsize(820, 520)
        self.root.configure(bg=BG_DARK)

        # Resolve directories
        self.app_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.notes_dir = os.path.join(self.base_dir, "notes")
        os.makedirs(self.notes_dir, exist_ok=True)

        self.metadata_file = os.path.join(self.notes_dir, ".stellar_metadata.json")
        self.metadata = self.load_metadata()

        # Set window icon
        self.set_app_icon()

        # Application State
        self.current_note_path = None
        self.is_external_file = False
        self.is_dirty = False
        self.notes = []
        self.active_tab = "all"  # 'all' | 'pinned'
        self.autosave_timer = None
        self.stats_timer = None

        # Voice Narration ("Talking Note") State
        self.speech_process = None
        self.speech_temp_path = None
        self.is_speaking = False

        # Build GUI
        self.build_ui()

        # Bind Global Keyboard Shortcuts
        self.bind_shortcuts()

        # Refresh notes and load initial note
        self.refresh_notes_list()

        if initial_file and os.path.exists(initial_file):
            self.load_note(initial_file, is_external=True)
        elif self.notes:
            self.load_note(self.notes[0]["path"])
        else:
            self.create_new_note(initial=True)

        # Intercept window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)

    # ==========================================================================
    # ☆ ICON & METADATA MANAGEMENT
    # ==========================================================================
    def set_app_icon(self):
        icon_path = os.path.join(self.app_dir, "assets", "stellar_notes.ico")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(self.base_dir, "assets", "stellar_notes.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

    def load_metadata(self):
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"pinned": []}

    def save_metadata(self):
        try:
            with open(self.metadata_file, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, indent=2)
        except Exception:
            pass

    # ==========================================================================
    # ☆ GUI ARCHITECTURE
    # ==========================================================================
    def build_ui(self):
        # Top Cosmic Control Deck
        self.header_frame = tk.Frame(self.root, bg=CONSOLE_FRAME, height=50)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)

        # Brand / Logo
        self.brand_label = tk.Label(
            self.header_frame,
            text="⭐ STELLAR NOTES",
            font=("Segoe UI", 12, "bold"),
            bg=CONSOLE_FRAME,
            fg=ACCENT_GOLD,
            padx=16,
            pady=10
        )
        self.brand_label.pack(side=tk.LEFT)

        # Header Action Buttons
        self.btn_new = self.create_header_btn("➕ New Note", self.create_new_note, ACCENT_CYAN)
        self.btn_save = self.create_header_btn("💾 Save", self.save_current_note, ACCENT_GOLD)
        self.btn_pin = self.create_header_btn("⭐ Pin Note", self.toggle_pin_current, ACCENT_GOLD)
        
        # Audio / Narration ("Talking Note") Button
        self.btn_speech = self.create_header_btn("🔊 Read Aloud", self.toggle_speech, ACCENT_MINT)

        self.btn_open = self.create_header_btn("📂 Open File", self.open_external_file, TEXT_PRIMARY)
        self.btn_export = self.create_header_btn("📤 Export", self.export_current_note, TEXT_PRIMARY)
        self.btn_delete = self.create_header_btn("🗑️ Delete", self.delete_current_note, ACCENT_CORAL)

        # Main Split Console
        self.paned_window = tk.PanedWindow(
            self.root,
            orient=tk.HORIZONTAL,
            sashrelief=tk.FLAT,
            bg=CONSOLE_FRAME,
            bd=0,
            sashwidth=4
        )
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=8, pady=(4, 0))

        # ----------------------------------------------------------------------
        # LEFT PANE: Sidebar (Search + Notes Catalog)
        # ----------------------------------------------------------------------
        self.sidebar_frame = tk.Frame(self.paned_window, bg=SIDEBAR_BG, width=330)
        self.paned_window.add(self.sidebar_frame, minsize=260)

        # Search Box Container
        self.search_container = tk.Frame(self.sidebar_frame, bg=SIDEBAR_BG, padx=12, pady=10)
        self.search_container.pack(fill=tk.X)

        self.search_entry_frame = tk.Frame(self.search_container, bg=CARD_BG, highlightbackground=BORDER_COLOR, highlightthickness=1)
        self.search_entry_frame.pack(fill=tk.X)

        self.search_icon = tk.Label(self.search_entry_frame, text="🔍", bg=CARD_BG, fg=TEXT_MUTED, font=FONT_SMALL)
        self.search_icon.pack(side=tk.LEFT, padx=(8, 4), pady=4)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.filter_notes())
        self.search_entry = tk.Entry(
            self.search_entry_frame,
            textvariable=self.search_var,
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            insertbackground=ACCENT_CYAN,
            font=FONT_UI,
            bd=0
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=4, padx=(0, 6))

        # Filter Tabs Frame
        self.tabs_frame = tk.Frame(self.sidebar_frame, bg=SIDEBAR_BG, padx=12, pady=4)
        self.tabs_frame.pack(fill=tk.X)

        self.tab_all_btn = tk.Button(
            self.tabs_frame,
            text="All Transmissions",
            command=lambda: self.switch_tab("all"),
            bg=CARD_ACTIVE,
            fg=ACCENT_CYAN,
            relief=tk.FLAT,
            font=FONT_SMALL,
            bd=0,
            padx=10,
            pady=3,
            cursor="hand2"
        )
        self.tab_all_btn.pack(side=tk.LEFT, padx=(0, 6))

        self.tab_pinned_btn = tk.Button(
            self.tabs_frame,
            text="⭐ Pinned",
            command=lambda: self.switch_tab("pinned"),
            bg=CARD_BG,
            fg=TEXT_MUTED,
            relief=tk.FLAT,
            font=FONT_SMALL,
            bd=0,
            padx=10,
            pady=3,
            cursor="hand2"
        )
        self.tab_pinned_btn.pack(side=tk.LEFT)

        # Scrollable Note Catalog Canvas
        self.catalog_frame = tk.Frame(self.sidebar_frame, bg=SIDEBAR_BG)
        self.catalog_frame.pack(fill=tk.BOTH, expand=True, padx=(10, 0), pady=(8, 8))

        self.canvas = tk.Canvas(self.catalog_frame, bg=SIDEBAR_BG, bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.catalog_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.notes_inner_frame = tk.Frame(self.canvas, bg=SIDEBAR_BG)

        self.canvas.create_window((0, 0), window=self.notes_inner_frame, anchor="nw", tags="inner_frame")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.notes_inner_frame.bind(
            "<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>", 
            lambda e: self.canvas.itemconfig("inner_frame", width=e.width)
        )
        # Mousewheel binding
        self.bind_mousewheel(self.canvas, self.notes_inner_frame)

        # ----------------------------------------------------------------------
        # RIGHT PANE: Note Editor
        # ----------------------------------------------------------------------
        self.editor_pane = tk.Frame(self.paned_window, bg=EDITOR_BG)
        self.paned_window.add(self.editor_pane, minsize=450)

        # Title & Meta Header
        self.title_frame = tk.Frame(self.editor_pane, bg=EDITOR_BG, padx=18, pady=12)
        self.title_frame.pack(fill=tk.X)

        self.title_var = tk.StringVar()
        self.title_var.trace_add("write", self.on_title_modified)
        self.title_entry = tk.Entry(
            self.title_frame,
            textvariable=self.title_var,
            font=FONT_TITLE,
            bg=EDITOR_BG,
            fg=TEXT_PRIMARY,
            insertbackground=ACCENT_CYAN,
            bd=0
        )
        self.title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.pin_indicator = tk.Label(
            self.title_frame,
            text="",
            font=("Segoe UI", 13),
            bg=EDITOR_BG,
            fg=ACCENT_GOLD
        )
        self.pin_indicator.pack(side=tk.RIGHT, padx=6)

        # Subtle divider
        self.editor_divider = tk.Frame(self.editor_pane, bg=BORDER_COLOR, height=1)
        self.editor_divider.pack(fill=tk.X, padx=18)

        # Text Editor Area with custom scrollbar
        self.text_container = tk.Frame(self.editor_pane, bg=EDITOR_BG)
        self.text_container.pack(fill=tk.BOTH, expand=True, padx=14, pady=(8, 0))

        self.editor_scrollbar = tk.Scrollbar(self.text_container)
        self.editor = tk.Text(
            self.text_container,
            wrap=tk.WORD,
            font=FONT_EDITOR,
            bg=EDITOR_BG,
            fg=TEXT_PRIMARY,
            insertbackground=ACCENT_CYAN,
            selectbackground="#26334d",
            selectforeground=TEXT_PRIMARY,
            undo=True,
            autoseparators=True,
            bd=0,
            padx=14,
            pady=10,
            yscrollcommand=self.editor_scrollbar.set
        )
        self.editor_scrollbar.config(command=self.editor.yview)
        self.editor_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bind editor typing
        self.editor.bind("<KeyRelease>", self.on_editor_modified)

        # ----------------------------------------------------------------------
        # BOTTOM STATUS BAR
        # ----------------------------------------------------------------------
        self.status_bar = tk.Frame(self.root, bg=CONSOLE_FRAME, height=26, padx=14, pady=4)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_counts = tk.Label(
            self.status_bar,
            text="Words: 0 | Characters: 0 | Lines: 0",
            font=FONT_STATS,
            bg=CONSOLE_FRAME,
            fg=TEXT_MUTED
        )
        self.status_counts.pack(side=tk.LEFT)

        self.status_speech = tk.Label(
            self.status_bar,
            text="🔊 Ship Audio: Idle",
            font=FONT_STATS,
            bg=CONSOLE_FRAME,
            fg=TEXT_MUTED
        )
        self.status_speech.pack(side=tk.LEFT, padx=30)

        self.status_save = tk.Label(
            self.status_bar,
            text="● Synchronized to Base",
            font=FONT_STATS,
            bg=CONSOLE_FRAME,
            fg=ACCENT_MINT
        )
        self.status_save.pack(side=tk.RIGHT)

    def create_header_btn(self, text, command, fg_color):
        btn = tk.Button(
            self.header_frame,
            text=text,
            command=command,
            bg=CONSOLE_FRAME,
            fg=fg_color,
            activebackground=CARD_ACTIVE,
            activeforeground=fg_color,
            relief=tk.FLAT,
            font=FONT_UI_BOLD,
            padx=10,
            pady=4,
            cursor="hand2",
            bd=0
        )
        btn.pack(side=tk.LEFT, padx=2)
        # Hover effect
        btn.bind("<Enter>", lambda e: btn.configure(bg=CARD_ACTIVE))
        btn.bind("<Leave>", lambda e: btn.configure(bg=CONSOLE_FRAME))
        return btn

    def bind_mousewheel(self, widget, inner):
        def _on_mousewheel(event):
            widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
        widget.bind("<MouseWheel>", _on_mousewheel)
        inner.bind("<MouseWheel>", _on_mousewheel)

    def bind_shortcuts(self):
        self.root.bind("<Control-n>", lambda e: self.create_new_note())
        self.root.bind("<Control-s>", lambda e: self.save_current_note())
        self.root.bind("<Control-f>", lambda e: self.search_entry.focus_set())
        self.root.bind("<Control-p>", lambda e: self.toggle_pin_current())
        self.root.bind("<Control-d>", lambda e: self.delete_current_note())
        self.root.bind("<Control-space>", lambda e: self.toggle_speech())

    # ==========================================================================
    # ☆ NOTE CATALOG & SEARCH MANAGEMENT
    # ==========================================================================
    def refresh_notes_list(self):
        self.notes.clear()
        if not os.path.exists(self.notes_dir):
            return

        for filename in os.listdir(self.notes_dir):
            if filename.startswith(".") or not (filename.endswith(".md") or filename.endswith(".txt")):
                continue
            full_path = os.path.join(self.notes_dir, filename)
            if os.path.isfile(full_path):
                title, preview = self.extract_title_and_preview(full_path)
                mtime = os.path.getmtime(full_path)
                pinned = filename in self.metadata.get("pinned", [])
                self.notes.append({
                    "path": full_path,
                    "filename": filename,
                    "title": title,
                    "preview": preview,
                    "pinned": pinned,
                    "mtime": mtime
                })

        # Sort: pinned first, then by last modified descending
        self.notes.sort(key=lambda x: (not x["pinned"], -x["mtime"]))
        self.render_catalog_cards()

    def extract_title_and_preview(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            if not lines:
                return os.path.splitext(os.path.basename(path))[0], "No transmission content."
            
            first_line = lines[0].lstrip("#*-> ").strip()
            title = first_line if first_line else os.path.splitext(os.path.basename(path))[0]
            preview = lines[1].lstrip("#*-> ").strip() if len(lines) > 1 else ""
            if len(preview) > 60:
                preview = preview[:57] + "..."
            return title, preview or "Empty transmission..."
        except Exception:
            return os.path.splitext(os.path.basename(path))[0], "Unable to read note."

    def switch_tab(self, tab):
        self.active_tab = tab
        if tab == "all":
            self.tab_all_btn.configure(bg=CARD_ACTIVE, fg=ACCENT_CYAN)
            self.tab_pinned_btn.configure(bg=CARD_BG, fg=TEXT_MUTED)
        else:
            self.tab_pinned_btn.configure(bg=CARD_ACTIVE, fg=ACCENT_GOLD)
            self.tab_all_btn.configure(bg=CARD_BG, fg=TEXT_MUTED)
        self.filter_notes()

    def filter_notes(self):
        query = self.search_var.get().lower().strip()
        filtered = []
        for n in self.notes:
            if self.active_tab == "pinned" and not n["pinned"]:
                continue
            if query and query not in n["title"].lower() and query not in n["preview"].lower():
                continue
            filtered.append(n)
        self.render_catalog_cards(filtered)

    def render_catalog_cards(self, notes_to_show=None):
        for widget in self.notes_inner_frame.winfo_children():
            widget.destroy()

        display_notes = self.notes if notes_to_show is None else notes_to_show

        if not display_notes:
            empty_msg = tk.Label(
                self.notes_inner_frame,
                text="No transmissions found.\nClick '➕ New Note' to begin.",
                font=FONT_SMALL,
                bg=SIDEBAR_BG,
                fg=TEXT_MUTED,
                pady=40
            )
            empty_msg.pack(fill=tk.X)
            return

        for note in display_notes:
            is_active = (self.current_note_path == note["path"])
            card_bg = CARD_ACTIVE if is_active else CARD_BG

            card = tk.Frame(
                self.notes_inner_frame,
                bg=card_bg,
                highlightbackground=BORDER_ACTIVE if is_active else BORDER_COLOR,
                highlightthickness=1,
                cursor="hand2"
            )
            card.pack(fill=tk.X, pady=3, padx=2)

            # Top row: title + star
            top_row = tk.Frame(card, bg=card_bg)
            top_row.pack(fill=tk.X, padx=10, pady=(8, 2))

            star_text = "⭐ " if note["pinned"] else ""
            title_lbl = tk.Label(
                top_row,
                text=f"{star_text}{note['title']}",
                font=FONT_UI_BOLD,
                bg=card_bg,
                fg=ACCENT_GOLD if note["pinned"] else TEXT_PRIMARY,
                anchor="w"
            )
            title_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Preview snippet
            preview_lbl = tk.Label(
                card,
                text=note["preview"],
                font=FONT_SMALL,
                bg=card_bg,
                fg=TEXT_MUTED,
                anchor="w"
            )
            preview_lbl.pack(fill=tk.X, padx=10, pady=(0, 4))

            # Timestamp row
            mtime_dt = datetime.fromtimestamp(note["mtime"])
            date_str = mtime_dt.strftime("%b %d, %H:%M")
            date_lbl = tk.Label(
                card,
                text=date_str,
                font=("Consolas", 8),
                bg=card_bg,
                fg=TEXT_DIM,
                anchor="w"
            )
            date_lbl.pack(fill=tk.X, padx=10, pady=(0, 8))

            # Bind clicks
            for w in (card, top_row, title_lbl, preview_lbl, date_lbl):
                w.bind("<Button-1>", lambda e, p=note["path"]: self.select_note(p))
                w.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def select_note(self, path):
        if self.is_dirty:
            self.save_current_note()
        self.stop_speech()
        self.load_note(path)
        self.render_catalog_cards()

    # ==========================================================================
    # ☆ NOTE CONTENT & FILE OPERATIONS
    # ==========================================================================
    def load_note(self, path, is_external=False):
        try:
            self.is_loading = True
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            self.current_note_path = path
            self.is_external_file = is_external

            filename = os.path.basename(path)
            is_pinned = filename in self.metadata.get("pinned", [])

            # Extract title
            title, _ = self.extract_title_and_preview(path)
            self.title_var.set(title)
            self.pin_indicator.config(text="⭐" if is_pinned else "")

            # Set editor content without triggering dirty flag
            self.editor.delete("1.0", tk.END)
            self.editor.insert(tk.END, content)
            self.editor.edit_modified(False)
            self.is_dirty = False

            # Update window title and status
            note_name = os.path.basename(path)
            self.root.title(f"⭐ StellarNotes - [{note_name}]")
            self.update_stats()
            self.status_save.config(text="● Synchronized to Base", fg=ACCENT_MINT)
            self.render_catalog_cards()

        except Exception as e:
            messagebox.showerror("Transmission Error", f"Could not load note from disk: {e}")
        finally:
            self.is_loading = False

    def create_new_note(self, initial=False):
        if self.is_dirty:
            self.save_current_note()
        self.stop_speech()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"Note_{timestamp}.md"
        full_path = os.path.join(self.notes_dir, base_name)

        default_content = f"# New Transmission\n\nRecorded on {datetime.now().strftime('%B %d, %Y at %H:%M')}\n\n"
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(default_content)

            self.refresh_notes_list()
            self.load_note(full_path)
            self.title_entry.focus_set()
            self.title_entry.select_range(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create new note: {e}")

    def save_current_note(self):
        if not self.current_note_path:
            return

        try:
            content = self.editor.get("1.0", "end-1c")
            with open(self.current_note_path, "w", encoding="utf-8") as f:
                f.write(content)

            self.is_dirty = False
            self.status_save.config(text=f"● Saved at {time.strftime('%H:%M:%S')}", fg=ACCENT_MINT)
            self.refresh_notes_list()
        except Exception as e:
            self.status_save.config(text="○ Transmission Failed", fg=ACCENT_CORAL)
            messagebox.showerror("Write Failure", f"Failed to save transmission to disk: {e}")

    def schedule_autosave(self):
        if self.autosave_timer is not None:
            self.root.after_cancel(self.autosave_timer)
        self.autosave_timer = self.root.after(600, self.save_current_note)

    def on_editor_modified(self, event=None):
        if getattr(self, "is_loading", False):
            return
        if self.editor.edit_modified():
            self.is_dirty = True
            self.status_save.config(text="○ Unsaved Changes", fg=ACCENT_GOLD)
            self.schedule_autosave()
            self.schedule_stats_update()
            self.editor.edit_modified(False)

    def on_title_modified(self, *args):
        if getattr(self, "is_loading", False):
            return
        self.is_dirty = True
        self.status_save.config(text="○ Unsaved Changes", fg=ACCENT_GOLD)
        self.schedule_autosave()

    def toggle_pin_current(self):
        if not self.current_note_path:
            return
        filename = os.path.basename(self.current_note_path)
        pinned_list = self.metadata.setdefault("pinned", [])

        if filename in pinned_list:
            pinned_list.remove(filename)
            self.pin_indicator.config(text="")
        else:
            pinned_list.append(filename)
            self.pin_indicator.config(text="⭐")

        self.save_metadata()
        self.refresh_notes_list()

    def open_external_file(self):
        file_path = filedialog.askopenfilename(
            title="Open Transmission Document",
            filetypes=[("Text & Markdown", "*.md;*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.load_note(file_path, is_external=True)

    def export_current_note(self):
        if not self.current_note_path:
            return
        initial_name = os.path.basename(self.current_note_path)
        dest_path = filedialog.asksaveasfilename(
            title="Export Transmission",
            initialfile=initial_name,
            defaultextension=".md",
            filetypes=[("Markdown Document", "*.md"), ("Plain Text", "*.txt"), ("All Files", "*.*")]
        )
        if dest_path:
            try:
                content = self.editor.get("1.0", "end-1c")
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Export Success", f"Transmission exported successfully to:\n{dest_path}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"Could not export transmission: {e}")

    def delete_current_note(self):
        if not self.current_note_path:
            return

        note_title = self.title_var.get() or os.path.basename(self.current_note_path)
        confirm = messagebox.askyesno(
            "Purge Transmission",
            f"Are you sure you want to permanently purge '{note_title}' from the stars?",
            icon="warning"
        )
        if not confirm:
            return

        self.stop_speech()
        try:
            if os.path.exists(self.current_note_path):
                os.remove(self.current_note_path)

            filename = os.path.basename(self.current_note_path)
            pinned_list = self.metadata.get("pinned", [])
            if filename in pinned_list:
                pinned_list.remove(filename)
                self.save_metadata()

            self.refresh_notes_list()
            if self.notes:
                self.load_note(self.notes[0]["path"])
            else:
                self.create_new_note(initial=True)

        except Exception as e:
            messagebox.showerror("Purge Failed", f"Could not delete note: {e}")

    # ==========================================================================
    # ☆ VOICE NARRATION ("TALKING NOTE") ENGINE
    # ==========================================================================
    def toggle_speech(self):
        if self.is_speaking:
            self.stop_speech()
        else:
            self.start_speech()

    def start_speech(self):
        text_to_speak = self.editor.get("1.0", "end-1c").strip()
        if not text_to_speak:
            self.status_speech.config(text="🔊 Nothing to narrate.", fg=TEXT_MUTED)
            return

        # Prepare temporary file for zero-escaping transmission to SAPI
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as tf:
                tf.write(text_to_speak)
                self.speech_temp_path = tf.name
        except Exception as e:
            messagebox.showerror("Audio Error", f"Could not prepare audio buffer: {e}")
            return

        # Spawn background synthesis thread
        self.is_speaking = True
        self.btn_speech.config(text="⏹ Stop Audio", fg=ACCENT_CORAL)
        self.status_speech.config(text="🔊 Ship Audio: Narrating...", fg=ACCENT_MINT)

        speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        speech_thread.start()

    def _speech_worker(self):
        cmd = [
            "powershell",
            "-NoProfile",
            "-WindowStyle", "Hidden",
            "-Command",
            f"$txt = [System.IO.File]::ReadAllText('{self.speech_temp_path}'); "
            "Add-Type -AssemblyName System.Speech; "
            "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            "$synth.Speak($txt)"
        ]

        try:
            self.speech_process = subprocess.Popen(cmd)
            self.speech_process.wait()
        except Exception:
            pass
        finally:
            self.root.after(0, self._speech_finished)

    def _speech_finished(self):
        self.is_speaking = False
        self.btn_speech.config(text="🔊 Read Aloud", fg=ACCENT_MINT)
        self.status_speech.config(text="🔊 Ship Audio: Idle", fg=TEXT_MUTED)
        self.cleanup_temp_speech_file()

    def stop_speech(self):
        if self.speech_process:
            try:
                self.speech_process.terminate()
            except Exception:
                pass
            self.speech_process = None
        self._speech_finished()

    def cleanup_temp_speech_file(self):
        if self.speech_temp_path and os.path.exists(self.speech_temp_path):
            try:
                os.remove(self.speech_temp_path)
            except Exception:
                pass
            self.speech_temp_path = None

    # ==========================================================================
    # ☆ STATS & LIFECYCLE
    # ==========================================================================
    def schedule_stats_update(self):
        if self.stats_timer is not None:
            self.root.after_cancel(self.stats_timer)
        self.stats_timer = self.root.after(300, self.update_stats)

    def update_stats(self):
        content = self.editor.get("1.0", "end-1c")
        chars = len(content)
        words = len(content.split())
        lines = content.count("\n") + 1 if content else 0
        self.status_counts.config(text=f"Words: {words} | Characters: {chars} | Lines: {lines}")

    def on_window_close(self):
        self.stop_speech()
        if self.is_dirty:
            self.save_current_note()
        self.root.destroy()


def main():
    root = tk.Tk()
    initial_file = None
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        initial_file = sys.argv[1]
    
    app = StellarNotesApp(root, initial_file=initial_file)
    root.mainloop()


if __name__ == "__main__":
    main()
