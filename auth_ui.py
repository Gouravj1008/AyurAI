"""
Modern Ayurveda-themed Login and Signup UI
ChatGPT-style design with pink color scheme
"""

import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
from auth_manager import AuthManager

class AuthUI(tk.Tk):
    """Authentication UI with Login and Signup pages"""
    
    def __init__(self):
        super().__init__()
        
        self.title("🌿 Jarvis Ayurvedic Health Assistant")
        self.geometry("900x700")
        self.resizable(False, False)
        
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
        self.success_green = "#4CAF50"
        
        self.configure(bg=self.bg_dark)
        
        # Auth manager
        self.auth_manager = AuthManager()
        self.current_user = None
        
        # Create UI
        self._animation_job = None
        self.show_landing_page()
    
    def clear_window(self):
        """Clear all widgets from window"""
        if getattr(self, "_animation_job", None):
            try:
                self.after_cancel(self._animation_job)
            except Exception:
                pass
            self._animation_job = None
        for widget in self.winfo_children():
            widget.destroy()

    def _button(self, parent, text, command, bg=None, fg="white"):
        """Create a consistent flat action button."""
        btn = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 12, "bold"),
            bg=bg or self.accent_pink,
            fg=fg,
            activebackground=self.accent_gold,
            activeforeground="#07130f",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=command
        )
        btn.bind("<Enter>", lambda _e: btn.config(bg=self.accent_gold, fg="#07130f"))
        btn.bind("<Leave>", lambda _e: btn.config(bg=bg or self.accent_pink, fg=fg))
        return btn

    def show_landing_page(self):
        """Show Ayurveda-themed landing page before authentication."""
        self.clear_window()
        self.geometry("980x720")
        self.configure(bg=self.bg_dark)

        main_frame = tk.Frame(self, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True)

        hero = tk.Canvas(main_frame, bg=self.bg_dark, highlightthickness=0)
        hero.pack(fill=tk.BOTH, expand=True)

        rings = []
        for i in range(8):
            rings.append(hero.create_oval(120 + i * 70, 90 + i * 38, 210 + i * 70, 180 + i * 38, outline="#214c38", width=2))

        hero.create_text(490, 118, text="JARVIS AYURVEDA", fill=self.accent_light_pink, font=("Segoe UI", 14, "bold"))
        hero.create_text(490, 190, text="Ancient dosha wisdom,\nmodern AI guidance.", fill=self.text_light, font=("Segoe UI", 36, "bold"), justify=tk.CENTER)
        hero.create_text(
            490,
            286,
            text="Personal diet checks, dosha education, doctor guidance, and a calm assistant for everyday wellness.",
            fill=self.text_muted,
            font=("Segoe UI", 13),
            width=620,
            justify=tk.CENTER
        )

        action_frame = tk.Frame(hero, bg=self.bg_dark)
        hero.create_window(490, 370, window=action_frame)
        self._button(action_frame, "Start Login", self.show_login_page).pack(side=tk.LEFT, padx=8, ipadx=22, ipady=10)
        self._button(action_frame, "Create Account", self.show_signup_page, bg=self.accent_saffron, fg="#07130f").pack(side=tk.LEFT, padx=8, ipadx=22, ipady=10)

        card_frame = tk.Frame(hero, bg=self.bg_dark)
        hero.create_window(490, 535, window=card_frame)
        cards = [
            ("Dosha Check", "Vata, Pitta, Kapha profile with user-specific storage."),
            ("Diet Match", "Compare daily meals with your detected constitution."),
            ("Doctor Guide", "Know when to consult a Vaidya or medical doctor."),
        ]
        for title, body in cards:
            card = tk.Frame(card_frame, bg=self.bg_panel, highlightthickness=1, highlightbackground="#2f5f48")
            card.pack(side=tk.LEFT, padx=10, ipadx=16, ipady=14)
            tk.Label(card, text=title, bg=self.bg_panel, fg=self.accent_gold, font=("Segoe UI", 13, "bold")).pack(anchor=tk.W)
            tk.Label(card, text=body, bg=self.bg_panel, fg=self.text_muted, font=("Segoe UI", 10), wraplength=210, justify=tk.LEFT).pack(anchor=tk.W, pady=(8, 0))

        def animate(step=0):
            for idx, item in enumerate(rings):
                color = "#2f6f4e" if (step + idx) % 4 == 0 else "#214c38"
                hero.itemconfig(item, outline=color)
                hero.move(item, 0, -1 if (step + idx) % 2 == 0 else 1)
            self._animation_job = self.after(220, lambda: animate(step + 1))

        animate()
    
    def show_login_page(self):
        """Show login page"""
        self.clear_window()
        
        # Main container
        main_frame = tk.Frame(self, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Branding
        left_frame = tk.Frame(main_frame, bg=self.bg_panel, width=450)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        left_frame.pack_propagate(False)
        
        # Logo area
        logo_frame = tk.Frame(left_frame, bg=self.bg_panel)
        logo_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=80)
        
        # Logo
        logo_label = tk.Label(
            logo_frame,
            text="🌿",
            font=("Segoe UI", 100),
            bg=self.bg_panel,
            fg=self.accent_light_pink
        )
        logo_label.pack(pady=20)
        
        # Title
        title_label = tk.Label(
            logo_frame,
            text="Jarvis",
            font=("Segoe UI", 48, "bold"),
            bg=self.bg_panel,
            fg="white"
        )
        title_label.pack(pady=10)
        
        # Subtitle
        subtitle_label = tk.Label(
            logo_frame,
            text="Ayurvedic Health\nCompanion",
            font=("Segoe UI", 18),
            bg=self.bg_panel,
            fg=self.accent_gold,
            justify=tk.CENTER
        )
        subtitle_label.pack(pady=10)
        
        # Description
        desc_label = tk.Label(
            logo_frame,
            text="Personalized health guidance\nbased on ancient wisdom",
            font=("Segoe UI", 12),
            bg=self.bg_panel,
            fg=self.text_muted,
            justify=tk.CENTER
        )
        desc_label.pack(pady=20)
        
        # Right side - Login form
        right_frame = tk.Frame(main_frame, bg=self.bg_dark)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=50, pady=60)
        
        # Form title
        form_title = tk.Label(
            right_frame,
            text="Welcome Back",
            font=("Segoe UI", 32, "bold"),
            bg=self.bg_dark,
            fg=self.text_light
        )
        form_title.pack(pady=(0, 30), anchor=tk.W)
        
        # Username field
        tk.Label(
            right_frame,
            text="Username",
            font=("Segoe UI", 10),
            bg=self.bg_dark,
            fg=self.accent_light_pink
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.login_username = tk.Entry(
            right_frame,
            font=("Segoe UI", 12),
            bg=self.bg_panel,
            fg=self.text_light,
            insertbackground=self.accent_pink,
            relief=tk.FLAT,
            bd=0
        )
        self.login_username.pack(fill=tk.X, pady=(0, 20), ipady=12)
        
        # Password field
        tk.Label(
            right_frame,
            text="Password",
            font=("Segoe UI", 10),
            bg=self.bg_dark,
            fg=self.accent_light_pink
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.login_password = tk.Entry(
            right_frame,
            font=("Segoe UI", 12),
            bg=self.bg_panel,
            fg=self.text_light,
            insertbackground=self.accent_pink,
            relief=tk.FLAT,
            bd=0,
            show="•"
        )
        self.login_password.pack(fill=tk.X, pady=(0, 30), ipady=12)
        
        # Login button
        login_btn = tk.Button(
            right_frame,
            text="Sign In",
            font=("Segoe UI", 12, "bold"),
            bg=self.accent_pink,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self._handle_login
        )
        login_btn.pack(fill=tk.X, ipady=12, pady=(0, 20))

        landing_link = tk.Label(
            right_frame,
            text="Back to landing page",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_dark,
            fg=self.accent_gold,
            cursor="hand2"
        )
        landing_link.pack(anchor=tk.W)
        landing_link.bind("<Button-1>", lambda e: self.show_landing_page())
        
        # Signup link
        signup_frame = tk.Frame(right_frame, bg=self.bg_dark)
        signup_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Label(
            signup_frame,
            text="Don't have an account? ",
            font=("Segoe UI", 10),
            bg=self.bg_dark,
            fg=self.text_light
        ).pack(side=tk.LEFT)
        
        signup_link = tk.Label(
            signup_frame,
            text="Sign Up",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_dark,
            fg=self.accent_pink,
            cursor="hand2"
        )
        signup_link.pack(side=tk.LEFT)
        signup_link.bind("<Button-1>", lambda e: self.show_signup_page())
    
    def show_signup_page(self):
        """Show signup page"""
        self.clear_window()
        
        # Main container
        main_frame = tk.Frame(self, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Branding
        left_frame = tk.Frame(main_frame, bg=self.bg_panel, width=450)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        left_frame.pack_propagate(False)
        
        # Logo area
        logo_frame = tk.Frame(left_frame, bg=self.bg_panel)
        logo_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=60)
        
        logo_label = tk.Label(
            logo_frame,
            text="✨",
            font=("Segoe UI", 100),
            bg=self.bg_panel,
            fg=self.accent_gold
        )
        logo_label.pack(pady=20)
        
        title_label = tk.Label(
            logo_frame,
            text="Join Jarvis",
            font=("Segoe UI", 40, "bold"),
            bg=self.bg_panel,
            fg="white"
        )
        title_label.pack(pady=10)
        
        desc_label = tk.Label(
            logo_frame,
            text="Begin your personalized\nAyurvedic health journey",
            font=("Segoe UI", 12),
            bg=self.bg_panel,
            fg=self.text_muted,
            justify=tk.CENTER
        )
        desc_label.pack(pady=20)
        
        # Right side - Signup form
        right_frame = tk.Frame(main_frame, bg=self.bg_dark)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=50, pady=40)
        
        # Scrollable form
        canvas = tk.Canvas(right_frame, bg=self.bg_dark, highlightthickness=0)
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_dark)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form title
        form_title = tk.Label(
            scrollable_frame,
            text="Create Account",
            font=("Segoe UI", 28, "bold"),
            bg=self.bg_dark,
            fg=self.text_light
        )
        form_title.pack(pady=(0, 20), anchor=tk.W)
        
        # Full name
        tk.Label(
            scrollable_frame,
            text="Full Name",
            font=("Segoe UI", 10),
            bg=self.bg_dark,
            fg=self.accent_light_pink
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.signup_fullname = tk.Entry(
            scrollable_frame,
            font=("Segoe UI", 11),
            bg=self.bg_panel,
            fg=self.text_light,
            insertbackground=self.accent_pink,
            relief=tk.FLAT,
            bd=0
        )
        self.signup_fullname.pack(fill=tk.X, pady=(0, 15), ipady=10)
        
        # Username
        tk.Label(
            scrollable_frame,
            text="Username",
            font=("Segoe UI", 10),
            bg=self.bg_dark,
            fg=self.accent_light_pink
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.signup_username = tk.Entry(
            scrollable_frame,
            font=("Segoe UI", 11),
            bg=self.bg_panel,
            fg=self.text_light,
            insertbackground=self.accent_pink,
            relief=tk.FLAT,
            bd=0
        )
        self.signup_username.pack(fill=tk.X, pady=(0, 15), ipady=10)
        
        # Email
        tk.Label(
            scrollable_frame,
            text="Email",
            font=("Segoe UI", 10),
            bg=self.bg_dark,
            fg=self.accent_light_pink
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.signup_email = tk.Entry(
            scrollable_frame,
            font=("Segoe UI", 11),
            bg=self.bg_panel,
            fg=self.text_light,
            insertbackground=self.accent_pink,
            relief=tk.FLAT,
            bd=0
        )
        self.signup_email.pack(fill=tk.X, pady=(0, 15), ipady=10)
        
        # Password
        tk.Label(
            scrollable_frame,
            text="Password",
            font=("Segoe UI", 10),
            bg=self.bg_dark,
            fg=self.accent_light_pink
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.signup_password = tk.Entry(
            scrollable_frame,
            font=("Segoe UI", 11),
            bg=self.bg_panel,
            fg=self.text_light,
            insertbackground=self.accent_pink,
            relief=tk.FLAT,
            bd=0,
            show="•"
        )
        self.signup_password.pack(fill=tk.X, pady=(0, 15), ipady=10)
        
        # Confirm password
        tk.Label(
            scrollable_frame,
            text="Confirm Password",
            font=("Segoe UI", 10),
            bg=self.bg_dark,
            fg=self.accent_light_pink
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.signup_confirm = tk.Entry(
            scrollable_frame,
            font=("Segoe UI", 11),
            bg=self.bg_panel,
            fg=self.text_light,
            insertbackground=self.accent_pink,
            relief=tk.FLAT,
            bd=0,
            show="•"
        )
        self.signup_confirm.pack(fill=tk.X, pady=(0, 25), ipady=10)
        
        # Signup button
        signup_btn = tk.Button(
            scrollable_frame,
            text="Create Account",
            font=("Segoe UI", 12, "bold"),
            bg=self.accent_gold,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self._handle_signup
        )
        signup_btn.pack(fill=tk.X, ipady=12, pady=(0, 15))
        
        # Login link
        login_frame = tk.Frame(scrollable_frame, bg=self.bg_dark)
        login_frame.pack(fill=tk.X)
        
        tk.Label(
            login_frame,
            text="Already have an account? ",
            font=("Segoe UI", 10),
            bg=self.bg_dark,
            fg=self.text_light
        ).pack(side=tk.LEFT)
        
        login_link = tk.Label(
            login_frame,
            text="Sign In",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_dark,
            fg=self.accent_pink,
            cursor="hand2"
        )
        login_link.pack(side=tk.LEFT)
        login_link.bind("<Button-1>", lambda e: self.show_login_page())
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _handle_login(self):
        """Handle login"""
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showwarning("Error", "Please fill all fields")
            return
        
        success, message = self.auth_manager.login(username, password)
        
        if success:
            self.current_user = username
            messagebox.showinfo("Success", message)
            self.on_auth_success(username)
        else:
            messagebox.showerror("Error", message)
    
    def _handle_signup(self):
        """Handle signup"""
        fullname = self.signup_fullname.get().strip()
        username = self.signup_username.get().strip()
        email = self.signup_email.get().strip()
        password = self.signup_password.get()
        confirm = self.signup_confirm.get()
        
        if not all([fullname, username, email, password, confirm]):
            messagebox.showwarning("Error", "Please fill all fields")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        success, message = self.auth_manager.register(username, email, password, fullname)
        
        if success:
            messagebox.showinfo("Success", message)
            self.current_user = username
            self.on_auth_success(username)
        else:
            messagebox.showerror("Error", message)
    
    def on_auth_success(self, username: str):
        """Called when authentication is successful"""
        # Override this in subclass
        pass
