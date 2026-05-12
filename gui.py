import pystray
from PIL import Image
import threading
import time

from jarvis_old_backup import listen_once, speak, set_live_text_callback

import tkinter as tk
from tkinter import scrolledtext
import threading
# ========================
# DARK THEME COLORS
# ========================
BG_COLOR = "#121212"
FG_COLOR = "#EAEAEA"
ACCENT_COLOR = "#1DB954"   # green (AI-style)
BTN_COLOR = "#1F1F1F"
CHAT_BG = "#181818"

# Global state
thinking = False

# -----------------------
# GUI WINDOW
# -----------------------
root = tk.Tk()
root.attributes("-topmost", True) 
root.attributes("-toolwindow", True)
  # Always on top
root.overrideredirect(False)        # Keep window frame (safe for now)
root.title("Jarvis Assistant")
root.geometry("320x420")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

# Forward declarations for functions used in button commands
def hide_window():
    root.withdraw()

def show_window(icon=None, item=None):
    root.after(0, root.deiconify)

top_bar = tk.Frame(root, bg=BG_COLOR)
top_bar.pack(fill="x")

btn_min = tk.Button(
    top_bar, text="—", bg=BG_COLOR, fg=FG_COLOR,
    relief=tk.FLAT, command=hide_window
)
btn_min.pack(side="right", padx=5)

btn_close = tk.Button(
    top_bar, text="✖", bg=BG_COLOR, fg="red",
    relief=tk.FLAT, command=hide_window
)
btn_close.pack(side="right")


# -----------------------
# STATUS
# -----------------------
status_label = tk.Label(
    root,
    text="🟢 Idle",
    font=("Segoe UI", 12, "bold"),
    bg=BG_COLOR,
    fg=ACCENT_COLOR
)

status_label.pack(pady=5)
live_text_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 10),
    bg=BG_COLOR,
    fg=FG_COLOR,
    wraplength=280,
    justify="left"
)
live_text_label.pack(pady=5)
thinking_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 10, "italic"),
    bg=BG_COLOR,
    fg="#AAAAAA"
)
thinking_label.pack(pady=2)

# -----------------------
# CHAT BOX
# -----------------------
chat_box = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Segoe UI", 10),
    bg=CHAT_BG,
    fg=FG_COLOR,
    insertbackground=FG_COLOR,
    relief=tk.FLAT
)


def add_message(msg):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, msg + "\n")
    chat_box.see(tk.END)
    chat_box.config(state=tk.DISABLED)

add_message("🤖 Jarvis ready")

# -----------------------
# BUTTON ACTIONS
def update_live_text(text, final=False):
    global thinking

    if final:
        thinking = False
        thinking_label.config(text="")
        add_message(f"🧑 You: {text}")
        live_text_label.config(text="")
    else:
        live_text_label.config(text=f"🎙 {text}")

    if final:
        add_message(f"🧑 You: {text}")
        live_text_label.config(text="")
    else:
        live_text_label.config(text=f"🎙 {text}")
        set_live_text_callback(update_live_text)
# thinking = False

def thinking_animation():
    dots = ""
    while thinking:
        for dots in [".", "..", "..."]:
            if not thinking:
                break
            thinking_label.config(text=f"🧠 Jarvis is thinking{dots}")
            time.sleep(0.5)
    thinking_label.config(text="")
#-----------------------
def start_listening():
    global thinking

    status_label.config(text="🎙 Listening...")
    live_text_label.config(text="🎙 Listening...")

    listen_once()

    thinking = True
    threading.Thread(target=thinking_animation, daemon=True).start()

    status_label.config(text="🟢 Idle")


def fake_response():
   def start_listening():
    status_label.config(text="🎙 Listening...")
    add_message("🧑 You: (listening...)")

    listen_once()  # REAL JARVIS
    status_label.config(text="🟢 Idle")

def jarvis_reply():
    status_label.config(text="🟢 Idle")
    add_message("🤖 Jarvis: Hello! How can I help you?")

# -----------------------
# BUTTONS
# -----------------------
mic_btn = tk.Button(
    root,
    text="🎤 Speak",
    font=("Segoe UI", 12, "bold"),
    width=15,
    bg=BTN_COLOR,
    fg=FG_COLOR,
    activebackground=ACCENT_COLOR,
    activeforeground="black",
    relief=tk.FLAT,
    command=lambda: threading.Thread(target=start_listening).start()
)
mic_btn.pack(pady=12)

mic_btn.pack(pady=10)
# -----------------------
# DRAG WINDOW
# -----------------------
def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = root.winfo_x() + event.x - root.x
    y = root.winfo_y() + event.y - root.y
    root.geometry(f"+{x}+{y}")

root.bind("<Button-1>", start_move)
root.bind("<B1-Motion>", do_move)
# ========================
# SYSTEM TRAY
# ========================
def quit_app(icon, item):
    icon.stop()
    root.after(0, root.destroy)

def setup_tray():
    image = Image.open("jarvis.ico")
    menu = pystray.Menu(
        pystray.MenuItem("Open Jarvis", show_window),
        pystray.MenuItem("Exit", quit_app)
    )
    icon = pystray.Icon("Jarvis", image, "Jarvis Assistant", menu)
    icon.run()
threading.Thread(target=setup_tray, daemon=True).start()

root.mainloop()
