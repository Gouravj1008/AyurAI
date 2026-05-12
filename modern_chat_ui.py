"""
Modern ChatGPT-Style Ayurvedic Chatbot UI
Pink Ayurveda theme with smooth animations
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import time
import json
import os
from datetime import datetime
from typing import Optional

import config
from ai_brain_ayurveda import AyurvedicBrain
from error_handler import ErrorHandler, HealthCheck
from voice_input_improved import VoskSTTEngine
from hotword_secure import HotwordDetector
from auth_ui import AuthUI
from auth_manager import AuthManager
import logging

logger = logging.getLogger(__name__)

class LoadingAnimation:
    """Ayurveda-inspired loading animation"""
    
    FRAMES = [
        "🌿 .",
        "🌿 ..",
        "🌿 ...",
        "🌿 ⚡",
        "🌿 ✨",
    ]
    
    FRAMES = [
        "Jarvis is reading your pulse .",
        "Jarvis is reading your pulse ..",
        "Jarvis is reading your pulse ...",
        "Balancing dosha signals .",
        "Preparing Ayurveda guidance ..",
    ]

    def __init__(self, label):
        self.label = label
        self.current_frame = 0
        self.is_running = False
    
    def start(self):
        """Start animation"""
        self.is_running = True
        self._animate()
    
    def _animate(self):
        """Animate frames"""
        if self.is_running:
            self.label.config(text=self.FRAMES[self.current_frame % len(self.FRAMES)])
            self.current_frame += 1
            self.label.after(200, self._animate)
    
    def stop(self):
        """Stop animation"""
        self.is_running = False

class ModernChatbot(AuthUI):
    """Modern ChatGPT-style Ayurvedic Chatbot"""
    
    def __init__(self):
        # Initialize auth first
        super().__init__()
        
        # Color scheme - modern Ayurveda AI theme
        self.bg_dark = "#07130f"
        self.bg_panel = "#10231b"
        self.bg_input = "#183329"
        self.accent_pink = "#38A169"
        self.accent_light_pink = "#9AE6B4"
        self.accent_gold = "#D4AF37"
        self.accent_saffron = "#E9A13B"
        self.text_light = "#F3F7F0"
        self.text_muted = "#A7B8A5"
        
        # State
        self.ai_brain = None
        self.stt_engine = None
        self.hotword_detector = None
        self.is_listening = False
        self.current_user = None
        self.auth_manager = AuthManager()
    
    def on_auth_success(self, username: str):
        """Called after successful authentication"""
        self.current_user = username
        self.initialize_ai()
    
    def initialize_ai(self):
        """Initialize AI components"""
        try:
            self.ai_brain = AyurvedicBrain()
            saved_user = self.auth_manager.get_user(self.current_user) or {}
            saved_dosha = saved_user.get("dosha")
            if saved_dosha:
                self.ai_brain.user_dosha = saved_dosha
            logger.info("✅ AI brain initialized")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize AI: {e}")
            return
        
        try:
            self.stt_engine = VoskSTTEngine()
            logger.info("✅ Speech-to-text engine ready")
        except:
            self.stt_engine = None
            logger.warning("⚠️ Speech-to-text not available")
        
        try:
            self.hotword_detector = HotwordDetector()
            logger.info("✅ Hotword detector ready")
        except:
            self.hotword_detector = None
            logger.warning("⚠️ Hotword detection not available")
        
        # Show chat interface
        self.show_chat_interface()
    
    def show_chat_interface(self):
        """Show modern ChatGPT-style chat interface"""
        self.clear_window()
        self.geometry("1000x800")
        self.title("🌿 Jarvis - Ayurvedic Health Assistant")
        
        # Main layout
        main_frame = tk.Frame(self, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(main_frame, bg=self.accent_pink, height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg=self.accent_pink)
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Logo + Title
        logo_title = tk.Frame(header_content, bg=self.accent_pink)
        logo_title.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            logo_title,
            text="🌿 Jarvis",
            font=("Segoe UI", 24, "bold"),
            bg=self.accent_pink,
            fg="white"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(
            logo_title,
            text="Ayurvedic Health Companion",
            font=("Segoe UI", 11),
            bg=self.accent_pink,
            fg="white"
        ).pack(side=tk.LEFT)
        
        # User info + Logout
        user_frame = tk.Frame(header_content, bg=self.accent_pink)
        user_frame.pack(side=tk.RIGHT)
        
        user_name = self.auth_manager.get_user_full_name(self.current_user)
        tk.Label(
            user_frame,
            text=f"👤 {user_name}",
            font=("Segoe UI", 10),
            bg=self.accent_pink,
            fg="white"
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        logout_btn = tk.Button(
            user_frame,
            text="Logout",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg=self.accent_pink,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.logout
        )
        logout_btn.pack(side=tk.LEFT)
        
        # Content area
        content_frame = tk.Frame(main_frame, bg=self.bg_dark)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Chat area
        chat_frame = tk.Frame(content_frame, bg=self.bg_dark)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            height=25,
            bg=self.bg_panel,
            fg=self.text_light,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=15,
            insertbackground=self.accent_pink
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure text tags
        self.chat_display.tag_config("user", foreground=self.accent_pink, font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("assistant", foreground=self.accent_light_pink, font=("Segoe UI", 11))
        self.chat_display.tag_config("system", foreground=self.accent_gold, font=("Segoe UI", 10, "italic"))
        self.chat_display.tag_config("error", foreground="#FF6B6B", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("timestamp", foreground=self.text_muted, font=("Segoe UI", 9))
        
        # Welcome message
        self._add_message("SYSTEM", "Welcome to Jarvis! 🌿\n\nI'm your Ayurvedic health companion. Ask me anything about:\n• Dosha detection (Vata, Pitta, Kapha)\n• Personalized diet recommendations\n• Wellness and treatment plans\n• Ayurvedic remedies\n\nClick the buttons below to explore features or start chatting!", system=True)
        
        # Feature shortcuts
        shortcut_frame = tk.Frame(content_frame, bg=self.bg_dark)
        shortcut_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        shortcuts = [
            ("Dosha Info", self.show_dosha_info),
            ("Diet Check", self.show_diet_checker),
            ("Doctor Guide", self.show_doctor_recommendation),
            ("Detect Dosha", self.show_dosha_detection),
        ]
        for label, command in shortcuts:
            btn = tk.Button(
                shortcut_frame,
                text=label,
                font=("Segoe UI", 10, "bold"),
                bg=self.bg_input,
                fg=self.accent_light_pink,
                activebackground=self.accent_gold,
                activeforeground="#07130f",
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                padx=14,
                pady=8,
                command=command
            )
            btn.pack(side=tk.LEFT, padx=(0, 8))

        # Input area
        input_frame = tk.Frame(content_frame, bg=self.bg_dark)
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Message input
        input_label = tk.Label(
            input_frame,
            text="Your message:",
            font=("Segoe UI", 10),
            bg=self.bg_dark,
            fg=self.accent_light_pink
        )
        input_label.pack(anchor=tk.W, pady=(0, 8))
        
        input_container = tk.Frame(input_frame, bg=self.bg_input, relief=tk.FLAT, bd=1, highlightthickness=1, highlightbackground=self.accent_pink)
        input_container.pack(fill=tk.X)
        
        self.input_field = tk.Text(
            input_container,
            height=3,
            bg=self.bg_input,
            fg=self.text_light,
            font=("Segoe UI", 11),
            insertbackground=self.accent_pink,
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=12
        )
        self.input_field.pack(fill=tk.BOTH, expand=True)
        self.input_field.bind("<Control-Return>", lambda e: self._on_send())
        self.input_field.bind("<Return>", self._on_enter_send)
        self.input_field.bind("<Shift-Return>", lambda e: None)
        
        # Buttons frame
        button_frame = tk.Frame(input_frame, bg=self.bg_dark)
        button_frame.pack(fill=tk.X, pady=(12, 0), anchor=tk.E)
        
        # Send button
        send_btn = tk.Button(
            button_frame,
            text="📤 Send",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_pink,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=20,
            pady=8,
            command=self._on_send
        )
        send_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Voice button (if available)
        if self.stt_engine:
            voice_btn = tk.Button(
                button_frame,
                text="🎤 Voice",
                font=("Segoe UI", 10, "bold"),
                bg=self.accent_light_pink,
                fg="white",
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                padx=20,
                pady=8,
                command=self._on_voice
            )
            voice_btn.pack(side=tk.RIGHT, padx=5)
            self.voice_btn = voice_btn
        
        # Dosha detection button
        dosha_btn = tk.Button(
            button_frame,
            text="🔍 Detect Dosha",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_gold,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.show_dosha_detection
        )
        dosha_btn.pack(side=tk.RIGHT, padx=5)
        
        # Settings button
        settings_btn = tk.Button(
            button_frame,
            text="⚙️ Settings",
            font=("Segoe UI", 10, "bold"),
            bg=self.text_muted,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.show_settings
        )
        settings_btn.pack(side=tk.RIGHT, padx=5)
    
    def _add_message(self, role: str, message: str, system: bool = False):
        """Add message to chat"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M")
        
        if role == "USER":
            prefix = "You"
            tag = "user"
        elif role == "ASSISTANT":
            prefix = "🧘 Jarvis"
            tag = "assistant"
        elif role == "SYSTEM":
            prefix = "ℹ️ System"
            tag = "system"
        elif role == "ERROR":
            prefix = "Error"
            tag = "error"
        else:
            prefix = role
            tag = "assistant"
        
        # Add message with timestamp
        self.chat_display.insert(tk.END, f"{prefix} ", tag)
        self.chat_display.insert(tk.END, f"[{timestamp}]\n", "timestamp")
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def _on_enter_send(self, event):
        """Send on Enter; keep Shift+Enter for multi-line messages."""
        if event.state & 0x0001:
            return None
        self._on_send()
        return "break"
    
    def _on_send(self):
        """Handle send message"""
        message = self.input_field.get("1.0", tk.END).strip()
        if not message:
            return
        
        self._add_message("USER", message)
        self.input_field.delete("1.0", tk.END)
        
        # Show loading animation
        loading_frame = tk.Frame(self.chat_display, bg=self.bg_panel)
        loading_label = tk.Label(
            loading_frame,
            text="",
            bg=self.bg_panel,
            fg=self.accent_gold,
            font=("Segoe UI", 10, "italic"),
            padx=12,
            pady=8
        )
        loading_label.pack(anchor=tk.W)
        loading_animation = LoadingAnimation(loading_label)
        loading_animation.start()
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.window_create(tk.END, window=loading_frame)
        self.chat_display.insert(tk.END, "\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Get response in thread
        threading.Thread(target=self._get_response, args=(message, loading_frame, loading_animation), daemon=True).start()
    
    def _get_response(self, message: str, loading_frame=None, loading_animation=None):
        """Get AI response"""
        try:
            context = ""
            if self.ai_brain.user_dosha:
                context = f"User dosha: {self.ai_brain.user_dosha}. Give personalized Ayurveda guidance and include doctor-safety notes when needed."
            response = self.ai_brain.ask_with_context(message, context)
            self.after(0, lambda: self._finish_response_loading(loading_frame, loading_animation))
            self.after(0, lambda: self._add_message("ASSISTANT", response))
        except Exception as e:
            error_msg = ErrorHandler.handle_exception(e, "AI response")
            self.after(0, lambda: self._finish_response_loading(loading_frame, loading_animation))
            self.after(0, lambda: self._add_message("ERROR", error_msg))

    def _finish_response_loading(self, loading_frame=None, loading_animation=None):
        """Stop and remove response loading animation."""
        if loading_animation:
            loading_animation.stop()
        if loading_frame:
            try:
                loading_frame.destroy()
            except Exception:
                pass
    
    def _on_voice(self):
        """Handle voice input"""
        if self.is_listening:
            messagebox.showinfo("Info", "Already listening...")
            return
        
        self.is_listening = True
        self.voice_btn.config(state=tk.DISABLED, bg="#FF6B6B")
        threading.Thread(target=self._listen_voice, daemon=True).start()
    
    def _listen_voice(self):
        """Listen for voice"""
        try:
            text = self.stt_engine.listen(timeout_seconds=30)
            if text:
                self.after(0, lambda: self._add_message("USER", f"[Voice] {text}"))
                self.after(0, lambda: self._get_response(text, None))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.is_listening = False
            self.after(0, lambda: self.voice_btn.config(state=tk.NORMAL, bg=self.accent_light_pink))

    def _current_dosha(self) -> Optional[str]:
        """Return the active user's saved or detected dosha."""
        if self.ai_brain and self.ai_brain.user_dosha:
            return self.ai_brain.user_dosha
        user = self.auth_manager.get_user(self.current_user) or {}
        return user.get("dosha")

    def _show_text_dialog(self, title: str, body: str, width: int = 680, height: int = 520):
        """Show a themed read-only text dialog."""
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry(f"{width}x{height}")
        dialog.configure(bg=self.bg_dark)

        display = scrolledtext.ScrolledText(
            dialog,
            bg=self.bg_panel,
            fg=self.text_light,
            font=("Segoe UI", 10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=0,
            padx=16,
            pady=16,
            insertbackground=self.accent_pink
        )
        display.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)
        display.insert(tk.END, body)
        display.config(state=tk.DISABLED)

    def show_dosha_info(self):
        """Show information about all doshas and the user's current dosha."""
        active = self._current_dosha()
        sections = []
        if active:
            sections.append(f"Your saved dosha: {active.title()}\n")
        else:
            sections.append("No saved dosha yet. Use Detect Dosha for a personalized profile.\n")
        for dosha in ("vata", "pitta", "kapha"):
            sections.append(self.ai_brain.get_dosha_info(dosha))
        self._show_text_dialog("Dosha Information", "\n".join(sections))

    def show_diet_checker(self):
        """Let the user check a meal or daily diet against their dosha."""
        dialog = tk.Toplevel(self)
        dialog.title("Diet Check")
        dialog.geometry("620x520")
        dialog.configure(bg=self.bg_dark)

        dosha = self._current_dosha()
        tk.Label(
            dialog,
            text=f"Checking for: {dosha.title() if dosha else 'No dosha selected'}",
            font=("Segoe UI", 13, "bold"),
            bg=self.bg_dark,
            fg=self.accent_gold
        ).pack(anchor=tk.W, padx=16, pady=(16, 8))

        tk.Label(
            dialog,
            text="Enter what you ate today or a planned meal:",
            font=("Segoe UI", 10),
            bg=self.bg_dark,
            fg=self.text_light
        ).pack(anchor=tk.W, padx=16)

        diet_box = tk.Text(
            dialog,
            height=10,
            bg=self.bg_panel,
            fg=self.text_light,
            font=("Segoe UI", 10),
            insertbackground=self.accent_pink,
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=12
        )
        diet_box.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)

        def check():
            diet_text = diet_box.get("1.0", tk.END).strip()
            if not diet_text:
                messagebox.showwarning("Diet Check", "Please enter your meal or daily diet.")
                return
            result = self.ai_brain.check_diet_for_dosha(dosha, diet_text)
            self._add_message("SYSTEM", result, system=True)
            dialog.destroy()

        tk.Button(
            dialog,
            text="Check Diet",
            font=("Segoe UI", 11, "bold"),
            bg=self.accent_pink,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=check
        ).pack(fill=tk.X, padx=16, pady=(0, 16), ipady=10)

    def show_doctor_recommendation(self):
        """Collect symptoms and show safe doctor recommendation guidance."""
        dialog = tk.Toplevel(self)
        dialog.title("Doctor Recommendation")
        dialog.geometry("620x500")
        dialog.configure(bg=self.bg_dark)

        tk.Label(
            dialog,
            text="Describe symptoms or concerns:",
            font=("Segoe UI", 12, "bold"),
            bg=self.bg_dark,
            fg=self.accent_gold
        ).pack(anchor=tk.W, padx=16, pady=(16, 8))

        symptom_box = tk.Text(
            dialog,
            height=9,
            bg=self.bg_panel,
            fg=self.text_light,
            font=("Segoe UI", 10),
            insertbackground=self.accent_pink,
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=12
        )
        symptom_box.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)

        def recommend():
            symptoms = symptom_box.get("1.0", tk.END).strip()
            result = self.ai_brain.get_doctor_recommendation(self._current_dosha(), symptoms)
            self._add_message("SYSTEM", result, system=True)
            dialog.destroy()

        tk.Button(
            dialog,
            text="Get Recommendation",
            font=("Segoe UI", 11, "bold"),
            bg=self.accent_pink,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=recommend
        ).pack(fill=tk.X, padx=16, pady=(0, 16), ipady=10)
    
    def show_dosha_detection(self):
        """Show Dosha detection dialog"""
        dialog = tk.Toplevel(self)
        dialog.title("🧘 Dosha Detection")
        dialog.geometry("500x400")
        dialog.configure(bg=self.bg_dark)
        dialog.resizable(False, False)
        
        tk.Label(
            dialog,
            text="Describe your constitution:\n(e.g., slim body, fast metabolism, dry skin, anxious personality)",
            font=("Segoe UI", 11),
            bg=self.bg_dark,
            fg=self.text_light,
            justify=tk.LEFT,
            wraplength=450
        ).pack(pady=15, padx=15)
        
        text_area = tk.Text(
            dialog,
            height=8,
            bg=self.bg_panel,
            fg=self.text_light,
            font=("Segoe UI", 10),
            insertbackground=self.accent_pink,
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=10
        )
        text_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        def detect():
            constitution = text_area.get("1.0", tk.END).strip()
            if not constitution:
                messagebox.showwarning("Error", "Please describe your constitution")
                return
            
            dosha = self.ai_brain.detect_dosha(constitution)
            if not dosha:
                messagebox.showinfo("Dosha Detection", "I could not detect a clear dosha. Add details about body type, digestion, skin, sleep, mood, temperature, and energy.")
                return
            result_text = f"✨ Detected Dosha: {dosha.upper()}\n\n"
            result_text += self.ai_brain.get_dosha_info(dosha)
            result_text += "\n" + self.ai_brain.get_diet_recommendation(dosha)
            result_text += "\n" + self.ai_brain.get_doctor_recommendation(dosha)
            
            result_dialog = tk.Toplevel(self)
            result_dialog.title(f"🌿 {dosha.upper()} Profile")
            result_dialog.geometry("600x500")
            result_dialog.configure(bg=self.bg_dark)
            
            result_display = scrolledtext.ScrolledText(
                result_dialog,
                bg=self.bg_panel,
                fg=self.text_light,
                font=("Segoe UI", 10),
                relief=tk.FLAT,
                bd=0,
                padx=15,
                pady=15
            )
            result_display.pack(fill=tk.BOTH, expand=True)
            result_display.insert(tk.END, result_text)
            result_display.config(state=tk.DISABLED)
            
            self.auth_manager.update_user_dosha(self.current_user, dosha)
            self._add_message("SYSTEM", f"Saved your dosha as {dosha.title()}. Diet checks and chat replies will now use this profile.", system=True)
            dialog.destroy()
        
        detect_btn = tk.Button(
            dialog,
            text="🔍 Detect",
            font=("Segoe UI", 11, "bold"),
            bg=self.accent_pink,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=detect
        )
        detect_btn.pack(pady=15, padx=15, fill=tk.X, ipady=10)
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = tk.Toplevel(self)
        dialog.title("⚙️ Settings")
        dialog.geometry("600x400")
        dialog.configure(bg=self.bg_dark)
        
        tabs_frame = tk.Frame(dialog, bg=self.bg_dark)
        tabs_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        tk.Label(
            tabs_frame,
            text="🔧 System Health",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_dark,
            fg=self.accent_pink
        ).pack(anchor=tk.W, pady=(0, 10))
        
        health = HealthCheck.check_all_components()
        health_text = ""
        for component, status in health.items():
            status_icon = "✅" if status else "❌"
            health_text += f"{status_icon} {component.replace('_', ' ').title()}\n"
        
        health_display = scrolledtext.ScrolledText(
            tabs_frame,
            height=12,
            bg=self.bg_panel,
            fg=self.text_light,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=10
        )
        health_display.pack(fill=tk.BOTH, expand=True)
        health_display.insert(tk.END, health_text)
        health_display.config(state=tk.DISABLED)
    
    def logout(self):
        """Logout and return to login"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user = None
            self.ai_brain = None
            if self.stt_engine:
                self.stt_engine.cleanup()
            self.show_login_page()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    
    app = ModernChatbot()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
