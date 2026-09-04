# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: live_md_editor.py
# ☆ Date: September 3, 2026
# ☆
# ☆ Description: A live split-screen Tkinter Markdown editor with command-line argument support for context menu launching.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import markdown
from tkhtmlview import HTMLLabel

# ☆ Global variables
update_job = None
current_file = None  # ☆ Tracks the currently open file path

# ☆ Console UI Theme (Dark & comfortable for writing)
CONSOLE_BG = "#0f131a"       # ☆ Deep slate for text editor and window trim
CONSOLE_FRAME = "#1a202c"    # ☆ Spaceship hull frame
STAR_WHITE = "#e2e8f0"       # ☆ Clear white for editor typing
ALIEN_MINT = "#7ee787"       # ☆ Soft alien mint accent for console buttons
SELECTION_VIOLET = "#2a3447" # ☆ Subtle slate highlight in editor

# ☆ Document Preview Theme (True-to-final output)
PREVIEW_BG = "#ffffff"       # ☆ Standard document canvas
PREVIEW_TEXT = "#1f2328"     # ☆ Authentic dark charcoal reading text

def schedule_update(event=None):
    global update_job
    if update_job is not None:
        root.after_cancel(update_job)
    update_job = root.after(300, update_preview)

def update_preview():
    text = editor.get("1.0", tk.END)
    html_content = markdown.markdown(
        text, 
        extensions=['extra', 'codehilite', 'nl2br', 'sane_lists']
    )
    
    # ☆ Wrap preview in standard document styling so custom colors render accurately
    document_html = f"""
    <body style="background-color: {PREVIEW_BG}; color: {PREVIEW_TEXT}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.6; padding: 18px;">
        {html_content}
    </body>
    """
    html_viewer.set_html(document_html)

def load_file_content(path):
    global current_file
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        current_file = path
        editor.delete("1.0", tk.END)
        editor.insert(tk.END, text)
        update_preview()
        root.title(f"🛸 Galactic Markdown Editor - {current_file}")
    except Exception as e:
        messagebox.showerror("File Error", f"Could not load file: {e}")

def open_file():
    file_path = filedialog.askopenfilename(
        title="Beam Up a Markdown File",
        filetypes=(("Markdown files", "*.md"), ("All files", "*.*"))
    )
    if file_path:
        load_file_content(file_path)

def save_file():
    global current_file
    
    if current_file is None:
        file_path = filedialog.asksaveasfilename(
            title="Transmit to Base (Save)",
            defaultextension=".md",
            filetypes=(("Markdown files", "*.md"), ("All files", "*.*"))
        )
        if not file_path:
            return
        current_file = file_path

    try:
        with open(current_file, 'w', encoding='utf-8') as f:
            text = editor.get("1.0", "end-1c")
            f.write(text)
        
        root.title(f"🛸 Galactic Markdown Editor - {current_file}")
    except Exception as e:
        messagebox.showerror("Transmission Failure", f"Could not beam data to drive: {e}")

# ☆ Initialize main window
root = tk.Tk()
root.title("🛸 Galactic Markdown Editor - [Uncharted Territory]")
root.geometry("1080x640")
root.configure(bg=CONSOLE_FRAME)

# ☆ Set cosmic window icon if available
app_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(app_dir, "assets", "galaxy_md.ico")
if not os.path.exists(icon_path):
    icon_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "assets", "galaxy_md.ico")
if os.path.exists(icon_path):
    try:
        root.iconbitmap(icon_path)
    except Exception:
        pass

# ☆ Top menu bar for spaceship controls
menu_frame = tk.Frame(root, bg=CONSOLE_FRAME)
menu_frame.pack(fill=tk.X, padx=10, pady=6)

open_btn = tk.Button(
    menu_frame, 
    text="🛸 Beam Up File", 
    command=open_file, 
    bg=CONSOLE_BG, 
    fg=ALIEN_MINT, 
    activebackground=CONSOLE_FRAME, 
    activeforeground=ALIEN_MINT,
    relief=tk.FLAT,
    font=("Consolas", 10),
    padx=10,
    pady=3
)
open_btn.pack(side=tk.LEFT, padx=(0, 8))

save_btn = tk.Button(
    menu_frame, 
    text="📡 Transmit to Base", 
    command=save_file, 
    bg=CONSOLE_BG, 
    fg=ALIEN_MINT, 
    activebackground=CONSOLE_FRAME, 
    activeforeground=ALIEN_MINT,
    relief=tk.FLAT,
    font=("Consolas", 10),
    padx=10,
    pady=3
)
save_btn.pack(side=tk.LEFT)

# ☆ Create the split-screen pane
paned_window = tk.PanedWindow(
    root, 
    orient=tk.HORIZONTAL, 
    sashrelief=tk.FLAT, 
    bg=CONSOLE_FRAME, 
    bd=0
)
paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

# ☆ Left Pane: Text Editor
editor = tk.Text(
    paned_window, 
    wrap=tk.WORD, 
    font=("Consolas", 12), 
    bg=CONSOLE_BG, 
    fg=STAR_WHITE,
    insertbackground=ALIEN_MINT,
    selectbackground=SELECTION_VIOLET,
    selectforeground=STAR_WHITE,
    bd=0,
    padx=14,
    pady=14
)
paned_window.add(editor, width=540)

# ☆ Right Pane: HTML Viewer
welcome_msg = f"""
<body style="background-color: {PREVIEW_BG}; color: {PREVIEW_TEXT}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; text-align: center; padding-top: 50px;">
    <h2 style="color: #24292f; font-weight: 600;">( 👽 ) Transmission Console Ready</h2>
    <p style="color: #57606a; font-size: 13px;">Type Markdown on the left console to preview the authentic final document.</p>
</body>
"""
html_viewer = HTMLLabel(paned_window, html=welcome_msg, background=PREVIEW_BG)
paned_window.add(html_viewer, width=540)

# ☆ Bind typing & keyboard shortcuts
editor.bind("<KeyRelease>", schedule_update)
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Command-s>", lambda event: save_file())

if __name__ == "__main__":
    # ☆ If a file path was passed via right-click / command-line, load it immediately
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        load_file_content(sys.argv[1])
        
    root.mainloop()