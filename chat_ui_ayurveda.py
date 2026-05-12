"""
Jarvis Ayurveda Chatbot - Professional Tkinter GUI
5-tab interface with Chat, Health Profile, Diet Plans, Wellness Plans, and Settings
"""

import json
import logging
import os
import sys
import threading
from datetime import datetime
from typing import Optional

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk

import config
from ai_brain_ayurveda import AyurvedicBrain
from error_handler import ErrorHandler, HealthCheck
from voice_input_improved import VoskSTTEngine
from hotword_secure import HotwordDetector

logger = logging.getLogger(__name__)

# ==================== MAIN APPLICATION ====================
class AyurvedicChatbot(tk.Tk):
    """Main Ayurvedic Chatbot GUI Application"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("🌿 Jarvis Ayurvedic Health Assistant")
        self.geometry("1200x800")
        self.configure(bg="#1e1e1e")
        
        # Color scheme
        self.bg_color = "#1e1e1e"
        self.fg_color = "#e0e0e0"
        self.accent_color = "#4CAF50"
        
        # Initialize AI brain
        try:
            self.brain = AyurvedicBrain()
            logger.info("✅ AI brain initialized")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize AI: {e}")
            sys.exit(1)
        
        # Initialize voice components
        try:
            self.stt_engine = VoskSTTEngine()
            logger.info("✅ Speech-to-text engine ready")
        except:
            self.stt_engine = None
            logger.warning("⚠️  Speech-to-text not available")
        
        try:
            self.hotword_detector = HotwordDetector()
            logger.info("✅ Hotword detector ready")
        except:
            self.hotword_detector = None
            logger.warning("⚠️  Hotword detection not available")
        
        self.is_listening = False
        self.user_dosha = None
        self.conversation_history = []
        
        # Create UI
        self._create_ui()
        self._load_session()
        
        logger.info("🎨 UI created successfully")
    
    def _create_ui(self):
        """Create the main user interface"""
        # Top status bar
        status_frame = tk.Frame(self, bg="#0d47a1", height=30)
        status_frame.pack(fill=tk.X, side=tk.TOP)
        
        tk.Label(status_frame, text="🌿 Jarvis", bg="#0d47a1", fg="white", font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
        
        self.status_label = tk.Label(status_frame, text="Initializing...", bg="#0d47a1", fg="#4CAF50", font=("Segoe UI", 10))
        self.status_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self, style="")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Create tabs
        self._create_chat_tab()
        self._create_health_profile_tab()
        self._create_diet_tab()
        self._create_wellness_tab()
        self._create_settings_tab()
        
        self.update_status("Ready! 🟢")
    
    def _create_chat_tab(self):
        """Create chat interface tab"""
        chat_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(chat_frame, text="💬 Chat")
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            height=25,
            bg="#2d2d2d",
            fg=self.fg_color,
            font=("Courier New", 10),
            wrap=tk.WORD
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure tags for styling
        self.chat_display.tag_config("user", foreground="#4CAF50", font=("Courier New", 10, "bold"))
        self.chat_display.tag_config("assistant", foreground="#2196F3", font=("Courier New", 10))
        self.chat_display.tag_config("system", foreground="#FFC107", font=("Courier New", 9, "italic"))
        self.chat_display.tag_config("error", foreground="#f44336", font=("Courier New", 10, "bold"))
        
        # Input field
        tk.Label(chat_frame, text="Your message:", bg=self.bg_color, fg=self.fg_color).pack(anchor=tk.W, padx=5, pady=(5, 0))
        
        self.input_field = tk.Text(
            chat_frame,
            height=3,
            bg="#3d3d3d",
            fg=self.fg_color,
            font=("Courier New", 10),
            insertbackground=self.accent_color
        )
        self.input_field.pack(fill=tk.X, padx=5, pady=5)
        self.input_field.bind("<Control-Return>", lambda e: self._on_send())
        
        # Button frame
        button_frame = tk.Frame(chat_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(button_frame, text="📤 Send", command=self._on_send, bg=self.accent_color, fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        if self.stt_engine:
            self.voice_button = tk.Button(button_frame, text="🎤 Voice", command=self._on_voice, bg="#2196F3", fg="white", font=("Segoe UI", 10, "bold"))
            self.voice_button.pack(side=tk.LEFT, padx=5)
        
        if self.hotword_detector:
            self.hotword_button = tk.Button(button_frame, text="🔥 Hotword", command=self._on_hotword, bg="#FF9800", fg="white", font=("Segoe UI", 10, "bold"))
            self.hotword_button.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="🗑️ Clear", command=self._on_clear, bg="#f44336", fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self._add_message("SYSTEM", "Welcome to Jarvis Ayurvedic Health Assistant! 🌿\nType your question or click buttons to explore features.")
    
    def _create_health_profile_tab(self):
        """Create health profile tab"""
        profile_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(profile_frame, text="👤 Health Profile")
        
        # Dosha detection form
        form_frame = tk.Frame(profile_frame, bg="#2d2d2d", relief=tk.RAISED, bd=1)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(form_frame, text="Describe your constitution:", bg="#2d2d2d", fg=self.fg_color, font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.constitution_input = tk.Text(form_frame, height=5, bg="#3d3d3d", fg=self.fg_color, font=("Courier New", 10))
        self.constitution_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Button(form_frame, text="🔍 Detect Dosha", command=self._detect_dosha, bg=self.accent_color, fg="white", font=("Segoe UI", 10, "bold")).pack(pady=10)
        
        # Display health profile
        self.profile_display = scrolledtext.ScrolledText(profile_frame, height=20, bg="#2d2d2d", fg=self.fg_color, font=("Courier New", 10))
        self.profile_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.profile_display.config(state=tk.DISABLED)
    
    def _create_diet_tab(self):
        """Create diet recommendations tab"""
        diet_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(diet_frame, text="🍽️ Diet Plans")
        
        tk.Label(diet_frame, text="Select Dosha for diet recommendations:", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 11, "bold")).pack(pady=10)
        
        button_frame = tk.Frame(diet_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        for dosha in ["Vata", "Pitta", "Kapha"]:
            tk.Button(button_frame, text=f"📋 {dosha}", command=lambda d=dosha.lower(): self._show_diet(d), bg=self.accent_color, fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        self.diet_display = scrolledtext.ScrolledText(diet_frame, height=20, bg="#2d2d2d", fg=self.fg_color, font=("Courier New", 10))
        self.diet_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.diet_display.config(state=tk.DISABLED)
    
    def _create_wellness_tab(self):
        """Create wellness plans tab"""
        wellness_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(wellness_frame, text="⚕️ Wellness Plans")
        
        selection_frame = tk.Frame(wellness_frame, bg="#2d2d2d", relief=tk.RAISED, bd=1)
        selection_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(selection_frame, text="Dosha:", bg="#2d2d2d", fg=self.fg_color).pack(side=tk.LEFT, padx=5, pady=5)
        self.wellness_dosha_var = tk.StringVar(value="vata")
        ttk.Combobox(selection_frame, textvariable=self.wellness_dosha_var, values=["vata", "pitta", "kapha"], state="readonly", width=10).pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Label(selection_frame, text="Condition:", bg="#2d2d2d", fg=self.fg_color).pack(side=tk.LEFT, padx=5, pady=5)
        self.wellness_condition_var = tk.StringVar(value="digestion")
        ttk.Combobox(selection_frame, textvariable=self.wellness_condition_var, values=["digestion", "sleep", "stress"], state="readonly", width=10).pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(selection_frame, text="📋 Get Plan", command=self._show_wellness_plan, bg=self.accent_color, fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5, pady=5)
        
        self.wellness_display = scrolledtext.ScrolledText(wellness_frame, height=20, bg="#2d2d2d", fg=self.fg_color, font=("Courier New", 10))
        self.wellness_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.wellness_display.config(state=tk.DISABLED)
    
    def _create_settings_tab(self):
        """Create settings tab"""
        settings_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        tk.Label(settings_frame, text="System Status:", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, padx=10, pady=10)
        
        health_frame = tk.Frame(settings_frame, bg="#2d2d2d", relief=tk.RAISED, bd=1)
        health_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.health_display = scrolledtext.ScrolledText(health_frame, height=10, bg="#2d2d2d", fg=self.fg_color, font=("Courier New", 10))
        self.health_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.health_display.config(state=tk.DISABLED)
        
        button_frame = tk.Frame(settings_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(button_frame, text="🔧 Check Health", command=self._check_health, bg=self.accent_color, fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="💾 Save Session", command=self._save_session, bg=self.accent_color, fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
    
    # ==================== EVENT HANDLERS ====================
    def _on_send(self):
        """Send chat message"""
        user_input = self.input_field.get("1.0", tk.END).strip()
        if not user_input:
            messagebox.showwarning("Empty Message", "Please enter a message")
            return
        
        self._add_message("USER", user_input)
        self.input_field.delete("1.0", tk.END)
        threading.Thread(target=self._get_ai_response, args=(user_input,), daemon=True).start()
    
    def _on_voice(self):
        """Voice input"""
        if self.is_listening:
            messagebox.showinfo("Info", "Already listening...")
            return
        
        self.is_listening = True
        self.voice_button.config(state=tk.DISABLED, bg="#f44336", text="🔴 Listening...")
        self.update_status("Listening...")
        threading.Thread(target=self._listen_voice, daemon=True).start()
    
    def _listen_voice(self):
        """Listen for voice input"""
        try:
            text = self.stt_engine.listen(timeout_seconds=config.STT_TIMEOUT)
            if text:
                self._add_message("VOICE", text)
                self.after(0, lambda: self._get_ai_response(text))
        except Exception as e:
            error_msg = ErrorHandler.handle_exception(e, "Voice input")
            self.after(0, lambda: self._add_message("ERROR", error_msg))
        finally:
            self.is_listening = False
            self.after(0, lambda: self.voice_button.config(state=tk.NORMAL, bg="#2196F3", text="🎤 Voice"))
            self.after(0, lambda: self.update_status("Ready! 🟢"))
    
    def _on_hotword(self):
        """Listen for hotword"""
        if self.is_listening:
            messagebox.showinfo("Info", "Already listening...")
            return
        
        self.is_listening = True
        self.hotword_button.config(state=tk.DISABLED, bg="#f44336", text="🔴 Listening...")
        self.update_status("Listening for hotword...")
        threading.Thread(target=self._listen_hotword, daemon=True).start()
    
    def _listen_hotword(self):
        """Listen for hotword then get voice input"""
        try:
            if self.hotword_detector.listen_for_hotword(timeout_seconds=30):
                self._add_message("SYSTEM", "🔥 Hotword detected! Say your question...")
                text = self.stt_engine.listen(timeout_seconds=config.STT_TIMEOUT)
                if text:
                    self._add_message("VOICE", text)
                    self.after(0, lambda: self._get_ai_response(text))
        except Exception as e:
            error_msg = ErrorHandler.handle_exception(e, "Hotword detection")
            self.after(0, lambda: self._add_message("ERROR", error_msg))
        finally:
            self.is_listening = False
            self.after(0, lambda: self.hotword_button.config(state=tk.NORMAL, bg="#FF9800", text="🔥 Hotword"))
            self.after(0, lambda: self.update_status("Ready! 🟢"))
    
    def _get_ai_response(self, user_input: str):
        """Get AI response"""
        try:
            self.after(0, lambda: self.update_status("Thinking..."))
            response = self.brain.ask_ayurveda(user_input)
            self.after(0, lambda: self._add_message("ASSISTANT", response))
            self.after(0, lambda: self.update_status("Ready! 🟢"))
        except Exception as e:
            error_msg = ErrorHandler.handle_exception(e, "AI response")
            self.after(0, lambda: self._add_message("ERROR", error_msg))
            self.after(0, lambda: self.update_status("Ready! 🟢"))
    
    def _on_clear(self):
        """Clear chat"""
        if messagebox.askyesno("Clear Chat", "Are you sure?"):
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self._add_message("SYSTEM", "✨ Chat cleared")
    
    def _detect_dosha(self):
        """Detect user's Dosha"""
        constitution = self.constitution_input.get("1.0", tk.END).strip()
        if not constitution:
            messagebox.showwarning("Empty Input", "Please describe your constitution")
            return
        
        dosha = self.brain.detect_dosha(constitution)
        self.user_dosha = dosha
        
        self.profile_display.config(state=tk.NORMAL)
        self.profile_display.delete("1.0", tk.END)
        
        if dosha:
            profile_text = f"✅ DETECTED DOSHA: {dosha.upper()}\n\n"
            profile_text += self.brain.get_health_summary()
        else:
            profile_text = "Could not detect Dosha. Please provide more details."
        
        self.profile_display.insert(tk.END, profile_text)
        self.profile_display.config(state=tk.DISABLED)
    
    def _show_diet(self, dosha: str):
        """Show diet recommendations"""
        self.diet_display.config(state=tk.NORMAL)
        self.diet_display.delete("1.0", tk.END)
        self.diet_display.insert(tk.END, self.brain.get_diet_recommendation(dosha))
        self.diet_display.config(state=tk.DISABLED)
    
    def _show_wellness_plan(self):
        """Show wellness plan"""
        dosha = self.wellness_dosha_var.get()
        condition = self.wellness_condition_var.get()
        
        self.wellness_display.config(state=tk.NORMAL)
        self.wellness_display.delete("1.0", tk.END)
        self.wellness_display.insert(tk.END, self.brain.create_wellness_plan(dosha, condition))
        self.wellness_display.config(state=tk.DISABLED)
    
    def _check_health(self):
        """Check system health"""
        health = HealthCheck.check_all_components()
        
        self.health_display.config(state=tk.NORMAL)
        self.health_display.delete("1.0", tk.END)
        
        health_text = "🔧 System Health Check\n\n"
        for component, status in health.items():
            status_icon = "✅" if status else "❌"
            health_text += f"{status_icon} {component}: {'Ready' if status else 'Failed'}\n"
        
        health_text += f"\nOverall: {'✅ All systems ready!' if all(health.values()) else '⚠️ Some systems need attention'}"
        
        self.health_display.insert(tk.END, health_text)
        self.health_display.config(state=tk.DISABLED)
    
    def _add_message(self, role: str, message: str):
        """Add message to chat"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if role == "USER":
            prefix = f"[{timestamp}] YOU: "
            tag = "user"
        elif role == "ASSISTANT":
            prefix = f"[{timestamp}] 🧘 JARVIS: "
            tag = "assistant"
        elif role == "SYSTEM":
            prefix = f"[{timestamp}] ℹ️ "
            tag = "system"
        elif role == "ERROR":
            prefix = f"[{timestamp}] ❌ ERROR: "
            tag = "error"
        else:
            prefix = f"[{timestamp}] "
            tag = "assistant"
        
        self.chat_display.insert(tk.END, prefix, tag)
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def update_status(self, status: str):
        """Update status label"""
        self.status_label.config(text=status)
        self.update_idletasks()
    
    def _save_session(self):
        """Save chat session"""
        try:
            session = {
                "timestamp": datetime.now().isoformat(),
                "user_dosha": self.user_dosha
            }
            
            filename = f"sessions/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.makedirs("sessions", exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(session, f, indent=2)
            
            messagebox.showinfo("Session Saved", f"Session saved to {filename}")
            logger.info(f"Session saved: {filename}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))
    
    def _load_session(self):
        """Load previous session"""
        try:
            if os.path.exists("sessions") and os.listdir("sessions"):
                latest = max([os.path.join("sessions", f) for f in os.listdir("sessions")], key=os.path.getctime)
                with open(latest, 'r') as f:
                    session = json.load(f)
                    self.user_dosha = session.get("user_dosha")
                    self._add_message("SYSTEM", f"✅ Loaded previous session")
        except:
            pass
    
    def on_closing(self):
        """Handle window close"""
        if messagebox.askokcancel("Quit", "Save session before closing?"):
            self._save_session()
        
        if self.stt_engine:
            self.stt_engine.cleanup()
        if self.hotword_detector:
            self.hotword_detector.cleanup()
        
        logger.info("Chatbot closed")
        self.quit()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting Jarvis Ayurvedic Chatbot")
    
    app = AyurvedicChatbot()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
