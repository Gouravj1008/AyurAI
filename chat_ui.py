from voice_input import listen_live

from ai_brain import ask_ai
import threading

import tkinter as tk
from tkinter import scrolledtext

# ========================
# THEME
# ========================
BG = "#0f172a"
USER_BG = "#2563eb"
BOT_BG = "#1e293b"
TEXT = "#e5e7eb"

root = tk.Tk()
root.title("Jarvis AI")
root.geometry("420x600")
root.configure(bg=BG)

# ========================
# CHAT AREA
# ========================
chat = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 11),
    relief=tk.FLAT
)
chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
chat.config(state=tk.DISABLED)

# ========================
# INPUT AREA
# ========================
input_frame = tk.Frame(root, bg=BG)
input_frame.pack(fill=tk.X, padx=10, pady=10)

entry = tk.Entry(
    input_frame,
    font=("Segoe UI", 12),
    bg="#020617",
    fg=TEXT,
    insertbackground=TEXT
)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

def send_message():
    user_text = clean_text(entry.get())

    if not user_text:
        return
    entry.delete(0, tk.END)
    add_message("🧑 You", user_text)
    thinking()
    threading.Thread(
        target=bot_reply,
        args=(user_text,),
        daemon=True
    ).start()

send_btn = tk.Button(
    input_frame,
    text="Send",
    bg=USER_BG,
    fg="white",
    relief=tk.FLAT,
    command=send_message
)
send_btn.pack(side=tk.RIGHT, padx=(5, 0))
def use_mic():
    add_message("🎙", "Listening...")
    # Use live listening to capture speech and update entry
    def update_live_text(text):
        entry.delete(0, tk.END)
        entry.insert(0, text)

    def run():
        final_text = listen_live(update_live_text)
        if final_text:
            entry.delete(0, tk.END)
            entry.insert(0, final_text)
            send_message()
        else:
            add_message("🤖 Jarvis", "I didn't catch that.")

    threading.Thread(target=run, daemon=True).start()

mic_btn = tk.Button(
    input_frame,
    text="🎤",
    font=("Segoe UI", 12),
    bg="#334155",
    fg="white",
    relief=tk.FLAT,
    command=use_mic
)
mic_btn.pack(side=tk.RIGHT, padx=(0, 5))
def use_mic_live():
    entry.delete(0, tk.END)

    def update_live_text(text):
        entry.delete(0, tk.END)
        entry.insert(0, text)

    def run():
        add_message("🎙", "Listening...")
        final_text = listen_live(update_live_text)
        if final_text:
            entry.delete(0, tk.END)
            entry.insert(0, final_text)
            send_message()
        else:
            add_message("🤖 Jarvis", "I didn't catch that.")

    threading.Thread(target=run, daemon=True).start()


# ========================
# MESSAGE HELPERS
# ========================
def add_message(sender, msg):
    chat.config(state=tk.NORMAL)
    chat.insert(tk.END, f"\n{sender}: {msg}\n")
    chat.see(tk.END)
    chat.config(state=tk.DISABLED)
def thinking():
    add_message("🤖 Jarvis", "Thinking...")

def bot_reply(text):
    try:
        answer = ask_ai(text)
        stream_text("🤖 Jarvis", answer)

    except Exception as e:
        add_message("🤖 Jarvis", f"❌ Error: {e}")
        print("AI ERROR:", e)


add_message("🤖 Jarvis", "Hello! I am your AI assistant.")
def stream_text(sender, text, delay=25):
    chat.config(state=tk.NORMAL)
    chat.insert(tk.END, f"\n{sender}: ")
    chat.see(tk.END)

    for word in text.split():
        chat.insert(tk.END, word + " ")
        chat.see(tk.END)
        chat.update()
        root.after(delay)

    chat.insert(tk.END, "\n")
    chat.config(state=tk.DISABLED)
import re

def clean_text(text):
    text = text.strip()
    if not text:
        return text

    text = text[0].upper() + text[1:]
    if text[-1] not in ".?!":
        text += "."

    text = re.sub(r"\bi\b", "I", text)
    return text


root.mainloop()
