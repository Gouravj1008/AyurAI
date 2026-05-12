"""
Jarvis Ayurveda Chatbot - Enhanced UI
Complete chat interface with Dosha detection, diet recommendations, and wellness planning
"""

import json
import logging
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from datetime import datetime
from typing import Optional

import config
from ai_brain_ayurveda import get_brain
from voice_input_improved import VoskSTTEngine
from hotword_secure import HotwordDetector
from error_handler import ErrorHandler, HealthCheck

logger = logging.getLogger(__name__)

# ==================== CHAT UI APPLICATION ====================
class AyurvedicChatbot(tk.Tk):
    """Main Ayurvedic Chatbot UI"""
    
    def __init__(self):
        super().__init__()
        
        self.title("🌿 Jarvis - Ayurvedic Health Assistant")
        self.geometry("900x700")
        self.resizable(True, True)
        
        # Initialize components
        self.brain = None
        self.stt_engine = None
        self.hotword_detector = None
        self.is_listening = False
        self.user_dosha = None
        
        # Set color theme
        self.bg_color = "#1e1e1e"
        self.fg_color = "#e0e0e0"
        self.accent_color = "#4CAF50"
        self.configure(bg=self.bg_color)
        
        self._initialize_components()
        self._create_ui()
        self._load_session()
        
        logger.info("✅ Chatbot UI initialized")
    
    def _initialize_components(self):
        """Initialize AI brain and input engines"""
        try:
            logger.info("🔧 Initializing components...")
            
            # Show loading indicator
            self.update_status("Initializing AI brain...")
            self.brain = get_brain()
            self.update_status("Initializing voice engine...")
            self.stt_engine = VoskSTTEngine()
            
            if config.ENABLE_HOTWORD:
                self.update_status("Initializing hotword detector...")
                self.hotword_detector = HotwordDetector()
            
            self.update_status("Ready! 🟢")
            logger.info("✅ All components initialized")
        
        except Exception as e:
            error_msg = ErrorHandler.handle_exception(e, "Component initialization")
            messagebox.showerror("Initialization Error", error_msg)
            logger.error(f"Failed to initialize components: {e}")
            self.after(1000, self.quit)
    
    def _create_ui(self):
        """Create user interface"""
        
        # ==================== HEADER ====================
        header_frame = tk.Frame(self, bg="#2d2d2d", height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = tk.Label(
            header_frame,
            text="🌿 JARVIS AYURVEDIC HEALTH ASSISTANT",
            font=("Segoe UI", 16, "bold"),
            bg="#2d2d2d",
            fg=self.accent_color
        )
        title_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.status_label = tk.Label(
            header_frame,
            text="Initializing...",
            font=("Segoe UI", 10),
            bg="#2d2d2d",
            fg="#FFC107"
        )
        self.status_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # ==================== MAIN CONTENT ====================
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # ==================== CHAT TAB ====================
        self._create_chat_tab()
        
        # ==================== HEALTH PROFILE TAB ====================
        self._create_health_profile_tab()
        
        # ==================== DIET RECOMMENDATIONS TAB ====================
        self._create_diet_tab()
        
        # ==================== WELLNESS PLANS TAB ====================
        self._create_wellness_tab()
        
        # ==================== SETTINGS TAB ====================
        self._create_settings_tab()
        
        # ==================== INPUT FRAME ====================
        input_frame = tk.Frame(self, bg=self.bg_color)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        button_frame = tk.Frame(input_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, side=tk.LEFT, expand=True)
        
        self.send_button = tk.Button(
            button_frame,
            text="📤 Send",
            command=self._on_send,
            bg=self.accent_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8
        )
        self.send_button.pack(side=tk.LEFT, padx=5)
        
        self.voice_button = tk.Button(
            button_frame,
            text="🎤 Voice",
            command=self._on_voice,
            bg="#2196F3",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8
        )
        self.voice_button.pack(side=tk.LEFT, padx=5)
        
        self.hotword_button = tk.Button(
            button_frame,
            text="🔥 Hotword",
            command=self._on_hotword,
            bg="#FF9800",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            state=tk.NORMAL if config.ENABLE_HOTWORD else tk.DISABLED
        )
        self.hotword_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = tk.Button(
            button_frame,
            text="🗑️  Clear",
            command=self._on_clear,
            bg="#f44336",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8
        )
        clear_button.pack(side=tk.LEFT, padx=5)
    
    def _create_chat_tab(self):
        """Create chat tab"""
        chat_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(chat_frame, text="💬 Chat")
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            bg="#2d2d2d",
            fg=self.fg_color,
            font=("Courier New", 10),
            height=20,
            width=80
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure tags for styling
        self.chat_display.tag_config("user", foreground="#4CAF50", font=("Courier New", 10, "bold"))
        self.chat_display.tag_config("assistant", foreground="#2196F3", font=("Courier New", 10))
        self.chat_display.tag_config("system", foreground="#FFC107", font=("Courier New", 9, "italic"))\n        self.chat_display.tag_config("error", foreground="#f44336", font=("Courier New", 10, "bold"))\n        \n        # Input field\n        tk.Label(chat_frame, text=\"Your message:\", bg=self.bg_color, fg=self.fg_color).pack(\n            anchor=tk.W, padx=5, pady=(5, 0)\n        )\n        \n        self.input_field = tk.Text(\n            chat_frame,\n            height=3,\n            bg=\"#3d3d3d\",\n            fg=self.fg_color,\n            font=(\"Courier New\", 10),\n            insertbackground=self.accent_color\n        )\n        self.input_field.pack(fill=tk.X, padx=5, pady=5)\n        self.input_field.bind(\"<Control-Return>\", lambda e: self._on_send())\n    \n    def _create_health_profile_tab(self):\n        \"\"\"Create health profile tab\"\"\"\n        profile_frame = tk.Frame(self.notebook, bg=self.bg_color)\n        self.notebook.add(profile_frame, text=\"👤 Health Profile\")\n        \n        # Dosha detection form\n        form_frame = tk.Frame(profile_frame, bg=\"#2d2d2d\", relief=tk.RAISED, bd=1)\n        form_frame.pack(fill=tk.X, padx=10, pady=10)\n        \n        tk.Label(\n            form_frame,\n            text=\"Describe your constitution:\",\n            bg=\"#2d2d2d\",\n            fg=self.fg_color,\n            font=(\"Segoe UI\", 11, \"bold\")\n        ).pack(anchor=tk.W, padx=10, pady=(10, 5))\n        \n        self.constitution_input = tk.Text(\n            form_frame,\n            height=5,\n            bg=\"#3d3d3d\",\n            fg=self.fg_color,\n            font=(\"Courier New\", 10)\n        )\n        self.constitution_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)\n        \n        tk.Button(\n            form_frame,\n            text=\"🔍 Detect Dosha\",\n            command=self._detect_dosha,\n            bg=self.accent_color,\n            fg=\"white\",\n            font=(\"Segoe UI\", 10, \"bold\")\n        ).pack(pady=10)\n        \n        # Display health profile\n        self.profile_display = scrolledtext.ScrolledText(\n            profile_frame,\n            height=20,\n            bg=\"#2d2d2d\",\n            fg=self.fg_color,\n            font=(\"Courier New\", 10)\n        )\n        self.profile_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)\n        self.profile_display.config(state=tk.DISABLED)\n    \n    def _create_diet_tab(self):\n        \"\"\"Create diet recommendations tab\"\"\"\n        diet_frame = tk.Frame(self.notebook, bg=self.bg_color)\n        self.notebook.add(diet_frame, text=\"🍽️  Diet Plans\")\n        \n        tk.Label(\n            diet_frame,\n            text=\"Select Dosha for diet recommendations:\",\n            bg=self.bg_color,\n            fg=self.fg_color,\n            font=(\"Segoe UI\", 11, \"bold\")\n        ).pack(pady=10)\n        \n        # Dosha selection\n        button_frame = tk.Frame(diet_frame, bg=self.bg_color)\n        button_frame.pack(fill=tk.X, padx=10, pady=10)\n        \n        for dosha in [\"Vata\", \"Pitta\", \"Kapha\"]:\n            tk.Button(\n                button_frame,\n                text=f\"📋 {dosha}\",\n                command=lambda d=dosha.lower(): self._show_diet(d),\n                bg=self.accent_color,\n                fg=\"white\",\n                font=(\"Segoe UI\", 10, \"bold\"),\n                padx=15,\n                pady=5\n            ).pack(side=tk.LEFT, padx=5)\n        \n        # Diet display\n        self.diet_display = scrolledtext.ScrolledText(\n            diet_frame,\n            height=20,\n            bg=\"#2d2d2d\",\n            fg=self.fg_color,\n            font=(\"Courier New\", 10)\n        )\n        self.diet_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)\n        self.diet_display.config(state=tk.DISABLED)\n    \n    def _create_wellness_tab(self):\n        \"\"\"Create wellness plans tab\"\"\"\n        wellness_frame = tk.Frame(self.notebook, bg=self.bg_color)\n        self.notebook.add(wellness_frame, text=\"⚕️  Wellness Plans\")\n        \n        # Dosha and condition selection\n        selection_frame = tk.Frame(wellness_frame, bg=\"#2d2d2d\", relief=tk.RAISED, bd=1)\n        selection_frame.pack(fill=tk.X, padx=10, pady=10)\n        \n        tk.Label(\n            selection_frame,\n            text=\"Dosha:\",\n            bg=\"#2d2d2d\",\n            fg=self.fg_color\n        ).pack(side=tk.LEFT, padx=5, pady=5)\n        \n        self.wellness_dosha_var = tk.StringVar(value=\"vata\")\n        dosha_dropdown = ttk.Combobox(\n            selection_frame,\n            textvariable=self.wellness_dosha_var,\n            values=[\"vata\", \"pitta\", \"kapha\"],\n            state=\"readonly\",\n            width=10\n        )\n        dosha_dropdown.pack(side=tk.LEFT, padx=5, pady=5)\n        \n        tk.Label(\n            selection_frame,\n            text=\"Condition:\",\n            bg=\"#2d2d2d\",\n            fg=self.fg_color\n        ).pack(side=tk.LEFT, padx=5, pady=5)\n        \n        self.wellness_condition_var = tk.StringVar(value=\"digestion\")\n        condition_dropdown = ttk.Combobox(\n            selection_frame,\n            textvariable=self.wellness_condition_var,\n            values=[\"digestion\", \"sleep\", \"stress\"],\n            state=\"readonly\",\n            width=10\n        )\n        condition_dropdown.pack(side=tk.LEFT, padx=5, pady=5)\n        \n        tk.Button(\n            selection_frame,\n            text=\"📋 Get Plan\",\n            command=self._show_wellness_plan,\n            bg=self.accent_color,\n            fg=\"white\",\n            font=(\"Segoe UI\", 10, \"bold\")\n        ).pack(side=tk.LEFT, padx=5, pady=5)\n        \n        # Plan display\n        self.wellness_display = scrolledtext.ScrolledText(\n            wellness_frame,\n            height=20,\n            bg=\"#2d2d2d\",\n            fg=self.fg_color,\n            font=(\"Courier New\", 10)\n        )\n        self.wellness_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)\n        self.wellness_display.config(state=tk.DISABLED)\n    \n    def _create_settings_tab(self):\n        \"\"\"Create settings tab\"\"\"\n        settings_frame = tk.Frame(self.notebook, bg=self.bg_color)\n        self.notebook.add(settings_frame, text=\"⚙️  Settings\")\n        \n        # System health\n        tk.Label(\n            settings_frame,\n            text=\"System Status:\",\n            bg=self.bg_color,\n            fg=self.fg_color,\n            font=(\"Segoe UI\", 12, \"bold\")\n        ).pack(anchor=tk.W, padx=10, pady=10)\n        \n        health_frame = tk.Frame(settings_frame, bg=\"#2d2d2d\", relief=tk.RAISED, bd=1)\n        health_frame.pack(fill=tk.X, padx=10, pady=5)\n        \n        self.health_display = scrolledtext.ScrolledText(\n            health_frame,\n            height=10,\n            bg=\"#2d2d2d\",\n            fg=self.fg_color,\n            font=(\"Courier New\", 10)\n        )\n        self.health_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)\n        self.health_display.config(state=tk.DISABLED)\n        \n        # Configuration info\n        tk.Label(\n            settings_frame,\n            text=\"Configuration:\",\n            bg=self.bg_color,\n            fg=self.fg_color,\n            font=(\"Segoe UI\", 12, \"bold\")\n        ).pack(anchor=tk.W, padx=10, pady=(10, 5))\n        \n        config_frame = tk.Frame(settings_frame, bg=\"#2d2d2d\", relief=tk.RAISED, bd=1)\n        config_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)\n        \n        config_text = scrolledtext.ScrolledText(\n            config_frame,\n            height=10,\n            bg=\"#2d2d2d\",\n            fg=self.fg_color,\n            font=(\"Courier New\", 9)\n        )\n        config_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)\n        \n        config_info = f\"\"\"Device: {config.DEVICE_NAME}\nBase Model: {config.BASE_MODEL}\nAdapter: {config.ADAPTER_PATH}\nTemperature: {config.TEMPERATURE}\nMax Tokens: {config.MAX_TOKENS}\nHotword Enabled: {config.ENABLE_HOTWORD}\nTTS Enabled: {config.ENABLE_TTS}\nSTT Timeout: {config.STT_TIMEOUT}s\"\"\"\n        \n        config_text.insert(tk.END, config_info)\n        config_text.config(state=tk.DISABLED)\n        \n        # Buttons\n        button_frame = tk.Frame(settings_frame, bg=self.bg_color)\n        button_frame.pack(fill=tk.X, padx=10, pady=10)\n        \n        tk.Button(\n            button_frame,\n            text=\"🔧 Check Health\",\n            command=self._check_health,\n            bg=self.accent_color,\n            fg=\"white\",\n            font=(\"Segoe UI\", 10, \"bold\")\n        ).pack(side=tk.LEFT, padx=5)\n        \n        tk.Button(\n            button_frame,\n            text=\"💾 Save Session\",\n            command=self._save_session,\n            bg=self.accent_color,\n            fg=\"white\",\n            font=(\"Segoe UI\", 10, \"bold\")\n        ).pack(side=tk.LEFT, padx=5)\n    \n    # ==================== EVENT HANDLERS ====================\n    def _on_send(self):\n        \"\"\"Send chat message\"\"\"\n        user_input = self.input_field.get(\"1.0\", tk.END).strip()\n        if not user_input:\n            messagebox.showwarning(\"Empty Message\", \"Please enter a message\")\n            return\n        \n        self._add_message(\"USER\", user_input)\n        self.input_field.delete(\"1.0\", tk.END)\n        \n        # Get AI response in thread\n        threading.Thread(target=self._get_ai_response, args=(user_input,), daemon=True).start()\n    \n    def _on_voice(self):\n        \"\"\"Voice input\"\"\"\n        if self.is_listening:\n            messagebox.showinfo(\"Info\", \"Already listening...\")\n            return\n        \n        self.is_listening = True\n        self.voice_button.config(state=tk.DISABLED, bg=\"#f44336\", text=\"🔴 Listening...\")\n        self.update_status(\"Listening...\")\n        \n        threading.Thread(target=self._listen_voice, daemon=True).start()\n    \n    def _listen_voice(self):\n        \"\"\"Listen for voice input\"\"\"\n        try:\n            text = self.stt_engine.listen(timeout_seconds=config.STT_TIMEOUT)\n            if text:\n                self._add_message(\"VOICE\", text)\n                self.after(0, lambda: self._get_ai_response(text))\n                self._add_message(\"SYSTEM\", f\"✅ Recognized: {text}\")\n        except Exception as e:\n            error_msg = ErrorHandler.handle_exception(e, \"Voice input\")\n            self.after(0, lambda: self._add_message(\"ERROR\", error_msg))\n        finally:\n            self.is_listening = False\n            self.after(0, lambda: self.voice_button.config(state=tk.NORMAL, bg=\"#2196F3\", text=\"🎤 Voice\"))\n            self.after(0, lambda: self.update_status(\"Ready! 🟢\"))\n    \n    def _on_hotword(self):\n        \"\"\"Listen for hotword\"\"\"\n        if self.is_listening:\n            messagebox.showinfo(\"Info\", \"Already listening...\")\n            return\n        \n        self.is_listening = True\n        self.hotword_button.config(state=tk.DISABLED, bg=\"#f44336\", text=\"🔴 Listening...\")\n        self.update_status(\"Listening for hotword...\")\n        \n        threading.Thread(target=self._listen_hotword, daemon=True).start()\n    \n    def _listen_hotword(self):\n        \"\"\"Listen for hotword then get voice input\"\"\"\n        try:\n            if self.hotword_detector.listen_for_hotword(timeout_seconds=30):\n                self._add_message(\"SYSTEM\", \"🔥 Hotword detected! Say your question...\")\n                text = self.stt_engine.listen(timeout_seconds=config.STT_TIMEOUT)\n                if text:\n                    self._add_message(\"VOICE\", text)\n                    self.after(0, lambda: self._get_ai_response(text))\n            else:\n                self.after(0, lambda: self._add_message(\"SYSTEM\", \"⏱️  Hotword timeout\"))\n        except Exception as e:\n            error_msg = ErrorHandler.handle_exception(e, \"Hotword detection\")\n            self.after(0, lambda: self._add_message(\"ERROR\", error_msg))\n        finally:\n            self.is_listening = False\n            self.after(0, lambda: self.hotword_button.config(state=tk.NORMAL, bg=\"#FF9800\", text=\"🔥 Hotword\"))\n            self.after(0, lambda: self.update_status(\"Ready! 🟢\"))\n    \n    def _get_ai_response(self, user_input: str):\n        \"\"\"Get AI response\"\"\"\n        try:\n            self.after(0, lambda: self.update_status(\"Thinking...\"))\n            response = self.brain.ask_ayurveda(user_input)\n            self.after(0, lambda: self._add_message(\"ASSISTANT\", response))\n            self.after(0, lambda: self.update_status(\"Ready! 🟢\"))\n        except Exception as e:\n            error_msg = ErrorHandler.handle_exception(e, \"AI response generation\")\n            self.after(0, lambda: self._add_message(\"ERROR\", error_msg))\n            self.after(0, lambda: self.update_status(\"Ready! 🟢\"))\n    \n    def _on_clear(self):\n        \"\"\"Clear chat\"\"\"\n        if messagebox.askyesno(\"Clear Chat\", \"Are you sure?\"):\n            self.chat_display.config(state=tk.NORMAL)\n            self.chat_display.delete(\"1.0\", tk.END)\n            self.chat_display.config(state=tk.DISABLED)\n            self.brain.clear_history()\n            self._add_message(\"SYSTEM\", \"✨ Chat cleared\")\n    \n    def _detect_dosha(self):\n        \"\"\"Detect user's Dosha\"\"\"\n        constitution = self.constitution_input.get(\"1.0\", tk.END).strip()\n        if not constitution:\n            messagebox.showwarning(\"Empty Input\", \"Please describe your constitution\")\n            return\n        \n        dosha = self.brain.detect_dosha(constitution)\n        self.user_dosha = dosha\n        \n        self.profile_display.config(state=tk.NORMAL)\n        self.profile_display.delete(\"1.0\", tk.END)\n        \n        if dosha:\n            profile_text = f\"✅ DETECTED DOSHA: {dosha.upper()}\\n\\n\"\n            profile_text += self.brain.get_health_summary()\n        else:\n            profile_text = \"Could not detect Dosha. Please provide more details.\"\n        \n        self.profile_display.insert(tk.END, profile_text)\n        self.profile_display.config(state=tk.DISABLED)\n    \n    def _show_diet(self, dosha: str):\n        \"\"\"Show diet recommendations\"\"\"\n        self.diet_display.config(state=tk.NORMAL)\n        self.diet_display.delete(\"1.0\", tk.END)\n        self.diet_display.insert(tk.END, self.brain.get_diet_recommendation(dosha))\n        self.diet_display.config(state=tk.DISABLED)\n    \n    def _show_wellness_plan(self):\n        \"\"\"Show wellness plan\"\"\"\n        dosha = self.wellness_dosha_var.get()\n        condition = self.wellness_condition_var.get()\n        \n        self.wellness_display.config(state=tk.NORMAL)\n        self.wellness_display.delete(\"1.0\", tk.END)\n        self.wellness_display.insert(tk.END, self.brain.create_wellness_plan(dosha, condition))\n        self.wellness_display.config(state=tk.DISABLED)\n    \n    def _check_health(self):\n        \"\"\"Check system health\"\"\"\n        health = HealthCheck.check_all_components()\n        \n        self.health_display.config(state=tk.NORMAL)\n        self.health_display.delete(\"1.0\", tk.END)\n        \n        health_text = \"🔧 System Health Check\\n\\n\"\n        for component, status in health.items():\n            status_icon = \"✅\" if status else \"❌\"\n            health_text += f\"{status_icon} {component}: {'Ready' if status else 'Failed'}\\n\"\n        \n        health_text += f\"\\nOverall: {'✅ All systems ready!' if all(health.values()) else '⚠️  Some systems need attention'}\"\n        \n        self.health_display.insert(tk.END, health_text)\n        self.health_display.config(state=tk.DISABLED)\n    \n    def _add_message(self, role: str, message: str):\n        \"\"\"Add message to chat\"\"\"\n        self.chat_display.config(state=tk.NORMAL)\n        \n        timestamp = datetime.now().strftime(\"%H:%M:%S\")\n        \n        if role == \"USER\":\n            prefix = f\"[{timestamp}] YOU: \"\n            tag = \"user\"\n        elif role == \"VOICE\":\n            prefix = f\"[{timestamp}] 🎤 VOICE: \"\n            tag = \"user\"\n        elif role == \"ASSISTANT\":\n            prefix = f\"[{timestamp}] 🧘 JARVIS: \"\n            tag = \"assistant\"\n        elif role == \"SYSTEM\":\n            prefix = f\"[{timestamp}] ℹ️  \"\n            tag = \"system\"\n        elif role == \"ERROR\":\n            prefix = f\"[{timestamp}] ❌ ERROR: \"\n            tag = \"error\"\n        else:\n            prefix = f\"[{timestamp}] \"\n            tag = \"assistant\"\n        \n        self.chat_display.insert(tk.END, prefix, tag)\n        self.chat_display.insert(tk.END, f\"{message}\\n\\n\")\n        self.chat_display.see(tk.END)\n        self.chat_display.config(state=tk.DISABLED)\n    \n    def update_status(self, status: str):\n        \"\"\"Update status label\"\"\"\n        self.status_label.config(text=status)\n        self.update_idletasks()\n    \n    def _save_session(self):\n        \"\"\"Save chat session\"\"\"\n        try:\n            session = {\n                \"timestamp\": datetime.now().isoformat(),\n                \"user_dosha\": self.user_dosha,\n                \"history\": self.brain.conversation_history\n            }\n            \n            filename = f\"sessions/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json\"\n            os.makedirs(\"sessions\", exist_ok=True)\n            \n            with open(filename, 'w', encoding='utf-8') as f:\n                json.dump(session, f, indent=2, ensure_ascii=False)\n            \n            messagebox.showinfo(\"Session Saved\", f\"Session saved to {filename}\")\n            logger.info(f\"Session saved: {filename}\")\n        except Exception as e:\n            error_msg = ErrorHandler.handle_exception(e, \"Session save\")\n            messagebox.showerror(\"Save Error\", error_msg)\n    \n    def _load_session(self):\n        \"\"\"Load previous session\"\"\"\n        try:\n            import os\n            if os.path.exists(\"sessions\") and os.listdir(\"sessions\"):\n                latest_session = max(\n                    [os.path.join(\"sessions\", f) for f in os.listdir(\"sessions\")],\n                    key=os.path.getctime\n                )\n                \n                with open(latest_session, 'r', encoding='utf-8') as f:\n                    session = json.load(f)\n                    self.user_dosha = session.get(\"user_dosha\")\n                    self._add_message(\"SYSTEM\", f\"✅ Loaded previous session (Dosha: {self.user_dosha or 'Not detected'})\")\n        except Exception as e:\n            logger.warning(f\"Could not load session: {e}\")\n    \n    def on_closing(self):\n        \"\"\"Handle window close\"\"\"\n        if messagebox.askokcancel(\"Quit\", \"Save session before closing?\"):\n            self._save_session()\n        \n        if self.stt_engine:\n            self.stt_engine.cleanup()\n        if self.hotword_detector:\n            self.hotword_detector.cleanup()\n        \n        logger.info(\"Chatbot closed\")\n        self.quit()

# ==================== MAIN ====================
if __name__ == \"__main__\":\n    import os\n    \n    # Setup logging\n    logging.basicConfig(\n        level=logging.INFO,\n        format=\"%(asctime)s - %(name)s - %(levelname)s - %(message)s\",\n        handlers=[\n            logging.FileHandler(config.LOG_FILE),\n            logging.StreamHandler()\n        ]\n    )\n    \n    logger = logging.getLogger(__name__)\n    logger.info(\"🚀 Starting Jarvis Ayurvedic Chatbot\")\n    \n    app = AyurvedicChatbot()\n    app.protocol(\"WM_DELETE_WINDOW\", app.on_closing)\n    app.mainloop()\n